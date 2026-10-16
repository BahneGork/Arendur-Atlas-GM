---
class: Barbarian

tags: [playercharacters, Arendur]
---

#playercharacters 

```dataview
table class1, class2
from "01 GM/The Arendur Rising Campaign/The Bible/04 Fact sheets/03 People/Playercharacters"
where (class1 = this.class)
```

# Active Pc's
```dataview
table player, class1, path1, class2, path2, race, level
	from "01 GM/The Arendur Rising Campaign/The Bible/04 Fact sheets/03 People/Playercharacters"
where (status="active" and type="pc")
```

# Retainers
```dataview
table type, patron, Last-Location
from "01 GM/The Arendur Rising Campaign/The Bible/04 Fact sheets/03 People"
where (status = "retainer")
```


#Arendur