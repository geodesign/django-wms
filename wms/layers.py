import mapscript

from django.db import connection
from django.conf import settings
from django.contrib.gis.db import models

try:
    from raster.fields import RasterField
except:
    RasterField = None
    pass

def to_hex(color):
    if not color[0] == '#':
        rgb = tuple(map(int, color.split(' ')))
        color = '#%02x%02x%02x' % rgb
    return color

class WmsLayer():
    """
    WMS Layer class representing mapserver layers. Use this class to serve data
    from models as WMS layers.

    By default, WmsLayer will use the first spatial field it finds, but the
    field to use can also be specified explicitly using geo_field_name.
    """

    model = None
    name = None
    geo_field_name = None
    layer_name = None
    where = None
    cartography = []
    classitem = None

    def dispatch_by_type(self):
        """
        Instantiates layer based on type of spatial field. Finds spatial field
        automatically if not set explicitly.
        """
        # Get data type for this model
        field_name = self.get_spatial_field().__class__.__name__

        if field_name == 'RasterField':
            return self.get_raster_layer()
        else:
            return self.get_vector_layer(field_name)

    def get_spatial_field(self):
        """
        Returns the spatial type for the given model based on field types.
        """
        # Setup geo field options
        geo_field_options = [models.PointField, models.LineStringField,
                             models.PolygonField, models.MultiPolygonField]
        if RasterField:
            geo_field_options += [RasterField]

        # If name is specified, use it, otherwise loop through candidates
        if self.geo_field_name:
            return self.model._meta.get_field_by_name(self.geo_field_name)
        else:
            for field in self.model._meta.concrete_fields:
                
                if any([issubclass(field.__class__, geofield)
                                for geofield in geo_field_options]):
                    return field

        # Raise error if no spatial field match was found
        raise TypeError('No spatial field match found in specified model. '\
            'Specify a model that has a spatial field')

    def get_name(self):
        """
        Returns WMS layer name, defaults to model name if not provided.
        """
        if self.name:
            return self.name
        else:
            return self.model._meta.model_name

    def get_srs(self):
        """
        Returns srs for this layer based on field specification.
        """
        instance = self.model.objects.first()

        if hasattr(instance, 'rasterlayer'):
            return str(instance.rasterlayer.srid)
        else:
            return str(self.get_spatial_field().srid)

    def get_base_layer(self):
        """
        Instantiates and returns a base WMS layer with attributes that are
        not specific to data types.
        """
        # Instanciate mapscript layer
        layer = mapscript.layerObj()
        layer.status = mapscript.MS_OFF
        layer.name = self.get_name()
        layer.setProjection('init=epsg:' + self.get_srs())
        layer.metadata.set('wms_title', 'Landcover')
        layer.opacity = 80

        # Allow debugging
        if settings.DEBUG:
            layer.debug = mapscript.MS_ON

        return layer

    def get_vector_layer(self, field_name):
        """
        Connect this layer to a vector data model.
        """
        # Get base layer
        layer = self.get_base_layer()

        # Specify input data type
        layer_types = {
                'PointField': mapscript.MS_LAYER_POINT,
                'LineStringField': mapscript.MS_LAYER_LINE,
                'PolygonField': mapscript.MS_LAYER_POLYGON,
                'MultiPolygonField': mapscript.MS_LAYER_POLYGON
                }
        layer.type = layer_types[field_name]

        # Set connection to DB
        layer.setConnectionType(mapscript.MS_POSTGIS, '')
        layer.connection = 'host={host} dbname={dbname} user={user} '\
                           'port={port} password={password}'.format(
            host=settings.DATABASES['default']['HOST'],
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            port=settings.DATABASES['default']['PORT'],
            password=settings.DATABASES['default']['PASSWORD']
            )

        # Select data column
        layer.data = 'geom FROM {0}'.format(self.model._meta.db_table)

        # Set class item
        if self.classitem:
            layer.classitem = self.classitem

        # Cartography settings
        if self.cartography:
            for cart in self.cartography:
                # Set categorization
                category = mapscript.classObj(layer)
                category.setExpression(cart.get('expression', ''))
                category.name = cart.get('name', cart.get('expression',''))
                # Set category style
                style = mapscript.styleObj(category)
                style.color.setHex(to_hex(cart.get('color', '#777777')))
                style.outlinecolor.setHex(to_hex(cart.get('outlinecolor', '#000000')))
                style.width = cart.get('width', 1)
        else:
            category = mapscript.classObj(layer)
            category.name = layer.name
            style = mapscript.styleObj(category)
            style.color.setHex('#777777')
            style.outlinecolor.setHex('#000000')
            style.width = 1

        return layer

    def get_raster_layer(self):
        """
        Connect this layer to a raster model.
        """
        # Get base layer and specify type
        layer = self.get_base_layer()
        layer.type = mapscript.MS_LAYER_RASTER
        
        # Set class item
        if self.classitem:
            layer.classitem = self.classitem
        else:
            layer.classitem="[pixel]"

        # Set data source
        layer.data = "PG:host='{host}' dbname='{dbname}' user='{user}' "\
                     "port='{port}' password='{password}' mode=2 ".format(
                            host=settings.DATABASES['default']['HOST'],
                            dbname=settings.DATABASES['default']['NAME'],
                            user=settings.DATABASES['default']['USER'],
                            port=settings.DATABASES['default']['PORT'],
                            password=settings.DATABASES['default']['PASSWORD']
                        )

        layer.data += "table='" + self.model._meta.db_table + "'"

        # Set where clause if provided
        if self.where:
            layer.data += " where='" + self.where + "'"

        # Set nodata if provided
        if self.nodata:
            layer.addProcessing("NODATA=" + self.nodata)

        # Class and style settings
        if self.cartography:
            for cart in self.cartography:
                # Set categorization
                category = mapscript.classObj(layer)
                category.setExpression(cart['expression'])
                category.name = cart['name']
                # Set category style
                style = mapscript.styleObj(category)
                style.color.setHex(to_hex(cart['color']))
        else:
            category = mapscript.classObj(layer)
            category.name = self.get_layer_name()
            style = mapscript.styleObj(category)
            style.color.setHex('#FF00FF')

        return layer
