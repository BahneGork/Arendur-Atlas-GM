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

from curation import MAPS, PARTY_EXTRA, PLACES, PORTALS

# Files of the site itself, copied as they are.
SITE = ["index.html", "css", "js", "vendor"]


def filter_atlas(out):
    """The GM atlas data -> the players' atlas data, plus problems that must stop the build."""
    problems = []
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
        places[pid] = p

    maps = {k: {kk: vv for kk, vv in m.items() if kk != "players" and not (kk == "place" and vv not in keep)}
            for k, m in MAPS.items() if k not in gm_maps}
    portals = [p for p in PORTALS if p["map"] not in gm_maps and p["to"] not in gm_maps]
    sessions = [{**s, "places": [x for x in s["places"] if x in keep]} for s in out["sessions"] if s.get("players", True)]
    people = {k: p for k, p in out["people"].items()
              if not (p.get("noNote") and not PARTY_EXTRA.get(p["name"], {}).get("players"))}

    res = {**out, "campaign": {**out["campaign"], "audience": "players"}, "maps": maps, "portals": portals,
           "places": places, "sessions": sessions, "people": people}
    return res, problems


def gm_only_strings():
    """Names and texts that only the GM may see, for the leak check."""
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


def leak_check(texts):
    """Every GM-only string must be absent from the players' files."""
    blob = "\n".join(texts).lower()
    return [f"LEAK: '{s}' ({where}) is in the players' edition" for where, s in gm_only_strings()
            if len(s) >= 4 and re.search(r"(?<![\wæøå])" + re.escape(s.lower()) + r"(?![\wæøå])", blob)]


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
