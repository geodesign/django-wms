from math import pi

import mapscript

from django.http import HttpResponse
from django.views.generic import View

from wms.maps import WmsMap

class WmsView(View):
    """WMS view class for setting up WMS endpoints"""

    map_class = None

    def __init__(self, **kwargs):
        # Setup mapscript IO stream
        mapscript.msIO_installStdoutToBuffer()

        # Verify that map class has been specified correctly
        if not self.map_class or not issubclass(self.map_class, WmsMap):
            raise TypeError('map_class attribute is not a subclass of WmsMap. '\
                'Specify map in map_class attribute.')

        # Instantiate map
        self.map = self.map_class().get_map_object()

        # Setup wms view allowing only GET requests
        super(WmsView, self).__init__(http_method_names=['get'], **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Html GET method of WmsView. This view renders WMS requests into 
        corresponding responses using the attached WmsMap class.
        Responses are mainly images and xml files.
        """
        # Setup wms request object
        ows_request = mapscript.OWSRequest()

        # Get ows parameters, try using tiles, otherwise use request
        parameters = self.tiles()
        if not parameters:
            parameters = request.GET

        for param, value in parameters.items():
            ows_request.setParameter(param, value)

        # Dynamically use host for declaring service endpoint
        onlineresource = request.build_absolute_uri().split('?')[0] + '?'
        self.map.setMetaData('wms_onlineresource', onlineresource)

        # Dispatch map rendering
        self.map.OWSDispatch(ows_request)
        
        # Store contenttype
        contenttype = mapscript.msIO_stripStdoutBufferContentType()

        # Strip buffer from headers
        mapscript.msIO_stripStdoutBufferContentHeaders()

        # Create response
        response = HttpResponse()

        # Set contenttype
        response['Content-Type'] = contenttype

        # Write data to response
        response.write(mapscript.msIO_getStdoutBufferBytes())

        return response

    def get_tile_bounds(self, x, y, z):
        """
        Calculates tile bounding box from Tile Map Service XYZ indices.
        """
        # Setup scale factor for bounds calculations
        res = 2 * pi * 6378137
        shift = res / 2.0
        scale = res / 2**z

        # Calculate bounds
        minx = x * scale - shift
        maxx = (x+1) * scale - shift
        miny = shift - (y+1) * scale
        maxy = shift - y * scale

        # Convert bounds to query string
        return ','.join([repr(coord) for coord in [minx, miny, maxx, maxy]])

    def tiles(self):
        """
        This method checks the url parameters for xyz arguments, if found it
        uses those to compute bounds for wms rendering.
        """
        # Try to get tile indices from url
        x = self.kwargs.get('x', '')
        y = self.kwargs.get('y', '')
        z = self.kwargs.get('z', '')

        if not (x and y and z):
            return None
        else:
            # Convert indices to integers
            x,y,z = int(x), int(y), int(z)

            # Get the tile bounds
            tilebounds = self.get_tile_bounds(x,y,z)

            # Get layers to draw from url
            layers = self.kwargs.get('layers')

            # Get image format from url
            format = {'.png': 'image/png', 
                      '.jpg':'image/jpeg'}[self.kwargs.get('format')]

            # Setup wms parameter object
            return {
                    'SERVICE': 'WMS',
                    'REQUEST': 'GetMap',
                    'VERSION': '1.1.1',
                    'TRANSPARENT': 'true',
                    'HEIGHT': '256',
                    'WIDTH': '256',
                    'SRS': 'EPSG:3857',
                    'FORMAT': format,
                    'LAYERS': layers,
                    'BBOX': tilebounds
                    }
