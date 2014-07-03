import mapscript

from django.conf import settings
from django.contrib.gis.db import models

from raster.fields import RasterField

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

    def __init__(self):
        self.dispatch_by_type()

    def get_spatial_type(self):
        """
        Returns the spatial type for the given model based on field types.
        """

        # Setup geo field options
        geo_field_options = [
                ('point', models.PointField),
                ('line', models.LineStringField),
                ('polygon', (models.PolygonField,models.MultiPolygonField)), 
                ('raster', RasterField)
            ]

        # Get geo field candidates
        if self.geo_field_name:
            check_fields = [self.model._meta.get_field_by_name(
                                                self.geo_field_name)]
        else:
            check_fields = self.model._meta.get_fields_with_model()

        # Loop through candidates and try to match
        for field in check_fields:
            field_matches = [geofield[0] for geofield in geo_field_options 
                                if issubclass(field[0].__class__, geofield[1])]
            
            if field_matches:
                return field_matches[0]

        # Raise error if no spatial field is found
        raise TypeError('No spatial field match found in specified model. '\
            'Specify a model that has a spatial field')

    def dispatch_by_type(self):
        """
        Chooses layer setup based on type
        """
        # Get data type for this model
        data_type = self.get_spatial_type()

        # Specify method options
        method_options = {
                'point': self.get_point_layer,
                'line': self.get_point_layer,
                'polygon': self.get_polygon_layer,
                'raster': self.get_raster_layer
                }

        # Call matched method
        return method_options[data_type]()

    def get_layer_name(self):
        """
        Returns layer name, defaults to model name
        """
        if self.name:
            return self.name
        else:
            return self.model._meta.model_name

    def get_base_layer(self):
        """
        Instantiates and returns a base WMS layer with attributes that are
        not specific to data types.
        """
        # Instanciate mapscript layer
        layer = mapscript.layerObj()
        layer.status = mapscript.MS_OFF
        layer.name = self.get_layer_name()
        layer.setProjection('init=epsg:3086')
        layer.metadata.set('wms_title', 'Landcover')
        layer.metadata.set('wms_srs', 'EPSG:3086')
        layer.opacity = 80

        return layer

    def get_point_layer(self):
        """
        Connect this layer to a point geometry model.
        """
        print 'Dispatched to point'

    def get_line_layer(self):
        """
        Connect this layer to a line string model.
        """
        print 'Dispatched to line'

    def get_polygon_layer(self):
        """
        Connect this layer to a polygon model.
        """
        print 'Dispatched to polygon'

    def get_raster_layer(self):
        """
        Connect this layer to a raster model.
        """
        # Get base layer and specify type
        layer = self.get_base_layer()
        layer.type = mapscript.MS_LAYER_RASTER
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

        # Class settings
        if self.cartography:
            for cart in self.cartography:
                category = mapscript.classObj(layer)
                category.setExpression(cart['expression'])
                category.name = cart['name']
                species_style = mapscript.styleObj(category)
                species_style.color.setHex(cart['color'])
        else:
            category = mapscript.classObj(layer)
            category.name = cart['']
            species_style = mapscript.styleObj(category)
            species_style.color.setHex('#FF00FF')

        return layer
