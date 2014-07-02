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
    geo_field_name = ''
    name = ''

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

    def get_base_layer(self):
        """
        Instantiates and returns a base WMS layer with attributes that are
        not specific to data types.
        """
        # Instanciate mapscript layer
        layer = mapscript.layerObj()
        layer.status = mapscript.MS_OFF
        layer.name = 'Landcover'
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

        # Set data source
        layer.data = 'PG:host={host} dbname={dbname} user={user} '\
                'port={port} password={password} mode=2 '.format(
            host=settings.DATABASES['default']['HOST'],
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            port=settings.DATABASES['default']['PORT'],
            password=settings.DATABASES['default']['PASSWORD']
            ) #where='rid=21902'

        layer.data += 'table=raster_rastertile'

        layer.addProcessing("NODATA=0")
        layer.classitem="[pixel]"

        # Class settings
        class1 = mapscript.classObj(layer)
        class1.setExpression("1")
        class1.name = 'One'
        species_style = mapscript.styleObj(class1)
        species_style.color.setHex('#000000')

        class2 = mapscript.classObj(layer)
        class2.setExpression("([pixel]>1)")
        class2.name = 'More than one'
        species_style = mapscript.styleObj(class2)
        species_style.color.setHex('#555444')

        return layer
