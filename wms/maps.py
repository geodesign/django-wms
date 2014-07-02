"""
Map objects representing mapserver map files.

Each map object should be connected to a single wms url endpoint.
"""

import mapscript

class WmsMap():
    """Base map object"""

    def __init__(self, title='Django-wms service', srs=['4326', '3086'],
            enable_requests=['GetMap', 'GetLegendGraphic', 'GetCapabilities'],
            legend_size=(20,20)):

        self.title = title
        self.srs = srs
        self.enable_requests = enable_requests
        self.legend_size = legend_size

        self.map_object = mapscript.mapObj()

    def get_map(self):
        """
        Method to setup map object based on the input parameters. The map
        object represents the mapserver mapfile and is used to render
        the wms requests.
        """
        
        # Set map object properties
        self.map_object.setProjection('init=epsg:4326')
        self.map_object.setMetaData('wms_title', self.title)
        self.map_object.setMetaData('wms_onlineresource', '/wms/?')
        self.map_object.setMetaData('wms_srs', 'epsg:' + ' epsg:'.join(self.srs))
        self.map_object.setMetaData('wms_enable_request', ' '.join(self.enable_requests))
        self.map_object.outputformat.transparent = mapscript.MS_ON

        # Set legend item size
        self.map_object.legend.keysizex = self.legend_size[0]
        self.map_object.legend.keysizey = self.legend_size[1]

        return self.map_object

    def register(self, layer):
        """Register layer object to the map instance"""

        self.map_object.insertLayer(layer.layer_object)
