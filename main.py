import folium
import pandas


def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation <= 3000:
        return 'orange'
    else:
        return 'red'


m = folium.Map(
    location=(38.58, -99.09),
    zoom_start=6,
    tiles="Mapbox Bright"
)

data = pandas.read_csv("volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

fgv = folium.FeatureGroup(name="Volcanoes")
for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(
        location=(lt, ln),
        popup=str(el)+" m",
        radius=6,
        color=color_producer(el),
        fill_opacity=0.7
    ))


fgp = folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(data=(open("world.json", 'r', encoding='utf-8-sig').read()),
                             style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                             else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

m.add_child(fgv)
m.add_child(fgp)
m.add_child(folium.LayerControl())

m.save("index.html")
