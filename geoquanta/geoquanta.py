"""Main module."""

import ipyleaflet
from ipyleaflet import basemaps

class Map(ipyleaflet.Map):

    def __init__(self, center=[22, 79], zoom=4, **kwargs):
        super().__init__(center=center, zoom=zoom, **kwargs)
        self.add_control(ipyleaflet.LayersControl(position='topright'))

    def add_tile_layer(self, url, name, **kwargs):
        layer = ipyleaflet.TileLayer(url=url, name=name, **kwargs)
        self.add(layer)

    def add_basemap(self, name):
        if isinstance(name, str):
            url = eval(f"basemaps.{name}").build_url()
            self.add_tile_layer(url, name)
        else:
            self.add(name)

    def add_geojson(self, data, name="geojson", **kwargs):
        
        import json
        import requests
        
        if isinstance(data, dict):
            data = data
        elif data.startswith("http"):
            data = requests.get(data).json()
        elif data.lower().endswith((".json", ".geojson")):
            with open(data) as fp:
                data = json.load(fp)
        else:
            data = data

        if "style" not in kwargs:
            kwargs["style"] = {"color": "blue", 'fillOpacity': 0.2, 'weight': 1}

        if "hover_style" not in kwargs:
            kwargs["hover_style"] = {'color': 'white', 'fillOpacity': 0.6}

        layer = ipyleaflet.GeoJSON(data=data, name=name, **kwargs)
        self.add(layer)

    def add_shapefile(self, data, name="shp", **kwargs):

        import shapefile

        if isinstance (data, str):
            with shapefile.Reader(data) as shp:
                data = shp.__geo_interface__

        if "style" not in kwargs:
            kwargs["style"] = {"color": "blue", 'fillOpacity': 0.2, 'weight': 1}

        if "hover_style" not in kwargs:
            kwargs["hover_style"] = {'color': 'white', 'fillOpacity': 0.6}

        self.add_geojson(data, name, **kwargs)
