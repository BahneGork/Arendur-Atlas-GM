---
title:
  "{ title }":
aliases:
  - Delios
tags: [MOC, location, civilizationhub, secretsnclues, secretsrevealed, Arendur]
---

#MOC #location #civilizationhub
Main: [[The Bedegaarn Barony MOC|Bedegaarn Barony]]
Related: [[Click claw moors]] - [[Misty Falls]]

# Apperance
![[Pasted image 20240703235004.png|300]]
Blue and white bindingsværk huse (half-timbering)
Center of town is a circle, with a large well in the center, The mayor's house is to the north of the well.

## Town Square
Many shops lies around the town square.
Many town festivities take place on the centeral town space that is the town square. 
# Factions Operating in Delios
- [[The Ruby Throne]] has a representation in town, it is no more than a single merchant in charge of handling the buying of lumber. [[Robert Abrami]]. 
- [[Privy council of Arendur]] the trade of lumber from Delios to Arendur is too important to be left alone just for the guilds, the Duke of the region has appointed someone as their man to oversee that everything is above board. [[Oscar Delgado]]. He overrides the Barons (Hexton) men in matters of lumber.
- [[Abbesses]] who run the brothel "The harrt house", the real bosses behind [[Josie Harrt]]
- [[Woodriders]] a band of ratcatchers, bounty hunters and sellswords, leader [[Bear]]
- [[Orlocks]] local "biker gang"
- 


# POI's
## Inside Delios
```dataview
List
from #poi/location and #town/location and #delios 
```

## Outside Delios
```dataview
List
from #poi and #location and #Delios/outskirts or #lumberranch 
```

# NPCs
```dataview
list

where currentlocation="Delios"

```

# Secrets
- [ ] [[Anden tavern]] has a rat infestation in their basement, there are tunnels that leads to all under the town #secretsnclues 
- [ ] [[ranch falca]] has a vampire spawn locked away in a cave, tapping its blood to brew elixir for the lumberjacks to produce lumber faster. #secretsnclues 
- [ ] [[Lord Vermil]] is a vampire, from the ancient empire of Azarumme. #secretsnclues 
- [ ] [[Jago]] is running from something in [[Akacia]] #secretsnclues 
- [ ] [[Josie Harrt]] is being strongarmed by her criminal past in [[Arendur]] #secretsnclues 
- [ ] [[Abbesses]] are not working for [[Josie Harrt]] #secretsnclues 
- [ ] [[TomTom]] from the [[Orlocks]] went missing 4 weeks ago #secretsnclues 
- [ ] A vampire hunter visited town 2 maybe 3 weeks ago #secretsnclues 
- [ ] [[Ramon Chartrand - Alkymist]] has been asking [[Father Belderone]] about undead and vampires alot the last 2 weeks   #secretsnclues 
- [ ] [[keyleigh dufaigh]] is a slave trader from [[Akacia]], though not trading in town. #secretsnclues 
- [ ] [[Marta Alamilla]] is all proper on the surface, but she is trying to organize a rebellion against the new baron's knights #secretsnclues 
- [x] [[Angel the executioner]] is in town, snooping? assassinating? making deals? will offer the shadowcompany a job in the baron's army. ✅  #secretsrevealed 
- [ ] [[Lord Vermil]] paid for [[Jago's]] workshop and set him up as whitegold smith #secretsnclues 
- [ ] Ancient sewers run underneath [[14 Locations/Delios - the town - the town/Delios]] #secretsnclues 

# Non-hook Secrets
someone is having an affair
someone wants to ruin anothers business
someone meddles in everyones affairs
someone is a gossip


# Notes about Delios
```dataview
Table without ID Tag, map(rows, (r) => link(r.file.link, r.title)) as Notes
from #delios 
flatten file.tags as Tag
group by Tag 


```


#Arendur