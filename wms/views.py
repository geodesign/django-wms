from math import pi

import mapscript
from PIL import Image
from raster.models import RasterTile

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


        # Setup wms view allowing only GET requests
        super(WmsView, self).__init__(http_method_names=['get'], **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Html GET method of WmsView. This view renders WMS requests into
        corresponding responses using the attached WmsMap class.
        Responses are mainly images and xml files.
        """
        # Create response
        response = HttpResponse()

        # Setup wms request object
        ows_request = mapscript.OWSRequest()

        # If tile kwargs were provided, add tile parameters to request
        tileparams = self.tilemode()

        if tileparams:
            # Get image format from url
            format = {'.png': 'image/png',
                      '.jpg': 'image/jpeg'}[self.kwargs.get('format')]

            # Return empty image if tile cant be found
            if not self.tile_exists(*tileparams):
                # Get image type and size
                imagetype = 'PNG' if format == 'image/png' else 'JPEG'
                imagesize = 256, 256
                response['Content-Type'] = format

                # Create image and save it to response
                im = Image.new("RGBA", imagesize, (0, 0, 0, 0))
                im.save(response, imagetype)

                return response
            else:
                tilebounds = self.get_tile_bounds(*tileparams)

                # Get layer name
                layers = self.kwargs.get('layers')

                # Setup wms parameter object
                request_data = {
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

                request.GET = dict(request.GET.items() + request_data.items())

        # Set ows parameters from request data
        for param, value in request.GET.items():
            ows_request.setParameter(param, value)

        # Instantiate WmsMap class
        self.wmsmap = self.map_class(request, **kwargs)

        # Dynamically use host for declaring service endpoint
        onlineresource = request.build_absolute_uri().split('?')[0] + '?'
        self.wmsmap.map_object.setMetaData('wms_onlineresource',
                                           onlineresource)

        # Dispatch map rendering
        self.wmsmap.map_object.OWSDispatch(ows_request)

        # Strip buffer from headers
        mapscript.msIO_stripStdoutBufferContentHeaders()

        # Store contenttype
        contenttype = mapscript.msIO_stripStdoutBufferContentType()

        # Write data to response
        response.write(mapscript.msIO_getStdoutBufferBytes())

        # Set contenttype
        response['Content-Type'] = contenttype

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

    def tilemode(self):
        """Returns true if the request is for XYZ tiles"""

        # Try to get tile indices from url
        x = self.kwargs.get('x', '')
        y = self.kwargs.get('y', '')
        z = self.kwargs.get('z', '')

        if not (x and y and z):
            return False
        else:
            return int(x), int(y), int(z)

    def tile_exists(self, x, y, z):
        """Returns true if the requested XYZ tile exists"""
        return RasterTile.objects.filter(
                tilex=x,
                tiley=y,
                tilez=z,
                filename=self.kwargs.get('layers', '')).exists()
