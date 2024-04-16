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
        
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True
        
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
        
    def add_image(self, url, bounds, name='image', **kwargs):
        """
        Adds an image overlay to the map.

        Args:
        - url (str): The URL of the image.
        - bounds (tuple): A tuple of the form (south, west, north, east) representing the bounds of the image overlay.
        - name (str, optional): The name of the image overlay. Default is 'image'.
        - **kwargs: Additional keyword arguments accepted by ipyleaflet.ImageOverlay.
        """
        layer = ipyleaflet.ImageOverlay(url=url, bounds=bounds, name=name, **kwargs)
        self.add(layer)
        
    def add_raster (self, data, name="raster", zoom_to_layer=True, **kwargs):
        """
        Add a raster layer to the map.

        Args:
            data: The raster data to be added to the map.
            name (str): The name of the raster layer (default is "raster").
            zoom_to_layer (bool): Whether to zoom to the added layer (default is True).
            **kwargs: Additional keyword arguments to be passed.

        Raises:
            ImportError: If the localtileserver package is not installed.
        """
        try:
            from localtileserver import TileClient, get_leaflet_tile_layer
        except ImportError:
            raise ImportError("Please install the localtileserver package.")
        
        client = TileClient(data)
        layer = get_leaflet_tile_layer(client, name=name)
        self.add(layer)
        
        if zoom_to_layer:
            self.center = client.center()
            self.zoom = client.default_zoom
    