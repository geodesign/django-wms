import mapscript

from django.http import HttpResponse

# from .models import SpeciesStyle, ActivityStyle
# from .maps.map import get_base_map
# from .maps.layers import get_species_layer, get_activity_layer

###############################################################################
def wms(request):
    """WMS view for isias layers"""
    
    return HttpResponse('Welcome to django-wms')

    # # Setup wms request object
    # wms_request = mapscript.OWSRequest()

    # # Convert application request parameters (req.args)
    # for param, value in request.GET.items():
    #     wms_request.setParameter(param, value)

    # # Get base map object
    # wms_map = get_base_map()
    
    # # Get timestep id values
    # ts_ids = request.GET.get('SCENARIOTIMESTEP', '-1')
    # if not ts_ids:
    #     ts_ids = '-1'
    
    # ##############
    # # Set species id list
    # if species_id:
    #     species_ids = [species_id]
    # else:
    #     species_ids = request.GET.get('SPECIES', '-1')
    #     if not species_ids:
    #         species_ids = '-1'
    #     species_ids = species_ids.split(',')

    # # Get layer for species
    # spe_lyr = get_species_layer(ts_ids)

    # # Setup class styles for each species id
    # for spe_id in species_ids:

    #     # Try to get layer style for this species
    #     if SpeciesStyle.objects.filter(species_id=spe_id).exists():
    #         style = SpeciesStyle.objects.get(species_id=spe_id)
    #     else:
    #         # Use default if style is not set for this species
    #         style = SpeciesStyle(species_id=spe_id)
        
    #     # Class settings
    #     species_class = mapscript.classObj(spe_lyr)
    #     species_class.setExpression(spe_id)
    #     species_class.name = ''

    #     # Style settings
    #     species_style = mapscript.styleObj(species_class)
    #     species_style.color.setHex(style.background_hex)
    #     species_style.outlinecolor.setHex(style.outline_hex)
    #     species_style.width = style.outline_width

    #     # Add hatch symbol if hatch angle is specified in style
    #     if style.hatch_angle:
    #         species_style.setSymbolByName(wms_map, 'hatch')
    #         species_style.size = 2*style.outline_width
    #         species_style.angle = style.hatch_angle

    # ##############
    # # Set activity id list
    # if activity_id:
    #     activity_ids = [activity_id]
    # else:
    #     activity_ids = request.GET.get('ACTIVITY', '-1')
    #     if not activity_ids:
    #         activity_ids = '-1'
    #     activity_ids = activity_ids.split(',')

    # # Get layer with activity data
    # act_lyr = get_activity_layer(ts_ids)

    # # Setup class styles for each activity id
    # for act_id in activity_ids:

    #     # Try to get layer style for this activity
    #     if ActivityStyle.objects.filter(activity_id=act_id).exists():
    #         style = ActivityStyle.objects.get(activity_id=act_id)
    #     else:
    #         # Use default if style is not set for this species
    #         style = ActivityStyle(activity_id=act_id)

    #     # Set class and style for this activity
    #     activity_class = mapscript.classObj(act_lyr)
    #     activity_class.setExpression(act_id)
    #     activity_class.name = ''

    #     # Style settings
    #     activity_style = mapscript.styleObj(activity_class)
    #     activity_style.color.setHex(style.color_hex)
    #     activity_style.outlinecolor.setHex(style.color_hex)
    #     activity_style.width = 2

    #     # Set symbol
    #     activity_style.setSymbolByName(wms_map, style.symbol)
    
    # # Bind layers to map object
    # wms_map.insertLayer(act_lyr)
    # wms_map.insertLayer(spe_lyr)
    
    if wms_request.getValueByName('REQUEST').lower() == 'getmap':
        # Map loads parameters from OWSRequest
        wms_map.loadOWSParameters(wms_request)
        # Render the Map
        image = wms_map.draw().getBytes()
    elif wms_request.getValueByName('REQUEST').lower() == 'getlegendgraphic':
        
        # Toggle layer on off, to only show one symbol type in legend image
        if 'activity' in wms_request.getValueByName('LAYERS'):
            spe_lyr.status = mapscript.MS_OFF
        else:
            act_lyr.status = mapscript.MS_OFF

        # Render the Legend
        image = wms_map.drawLegend().getBytes()

    # Create response
    response = HttpResponse()
    response['Content-length'] = len(image)
    response['Content-Type'] = wms_request.getValueByName('FORMAT')
    response.write(image)
    return response