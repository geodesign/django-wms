import mapscript

from django.conf import settings

from .symbols import WmsSymbolSet

class WmsMap():
    """
    Map objects representing mapserver map files.
    """

    layer_classes = []
    symbolset_class = WmsSymbolSet
    title = 'Django-wms service'
    srs = ['4326', '3086', '3857']
    enable_requests = ['GetMap', 'GetLegendGraphic', 'GetCapabilities']
    legend_size = (20, 20)

    def __init__(self):
        """
        Method to setup map object based on the input parameters. The map
        object represents the mapserver mapfile and is used to render
        the wms requests.
        """
        self.map_object = mapscript.mapObj()

        self.register_symbolset()
        self.register_layers()

        # Set map object properties
        self.map_object.setProjection('init=epsg:4326')
        self.map_object.setExtent(-180, -90, 180, 90)
        self.map_object.setSize(500, 500)
        self.map_object.setMetaData('wms_title', self.title)
        self.map_object.setMetaData('wms_srs', 'epsg:' + ' epsg:'.join(self.srs))
        self.map_object.setMetaData('wms_enable_request',
                               ' '.join(self.enable_requests))
        self.map_object.outputformat.transparent = mapscript.MS_ON

        # Set legend item size
        self.map_object.legend.keysizex = self.legend_size[0]
        self.map_object.legend.keysizey = self.legend_size[1]

        # Allow debugging
        if settings.DEBUG:
            self.map_object.debug = mapscript.MS_ON

    def get_layers(self):
        """
        Instantiates and returns a list of layers for this map.
        """
        # Create layer instances
        return [layer() for layer in self.layer_classes]

    def register_layers(self):
        """
        Registers all layer objects into a map object.
        """
        # Get layers
        layers = self.get_layers()

        # Check for naming consistency
        names = [layer.name for layer in layers]
        if len(names) > 1 and len(set(names)) != len(names):
            raise ValueError('Found two identical layer names in single map. '\
                'Specify unique names for layers. This error be due to '\
                'automatic naming which uses the model name as layer name '\
                'by default.')

        # Register layers
        for layer in layers:
            # Get layer
            dispatched_layer = layer.dispatch_by_type()

            # Update symbol index if symbol name was given
            # This is necessary because mapscript links the symbol index from
            # the map level symbolset with the layer level style object. So
            # this step can not be executed when instantiating the layer.
            i = 0
            while dispatched_layer.getClass(i):
                style = dispatched_layer.getClass(i).getStyle(0)
                if style.symbolname:
                    style.setSymbolByName(self.map_object, style.symbolname)
                i += 1

            # Insert layer object into map
            self.map_object.insertLayer(dispatched_layer)

    def register_symbolset(self):
        """Registers a symbol set in the current map"""

        symbolset = self.symbolset_class()

        # Add symbols
        for symb in symbolset.get_symbols():
            self.map_object.symbolset.appendSymbol(symb)
