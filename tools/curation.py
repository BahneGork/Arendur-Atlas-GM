"""Hand-curated atlas data for the Arendur Rising campaign: the GM atlas, and the players' edition.

This file lives only in the PRIVATE repo. Everything here is GM knowledge unless marked
players=True (places, maps, party). Players' fields: name, summary, where, aliases, the position
(unless secret_at=True). GM-only text goes in gm="...". build.py --players writes the players'
edition to the public repo and stops if a GM-only name or text would reach it (tools/players.py).

For players=True entries, every statement must be something the players know. Sources, in order: the Player Vault (its chronicle, "4.Locations heard
of or visited", missions, handouts), the player map EastBlackwood-PC.png, and the owner's Obsidian
Leaflet pins on maps the players have seen. "(K12)" = point 12 in the player chronicle
"The Shadow Company - book 1 - Red hand of doom".

Positions are pixel coordinates (x, y) on the source map images. `approx=True` marks places not
printed on a map, placed from what the chronicle says. Delios pins come from the owner's Leaflet map
"Deliosmap2" (x = lng * 512, y = -lat * 512, checked against the Delios handout).
`note=""` means the place has no published note yet; its panel shows `summary` instead.
"""

GARDEN_URL = ""  # the garden's public URL, for "Åbn i haven" links (no trailing slash)

# Campaign settings used by build.py and the site.
CAMPAIGN = {
    "title": "Arendur",
    "start": "ursia",                    # map shown first
    "repo": "BahneGork/Arendur-Atlas-GM",   # where "Gem for alle" commits moved pins (the private repo)
    "notes_repo": "https://github.com/BahneGork/GMnostes.git",
    # Player-safe folders only: anything under them is shown in the public atlas.
    "notes_dirs": [
        "src/site/notes/01 GM/Campaigns/The Arendur Rising Campaign/The Shadow Company/Bible/Player Vault",
        "src/site/notes/01 GM/Campaigns/The Arendur Rising Campaign/Handouts/Cutscenes",
    ],
    "home_note": "1.This is the player vault for the Arendur Rising campaign",
    "hubs": ["1.This is the player vault for the Arendur Rising campaign", "2.Campaign Journal",
             "4.Locations heard of or visited", "5.People", "+Mission Board", "_Cutscenes Index"],
    "skip_notes": ["README"],
    "gm": "",
    # Rejsen follows the chronicle in stages, because which session did what isn't recorded (owner).
    "unit": "Etape",
    "readLabel": "Læs krøniken",
}

MAPS = {
    # ursia-baronies-map.png; the coloured areas are the baronies, coloured by the noble house the baron serves (owner).
    "ursia": {"players": True, "name": "Ursia", "image": "maps/ursia.webp", "size": [7092, 5686]},
    # The players' version of the East Blackwood map (EastBlackwood-PC.png). Its labels are player knowledge.
    "blackwood": {"players": True, "name": "East Blackwood", "image": "maps/blackwood.webp", "size": [1131, 1080],
                  "place": "east-blackwood"},
    # "Delios no pins.png", the base of the players' Delios handout.
    "delios": {"players": True, "name": "Delios", "image": "maps/delios.webp", "size": [7680, 4320], "place": "delios"},
}

# Links between maps, drawn as signposts at the map edge (never next to pins).
PORTALS = [
    {"map": "blackwood", "to": "ursia", "label": "Ursia", "hint": "hele landet", "at": [80, 1040], "arrow": "↑"},
    {"map": "delios", "to": "blackwood", "label": "East Blackwood", "hint": "egnen omkring", "at": [7300, 200],
     "arrow": "↑"},
]

# kind: by | borg | taarn | hule | helligt | havn | vildmark | sted
PLACES = {
    # --- Ursia ---
    "arendur": dict(note="", players=True, name="Arendur", map="ursia", at=[4433, 3040], kind="by", visited=True,
                    summary="Hovedstaden, omgivet af den store mur som dværgene byggede (K95). "
                            "Her begyndte kompagniets historie med goblinhulerne tæt ved byen (K1)."),
    # Gutbust caves = the goblin caves, and the farm was visited: per the owner (2026-10-16).
    "goblin-caves": dict(note="", players=True, parent="arendur", kind="hule", name="Gutbust-hulerne", visited=True,
                         aliases=["Goblinhulerne ved Arendur", "Gutbuster", "Gutbust hulerne"],
                         summary="Goblinhulerne uden for Arendur (missionen Gutbuster Ooze). "
                                 "Røde hånd-gobliner: goblin boss Krazkar blev besejret, warlocken Moogzt undslap (K1–K6)."),
    "farmer-john": dict(note="", players=True, parent="arendur", kind="sted", name="Farmer Johns gård", visited=True,
                        summary="En gård uden for Arendur. Gruppen var derude for at besøge og undersøge den."),
    "kvalec": dict(note="", players=True, name="Kvalec", map="ursia", at=[1672, 3369], kind="by",
                   summary="By mod vest. Lejesoldaterne Blackdaggers kom herfra (K2)."),
    # scroll=True: drawn as a scroll that opens the East Blackwood map (owner's idea, 2026-10-16).
    "east-blackwood": dict(note="", players=True, scroll=True, map="ursia", at=[5071, 4391], approx=True, kind="vildmark",
                           name="East Blackwood",
                           where="Skoven i Bedegaarn-baroniet.",
                           summary="Skovegnen omkring Delios og Teslions, hvor det meste af kompagniets "
                                   "eventyr har fundet sted. Se kortet over East Blackwood."),

    # --- East Blackwood (labels on the players' map) ---
    # also=[(map, at, approx)]: the same place on further maps. The Ursia positions are estimates around the
    # owner's pin "Bedegaarn barony – Duke Alvares" (4752, 4066), in the open land north of the forest.
    "delios": dict(note="", players=True, name="Delios", map="blackwood", at=[707, 465], kind="by", visited=True,
                   also=[("ursia", [4895, 4157], True)],
                   summary="By med tømmer-ranches i Blackwood. Gruppen kom til festival her (K62–K64), "
                           "og borgmester Osric hyrede kompagniet (K66). Gruppens base mellem ekspeditionerne (K90, K110). "
                           "Brumor har sat et gadekøkken op for byens hjemløse."),
    "teslions": dict(note="", players=True, name="Teslions", map="blackwood", at=[858, 768], kind="by", visited=True,
                     also=[("ursia", [5261, 4115], True)],
                     summary="Den sidste by før grænsen. Fik tid til at evakuere, fordi gruppen ødelagde "
                             "Skullgorge-broen (K24), men blev senere overrendt af horden (K38)."),
    "logen": dict(note="", players=True, parent="teslions", kind="sted", name="Logen i Teslions"),
    "lady-dagger-shop": dict(note="", players=True, parent="teslions", kind="sted", name="Lady Daggers butik",
                             summary="Lady Daggers butik og private kammer i Teslions."),
    "lady-dagger-caves": dict(note="", players=True, map="blackwood", at=[1005, 885], kind="hule", visited=True,
                              name="Lady Daggers huler",
                              summary="Lady Dagger kidnappede Pinna og Siertianna for at lokke gruppen til "
                                      "sit ritual (K28). I hulerne lå også købmandskaravanernes loot (K30)."),
    "skygge-vaulten": dict(note="", players=True, parent="lady-dagger-caves", kind="hule", name="Skygge-vaulten", visited=True,
                           summary="En forseglet vault i en sprække under hulerne: \"Ved Kiri-Joliths kraft og "
                                   "Helgen Worlocks autoritet skal denne boks/vault forblive låst\" (K31–K33)."),
    "maakengorge": dict(note="", players=True, map="blackwood", at=[893, 868], kind="vildmark", name="Maakengorge"),
    "sunken-citadel": dict(note="", players=True, map="blackwood", at=[522, 745], kind="hule", visited=True,
                           name="Det sunkne citadel",
                           summary="Røde hånd-gobliner under Warchief Ratbag. I bunden stod et dødt træ, hvor "
                                   "goblin-warlocks var ved at åbne en portal til Feydark (K14–K20)."),
    "camp-oxbar": dict(note="", players=True, map="blackwood", at=[535, 800], approx=True, kind="hule", name="Camp Oxbar",
                       visited=True, where="I Underdark; kortet viser Oxbar ved det sunkne citadel.",
                       summary="Dværgen Oxbars underjordiske ekspedition, som gruppen reddede (K13)."),
    "skullgorge": dict(note="", players=True, map="blackwood", at=[328, 630], kind="vildmark", name="Skullgorge-broen",
                       visited=True, aliases=["Skull Gorge", "Skullgorge"],
                       summary="Gruppen ødelagde broen i kampen mod gobliner og en grøn drage og "
                               "forsinkede den røde hånds horde i flere dage (K21–K22)."),
    "blackspear": dict(note="", players=True, map="blackwood", at=[615, 140], kind="borg", name="Castle Blackspear",
                       summary="Ruiner, hvor den sorte drage Regilarix holder dværgehelten Grozon fanget (K94). "
                               "Det hemmelige våben kom herfra (K40–K41). Kompagniet er på vej herhen (K106)."),
    "blackspear-swamp": dict(note="", players=True, map="blackwood", at=[651, 161], approx=True, kind="vildmark",
                             name="Blackspear-sumpen", where="Omkring Castle Blackspear."),
    "ranger-hut": dict(note="", players=True, map="blackwood", at=[726, 333], approx=True, kind="sted", name="Rangerhytten",
                       where="Nordvest for Delios (de spilledes stedliste).",
                       summary="En ranger, der har overlevet en kamp med den sorte drage (K106)."),
    "bedegaarn": dict(note="", players=True, map="blackwood", at=[978, 305], kind="borg", name="Bedegaarn",
                      also=[("ursia", [4757, 3953], True)],
                      summary="Baroniets 'hovedstad' og sæde."),
    "click-claw": dict(note="", players=True, map="blackwood", at=[740, 525], approx=True, kind="borg", name="Click Claw Watch",
                       visited=True, where="Ved vejen gennem bakkelandet op mod Delios.",
                       summary="Et fort fra Ork-krigen, der beskytter vejen gennem bakkelandet op mod Delios (K61)."),
    "raven-tomb": dict(note="", players=True, map="blackwood", at=[780, 495], approx=True, kind="hule",
                       name="Ravnekongens grav", visited=True, where="Ude i Click Claw-bakkelandet (K68–K69).",
                       aliases=["Tomb of the Raven king", "Ravne Kongens grav"],
                       summary="Her mødte gruppen Ravnekongen, som belønnede dem med et banner (K85–K88)."),
    "rirroneth-wheel": dict(note="", players=True, parent="raven-tomb", kind="sted", name="Rirroneths hjul", visited=True),
    "fallen-star": dict(note="", players=True, map="blackwood", at=[770, 575], approx=True, kind="sted", name="Fallen Star",
                        visited=True, where="En landevejskro på vejen mod Delios (K57).",
                        summary="Landevejskro, hvor Anton og Frekka sluttede sig til gruppen (K57–K58). "
                                "Skyggekompagniets hovedkvarter (Summary Session 47)."),
    "mausoleum": dict(note="", players=True, map="blackwood", at=[785, 610], approx=True, kind="hule", name="Mausoleet",
                      visited=True, where="Ikke langt fra Fallen Star (K54–K57).",
                      summary="Gammelt gravsted med et elverbroderet vægtæppe. Tidsmagi sendte gruppen tilbage "
                              "til et overfald på hertugen 'den sorte ørn' (K54–K56)."),
    "blackbriar": dict(note="", players=True, map="blackwood", at=[800, 660], approx=True, kind="helligt",
                       name="Blackbriar kloster", visited=True,
                       where="På vejen mellem Teslions og Delios (K46).",
                       summary="Munkene blev dræbt af ghouls fra en skjult krypt fra imperiet Azerumme; "
                               "THE necromancer undslap (K46–K51)."),
    "anadur": dict(note="", players=True, map="blackwood", at=[1095, 25], kind="by", name="Anadur"),
    "kraeltor": dict(note="", players=True, map="blackwood", at=[875, 178], kind="by", name="Kraeltor"),
    "taernu": dict(note="", players=True, map="blackwood", at=[1028, 555], kind="by", name="Taernu"),
    "gaernur": dict(note="", players=True, map="blackwood", at=[1027, 810], kind="by", name="Gaernur"),
    "red-hand-warcamp": dict(note="", players=True, map="blackwood", at=[38, 445], kind="sted", name="Den røde hånds lejr"),
    "cinderhill": dict(note="", players=True, map="blackwood", at=[258, 445], kind="vildmark", name="Cinderhill"),

    # --- Delios (the owner's pins) ---
    # Delios visits below (inn, tavern, bookshop, professor, stables, Milly Bell, Jago's Jewel, Operation Mongoose,
    # church ruins (Anton), St. Gaed and the Oathstone (Brumor), herbalist and Gold Loaf ("vist"), Brumor's soup kitchen): per the owner (2026-10-16).
    "dusty-tome": dict(note="", players=True, map="delios", at=[4654, 2016], parent="delios", kind="sted", name="Dusty Tome – boghandel",
                       visited=True, summary="Anton har besøgt boghandleren."),
    "tower-ruins": dict(note="", players=True, map="delios", at=[4716, 939], parent="delios", kind="taarn", name="Tårnruinen"),
    "old-church": dict(note="", players=True, map="delios", at=[5047, 1008], parent="delios", kind="helligt", name="Den gamle kirkeruin",
                       visited=True, summary="Anton har været i kirkeruinerne."),
    "ravenscrest": dict(note="", players=True, map="delios", at=[4707, 2693], parent="delios", kind="sted", name="Ravenscrest Emporium"),
    "egas-mannon": dict(note="", players=True, map="delios", at=[4873, 3024], parent="delios", kind="sted", name="Professor Egas Mannon",
                        visited=True, summary="Anton lærte af Egas Mannon og fik Book of the Raven (K99–K100)."),
    "anden": dict(note="", players=True, map="delios", at=[4839, 2554], parent="delios", kind="sted", name="Anden tavern",
                  visited=True, summary="Nogle af gruppen har været på besøg i kroen."),
    "stormpine": dict(note="", players=True, map="delios", at=[4458, 2879], parent="delios", kind="sted", name="Stormpine Hall – gentlemen club"),
    "osric-stables": dict(note="", players=True, map="delios", at=[4364, 2746], parent="delios", kind="sted", name="Osric's Gilded Stables",
                       visited=True, summary="Gruppen har været i staldene."),
    "operation-mongoose": dict(note="", players=True, map="delios", at=[4096, 3268], parent="delios", kind="sted", name="Operation Mongoose",
                            visited=True, summary="Gruppen var til stede ved Operation Mongoose."),
    "black-eagle": dict(note="", players=True, map="delios", at=[4016, 3106], parent="delios", kind="sted", name="Black Eagle square"),
    "osric-loaf": dict(note="", players=True, map="delios", at=[4008, 2811], parent="delios", kind="sted", name="Osric's Gold Loaf",
                      visited=True, summary="Gruppen har været i Osric's Gold Loaf."),
    "black-portrait": dict(note="", players=True, map="delios", at=[3660, 3151], parent="delios", kind="sted", name="Black Portrait Inn",
                           visited=True, summary="Kroen, hvor gruppen har boet i Delios."),
    "herbalist": dict(note="", players=True, map="delios", at=[3586, 3628], parent="delios", kind="sted", name="Herbalist",
                     visited=True, summary="Gruppen har været hos herbalisten."),
    "oathstone": dict(note="", players=True, map="delios", at=[3440, 3946], parent="delios", kind="helligt", name="Oathstone of the Ancients",
                     visited=True, summary="Brumor har besøgt Oathstone."),
    "harrt-house": dict(note="", players=True, map="delios", at=[1996, 2673], parent="delios", kind="sted", name="The Harrt House"),
    "town-square": dict(note="", players=True, map="delios", at=[3796, 2486], parent="delios", kind="sted", name="Town Square"),
    "milly-bell": dict(note="", players=True, map="delios", at=[3811, 2224], parent="delios", kind="sted", name="The Milly Bell",
                       visited=True, summary="Gruppen har været i The Milly Bell."),
    "town-hall": dict(note="", players=True, map="delios", at=[4099, 2311], parent="delios", kind="borg", name="Town Hall",
                      summary="Cedric var blandt VIP-gæsterne i borgmesterboligen under festivalen (K64)."),
    "gaeds-sanctuary": dict(note="", players=True, map="delios", at=[3982, 1830], parent="delios", kind="helligt", name="Gaed's sanctuary",
                            aliases=["St. Gaed kirken", "St. Gaed"], visited=True,
                            summary="St. Gaed-kirken. Brumor har været i kirken."),
    "jagos-jewel": dict(note="", players=True, map="delios", at=[3414, 1674], parent="delios", kind="sted", name="Jago's Jewel",
                        visited=True, summary="Gruppen har været i Jago's Jewel."),

    # --- Off the maps ---
    "rirroneth": dict(note="", players=True, offmap="other", kind="vildmark", name="Rirroneths domæne", visited=True,
                      where="Et domæne i Far Realm.",
                      summary="Gruppen kom hertil gennem Rirroneths hjul (K70–K71)."),
    "pearl-fortress": dict(note="", players=True, parent="rirroneth", kind="borg", name="Perleborgen", visited=True,
                           aliases=["Pearl Fortress"],
                           summary="Den celestiale elver 'Bittersweet lovers anticipation'. Ravnesværdet fuldførte "
                                   "lovens ritual, og borgen smuldrede (K72–K73)."),
    "festering-spire": dict(note="", players=True, parent="rirroneth", kind="hule", name="Labyrinth caves of the festering spire",
                            visited=True),
    "steel-castle": dict(note="", players=True, offmap="other", kind="borg", name="Stålridderborgen",
                         aliases=["Steel Castle"], where="Sydpå, ca. 27 dages rejse fra Teslions (K43).",
                         summary="Knighthood of Steel. De overlevende fra Teslions blev eskorteret hertil (K42–K43)."),
    "akalane": dict(note="", players=True, offmap="other", kind="by", name="Akalane",
                    where="På den anden side af Blackwood-skoven.",
                    summary="By som Delios handler med."),
    "dead-mountain": dict(note="", players=True, offmap="other", kind="vildmark", name="Dødebjerget", visited=True,
                          summary="Gruppen udryddede udøde her; et mægtigt monster vågnede, og Brumor døde (K107–K109)."),
}

OFFMAP = {
    "other": {"name": "Andre steder", "hint": "Steder uden kendt placering",
              "summary": "Steder fra krøniken, hvor vi ikke kender placeringen – eller som slet ikke ligger i denne verden."},
}

REGIONS = {}

# The journey: the player chronicle (K1–K110) grouped into stages. Which session each stage was
# played in isn't recorded (owner, 2026-10-16), so these are stages, not sessions.
CHRONICLE = "The Shadow Company - book 1 - Red hand of doom."
SESSIONS = [
    (1, "Oozebusters og Gutbust-hulerne", ["goblin-caves"], CHRONICLE,
     "Røde hånd-gobliner i Gutbust-hulerne ved Arendur. Goblin boss Krazkar falder, warlocken Moogzt undslipper (K1–K10)."),
    (2, "Gennem Underdark", ["camp-oxbar"], CHRONICLE,
     "The Fulcrom hyrer holdet til at undersøge gobliner sydpå. Undervejs reddes dværgen Oxbars ekspedition (K12–K13)."),
    (3, "Det sunkne citadel", ["sunken-citadel"], CHRONICLE,
     "Warchief Ratbag og en portal til Feydark. Nathaniel brænder det døde træ – og unge Nat stiger op af asken (K14–K20)."),
    (4, "Skullgorge-broen", ["skullgorge"], CHRONICLE,
     "Broen ødelægges i kampen mod gobliner og en grøn drage. Horden forsinkes i flere dage (K21–K22)."),
    (5, "Teslions forbereder sig", ["teslions"], CHRONICLE,
     "En hydra på vejen. Teslions evakuerer, og Den sorte liljes Måneridder eftersøger baronens mordere (K23–K27)."),
    (6, "Lady Daggers huler", ["lady-dagger-caves", "skygge-vaulten"], CHRONICLE,
     "Pinna og Siertianna reddes fra Lady Daggers ritual. Under hulerne ligger en forseglet vault (K28–K35)."),
    (7, "Teslions falder", ["teslions"], CHRONICLE,
     "Byen er overrendt. Krazkar er genopstået, og det hemmelige våben fra Blackspear er en avlet øgle. "
     "De overlevende eskorteres mod Stålridderborgen (K36–K44)."),
    (8, "Blackbriar kloster", ["blackbriar"], CHRONICLE,
     "Ghouls fra en krypt fra imperiet Azerumme havde dræbt munkene. THE necromancer undslipper (K45–K51)."),
    (9, "Mausoleet og den sorte ørn", ["mausoleum"], CHRONICLE,
     "Baghold fra en røde hånd-dødsgruppe. Tidsmagi sender gruppen tilbage for at redde hertugen 'den sorte ørn' (K52–K56)."),
    (10, "Fallen Star", ["fallen-star"], CHRONICLE,
     "Teleporterende monstre ved landevejskroen. Anton og Frekka slår følge med gruppen (K57–K60)."),
    (11, "Festival i Delios", ["click-claw", "delios", "town-hall"], CHRONICLE,
     "Forbi Click Claw Watch til festivalen i Delios. Borgmester Osric hyrer kompagniet (K61–K66)."),
    (12, "Ravnekongens grav", ["raven-tomb", "rirroneth-wheel"], CHRONICLE,
     "Ud i Click Claw-bakkelandet til Ravnekongens grav og Rirroneths hjul (K67–K70)."),
    (13, "Rirroneth og Perleborgen", ["rirroneth", "pearl-fortress"], CHRONICLE,
     "Perleborgen smuldrer, Cedric tager Ravnesværdet, og Lady Dazran viser vejen hjem (K71–K84)."),
    (14, "Tilbage hos Ravnekongen", ["raven-tomb"], CHRONICLE,
     "Ravnekongen belønner gruppen med et banner (K85–K89)."),
    (15, "Skyggekompagniet", ["delios", "egas-mannon"], CHRONICLE,
     "Træning i Delios, Cedrics ed, Antons studier hos Egas Mannon, og gruppen sværger ed til Skyggekompagniet (K90–K105)."),
    (16, "Dødebjerget", ["dead-mountain", "delios"], CHRONICLE,
     "På vej mod Castle Blackspear: udøde ved Dødebjerget. Brumor dør og bringes tilbage – for en pris (K106–K110)."),
]

LOCATION_ALIASES = {}
NOT_PLACES = set()

PARTY = []  # party members with a published note (none yet)
PARTY_STATUS = {}
PARTY_NAMES = {}
PARTY_PERIODS = {}
SOLO_SESSIONS = {}
# Class and Company title per PC (the owner's "Campaign bible summary"; titles were given in K102).
PARTY_CLASS = {
    "Cedric Belmote": "Paladin / Eldritch Knight · Vice-Consul i Skyggekompagniet",
    "Brumor Stålfod": "Cleric · Chaplain i Skyggekompagniet",
    "Anton Keene": "Wizard (tid) · Chancellor Arcane i Skyggekompagniet",
    "Frekka Flammehår": "Barbarian (Bear Totem) / Battlemaster · Castellan i Skyggekompagniet",
}
PARTY_RACE = {}
PARTY_ORIGIN = {}
# The PCs have no published notes, so their cards show what the chronicle says.
PARTY_EXTRA = {
    "Cedric Belmote": dict(aliases=["Cedric"], players=True, race="", social="", role="", dead=False,
                           statusNote="Bærer Xerathal – Ravnekongens sværd (K76, K86)."),
    "Brumor Stålfod": dict(aliases=["Brumor"], players=True, race="", social="", role="", dead=False,
                           statusNote="Udvalgt af Silverbeard til Silver Sentinel-ordenen (K93). Døde ved Dødebjerget "
                                      "og blev bragt tilbage (K109). Har sat et gadekøkken op for de hjemløse i Delios."),
    "Anton Keene": dict(aliases=["Anton"], players=True, race="", social="", role="", dead=False,
                        statusNote="Sluttede sig til gruppen ved Fallen Star (K58). Studerer hos Egas Mannon (K99–K100)."),
    "Frekka Flammehår": dict(aliases=["Frekka"], players=True, race="", social="", role="", dead=False,
                             statusNote="Sluttede sig til gruppen ved Fallen Star (K58)."),
}
NOT_PEOPLE = {"Locations heard of or visited"}  # a copy of the locations list filed under People/
