Maps
====
To create a usable wms map, subclass WmsMap and add WmsLayers to it. The WmsMap class in django-raster represents the `MAP <http://mapserver.org/mapfile/map.html>`_ directive in the MapServer terminology. WmsMap defines global parameters for a map service endpoint. Only the most important MapServer MAP parameters are implemented in django-wms. The missing parameters still need to be added. The parameters that are currently implemented are listed below.

The WmsMap allone does specifiy global setup, but data has to be added through layers. Each WMS layer that can be accessed through the WmsMap is represented by a WmsLayer subclass. Specify a list of layers classes when creating a WmsLayer subclass. For example
::
    # In myapp.wmsmap

    from wms.maps import WmsMap
    from myapp.wmslayers import MyFirstLayer, MySecondLayer, MyThirdLayer

    class MyMap(WmsMap):
        layer_classes = [MyFirstLayer, MySecondLayer, MyThirdLayer]

Map parameters
--------------
A list of map parameters that can be specified as class attributes when subclassing WmsMap.

**Title**

The title of a WMS service endpoint. Defaults to
::
    title = 'Django-wms service'

**SRS**

An array of map projections (srid) can be requested through the map. Defaults to
::
    srs = ['4326', '3086', '3857']

**Enable-requests**

WMS request types thata are allowed for the map. Defaults to
::

    enable_requests = ['GetMap', 'GetLegendGraphic', 'GetCapabilities']

**Legend size**

Size in pixels of rendered icons on legends returned by the GetLegendGraphic request. Defaults to
::
    legend_size = (20, 20)
