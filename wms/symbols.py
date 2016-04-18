import mapscript


class WmsSymbolSet():
    """
    Symbol set for rendering data using different cartograpy styles.
    This includes styles for Points, Lines and Polygons (fills and outlines).
    """
    symbol_size = 10
    preset_symbols = []
    custom_symbols = []

    def __init__(self):
        """Initiates the preset symbols for the symbolset"""
        self._create_preset_point_symbols()
        self._create_preset_polygon_symbols()

    def get_symbols(self):
        """Returns an array of mapscript symbols"""
        return self.preset_symbols + self.custom_symbols

    def _create_preset_point_symbols(self):
        """Initiates preset point symbols"""

        # Circle symbol
        symb = mapscript.symbolObj('circle')
        symb.type = mapscript.MS_SYMBOL_ELLIPSE
        symb.filled = mapscript.MS_TRUE
        line = mapscript.lineObj()
        line.add(mapscript.pointObj())
        symb.setPoints(line)
        symb.sizex = self.symbol_size
        symb.sizey = self.symbol_size
        self.preset_symbols.append(symb)

        # Square symbol
        symb = mapscript.symbolObj('square')
        symb.type = mapscript.MS_SYMBOL_VECTOR
        symb.filled = mapscript.MS_TRUE
        line = mapscript.lineObj()
        for pnt in [(0,0), (0, 10), (10, 10), (10, 0), (0, 0)]:
            line.add(mapscript.pointObj(pnt[0], pnt[1]))
        symb.setPoints(line)
        symb.sizex = self.symbol_size
        symb.sizey = self.symbol_size
        self.preset_symbols.append(symb)

        # Triangle symbol
        symb = mapscript.symbolObj('triangle')
        symb.type = mapscript.MS_SYMBOL_VECTOR
        symb.filled = mapscript.MS_TRUE
        line = mapscript.lineObj()
        for pnt in [(0,0), (14, 0), (7, 7), (0, 0)]:
            line.add(mapscript.pointObj(pnt[0], pnt[1]))
        symb.setPoints(line)
        symb.sizex = self.symbol_size
        symb.sizey = self.symbol_size
        self.preset_symbols.append(symb)

        # Cross symbol
        symb = mapscript.symbolObj('cross')
        symb.type = mapscript.MS_SYMBOL_VECTOR
        symb.filled = mapscript.MS_FALSE
        line = mapscript.lineObj()
        for pnt in [(0,0), (10, 10), (-99, -99), (0, 10), (10, 0)]:
            line.add(mapscript.pointObj(pnt[0], pnt[1]))
        symb.setPoints(line)
        symb.sizex = self.symbol_size
        symb.sizey = self.symbol_size
        self.preset_symbols.append(symb)

        # Diagonal symbol
        symb = mapscript.symbolObj('diagonal')
        symb.type = mapscript.MS_SYMBOL_VECTOR
        symb.filled = mapscript.MS_FALSE
        line = mapscript.lineObj()
        for pnt in [(0,0), (10, 10)]:
            line.add(mapscript.pointObj(pnt[0], pnt[1]))
        symb.setPoints(line)
        symb.sizex = self.symbol_size
        symb.sizey = self.symbol_size
        self.preset_symbols.append(symb)

    def _create_preset_polygon_symbols(self):
        """Create Preset polygon symbols"""
        # Hatch symbol from http://lists.osgeo.org/pipermail/\
        # mapserver-users/2011-September/069884.html
        symb = mapscript.symbolObj('hatch')
        symb.type = mapscript.MS_SYMBOL_HATCH
        self.preset_symbols.append(symb)
