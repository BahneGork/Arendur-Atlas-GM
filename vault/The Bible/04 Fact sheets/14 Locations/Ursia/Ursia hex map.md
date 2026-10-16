---
map_height_y: 751
map_width_x: 446
scale_pixels: 12
scale_pixels_range: 24
mapCalc1: 2
---

```leaflet  
id: diamor-ursia-hex1 ### Must be unique with no spaces  
image: [[diamor-Ursia.png]] ### Link to the map image file. Do not add a ! in front of the image  
bounds: [[0,0], [751, 446]] ### Size of the map in px Height_y, Width_x. Ignore 0,0  
height: 760px ### Size of the leaflet embed in px on your screen  
width: 65% ### Size of the leaflet embed in your note  
lat: 375,5 ### To center the map, make this half of the map height.  
long: 223 ### To center the map, make this half of the map width.  
minZoom: -1 ### Controls how far away from the map you can zoom out. Hover over the target icon to see the current level.  
maxZoom: 4 ### Controls how far towards the map you can zoom in. Hover over the target icon to see the current level.  
defaultZoom: 1.5 ### Sets the default zoom level when the map loads. Hover over the target icon to see the current level.  
zoomDelta: 0.5 ### Adjust how much the zoom changes when you zoom in or out.  
unit: mi ### The value displayed when measuring so you know what type of unit is being measure.  
scale: 2 ### Real units/px (resolution) of your map  
recenter: true  
darkmode: false ### marker
```
