import gmplot

def coordenadas(path):
    lat = []
    long = []
    for coordenada in path:
        longg,latt = list(map(float,coordenada[1:-1].split(',')))
        long.append(longg)
        lat.append(latt)
    return lat,long

def graficarMapa(path):
    lat,long = coordenadas(path)
    gmapone = gmplot.GoogleMapPlotter(6.199328, -75.579521,14)
    gmapone.scatter(lat,long,'red',size = 3,marker = False)
    gmapone.plot(lat,long,'green',edge_width = 5)
    gmapone.draw('map.html')
    
