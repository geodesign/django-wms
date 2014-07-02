import mapscript

from django.conf import settings

class WmsLayer():
    """Base layer object"""

    layer_types = ['line', 'point', 'polygon', 'raster']

    def __init__(self):
        # Instanciate mapscript layer
        layer = mapscript.layerObj()

        layer.status = mapscript.MS_OFF

        layer.type = mapscript.MS_LAYER_RASTER
        layer.name = 'Landcover'
        # layer.opacity = 80
        layer.data = "PG:host='{host}' dbname={dbname} user={user} '\
                'port={port} password={password} table=raster_rastertile '\
                'schema=public mode=2".format(
            host=settings.DATABASES['default']['HOST'],
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            port=settings.DATABASES['default']['PORT'],
            password=settings.DATABASES['default']['PASSWORD']
            ) #where='rid=21902'
        
        layer.setProjection('init=epsg:3086')
        layer.metadata.set('wms_title', 'Landcover')
        layer.metadata.set('wms_srs', 'EPSG:3086')
        
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

        self.layer_object = layer
