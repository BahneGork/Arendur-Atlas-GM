---
adventuretype: Short adventure
TrackerStart: 5
Tracker: 9
value1: 2
value2: 2
value3: 0
value4: 0
value5: 0
tags: [angryadventure, template, delios, deadmountain, shortadventures, Arendur]
---

#angryadventure #template #delios #deadmountain #shortadventures 

# XP Awards for Encounters and Objectives

-   Minor Encounter = 0.5x Award
-   Major Encounter = 1x Award
-   Climactic Encounter = 1.5x Award
-   Minor Objective = 0.5x Award
-   Major Objective = 1x Awards 
 
**Current level XP Award**
worth::  `= [[XPthresholdlookuptable]].xpawards["level"+[[Global values]].level].XP`



# Session Structure
> 1 major objective - adventure resolution 
> 1 climactic encounter - one pr session 
> 5 additional awards (objectives/encounters): minor=0,5 award or major=1 award 
##### Session 1
- [x] Minor encounter, Defend the Northern guard tower ✅ 2025-06-25
- [x] Minor objective, Secure wells from poison/corruption ✅ 2025-06-25
- [ ] Minor objective, clear a path to the church 
- [ ] Major encounter, the aranae assassin ambush 
- [ ] Climactic 1 - Defeat the Lysandra
- [ ] Major objective 1 - Resolution - Defend the town (town defense tracker status)

## Major Objective X 1 - Defend the Town from Undead Assault
1 x medium difficulty xp awards
Major award xp worth:: `= [[XPthresholdlookuptable]].xpawards["level"+[[Global values]].level].XP`

Town status tracker: 5  (just a palisade and two towers)
- If the tracker reaches 0 the town has fallen. 
- If the tracker ends at 1-4 it's a partial failure 
- If the tracker ends at 5-7 it's a partial success 
- If the tracker ends at 8-10 it's a full success 
- For each successful encounter/objective plus to tracker
- For each failed encounter/ojbective minus to tracker 
- Some encounter/objectives can be half-successes/failures, if so +1/-1. otherwise +2 or -2.
	- partial success: if an encounter/objective resolves with a positive feel 
	- partial failure: if an encounter/objective resolves with a defeated feel but some good was achieved, rescuing civilians but lost important supply.
- Other factors that can affect the tracker:
	- important npc casualty 
	- Critical locations overrun
	- Rallying Defenders, 

```meta-bind-button
style: primary
label: Recalculate
id: recalc-tracker
actions:
  - type: updateMetadata
    bindTarget: Tracker
    evaluate: true
    value: "Number(getMetadata('TrackerStart') || 0) + Number(getMetadata('value1') || 0) + Number(getMetadata('value2') || 0) + Number(getMetadata('value3') || 0)"
  - type: sleep
    ms: 1000
  - type: command
    command: dataview:dataview-rebuild-current-view
```

Tracker status: `= this.Tracker`


## Climactic Encounter X 1 - Defeating the Boss of the Undeads
1,5 x medium difficulty xp awards
Award XP worth: `= [[XPthresholdlookuptable]].xpawards["level"+[[Global values]].level].XP*1.5`




## ✅North Gate Defense
- [x] Defend the Northern guard tower (Minor)
0,5 x medium difficulty xp awards 
Award XP worth: `=900/2`
The ground around the gate is muddy from recent rains, -5 ft move to any non-undead 
Gate: 40HP AC 12
WAVES 
- wave 1 arrival 
	- 10 [[Skeletons]], 10 [[Zombies]], 2 [[Wight]] attacks the gate, battering with claws, weapons. 
	- Zombies and skeletons deal 4d6 dmg pr turn 
	- DC 14 Athletics or Survival use avalable resources pikes, debris, rope, lumber to strengthening the gate with 10hp 
	- DC 15 perception, notice undead creature sneaking around see wave 2 
- wave 2 escalation 
	- 5 [[Ghouls#Ghouls]], 2 [[Wight]] sneaks around trying to climb/scale the wall 
- wave 3 climactic push 
	- A Bodak joins and hangs back but stays close enough so that 10ft on the other side of the wall is within its aura 

**Healing the Fear:** A **Paladin** or **Cleric** might use **Lay on Hands** or **Protection from Evil and Good** to counteract the **Aura of Despair** or **frightened** conditions.
### **Victory And Failure Conditions**
- **Full Success (+2 Town Defense Tracker):** The gate holds, and the undead are repelled entirely. The Bodak is defeated before it can destroy the gate.
- **Partial Success (+1 Town Defense Tracker):** The gate is damaged but remains standing, and most of the undead attackers are eliminated or routed.
- **Partial Failure (-1 Town Defense Tracker):** The gate collapses under the Bodak’s assault, allowing some undead to spill into the town, but the defenders manage to slow their advance.
- **Full Failure (-2 Town Defense Tracker):** The gate collapses entirely, and the undead breach in significant numbers, overwhelming nearby defenders and forcing a retreat.

Game result - Tracker add value: +1

`INPUT[number(class(small-input)):value1]`



## ✅Secure Wells (watersupply) from poisoning/corruption (Minor)
- [x] Secure the wells from corruption
0,5 x medium difficulty xp awards 
Award XP worth: `=900/2`
Someone shouts *They're going for the well!!*
At the northern gate, there is a well closeby and villagers have observed undeads breaking off going for the well. 
Minotaur sherif [[Rinaken Stormbane]] "There are 9 wells in town, could they be trying to poison us?"
Full success - 6+ wells defended  +2
partial success 3-5 wells  +1
partial failure 1-2 wells defended -1
full failure 0 wells -2 

Game result - tracker add value: +2

`INPUT[number(class(small-input)):value2]`

### Wells
**Well 1** 
- 6 [[Skeletons]] 1 [[Wight]] with necrotic ichor 
**Well 2**
- 1 [[Shadow]] 2 [[Ghouls#Ghouls]] attacking [[Dusty tome - bookshop]] owner
- Contamination has begun, but can still be purified
	- DC 15 medicine, prof. [[Herbalism kit]] 
**Well 3**
- 3 [[Zombies]], [[Wight]], 3 [[Shadow]]
	- They have damaged the well's structure, it is in danger of collapsing. 
	- DC 15 mason's tools stabilize the well mid-combat 
**Well 4**
- 5 [[Skeletons]], 1 [[Ghouls#Ghast]], 2 [[Ghouls#Ghouls]]
	- 2 skeletons burning from Professor Egas throwing Alchemical fire at them 
	- he has 4 left 
**Well 5** town square 
- area filled with panicking villagers.
- 2 [[Shadow]] 2 [[Ghouls#Ghouls]] are heading for the well, but picking off civilians 
	- DC 13 persuasion or intimidation to organize the villagers in a retreat 
**Well 6** 
- 2 [[Zombies]] 2 [[Ghouls#Ghouls]], 1 [[Specter]] 
- dragging wounded defenders towards the well, perhaps to throw them in. 
- DC 15 Athletics to grasp the defenders mid-combat and pull them away 

**Well 7**
- 6 [[Skeletons]], 2 [[Wight]] are attacking the wooden structure of the well house with the bucket and rope to topple it and destroy the well 

**Well 8**
- The well here is already spreading a glowing green necrotic mist 
- This was not caused by ichor like the others, there is some item down in the water 
- DC 15 sleight of hand using the bucket to fetch the item 
- 2 attempts, then it is too late the well is permanently corrupted 

**Well 9**
- 5 [[Zombies]], 1 [[Wight]] casting a ritual spell to corrupt the water 



## Clear a Path to the Church (Minor)
- [ ] Path cleared, civilians led to safety, 0 casualties +2
- [ ] Path cleared, civilians led to safety, 2+ casualties +1
- [ ] Path cleared, civilians led to safety, 4+ casualties -1
- [ ] Path not cleared, civilians not led to safety or 8+ casualties -2

0,5 x medium difficulty xp awards 
Award XP worth: `=900/2`

Full success   +2
partial success   +1
partial failure  -1
full failure  -2 

`INPUT[number(class(small-input)):value3]`

### Hook
- a young apprentice from the church finds the pc's slightly injured and out of breath.
- "The undead.. they are swarming the street, we're trying to put the injured in the church but they are blocking the way!"
- People from various places in town are trying to make it to the church for safety and healing. They will be overwhelmed by the undead and are scattering instead. 
- "please help! They came out of nowhere and more are coming, it's urgent " "the children, the elders" "people are being chased out of their homes, the church is a holy place. [[01 GM/The Arendur Rising Campaign/The Shadow Company/Bible/Player Vault/People/Father Belderone|Father Belderone]] knows how to activate the seal, we can protect them" 


### Obstacles
**Set the scene**: 12 people are cowering behind some **crates**, **doorways** and **Carts**, the way ahead of them towards the church is blocked by undeads. Skeletons are shooting at them from behind knocked over carts and crates, the street itself is filled with zombies waiting for them to come running.  

- Escort 12 civilians, 15ft move, can be pursuaded or intimidated to dash, but dashing requires dex check acrobatics to avoid slipping and falling on the rain soaked cobblestones
- One or more collapsed market stall across a street 
	- DC 13 athletics 
- Blockade of 6 [[Skeletons]] archers behind crates, carts and stalls, 4 zombies in the street, 1 ghast behind cover giving commands
- 3 ambushes along the way 

Just outside the church's closed doors, lingers one minibosses Oathrot Wraith  ToB3 pg 396
	- [[Sir Corvin Dorn - BlackWing]] 
		- the oathrot will focus on Cedric as it recognizes the evil sword in Cedric's hands 
	- around it stands 10 [[Zombies]], 5 [[Ghouls#Ghouls]] and 15 [[Skeletons]] 
	while Lysandra is inside tormenting [[Father Belderone]] 

## Defeat Lysandra the oathrot wraith 
- [ ] Defeated Lysandra 
1,5 x medium difficulty xp awards 
Award XP worth: 1350

[[Sister Lysandra - the silver flame]] will 

## Western Palisade Breached (major)
- [ ] Defeated the undead breach 
1 x medium difficulty xp awards 
Award XP worth: 900

The palisade in the narrow end towards the graveyard has been breached and undeads are running in 
Wave of Skeletons and Zombie minions before they reach the breach 
in the breach stands a flesh golem with 6 skeletons and behind them 3 wight archers 

Clearing out the minions and the flesh golem ensures that the breach can be plugged.
From the breach, they can see a sickly green light in the distance, in the direction of the graveyard 

`INPUT[number(class(small-input)):value4]`


## The Aranae Assassin Ambush (Major)
- [ ] Defeated the assassin
Floating encounter 

1 x medium difficulty xp awards 
Award XP worth: 900


## Graveyard Battle - Defeat the Cyclops Necro Tyrant (Climactic)
- [ ] Climax overcome, boss defeated 
1 x medium difficulty xp awards 
Award XP worth: 1350

`INPUT[number(class(small-input)):value5]`

Battlefield features 
- tombstones and mausoleums: ½ to 3/4 cover
- uneven ground: difficult terrain 
- grave pit: a central spawn point for undeads, every round 1d4 undeads crawl out at initiative 20
	- 1: 2 ghouls 
	- 2: 3 skeletons 
	- 3: 3 zombies 
	- 4: 1 wight 
- Necrotic miasma: 30ft aura cyclops, DC 15 con or take 7 necrotic dmg 
Cyclops is holding his amulet of necro tyrany and channeling its power into the earth 
Nearby stands 5 skeletons, 2 shadows, 2 wight and another Oathrot Wraith lieutenant 

the grave pit can be sealed with a mausoleum door DC 18 str 

Cyclops HP: 138  AC: 16 spd 30
2 x Slam: bludgeoning + necrotic damage +10hit 10ft 4d8 on crit knocked prone DC 18 str push 10ft. AOO 10ft
Corpse bolt (recharge 5-6): AoE +7 to hit range 60 8d6 necro 10ft radius DC 15 dex for half 
Reanimation command: as a bonus action one destroyed undead can rise again with 50% hp
has a [[Javelin of Lightning]]

## Sub-Graveyard Defeat a Lieutenant Wight (Minor)
0,5 x medium difficulty xp awards 
Award XP worth: `=900/2`
Oathrot wraith in the graveyard battle 




# Loot

66 coins 
most on the cyclops at graveyard 

Rest of the cyclops loot is in the mountain "hoard" 

2 gemstones 
	Tiger eye - common 25-45gp 2d6x5
	Pearl - rare 250-450gp 2d6x50
1 art object 
	Necklace - rare 1000gp 3d6x100
lazy gm generator https://slyflourish.com/random_generators/sf-random-generator.html 

#Arendur