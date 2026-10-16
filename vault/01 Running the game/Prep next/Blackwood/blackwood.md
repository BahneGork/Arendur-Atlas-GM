---
type: region
Parent-Region: Bedegaarn Barony
this-region: Blackwood
visitedcount: 1
lastvisitdate:
tags: [Region, blackwood, visited, Arendur]
---

#Region #blackwood #visited 

Region: [[Ursia]]
subregion1: [[The Bedegaarn Barony MOC|Bedegaarn Barony]]
this region: [[blackwood]]

# History


# Enviroment
Dominant terrain/climate/have-need
# POIs
Locations/monuments/industries
```dataview
list
where type="poi"
where Parent-Region=this.this-region
```

# Lairs
poi that "spawns" monsters in the wilderness
```dataview
list
where type="lair"
where Parent-Region=this.this-region
```
# Hazards
dangerous "things" the region spawns that isnt a monster
- [[Quicksand]] 
- [[Swarm of Insects]] 
- [[Swarm of Quippers]] 
- Mist n fog decreasing visibility -> more prone to hazards 
- Treacherous footing: the ground in a swamp is often unstable and difficult to traverse, making it easy to lose your balance or fall into the water.
-   Poisonous plants: many swamps are filled with plants that are toxic to humans, such as poison ivy and stinging nettles.
-   Flash floods: sudden and heavy rainfall can cause the water level in a swamp to rise rapidly, creating a dangerous and unpredictable environment.
-   Acidic pools: some swamps contain pools of Regilarix acid drool, which can be damaging if entered.
-   Vengeful spirits: some swamps are said to be haunted by the ghosts of those who have died in their waters, who may seek to take revenge on those who intrude on their domain.

# Sub Regions
which subregions lies within this region.
```dataview
list 
where Parent-Region=this.this-region
where type="region"
```
# Parent Region
is this region a subregion of another?
```dataview
list
where this-region=this.Parent-Region
```




#Arendur