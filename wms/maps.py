import mapscript

from wms.layers import WmsLayer

class WmsMap():
    """
    Map objects representing mapserver map files.
    """

    layer_classes = []
    title='Django-wms service'
    srs=['4326', '3086', '3857']
    enable_requests=['GetMap', 'GetLegendGraphic', 'GetCapabilities']
    legend_size=(20,20)

    def get_map_object(self):
        """
        Method to setup map object based on the input parameters. The map
        object represents the mapserver mapfile and is used to render
        the wms requests.
        """
        map_object = mapscript.mapObj()

        self.register_layers(map_object)
        
        # Set map object properties
        map_object.setProjection('init=epsg:4326')
        #map_object.setExtent(-180, -90, 180, 90)
        #map_object.setSize(500, 500)
        map_object.setMetaData('wms_title', self.title)
        map_object.setMetaData('wms_onlineresource', '/wms/?')
        map_object.setMetaData('wms_srs', 'epsg:' + ' epsg:'.join(self.srs))
        map_object.setMetaData('wms_enable_request', ' '.join(self.enable_requests))
        map_object.outputformat.transparent = mapscript.MS_ON

        # Set legend item size
        map_object.legend.keysizex = self.legend_size[0]
        map_object.legend.keysizey = self.legend_size[1]

        return map_object

    def get_layers(self):
        """
        Instantiates and returns a list of layers for this map.
        """
        return [layer() for layer in self.layer_classes]

    def register_layers(self, map_object):
        """
        Registers all layer objects into a map object.
        """
        # Get layers
        layers = self.get_layers()

        # Check for naming consistency
        names = [layer.name for layer in layers]
        if len(names) > 1 and len(set(names)) != len(names):
            raise ValueError('Found two identical layer names in single map. '\
                'Specify unique names for layers. This error be due to automatic naming '\
                'which uses the model name as layer name by default.')

        # Register layers
        for layer in layers:
            map_object.insertLayer(layer.dispatch_by_type())
