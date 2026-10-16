---
tags: [session40, Arendur]
---

Session: #session40

Real date: 14 nov 2022
Location:  Rirroneth Domain
situation:  Mindflayer labyrinth
Date: 12th Mirtul
Hour: 13:30? (time doesnt exist)

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
# Start Scene
Brumor & Anton løber imod døråbningen, Cedric står og observerer og Frekka forsvandt fra syne.

Frekka:
[[Ancient broken archway - Eldorath]]
Du træder igennem døråbningen og mærker øjeblikketligt en anderledes form for stilhed, ikke blot lydløst, men tavshed på et helt andet niveau. Som om for første gang siden i trådte ud på det her andet plan er der fred og ro i dit sind.
Men også hvad du ser ændrer sig, hvor før der bare var en "helt almindelig hule" er der nu et mesterværk af et klinkegulv i hvidt, gult og blåt. 

Brumor & Anton:

Cedric:



# Handouts
![[Intellect devourer image.png]]

![[Vampiric Mindflayer image.png]]

#Arendur