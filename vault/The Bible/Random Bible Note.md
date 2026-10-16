---
tags: [Arendur]
---

# Random Bible Note
```dataviewjs 
let docs = dv.pages('"01 GM/Campaigns/The Arendur Rising Campaign/The Bible"');
let length = docs.length; 
let numberToReturn = 5; 
var randos = getRandos(docs, length, numberToReturn);

dv.list(randos); 

function getRandos(list, max, itemNum) { 
	var items = []; 
	for (var i=0;i<itemNum;i++) {
		items.push(list[Math.floor(Math.random() * max)].file.link);
	} 
	return items; 
}
```




#Arendur