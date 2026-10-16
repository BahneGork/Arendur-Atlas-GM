---
tags: [session40, lootfound, Arendur]
---

Session: #session40

Real date: 31 oct 2022
Location:  Rirroneth Domain
situation:  Travelling
Date: 12th Mirtul
Hour: 13:30?

Characterslevel:: `=[[Global party values]].level`
Total sum of player levels: `= [[Global party values]].players*[[Global party values]].level`
```dataviewjs
dv.span("Deadly threshold for your party: ")
let gpage = dv.page("Global party values")

if (gpage.level > 3)
{
dv.span(gpage.level * gpage.players/2)
}
else
{
dv.span(gpage.level * gpage.players/4)
}
```
### Start Scene

Mens i holder lejr og tager et velfortjent hvil, opdager i at samlet 2 dages rationer/drikke til hele holdet er fordærvet, uagtet om det er rationer eller brumor's hellige mad.
en stor hule, med slimet sø og en ø.
4 udgange ud over den i kom ind ad, alle sammen ligner lidt hinanden.
(next tile - broken archway)

- (er der nogle der roder med loot mens der holdes lejr?)
- afklar evt. identifies, appriasals osv.

1d4 hvem er på vagt  `dice: 1d4` , den sidste vagt

1 skikkelse nærmer sig i udkanten af synsfeltet, en i rustning og en i robes.
- veteran  
	- [[Veteran]] stats +1 str mod (19), +1dmg
	- [[Gladiator]] stats
- mind controlled sentries, intellect devourers med kontakt til vampire mindflayers
- ~~når gruppen forlader tiny hut, træder skikkelsen et par skridt nærmere.~~
	- veteran skyder med en heavy crossbow mod Anton [[Poisons 5e#Crawler Mucus (Contact)]] dc 13 con, smider crossbow fra sig og bevæger sig op til Cedric og laver et shortsword attack - Gladiator shield basher brumor og stikker efter ham 2 gange med sit spyd
	- gladiator shield basher brumor hvis han står op og bevæger sig over til Cedric og hjælper veteranen.
- når de dør eksploderer baghovedet og en intellect devourer løber ud i mørket
-~~ hvis nogen er i live i 3 runde, bliver cedric, frekka og brumor angrebet af Devour Intellect DC 13 int save 4d6 psychic dmg, fail by 5 or more you are stunned - retry save end of next turn.~~
- ~~Vampiric mindflayer might join the fight, jumping down from the ceiling.~~
- Veteran, Wizard loot
	- veteran
		- longsword, #lootfound 
		- short sword, #lootfound 
		- heavy crossbow, #lootfound 
		- 10 bolts,  #lootfound 
		- 1 vial of crawler poison (3 more uses) #lootfound 
		- splint mail armor #lootfound
		- 20gp 10sp #lootfound 
		- Gauntlets of Ogre strength  #lootfound
		- Amulet of a purple gauntled fist (band of the purple fist) #lootfound 
	- wizard
		- quarter staff +1
		- 30gp, 1 pearl
		- Amulet of purple gauntled fist (band of the purple fist)
		- no spell book, spell scroll of cloudkill
		- spell ingredient pouch
		- 1 greater healing potion 
	- gladiator
		- leather armor
		- small shield
		- spear
		- 10gp #lootfound
		- dagger

![[Intellect devourer image.png]]

![[Vampiric Mindflayer image.png]]

#Arendur