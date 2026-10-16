---
category: moc

tags: [domainmoc, Rirroneth, poi-landmarks, Arendur]
---

#domainmoc #Rirroneth #poi-landmarks

MAP: [[Rirroneth domain map.png]]

# POI's
```dataview
Table without ID
	file.link as "Name", 
	region as "Region"
from #Rirroneth 
where contains(category, "poi")
Flatten region
sort region ASC
```


#Arendur