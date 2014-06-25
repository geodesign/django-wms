import mapscript

from .symbolset import get_symbols

###############################################################################
def get_base_map():
    # Instanciate base map object
    basemap = mapscript.mapObj()
    basemap.setProjection('init=epsg:4326')
    basemap.setExtent(-180, -90, 180, 90)
    basemap.setSize(500, 600)
    basemap.setMetaData("wms_title", "Florida Beaches HCP Server")
    basemap.setMetaData("wms_onlineresource", "http://isias.elasticbeanstalk.com/wms/?")
    basemap.setMetaData("wms_srs", "epsg:3086 epsg:4326 epsg:3857")
    basemap.setMetaData("wms_enable_request", "*")
    basemap.setMetaData("wms_feature_info_mime_type", "text/html")
    basemap.outputformat.transparent = mapscript.MS_ON

    # Add symbols
    for symb in get_symbols():
        basemap.symbolset.appendSymbol(symb)

    # Set legend
    basemap.legend.keysizex = 30
    basemap.legend.keysizey = 18
    basemap.legend.keyspacingx = 0

    return basemap
    