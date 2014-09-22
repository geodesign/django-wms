Django WMS Framework
======================
The Django WMS Framework is a toolkit that makes it easy to build a `Web Map Service (WMS) <http://en.wikipedia.org/wiki/Web_Map_Service>`_ or a x-y-z `Tile Map Service <http://en.wikipedia.org/wiki/Tile_Map_Service>`_. Rendering of both vector and raster data formats are supported.

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
The structure of django-wms is therefore oriented around how MapServer works. The concept of mapfiles and the layer objects defined in mapfiles are translated into a ``Maps`` module and a ``Layers`` module within django-wms.

`Web Map Service <http://en.wikipedia.org/wiki/Web_Map_Service>`_
`Tile Map Service <http://en.wikipedia.org/wiki/Tile_Map_Service>`_


Getting started
---------------


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. autoclass:: wms.views.WmsView

