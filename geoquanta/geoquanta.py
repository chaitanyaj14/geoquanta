"""Main module."""

import ipyleaflet
from ipyleaflet import basemaps

class Map(ipyleaflet.Map):
    """This is the map class that inherits from ipyleaflet.Map.

    Args:
        ipyleaflet (Map): The ipyleaflet.Map class
    """
    def __init__(self, center=[22, 79], zoom=4, **kwargs):
        """Initialize the map.

        Args:
            center (list, optional): Set the center of the map. Defaults to [22, 79].
            zoom (int, optional): Set the zoom level of the map. Defaults to 4.
        """
        super().__init__(center=center, zoom=zoom, **kwargs)
        self.add_control(ipyleaflet.LayersControl(position='topright'))

    def add_tile_layer(self, url, name, **kwargs):
        """Adds a tile layer to the map.

        Args:
        url (str): The URL of the tile layer.
        name (str): The name of the tile layer.
        **kwargs: Additional keyword arguments accepted by ipyleaflet.TileLayer.
        """
        layer = ipyleaflet.TileLayer(url=url, name=name, **kwargs)
        self.add(layer)

    def add_basemap(self, name):
        """
        Adds a basemap to the map.

        Args:
        name (str or ipyleaflet.basemaps.BaseMap): The name of the basemap as a string, or a pre-defined ipyleaflet basemap.
        """
        if isinstance(name, str):
            url = eval(f"basemaps.{name}").build_url()
            self.add_tile_layer(url, name)
        else:
            self.add(name)

    def add_geojson(self, data, name="geojson", **kwargs):
        """
        Adds a GeoJSON layer to the map.

        Args:
        data (dict or str): The GeoJSON data as a dictionary, URL, or file path.
        name (str): The name of the GeoJSON layer (default is "geojson").
        **kwargs: Additional keyword arguments accepted by ipyleaflet.GeoJSON.
        """
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
        """
        Adds a shapefile as a GeoJSON layer to the map.

        Args:
        data (str): The path to the shapefile.
        name (str): The name of the GeoJSON layer (default is "shp").
        **kwargs: Additional keyword arguments accepted by add_geojson.
        """

        import shapefile

        if isinstance (data, str):
            with shapefile.Reader(data) as shp:
                data = shp.__geo_interface__

        if "style" not in kwargs:
            kwargs["style"] = {"color": "blue", 'fillOpacity': 0.2, 'weight': 1}

        if "hover_style" not in kwargs:
            kwargs["hover_style"] = {'color': 'white', 'fillOpacity': 0.6}

        self.add_geojson(data, name, **kwargs)
