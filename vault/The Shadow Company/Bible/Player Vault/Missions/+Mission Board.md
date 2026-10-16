---
title: "Mission Board"
dg-publish: true
tags: [missions, Arendur]
---

#missions

```dataview
table without ID link(file.link, default(file.aliases[0], file.name)) AS Mission,  status as status
from "01 GM/Campaigns/The Arendur Rising Campaign/The Shadow Company/Bible/Player Vault/Missions"
where file.name != this.file.name
SORT status ASC


```


#Arendur