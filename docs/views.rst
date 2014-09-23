Map Views
=========
The third step in creating a map service is to create a class based view by extending the ``WmsView`` class. The WmsView class passes the request from django to mapscript and returns the rendered image. By default, the WmsView acts as a proper Web Map Service view, and expects the corresponding parameters in the html request for it to work. It can also act as Tile Map Service if the urlpattern is configured accordingly (see below).

After creating at least one WmsLayer and adding it to a WmsMap, the WmsView can be setup by sublcassing VmsView and pointing the newly created class to the WmsMap subclass. ::
    
    # In myapp.wmsviews

    from wms.views import WmsView
    from myapp.wmsmaps import MyWmsMap

    class MyWmsView(WmsView):
        map_class = MyWmsMap

Web Map Server
--------------
With a view prepared, the view can be added to a url pattern by calling the ``as_view()`` method, which will return a proper view function. In the case of a WMS url, the url pattern is straightforward. ::

    # urls.py

    from django.conf.urls import patterns,url
    from myapp.wmsviews import MyWmsView

    urlpatterns = patterns('',
        # WMS endpoint
        url(r'^wms/$', MyWmsView.as_view(), name='wms'),
    )

Since MapServer works with query parameters, the WmsView urlpattern is simple, all additional information is passed on through the GET request parameters. The WmsView will automatically handle those request parameters to render a corresponding image.

Tile Map Server (XYZ)
-----------------------
The same view can also be used to create a Tile Map Service. The TMS functionality looks for five arguments it obtains from the urlpattern: `layers`, `x`, `y`, `z` and `format`. If those three arguments are present in the urlpattern, the view will act as a tile map service and return the corresponding indexed tile for the layer and format requested. An example url configuration could look like this::

    # urls.py

    from django.conf.urls import patterns,url
    from myapp.wmsviews import MyWmsView

    urlpatterns = patterns('',
        # TMS endpoint
        url(r'^tile/(?P<layers>[^/]+)/(?P<z>[0-9]+)/(?P<x>[0-9]+)/(?P<y>[0-9]+)(?P<format>\.jpg|\.png)$',
            MyWmsView.as_view(), name='tile'),
    )

In the TMS case, the WmsView calculates the lat/lon bounds for the requested tile behind the scenes and passes that on to the "normal" WmsView mode. The TMS functionality is thus simply a routine that is sandwiched between the normal WmsView part and the request, dynamically calculating tile bounds from the x-y-z indices.

Caching
-------
For larger data sets, the dynamic rendering of WMS or TMS request can be quite expensive. Also, for mapping applications, the requested map fragments are often repeated. This is specially true for indexed tiles, as those have short and static urls. WMS requests often have coordinate values that are floating point numbers and tend to vary more.

In any case, it is recommended to use the django-wms package in combination with a caching framework. If a caching backend is configured, caching the map service views is trivial. One simple example is the following, where the reuqested tiles would be cached for 24 hours ::
    
    from django.views.decorators.cache import cache_page
    
    url(r'^tile/(?P<layers>[^/]+)/(?P<z>[0-9]+)/(?P<x>[0-9]+)/(?P<y>[0-9]+)(?P<format>\.jpg|\.png)$',
        cache_page(60 * 60 * 24)(MyWmsView.as_view()), name='tile'),

For more information on how to setup caching with django, see the `official documentation <https://docs.djangoproject.com/en/dev/topics/cache/>`_.

Module docs
-----------
Auto-generated part of the module documentation.

.. automodule:: wms.views
    :members: