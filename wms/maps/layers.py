import mapscript

from django.conf import settings

###############################################################################
# Create base layer
baselayer = mapscript.layerObj()
baselayer.setProjection('init=epsg:4326')
baselayer.status = mapscript.MS_ON
baselayer.setConnectionType(mapscript.MS_POSTGIS, '')
baselayer.connection = 'host={host} dbname={dbname} user={user} port={port} password={password}'.format(
    host=settings.DATABASES['default']['HOST'],
    dbname=settings.DATABASES['default']['NAME'],
    user=settings.DATABASES['default']['USER'],
    port=settings.DATABASES['default']['PORT'],
    password=settings.DATABASES['default']['PASSWORD']
    )

###############################################################################
def get_species_layer(timestep_ids):

    # Setup species layer
    species_layer = baselayer.clone()
    species_layer.type = mapscript.MS_LAYER_POLYGON
    species_layer.name = 'species'
    species_layer.classitem = 'species_id'
    species_layer.opacity = 80

    species_layer.data = '''geom FROM (
        SELECT DISTINCT
            patch.id AS habitatpatch_id,
            patch.species_id AS species_id,
            patch.geom AS geom
        FROM species_habitatpatch patch
        INNER JOIN scenarios_scenariotimestep_habitatpatchcollections scts
            ON patch.collection_id=scts.habitatpatchcollection_id
        WHERE scts.scenariotimestep_id IN ({timestep_ids})
        ) AS newtable USING UNIQUE habitatpatch_id USING SRID=4326'''.format(timestep_ids=timestep_ids)

    return species_layer

###############################################################################
def get_activity_layer(timestep_ids):

    # Setup activity layer
    activity_layer = baselayer.clone()
    activity_layer.type = mapscript.MS_LAYER_POINT
    activity_layer.name = 'activity'
    activity_layer.classitem = 'activity_id'
    activity_layer.opacity = 80

    activity_layer.data = '''geom FROM (
        SELECT DISTINCT
            spot.id AS activityspot_id,
            spot.activity_id AS activity_id,
            spot.geom AS geom
        FROM activities_activityspot spot
        JOIN scenarios_scenariotimestep_activityspotcollections scts
            ON spot.collection_id=scts.activityspotcollection_id
        WHERE scts.scenariotimestep_id IN ({timestep_ids})
        ) AS newtable USING UNIQUE activityspot_id USING SRID=4326'''.format(timestep_ids=timestep_ids)

    return activity_layer
