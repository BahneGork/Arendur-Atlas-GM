# Arendur Atlas – GM

The private GM edition of the Arendur Rising atlas, and the source of the players' edition.

- **GM atlas**: everything, including GM-only places, maps and notes. View it locally:
  `python3 -m http.server 8000`, then http://localhost:8000
- **Players' edition**: only what is marked `players=True`, published to the public repo
  [Arendur-Atlas](https://github.com/BahneGork/Arendur-Atlas) → https://bahnegork.github.io/Arendur-Atlas/

## Build
```bash
python3 tools/build.py                              # GM atlas into data/
python3 tools/build.py --players ../Arendur-Atlas   # + the players' edition into the public repo
```
Then commit and push the public repo. The players' build stops if any GM-only name or text would reach it.

## Showing something to the players
In `tools/curation.py`, set `players=True` on the place (or map, or party member). Keep GM-only facts in `gm="..."`; use `secret_at=True` if the players know the place but not where it is.

## Adding a map
1. Save the image as WebP in `maps/` (max ~4096 px wide; keep positions in the original image's pixels).
2. Add it to `MAPS` with its original `size`, `place` = the place whose panel opens it, and `players: True` if the players have seen it.
3. Add a signpost back in `PORTALS`, at an empty map edge.

## Moving and placing pins
On either site: **Signaturer → Redigér placeringer**, drag pins, then **Gem for alle** (commits a file to `moves/` in this repo; the "Rebuild atlas" workflow applies it to the GM atlas). Publish the players' edition afterwards.

## Layout
- `tools/curation.py`: all atlas data (GM + players). `tools/build.py`, `tools/players.py`: the build and the players' filter.
- `index.html`, `css/`, `js/`: the site, shared by both editions
- `data/`: the GM atlas (generated)
- `maps/`: all map images (only the players' maps are copied to the public repo)
- `docs/assessment.md`: what the notes support, and open questions
