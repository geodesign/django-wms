import mapscript

def get_symbols(size = 10):
    """Returns a list of symbols for mapserver"""
    # Set symbol size, setup empty list
    symbol_size = size
    symbols = []

    # Circle symbol
    symb = mapscript.symbolObj('circle')
    symb.type = mapscript.MS_SYMBOL_ELLIPSE
    symb.filled = mapscript.MS_TRUE
    line = mapscript.lineObj()
    line.add(mapscript.pointObj())
    symb.setPoints(line)
    symb.sizex = symbol_size
    symb.sizey = symbol_size
    symbols.append(symb)

    # Square symbol
    symb = mapscript.symbolObj('square')
    symb.type = mapscript.MS_SYMBOL_VECTOR
    symb.filled = mapscript.MS_TRUE
    line = mapscript.lineObj()
    for pnt in [(0,0), (0, 10), (10, 10), (10, 0), (0, 0)]:
        line.add(mapscript.pointObj(pnt[0], pnt[1]))
    symb.setPoints(line)
    symb.sizex = symbol_size
    symb.sizey = symbol_size
    symbols.append(symb)

    # Triangle symbol
    symb = mapscript.symbolObj('triangle')
    symb.type = mapscript.MS_SYMBOL_VECTOR
    symb.filled = mapscript.MS_TRUE
    line = mapscript.lineObj()
    for pnt in [(0,0), (14, 0), (7, 7), (0, 0)]:
        line.add(mapscript.pointObj(pnt[0], pnt[1]))
    symb.setPoints(line)
    symb.sizex = symbol_size
    symb.sizey = symbol_size
    symbols.append(symb)

    # Cross symbol
    symb = mapscript.symbolObj('cross')
    symb.type = mapscript.MS_SYMBOL_VECTOR
    symb.filled = mapscript.MS_FALSE
    line = mapscript.lineObj()
    for pnt in [(0,0), (10, 10), (-99, -99), (0, 10), (10, 0)]:
        line.add(mapscript.pointObj(pnt[0], pnt[1]))
    symb.setPoints(line)
    symb.sizex = symbol_size
    symb.sizey = symbol_size
    symbols.append(symb)

    # Diagonal symbol
    symb = mapscript.symbolObj('diagonal')
    symb.type = mapscript.MS_SYMBOL_VECTOR
    symb.filled = mapscript.MS_FALSE
    line = mapscript.lineObj()
    for pnt in [(0,0), (10, 10)]:
        line.add(mapscript.pointObj(pnt[0], pnt[1]))
    symb.setPoints(line)
    symb.sizex = symbol_size
    symb.sizey = symbol_size
    symbols.append(symb)

    # Hatch symbol http://lists.osgeo.org/pipermail/mapserver-users/2011-September/069884.html
    symb = mapscript.symbolObj('hatch')
    symb.type = mapscript.MS_SYMBOL_HATCH
    symbols.append(symb)

    return symbols
