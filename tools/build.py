"""Build data/atlas.json from the curated places and the published notes.

Usage: python3 tools/build.py [--notes <path-to-notes-root>] [--players <public-repo-dir>]
Always builds the GM atlas into data/ (this private repo). With --players, also writes the players'
edition (only what is marked players=True) into the public repo's checkout; see tools/players.py.
By default the notes are fetched from GitHub (CAMPAIGN["notes_repo"] in curation.py, where the
Obsidian Digital Garden plugin publishes them) into .cache/. Only the folders in
CAMPAIGN["notes_dirs"] are read. Notes are only read, never modified.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from urllib.parse import quote, unquote

sys.path.insert(0, os.path.dirname(__file__))
from curation import (CAMPAIGN, GARDEN_URL, LOCATION_ALIASES, MAPS, NOT_PEOPLE, NOT_PLACES,  # noqa: E402
                      OFFMAP, PARTY, PARTY_CLASS, PARTY_EXTRA, PARTY_NAMES, PARTY_ORIGIN, PARTY_PERIODS, PARTY_RACE,
                      PARTY_STATUS, PLACES, PORTALS, SOLO_SESSIONS,
                      REGIONS, SESSIONS)
import players as pl  # noqa: E402
import threads as thr  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = CAMPAIGN["notes_repo"]
CACHE = os.path.join(ROOT, ".cache", "notes")
NOTES_DIRS = CAMPAIGN["notes_dirs"]


def fetch_notes():
    """Sparse, shallow copy of the published notes; refreshed on every build."""
    git = ["git", "-C", CACHE]
    try:
        if not os.path.isdir(CACHE):
            subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--sparse", REPO, CACHE],
                           check=True)
            subprocess.run(git + ["sparse-checkout", "set", "--no-cone"] + [f"/{d}/" for d in NOTES_DIRS], check=True)
        else:
            subprocess.run(git + ["fetch", "-q", "--depth", "1", "origin", "main"], check=True)
            subprocess.run(git + ["reset", "-q", "--hard", "origin/main"], check=True)
    except (subprocess.CalledProcessError, OSError) as e:
        print(f"warning: could not update notes from GitHub ({e}); using the cached copy")
    rev = subprocess.run(git + ["log", "-1", "--format=%h %ci"], capture_output=True, text=True).stdout.strip()
    print(f"notes: GitHub {rev}")
    return CACHE


ARGS = argparse.ArgumentParser()
ARGS.add_argument("--notes", help="notes root instead of fetching them from GitHub")
ARGS.add_argument("--players", metavar="DIR", help="also write the players' edition into DIR (the public repo)")
ARGS = ARGS.parse_args()
ROOT_DIR = ARGS.notes or fetch_notes()
NOTE_DIRS = [os.path.join(ROOT_DIR, d) for d in NOTES_DIRS]

WIKILINK = re.compile(r"\[\[(?:[^\]|]*/)?([^\]|/#]+?)(?:#[^\]|]*)?(?:\\?\|([^\]]+))?\]\]")


def load_notes():
    notes = {}
    for base in NOTE_DIRS:
        for dirpath, _, files in os.walk(base):
            for f in files:
                if not f.endswith(".md"):
                    continue
                path = os.path.join(dirpath, f)
                text = open(path, encoding="utf-8").read()
                meta, body = {}, text
                m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
                if m:
                    try:
                        meta = json.loads(m.group(1))
                    except ValueError:
                        pass
                    body = text[m.end():]
                rel = os.path.relpath(path, base)
                # Some titles exist in several folders; the Locations note wins.
                if notes.get(f[:-3], {}).get("folder") == "Locations":
                    continue
                notes[f[:-3]] = {"folder": rel.split(os.sep)[0] if os.sep in rel else "",
                                 "marked_visited": "Locationsvisited" in rel.split(os.sep)[:-1],
                                 "permalink": meta.get("permalink"), "body": body,
                                 "props": meta.get("dg-note-properties") or {}}
    return notes


def link_label(m):
    """Visible text of a wikilink; aliases that are full paths show just the note name."""
    return (m.group(2) or m.group(1)).split("/")[-1].strip()


def plain(text, ids=None):
    """Strip markdown; with `ids`, wikilinks to known notes become [name](#note/<id>) links."""
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[*_`]+(?![^\[]*\]\])", "", text)
    text = WIKILINK.sub(lambda m: f"[{link_label(m)}](#note/{ids[m.group(1).strip()]})"
                        if ids and m.group(1).strip() in ids else link_label(m), text)
    return re.sub(r"\s+", " ", text).strip()


def summarize(body, ids=None):
    """First descriptive paragraph of a note, cut to at most ~2 sentences (links kept with `ids`)."""
    for pattern in (r"## Description\n+(.+?)(?:\n\n|\n#|$)", r"(?i:#* *beskrivelse):?\s*\n(.+?)(?:\n[A-ZÆØÅ ]{4,}\n|\n#|$)"):
        m = re.search(pattern, body, re.S)
        if m:
            text = plain(m.group(1), ids)
            break
    else:
        return ""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    out = ""
    for s in sentences:
        # never cut inside a link such as [Hr. Flick](#note/...)
        if len(out) + len(s) > 320 and out and out.count("[") == out.count("]("):
            break
        out = (out + " " + s).strip()
    return out


def note_url(note):
    if not GARDEN_URL or not note or not note.get("permalink"):
        return ""
    return GARDEN_URL + quote(note["permalink"], safe="/()'")


def links_in(body):
    body = re.split(r"\n## Referenced In", body)[0]
    return {m.group(1).strip() for m in WIKILINK.finditer(body)}


def inside(pt, poly):
    x, y = pt
    hit = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            hit = not hit
    return hit


# Note groups shown in the reader, by top-level folder.
GROUPS = {"Locations": "Steder", "People": "Personer", "Factions": "Factions", "Items": "Genstande",
          "Loot": "Loot", "Missions": "Missioner", "Journal": "Journal", "Setting lore": "Lore", "Lore": "Lore",
          "Characters": "Karakterer", "Rules": "Regler", "": "Andet"}
SKIP_NOTES = set(CAMPAIGN.get("skip_notes", []))  # e.g. generated Dataview output
# Overview notes that link to everything; readable, but not shown as "related".
HUBS = set(CAMPAIGN.get("hubs", []))


def slug(title):
    t = title.lower().replace("æ", "ae").replace("ø", "o").replace("å", "a")
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def reader_markdown(body, ids):
    """Obsidian/garden markdown -> plain markdown with in-atlas links (#note/<id>)."""
    md = re.sub(r"```(?:leaflet|dataview|dataviewjs|base)\b.*?```", "", body, flags=re.S)
    # "Referenced In" and "Tags" repeat what the reader's related-notes box already shows.
    md = re.sub(r"(?ms)^## (?:Referenced In|Tags)\s*$.*?(?=^## |\Z)", "", md)
    md = re.sub(r"<svg.*?</svg>", "", md, flags=re.S)
    md = re.sub(r"<[^>]+>", "", md)
    md = re.sub(r"!\[\[[^\]]*\]\]|!\[[^\]]*\]\([^)]*\)", "", md)
    md = WIKILINK.sub(lambda m: f"[{link_label(m)}](#note/{ids[m.group(1).strip()]})"
                      if m.group(1).strip() in ids else link_label(m), md)

    def garden_link(m):  # [text](/02 Player/.../Title/) links from embeds
        title = unquote(m.group(2).rstrip("/").split("/")[-1].split("#")[0])
        return f"[{m.group(1)}](#note/{ids[title]})" if title in ids else m.group(1)
    md = re.sub(r"\[([^\]]*)\]\((/02[^)]*)\)", garden_link, md)
    md = re.sub(r"(?m)^\s*(?:#[^\s#][^\s]*\s*)+$", "", md)          # tag-only lines
    home = re.escape(CAMPAIGN.get("home_note", ""))
    if home:
        md = re.sub(rf"(?m)^\[?{home}\]?(?:\([^)]*\))?\s*$", "", md)  # navigation back-link
    md = re.sub(r"(?m)^\{[^}]*\}\s*$", "", md)                       # { .block-language-dataview}
    md = re.sub(r"(?m)^\s*#+\s*$", "", md)                            # empty headings
    md = re.sub(r"(?m)^([\wæøåÆØÅ ]+):: ?(.*)$", r"**\1:** \2", md)   # dataview inline fields
    return re.sub(r"\n{3,}", "\n\n", md).strip()


def note_ids(notes):
    return {t: slug(t) for t in notes if t not in SKIP_NOTES and notes[t]["folder"] != "bases"}


def export_notes(notes, ids, place_of, session_of):
    out = {}
    for title, nid in ids.items():
        n = notes[title]
        # All links, including "Referenced In": that section is how notes point back to sessions.
        linked = {m.group(1).strip() for m in WIKILINK.finditer(n["body"])}
        links = sorted({ids[t] for t in linked if t in ids and t != title and t not in HUBS})
        group = ("Sessioner" if title in session_of else "Gruppen" if title in PARTY
                 else GROUPS.get(n["folder"], "Andet"))
        out[nid] = {"title": title, "group": group,
                    "md": reader_markdown(n["body"], ids), "links": links, "backlinks": []}
        if title in place_of:
            out[nid]["place"] = place_of[title]
        if title in session_of:
            out[nid]["session"] = session_of[title]
    for nid, n in out.items():
        if n["title"] in HUBS:
            continue
        for target in n["links"]:
            out[target]["backlinks"].append(nid)
    with open(os.path.join(ROOT, "data", "notes.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    return ids


def prop_targets(value):
    """Note titles named by a property value: [[links]] inside strings, or the plain string itself."""
    out = []
    for v in value if isinstance(value, list) else [value]:
        if not isinstance(v, str) or not v.strip():
            continue
        found = [m.group(1).strip() for m in WIKILINK.finditer(v)]
        out += found or [v.strip()]
    return out


# Disposition / friend-or-foe values -> ally | neutral | enemy | unknown
STANCE = {"ally": "ally", "friend": "ally", "deceased-ally": "ally", "neutral": "neutral",
          "conditional": "neutral", "enemy": "enemy", "foe": "enemy", "hostile": "enemy"}


def text_prop(value):
    vals = [v for v in (value if isinstance(value, list) else [value]) if isinstance(v, str) and v.strip()]
    return ", ".join(WIKILINK.sub(link_label, v) for v in vals)


def character_sheets():
    """Race and class from the player character notes in Characters/, keyed by lower-case name and alias."""
    sheets = {}
    for dirpath, _, files in (w for base in NOTE_DIRS for w in os.walk(os.path.join(base, "Characters"))):
        for f in files:
            m = re.match(r"^---\n(.*?)\n---\n", open(os.path.join(dirpath, f), encoding="utf-8").read(), re.S)
            try:
                pr = json.loads(m.group(1)).get("dg-note-properties", {}) if m else {}
            except ValueError:
                continue
            if pr.get("type") != "pc" or not pr.get("class"):
                continue
            cls = pr["class"] + (f" ({pr['subclass']})" if pr.get("subclass") and pr["subclass"] != "uknown" else "")
            sheet = {"race": pr.get("race", ""), "class": cls}
            for name in [f[:-3]] + [a for a in pr.get("aliases") or [] if isinstance(a, str)]:
                sheets[name.lower()] = sheet
    return sheets


def build_people(notes, note_id, session_of):
    """People and factions from their notes' properties, placed on atlas places where possible."""
    sheets = character_sheets()
    where = {p["note"]: pid for pid, p in PLACES.items()}
    where.update({a: pid for pid, p in PLACES.items() for a in p.get("aliases", [])})
    where.update({r["note"]: f"region:{rid}" for rid, r in REGIONS.items()})
    where.update({a: f"region:{rid}" for rid, r in REGIONS.items() for a in r.get("aliases", [])})
    where.update(LOCATION_ALIASES)

    def place_of(props):
        for key in ("location_primary", "Location", "location"):
            for t in prop_targets(props.get(key)):
                if t in where:
                    return where[t]
        return None

    def sessions_of(title, props):
        nums = {session_of[t] for t in prop_targets(props.get("sessions")) if t in session_of}
        nums |= {num for t, num in session_of.items() if title in links_in(notes[t]["body"])}
        return sorted(nums)

    factions = {}
    for title, n in notes.items():
        if n["folder"] != "Factions" or title not in note_id:
            continue
        pr = n["props"]
        factions[note_id[title]] = {
            "name": title, "seat": place_of(pr),
            "stance": STANCE.get(str(pr.get("friend-or-foe", "")).lower(), "unknown"),
            "type": text_prop(pr.get("faction_type")), "status": text_prop(pr.get("status")),
            "leader": [note_id[t] for t in prop_targets(pr.get("leader")) if t in note_id],
            "sessions": sessions_of(title, pr), "members": [],
        }
    people = {}
    for title, n in notes.items():
        in_party = title in PARTY
        if (n["folder"] != "People" and not (in_party and n["folder"] == "Characters")) or title not in note_id \
                or (title in NOT_PEOPLE and not in_party) \
                or re.search(r"\.(png|jpe?g|webp)$", title, re.I):  # image notes are not people
            continue
        pr = n["props"]
        disp = str(pr.get("disposition", "")).lower()
        status, status_note = PARTY_STATUS.get(title, (str(pr.get("status", "")).lower(), ""))
        fids = []
        for key in ("affiliation", "Faction", "faction"):
            for t in prop_targets(pr.get(key)):
                if note_id.get(t) in factions and note_id[t] not in fids:
                    fids.append(note_id[t])
        pid = note_id[title]
        people[pid] = {
            "name": title, "place": place_of(pr),
            "stance": STANCE.get(disp, "ally" if in_party else "unknown"),  # party members are allies unless noted
            "dead": status == "dead" or disp.startswith("deceased"),
            "status": status if status not in ("", "alive", "unknown") else "",
            "race": "" if pr.get("race") in (None, "unspecified") else text_prop(pr.get("race")),
            # social_status is generic filler on the party's notes ("commoner"), so it is left out for them
            "social": "" if in_party else text_prop(pr.get("social_status")),
            "role": text_prop(pr.get("role")) or text_prop(pr.get("Profession")),
            "aliases": [a for a in pr.get("aliases") or [] if isinstance(a, str)],
            "factions": fids, "sessions": sessions_of(title, pr),
            "pc": in_party, "statusNote": status_note,
        }
        if in_party:
            # A party member's location in their note is where they come from; they travel with the group.
            people[pid]["origin"], people[pid]["place"] = PARTY_ORIGIN.get(title, people[pid]["place"]), None
            # Race and class only from their character note; the People/ properties for the party are unreliable.
            names = [title.lower()] + [a.lower() for a in people[pid]["aliases"]] + [w.lower() for w in title.split()]
            sheet = next((sheets[n] for n in names if n in sheets), None)
            people[pid]["race"] = (sheet or {}).get("race") or PARTY_RACE.get(title, "")
            people[pid]["role"] = PARTY_CLASS.get(title) or (sheet or {}).get("class", "")
        for f in fids:
            factions[f]["members"].append(pid)
    # Party members without a note: sessions from their name in the logs.
    for name, extra in PARTY_EXTRA.items():
        names = [name] + extra["aliases"]
        pat = re.compile(r"(?<![\wæøå])(" + "|".join(re.escape(x.lower()) for x in names) + r")(?![\wæøå])")
        nums = sorted(num for t, num in session_of.items() if t in notes and pat.search(plain(notes[t]["body"]).lower()))
        people[slug(name)] = {"name": name, "place": None, "stance": "ally", "dead": extra["dead"], "status": "",
                              "race": extra["race"] or PARTY_RACE.get(name, ""), "social": extra["social"],
                              "role": PARTY_CLASS.get(name) or extra["role"],
                              "aliases": extra["aliases"], "factions": [], "sessions": nums, "pc": True,
                              "statusNote": extra["statusNote"], "noNote": True}
    return people, factions


def follow_renames(notes):
    """Curated titles whose note was renamed in the vault: follow the new note's aliases (any case)."""
    by_name = {t.lower(): t for t in notes}
    for t, n in notes.items():
        for a in n["props"].get("aliases") or []:
            if isinstance(a, str):
                by_name.setdefault(a.lower(), t)
    renamed = {}

    def res(title):
        new = title if title in notes else by_name.get(title.lower(), title)
        if new != title:
            renamed[title] = new
        return new

    for p in list(PLACES.values()) + list(REGIONS.values()):
        new = res(p["note"])
        if new != p["note"]:
            p.setdefault("aliases", []).append(p["note"])
            p["note"] = new
    PARTY[:] = [res(x) for x in PARTY]
    for d in (PARTY_NAMES, PARTY_STATUS, PARTY_PERIODS, PARTY_CLASS, PARTY_RACE, PARTY_ORIGIN):
        for k in list(d):
            if res(k) != k:
                d[res(k)] = d.pop(k)
    for names in SOLO_SESSIONS.values():
        names[:] = [res(x) for x in names]
    return renamed


def main():
    notes = load_notes()
    renamed = follow_renames(notes)
    note_id = note_ids(notes)
    problems = []

    def note(title):
        if not title:  # a curated place without a published note
            return None
        if title not in notes:
            problems.append(f"missing note: {title}")
        return notes.get(title)

    # Who links to each place from People/ and Factions/.
    linked = defaultdict(lambda: {"People": set(), "Factions": set()})
    for title, n in notes.items():
        if n["folder"] in ("People", "Factions") and title not in NOT_PEOPLE:
            for target in links_in(n["body"]):
                linked[target][n["folder"]].add(title)

    sessions_at = defaultdict(list)
    for num, _, ids, *_ in SESSIONS:
        for pid in ids:
            if pid not in PLACES:
                problems.append(f"session {num}: unknown place {pid}")
            sessions_at[pid].append(num)

    places = {}
    for pid, p in PLACES.items():
        n = note(p["note"])
        titles = [p["note"]] + p.get("aliases", [])
        people = set().union(*(linked[t]["People"] for t in titles))
        factions = set().union(*(linked[t]["Factions"] for t in titles))
        places[pid] = {
            "name": p.get("name", p["note"]), "kind": p["kind"],
            "map": p.get("map"), "at": p.get("at"), "approx": p.get("approx", False),
            "also": [{"map": m, "at": at, "approx": approx} for m, at, approx in p.get("also", [])],
            "scroll": p.get("scroll", False), "gm": p.get("gm", ""),
            "parent": p.get("parent"), "region": p.get("region"), "offmap": p.get("offmap"),
            "where": p.get("where", ""), "aliases": p.get("aliases", []), "travel": p.get("travel", ""), "travelLost": p.get("travel_lost", False),
            "summary": p.get("summary") or (summarize(n["body"], note_id) if n else ""),
            "url": note_url(n), "sessions": sessions_at.get(pid, []),
            "people": sorted(people, key=str.lower), "factions": sorted(factions, key=str.lower),
        }
    # A place counts as visited if the party was there (a session, or its note sits in
    # Locations/Locationsvisited), or was in something inside it.
    for pid in list(places):
        n = notes.get(PLACES[pid]["note"])
        if places[pid]["sessions"] or (n and n["marked_visited"]) or PLACES[pid].get("visited"):
            cur = pid
            while cur:
                places[cur]["visited"] = True
                cur = places[cur]["parent"]
    for pid, p in places.items():
        p.setdefault("visited", False)
        if p["parent"] and p["parent"] not in places:
            problems.append(f"{pid}: unknown parent {p['parent']}")
        if not p["region"] and p["at"]:
            for rid, r in REGIONS.items():
                if r["map"] == p["map"] and r["poly"] and inside(p["at"], r["poly"]):
                    p["region"] = rid
                    break
        if not p["name"]:
            problems.append(f"{pid}: no name (a place without a note needs name=)")
        if not p["summary"] and PLACES[pid]["note"]:
            problems.append(f"{pid}: no summary")

    regions = {}
    for rid, r in REGIONS.items():
        n = note(r["note"])
        titles = [r["note"]] + r.get("aliases", [])
        regions[rid] = {
            "name": r["name"], "map": r["map"], "poly": r["poly"], "label": r.get("label"),
            "summary": r.get("summary") or (summarize(n["body"], note_id) if n else ""),
            "url": note_url(n),
            "people": sorted(set().union(*(linked[t]["People"] for t in titles)), key=str.lower),
            "factions": sorted(set().union(*(linked[t]["Factions"] for t in titles)), key=str.lower),
        }

    session_notes = {float(re.match(r"\d+(?:\.\d+)?", t).group()): t for t, n in notes.items()
                     if n["folder"] == "" and re.match(r"^\d+(?:\.\d+)?\s*[-\s]", t)}
    # Journey entries without a session log name their own note (e.g. a mission note).
    entry_note_of = {num: extra[0] for num, _, _, *extra in SESSIONS if extra}
    # A note shared by several entries (e.g. one chronicle for every stage) isn't itself "a session".
    shared = {t for t in entry_note_of.values() if list(entry_note_of.values()).count(t) > 1}
    entry_notes = {num: t for num, t in entry_note_of.items() if t not in shared}
    sessions = []
    for num, title, ids, *extra in SESSIONS:
        t = entry_note_of.get(num) or session_notes.get(num)
        if not t:
            problems.append(f"session {num}: note not found")
        d = re.match(r"^\d+\s*-?\s*(\d{2})(\d{2})(\d{2})\b", t or "")
        sessions.append({
            "num": num, "title": title, "places": ids, "url": note_url(notes.get(t)),
            "date": f"{d.group(1)}.{d.group(2)}.20{d.group(3)}" if d else "",
            "gm": CAMPAIGN.get("gm", ""), "summary": extra[1] if len(extra) > 1 else "",
        })

    # Location notes nobody has curated yet, so updates can spot new places.
    curated = {p["note"] for p in PLACES.values()} | {a for p in PLACES.values() for a in p.get("aliases", [])}
    curated |= {r["note"] for r in REGIONS.values()} | {a for r in REGIONS.values() for a in r.get("aliases", [])}
    uncurated = sorted(t for t, n in notes.items()
                       if n["folder"] == "Locations" and t not in curated and t not in NOT_PLACES)
    unplaced = [{"note": t, "summary": summarize(notes[t]["body"]), "url": note_url(notes[t])} for t in uncurated]

    place_of = {p["note"]: ("sted", pid) for pid, p in PLACES.items()}
    place_of.update({r["note"]: ("region", rid) for rid, r in REGIONS.items()})
    session_of = {t: int(num) if num == int(num) else num for num, t in {**session_notes, **entry_notes}.items()}
    export_notes(notes, note_id, place_of, session_of)
    people, factions = build_people(notes, note_id, session_of)

    # Tråde (hand-written in docs/traade.md) and the automatic tracking tools
    known = {float(s["num"]): s["num"] for s in sessions}
    threads = thr.parse_threads(os.path.join(ROOT, "docs", "traade.md"), known, slug)
    names = {pid: p["aliases"] + PARTY_NAMES.get(p["name"], []) for pid, p in people.items()}
    seen_in = thr.mentions(notes, note_id, session_notes, plain, links_in, WIKILINK, names)
    # A party member's other notes (e.g. "Winston Wildwood" in Characters/) count as the same person.
    for pid, p in people.items():
        for other in PARTY_NAMES.get(p["name"], []):
            if other in note_id and note_id[other] != pid:
                seen_in[pid] |= seen_in.get(note_id[other], set())
    # Cards list every session that links to or names the person/faction, plus the note's own list.
    to_int = lambda x: int(x) if x == int(x) else x
    for group in (people, factions):
        for pid, p in group.items():
            p["sessions"] = sorted({to_int(float(x)) for x in p["sessions"]} | {to_int(x) for x in seen_in.get(pid, ())})
    # The party: every session while they were with the group, except solo sessions they weren't in.
    for pid, p in people.items():
        if p["name"] in PARTY_PERIODS:
            first, last = PARTY_PERIODS[p["name"]]
            p["sessions"] = [s["num"] for s in sessions if s["num"] >= first and (last is None or s["num"] <= last)
                             and (s["num"] not in SOLO_SESSIONS or p["name"] in SOLO_SESSIONS[s["num"]])]
            p["period"] = [first, last]
    latest = max(session_notes, default=0)
    # duplicate notes that the atlas treats as aliases of another place (e.g. "knoglestammens huler 1")
    aliases = {a for p in PLACES.values() for a in p.get("aliases", [])}
    title_of = {v: k for k, v in note_id.items()}
    kind_of = {note_id[t]: n["folder"] for t, n in notes.items() if t in note_id}
    to_num = lambda x: int(x) if x == int(x) else x
    forgotten = sorted(
        ({"id": nid, "title": title_of[nid], "kind": kind_of[nid], "sessions": [to_num(x) for x in sorted(s)],
          "last": to_num(max(s))} for nid, s in seen_in.items()
         if len(s) >= 2 and max(s) <= latest - 12 and title_of[nid] not in NOT_PEOPLE | NOT_PLACES | aliases
         and not people.get(nid, {}).get("dead")),
        key=lambda f: (-len(f["sessions"]), -f["last"]))
    # "Nævnt sammen med": notes sharing the most sessions, leaving out those in over half of all sessions
    common = {nid for nid, s in seen_in.items() if len(s) > 0.5 * len(session_notes)}
    together = {}
    for nid, s in seen_in.items():
        pairs = sorted(((len(s & t), other) for other, t in seen_in.items()
                        if other != nid and other not in common and len(s & t) >= 2), reverse=True)[:8]
        if pairs:
            together[nid] = [[other, k] for k, other in pairs]
    tools = {"forgotten": forgotten, "latest": to_num(latest),
             "next": [{**x, "session": to_num(x["session"])} for x in thr.next_steps(notes, session_notes, plain)],
             "questions": [{**x, "session": to_num(x["session"])} for x in thr.open_questions(notes, session_notes, plain)]}
    notes_path = os.path.join(ROOT, "data", "notes.json")
    notes_out = json.load(open(notes_path, encoding="utf-8"))
    for nid, pairs in together.items():
        if nid in notes_out:
            notes_out[nid]["together"] = pairs
    json.dump(notes_out, open(notes_path, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    for item in list(places.values()) + list(regions.values()):
        for key in ("people", "factions"):
            item[key] = [[t, note_id.get(t)] for t in item[key]]
    for pid, p in PLACES.items():
        places[pid]["noteId"] = note_id.get(p["note"])
    for rid, r in REGIONS.items():
        regions[rid]["noteId"] = note_id.get(r["note"])
    for s in sessions:
        s["noteId"] = note_id.get(entry_note_of.get(s["num"]) or session_notes.get(s["num"]))

    out = {"campaign": {**{k: CAMPAIGN[k] for k in ("title", "start", "repo", "unit", "readLabel") if k in CAMPAIGN},
                        "audience": "gm"}, "maps": MAPS, "portals": PORTALS, "offmap": OFFMAP, "places": places,
           "people": people, "factions": factions, "threads": threads, "tools": tools,
           "regions": regions, "sessions": sessions, "unplaced": unplaced}
    with open(os.path.join(ROOT, "data", "atlas.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    # Stamp a new version into index.html so browsers (phones especially) skip cached files.
    version = datetime.now().strftime("%Y%m%d%H%M%S")
    index = os.path.join(ROOT, "index.html")
    html = open(index, encoding="utf-8").read()
    html = re.sub(r'\?v=[0-9]+"', f'?v={version}"', html)
    html = re.sub(r'ATLAS_VERSION = "[0-9]*"', f'ATLAS_VERSION = "{version}"', html)
    open(index, "w", encoding="utf-8").write(html)

    print(f"{len(places)} places, {len(regions)} regions, {len(sessions)} sessions (version {version})")
    print(f"{len(threads)} threads; tools: {len(forgotten)} forgotten, {len(tools['next'])} next steps, "
          f"{len(tools['questions'])} questions")
    placed = sum(1 for p in people.values() if p["place"])
    print(f"{len(people)} people ({placed} placed), {len(factions)} factions "
          f"({sum(1 for f in factions.values() if f['seat'])} with a seat)")
    print("new location notes, not yet in the atlas:", ", ".join(uncurated) or "none")
    for old, new in sorted(renamed.items()):
        print(f"followed rename: {old} -> {new} (update tools/curation.py when convenient)")
    if ARGS.players:
        if problems:
            print("players' edition NOT written: fix the problems first")
        else:
            data, leaks = pl.filter_atlas(out)
            notes_json = open(notes_path, encoding="utf-8").read()
            leaks += pl.leak_check([json.dumps(data, ensure_ascii=False), notes_json])
            if leaks:
                problems += leaks
                print("players' edition NOT written")
            else:
                pl.write(ARGS.players, ROOT, data, notes_json, version)
    for p in problems:
        print("PROBLEM", p)
    return 1 if problems else 0


sys.exit(main())
