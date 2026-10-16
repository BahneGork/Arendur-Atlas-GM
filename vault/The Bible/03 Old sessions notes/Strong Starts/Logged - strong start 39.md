---
tags: [session39, Arendur]
---

Session: #session39

Real date: ?
Location:  Rirroneth Domain
situation:  Travelling
Date: 12th Mirtul
Hour: 13:30

### Start Scene
When last we left our heroes.... Long rest inside tiny hut.

Landskabet er sten og kød, sener, tentakler, tarme, knogler, munde, øjne i alle afskygninger. En morbid afspejlning af den rigtige verden, træer buske, bakker, marker alt sammen i forvrænget kødlig tilstand. Et blegt blåt lys kaster skygger i landskabet, himlen ligner en fjern galakse med gul-grønne skyer og en mørk stjerne himmel. Siden i lagde jer til at sove er der kommet en gul/orange cirkel i himlen og inden i den er der det sorteste sort i nogen sinde har set.

I har fundet et lille område klemt inde mellem nogle "bakker" hvor i har holdt hvil. Da i begiver jer videre ser i flere steder i det fjerne lilla dis der hænger og svæver hen over landskabet. 

Rundt omkring på "jorden" har i også lagt mærke til pytter, med orange væske. Kort efter at i forlader jeres hvilested, kommer i til en uhellig cirkel af monster tænder på størrelse med ogres, dækket med udhugget ugenkendelige runer. I er ca 120 fod fra monumentet, en svag duft af salmiak hænger i luften. 

Passive Perception DC  disadv. 17
2 [[carrion crawler]] hidden in the ground
4 [[chuul]]s hiding in 2 pools of orange water 

Characterslevel:: `=[[Global party values]].level`

Total sum of player levels: `= [[Global party values]].players*[[Global party values]].level`

character level 4+
Deadly Total sum of monster CR: `=[[Global party values]].players*[[Global party values]].level/2`

character level 1-3
Deadly total sum of monster CR: `=[[Global party values]].players*[[Global party values]].level/4`

test characters level inline key: `=this.Characterslevel`

Deadly threshold `=[[Global party values]].Deadly`




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


#Arendur