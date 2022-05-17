import gmplot
import pandas as pd
apikey = '' #insertar API de google maps
def crearLimitesPoligono():
    lngs = []
    lats = []
    area = pd.read_csv('poligono_de_medellin.csv',sep=';')
    poligon = str(area['geometry'].to_list()[0])[9:-2].split(',')
    for coordenada in poligon:
        long,lat = list(map(float,coordenada[1:].split(' ')))
        lngs.append(long)
        lats.append(lat)
    return lats,lngs 
def coordenadas(path):
    lat = []
    long = []
    for coordenada in path:
        longg,latt = list(map(float,coordenada[1:-1].split(',')))
        long.append(longg)
        lat.append(latt)
    return lat,long

def graficarMapa(path1,path2,path3):
    latLimit, longLimit = crearLimitesPoligono()
    lat,long = coordenadas(path1)
    lat2,long2 = coordenadas(path2)
    lat3,long3 = coordenadas(path3)
    gmapone = gmplot.GoogleMapPlotter(
    6.267203842477565, -75.579710387, 12,
    apikey=apikey,)
    gmapone.polygon(latLimit,longLimit,face_color='white',
                    face_alpha = 0.4, edge_color='black', edge_width=10)
    gmapone.scatter(lat,long,'blue',size = 3,marker = False)
    gmapone.plot(lat,long,'blue',edge_width = 4)
    gmapone.scatter(lat,long,'green',size = 3,marker = False)
    gmapone.plot(lat2,long2,'green',edge_width = 5)
    gmapone.scatter(lat,long,'red',size = 3,marker = False)
    gmapone.plot(lat3,long3,'red',edge_width = 6)
    gmapone.marker(lat[0],long[0],label = 'A')
    gmapone.marker(lat[-1],long[-1],label = 'B')
    gmapone.draw('map.html')
