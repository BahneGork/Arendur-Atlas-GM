---
map_height_y: 1121
map_width_x: 1822
scale_pixels: 157.8
scale_pixels_range: 24
mapCalc1: 0.1520912547528517
---

> [!NOTE]- Quick Calculator  
> Map Height in Pixels: `INPUT[number:map_height_y]`  
> Map Width in Pixels: `INPUT[number:map_width_x]`  
> lat: `VIEW[{map_height_y} / 2][math]`  
> long: `VIEW[{map_width_x} / 2][math]`  
> How Many Pixels In Scale: `INPUT[number:scale_pixels]`  
> How Many Units in Scale: `INPUT[number:scale_pixels_range]`  
> Scale: `VIEW[1/({scale_pixels}/{scale_pixels_range})][math:mapCalc1]`

image2:: [[Delios no pins.png|Delios town]]
<br>
<br>


```leaflet  
id: mistyfallsregion22 ### Must be unique with no spaces  
image: Mistyfalls = [[MistyFallsRegion-Ursia.png|Misty Falls region]] ### Link to the map image file. Do not add a ! in front of the image 
bounds: [[0,0], [1121, 1822]] ### Size of the map in px Height_y, Width_x. Ignore 0,0  
height: 1121px ### Size of the leaflet embed in px on your screen  
width: 90% ### Size of the leaflet embed in your note  
lat: 560.5 ### To center the map, make this half of the map height.  
long: 911 ### To center the map, make this half of the map width.  
minZoom: -0.5 ### Controls how far away from the map you can zoom out. Hover over the target icon to see the current level.  
maxZoom: 3 ### Controls how far towards the map you can zoom in. Hover over the target icon to see the current level.  
defaultZoom: -0.5 ### Sets the default zoom level when the map loads. Hover over the target icon to see the current level.  
zoomDelta: 0.5 ### Adjust how much the zoom changes when you zoom in or out.  
unit: miles ### The value displayed when measuring so you know what type of unit is being measure.  
scale: 0.1520912547528517 ### Real units/px (resolution) of your map  
recenter: false  
darkmode: false ### marker
lock: false
draggable: true
```
