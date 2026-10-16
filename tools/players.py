"""The players' edition of the atlas: everything not marked players=True is left out.

Used by build.py with --players <dir>. The GM data (tools/curation.py, GM maps, GM text) lives only in
this private repo; <dir> is a checkout of the public repo, which receives nothing but the filtered site.

Default is hidden: a place, map or party member reaches the players only with players=True. Before
anything is written, the output is searched for every GM-only name and text; a hit stops the build.
"""
import json
import os
import re
import shutil

from curation import CAMPAIGN, MAPS, PARTY_EXTRA, PLACES, PORTALS

# Files of the site itself, copied as they are.
SITE = ["index.html", "css", "js", "vendor"]


def filter_atlas(out, notes_out, player_ids):
    """The GM atlas data and notes -> the players' data and notes (JSON text), plus problems that must stop
    the build. player_ids: the notes the players have (their vault, the cutscenes)."""
    problems = []
    ok = lambda ref: ref and ref[1] in player_ids  # [title, note id] pairs
    gm_maps = {k for k, m in MAPS.items() if not m.get("players")}
    keep = {pid for pid, p in PLACES.items() if p.get("players")}

    places = {}
    for pid in keep:
        p = dict(out["places"][pid])
        p.pop("gm", None)
        if p["parent"] and p["parent"] not in keep:
            problems.append(f"{pid}: shown to players, but its parent {p['parent']} is not")
        if p["map"] in gm_maps or PLACES[pid].get("secret_at"):
            # Known to the players, but not where it is (or only on a GM map).
            p.update(map=None, at=None, approx=False, offmap=p["offmap"] or (None if p["parent"] else "other"))
        p["also"] = [x for x in p["also"] if x["map"] not in gm_maps]
        p["people"] = [r for r in p["people"] if ok(r)]
        p["factions"] = [r for r in p["factions"] if ok(r)]
        if p.get("noteId") not in player_ids:
            # A GM note: no link, and its text never becomes the players' summary.
            p.update(noteId=None, url="")
            if not PLACES[pid].get("summary"):
                p["summary"] = ""
        places[pid] = p

    maps = {k: {kk: vv for kk, vv in m.items() if kk != "players" and not (kk == "place" and vv not in keep)}
            for k, m in MAPS.items() if k not in gm_maps}
    portals = [p for p in PORTALS if p["map"] not in gm_maps and p["to"] not in gm_maps]
    sessions = [{**s, "places": [x for x in s["places"] if x in keep],
                 "noteId": s["noteId"] if s.get("noteId") in player_ids else None}
                for s in out["sessions"] if s.get("players", True)]
    def own_view(item, field):
        """The players' placement: the guess from their own notes replaces the GM's (which used GM notes)."""
        cap = field[0].upper() + field[1:]
        item = dict(item)
        for k in (field, field + "Guess", field + "Mentions"):
            pk = "player" + cap + k[len(field):]
            if pk in item:
                item[k] = item[pk]
        if "playerMentionedWith" in item:
            item["mentionedWith"] = item["playerMentionedWith"]
        for k in [k for k in item if k.startswith("player")]:
            del item[k]
        ref = item.get(field)
        if ref and not ref.startswith("region:") and ref not in keep:
            item[field] = None
        item["mentionedWith"] = [x for x in item.get("mentionedWith", []) if x in keep]
        return item

    factions = {k: own_view({**f, "members": [m for m in f["members"] if m in player_ids],
                             "leader": [m for m in f["leader"] if m in player_ids]}, "seat")
                for k, f in out["factions"].items() if k in player_ids}
    people = {}
    for k, p in out["people"].items():
        if p.get("noNote") and PARTY_EXTRA.get(p["name"], {}).get("players") or not p.get("noNote") and k in player_ids:
            people[k] = own_view({**p, "factions": [f for f in p["factions"] if f in factions]}, "place")
    tools = {**out["tools"], "forgotten": [f for f in out["tools"]["forgotten"] if f["id"] in player_ids]}
    unplaced = [u for u in out["unplaced"] if u.get("id") in player_ids]

    notes = {}
    for nid, n in notes_out.items():
        if nid not in player_ids:
            continue
        n = {**n, "links": [x for x in n["links"] if x in player_ids],
             "backlinks": [x for x in n["backlinks"] if x in player_ids]}
        if "together" in n:
            n["together"] = [x for x in n["together"] if x[0] in player_ids]
        if n.get("place") and n["place"][0] == "sted" and n["place"][1] not in keep:
            del n["place"]
        notes[nid] = n

    res = {**out, "campaign": {**out["campaign"], "audience": "players"}, "maps": maps, "portals": portals,
           "places": places, "sessions": sessions, "people": people, "factions": factions, "tools": tools,
           "unplaced": unplaced}
    return res, json.dumps(notes, ensure_ascii=False, separators=(",", ":")), problems


def gm_only_strings():
    """Curated names and texts that only the GM may see, for the leak check."""
    shown = {s.lower() for pid, p in PLACES.items() if p.get("players")
             for s in [p.get("name", ""), p.get("note", "")] + p.get("aliases", []) if s}
    shown |= {m["name"].lower() for m in MAPS.values() if m.get("players")}
    found = []
    for pid, p in PLACES.items():
        if p.get("gm"):
            found.append((pid, p["gm"]))
        if not p.get("players"):
            for s in [p.get("name", ""), p.get("note", "")] + p.get("aliases", []):
                if s and s.lower() not in shown:
                    found.append((pid, s))
    for k, m in MAPS.items():
        if not m.get("players") and m["name"].lower() not in shown:
            found.append((f"map {k}", m["name"]))
    return found


def gm_note_titles(gm_titles):
    """Titles of GM-only notes that aren't also the name of something the players see."""
    shown = {s.lower() for p in PLACES.values() if p.get("players")
             for s in [p.get("name", ""), p.get("note", "")] + p.get("aliases", []) if s}
    return [t for t in gm_titles if t.lower() not in shown and t not in CAMPAIGN.get("leak_ok", [])]


def leak_check(atlas_json, notes_json, gm_titles=(), player_titles=()):
    """GM-only names and texts must be absent from the players' files.

    gm= texts may appear nowhere. Names of GM-only places, maps and notes are leaks in the generated atlas
    data, unless the players' own notes contain them: a name the players have written down themselves is
    known to them (what the GM knows about it never reaches them)."""
    atlas, own = atlas_json.lower(), notes_json.lower()
    known = {t.lower() for t in player_titles}
    has = lambda blob, s: re.search(r"(?<![\wæøå])" + re.escape(s.lower()) + r"(?![\wæøå])", blob)
    gm_text = {p["gm"] for p in PLACES.values() if p.get("gm")}
    leaks = [f"LEAK: '{s}' ({where}) is in the players' edition" for where, s in gm_only_strings()
             if len(s) >= 4 and (has(atlas, s) or has(own, s)) and (s in gm_text or not has(own, s))]
    leaks += [f"LEAK: GM note '{s}' is named in the players' atlas data"
              for s in gm_note_titles([t for t in gm_titles if t.lower() not in known])
              if len(s) >= 4 and has(atlas, s) and not has(own, s)]
    return leaks


def write(out_dir, root, data, notes_json, version):
    """Write the players' site into out_dir (a checkout of the public repo)."""
    for name in SITE:
        src, dst = os.path.join(root, name), os.path.join(out_dir, name)
        if os.path.isdir(src):
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    # The players' site may be found by search engines; the GM site may not.
    index = os.path.join(out_dir, "index.html")
    html = open(index, encoding="utf-8").read()
    html = re.sub(r'\n  <meta name="robots"[^\n]*', "", html)
    open(index, "w", encoding="utf-8").write(html)
    os.makedirs(os.path.join(out_dir, "data"), exist_ok=True)
    with open(os.path.join(out_dir, "data", "atlas.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    with open(os.path.join(out_dir, "data", "notes.json"), "w", encoding="utf-8") as f:
        f.write(notes_json)
    # Only the players' maps; any other image is removed.
    maps_dir = os.path.join(out_dir, "maps")
    os.makedirs(maps_dir, exist_ok=True)
    wanted = {os.path.basename(m["image"]) for m in data["maps"].values()}
    for f in os.listdir(maps_dir):
        if f not in wanted:
            os.remove(os.path.join(maps_dir, f))
    for f in wanted:
        shutil.copy2(os.path.join(root, "maps", f), os.path.join(maps_dir, f))
    print(f"players' edition written to {out_dir} (version {version}): {len(data['places'])} places, "
          f"{len(data['maps'])} maps, {len(data['sessions'])} stages, {len(data['people'])} people")
