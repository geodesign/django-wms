import mapscript

from django.http import HttpResponse

from django.views.generic import View

from wms.maps import WmsMap

###############################################################################
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

        # Set request parameters
        for param, value in request.GET.items():
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
