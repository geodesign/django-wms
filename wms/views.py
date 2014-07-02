import mapscript

from django.http import HttpResponse

from django.views.generic import View

###############################################################################
class WmsView(View):
    """WMS view class for setting up WMS endpoints"""

    def __init__(self, **kwargs):
        # Setup mapscript IO stream
        mapscript.msIO_installStdoutToBuffer()

        # Ceck if WmsMap has been specified
        if not hasattr(self, 'wmsmap'):
            raise ValueError('WmsView does not have a WmsMap attached. '\
                'Specify map class in wmsmap attribute.')

        # Setup wms view allowing only GET requests
        super(WmsView, self).__init__(http_method_names=['get'], **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Get method of WmsView. This view renders WMS requests into 
        corresponding responses using the attached WmsMap class.
        Responses are mainly images and xml files.
        """

        # Setup wms request object
        ows_request = mapscript.OWSRequest()

        # Set request parameters
        for param, value in request.GET.items():
            ows_request.setParameter(param, value)
        
        # Dispatch map rendering
        self.wmsmap.get_map().OWSDispatch(ows_request)
        
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
