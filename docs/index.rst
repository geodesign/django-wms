Django WMS Framework
======================
The Django WMS Framework is a toolkit that makes it easy to integrate a `Web Map Service (WMS) <http://en.wikipedia.org/wiki/Web_Map_Service>`_ or a x-y-z `Tile Map Service <http://en.wikipedia.org/wiki/Tile_Map_Service>`_ into a Django project. Rendering of both vector and raster data formats are supported.

Requirements
------------
The processing of spatial data in django-wms relies on `MapServer <http://mapserver.org/index.html>`_ and its python bindings `MapScript <http://mapserver.org/mapscript/mapscript.html>`_. Raster data integration depends on the `django-raster <https://pypi.python.org/pypi/django-raster/0.1.0>`_ package. The use of `PostGIS <http://postgis.net/>`_ as the database backend is required as well, for raster ntegration PostGIS >= 2.0 is required (see also django-raster package).

Installation
------------
1. Install package with ``pip install django-wms``

2. Add "wms" to your INSTALLED_APPS setting like this::

        INSTALLED_APPS = (
            ...
            'wms',
        )

Example
-------
The structure of django-wms is closely tied to how MapServer works. The concept of mapfiles is translated into a ``Maps`` module. Layer definitions and classes for symbology and cartography are represented in the ``Layers`` module within django-wms.

To create a mapping service, subclass the django-wms layer, map and view classes and connect them to an existing model in django that has a spatial field (such as Point, Polygon or MultiPolygon). An example ``wms_config.py`` module could look like this:::

    ### wms_config.py

    # Load django-wms classes
    from wms import maps, layers, views

    # Load model with spatial field (Point, Polygon or MultiPolygon)
    from myapp.models import MySpatialModel


    # Subclass the WmsLayer class and point it to a spatial model
    class MyWmsLayer(layers.WmsLayer):
        model = MySpatialModel

    # Subclass the WmsMap class and add the layer to it
    class MyWmsMap(maps.WmsMap):
        layer_classes = [ MyWmsLayer ]

    # Subclass the WmsView to create a view for the map
    class MyWmsView(views.WmsView):
        map_class = MyWmsMap

With the WmsView subclass in place, the only thing left to do to create a functional map service is to hook the view into a url. An example url configuration ``urls.py`` could be::
    
    ### urls.py

    # Import the wms view
    from myproject.wms_config import MyWmsView

    # Add url patterns to setup map services from the view
    urlpatterns = patterns('',

        # This creates a WMS endpoint
        url(r'^wms/$', MyWmsView.as_view(), name='wms'),

        # This creates a TMS endpoint
        url(r'^tile/(?P<layers>[^/]+)/(?P<z>[0-9]+)/(?P<x>[0-9]+)/(?P<y>[0-9]+)(?P<format>\.jpg|\.png)$',
            MyWmsView.as_view(), name='tms'),
    )

The django-wms package will automatically detect the first spatial field it can find in ``MySpatialModel`` and create a WMS endpoint from the class based view. If the three arguments ``x``, ``y`` and ``z`` are found in the urlpattern, the view functions as TMS endpoint.

Indices and tables
------------------
`Web Map Service <http://en.wikipedia.org/wiki/Web_Map_Service>`_
`Tile Map Service <http://en.wikipedia.org/wiki/Tile_Map_Service>`_


* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. autoclass:: wms.views.WmsView

