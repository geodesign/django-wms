==============
WMS for Django
==============

Django app for wms integration using mapscript.

Detailed documentation will be in the "docs" directory.

Quick start
-----------

1. Add "wms" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'wms',
    )

2. Include the wms URLconf in your project urls.py like this::

    url(r'^wms/', include('wms.urls')),

3. Run `python manage.py migrate` to create the wms models.
