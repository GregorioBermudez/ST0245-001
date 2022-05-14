import pandas as pd
import JsonApi
import mapRoute
import graphAlgorithms

data = pd.read_csv('calles_de_medellin_con_acoso.csv', sep = ';',)
data.harassmentRisk = data.harassmentRisk.fillna(data.harassmentRisk.mean())
grafo= {}
origenes_unicos = data.origin.unique()
# En este ciclo, se crea grafo como diccionario de diccionarios. 
# Inicialmente, las llaves son los origenes
# que estan en el dataframe 'data'
# Y los valores son diccionarios vacios.
for i in range(len(origenes_unicos)):
    grafo[origenes_unicos[i]] = {}
 
# Se completa el grafo. En el diccionario de cada valor,
# las llaves son los destinos, y los valores son
# la distancia y el porcentaje de acoso para ese destino
# Se tiene en cuenta el valor de 'oneway' en el dataframe, 
# ya que si es Verdadero, la relacion origen-destino es simetrica, y se debe
# añadir en ambos sentidos al diccionario.
for i in data.index:
    if data["oneway"][i]==False:
        grafo[data["origin"][i]][data["destination"][i]]=(data["length"][i],data["harassmentRisk"][i])
    else:
        grafo[data["origin"][i]][data["destination"][i]]=(data["length"][i],data["harassmentRisk"][i])
        try:
            grafo[data["destination"][i]][data["origin"][i]]=(data["length"][i],data["harassmentRisk"][i])
        except KeyError: # Este error se da cuando, el valor de 'oneway' es verdadero, y el destino debe ser un origen en el diccionario.
                         # En ciertos casos, ese destino no se encontraba como origen en el dataframe, por lo que no se encontraba en 
                         # 'grafos' y tratar de acceder a este genera 'KeyError'. La solucion es simplemente
                         # añadirlo como una nueva llave y crear el otro diccionario en el valor.
            grafo[data['destination'][i]]={data["origin"][i]:(data["length"][i],data["harassmentRisk"][i])}


def main():
    print('Por favor, sea muy específico al ingresar los lugares...')
    origen = JsonApi.generar_coordenadas(input("Ingrese lugar de origen: "))
    origenGrafo = graphAlgorithms.encontrarOrigenCercano(origen,data)
    origenGrafo = str((origenGrafo[1],origenGrafo[0]))
    destino =JsonApi.generar_coordenadas(input("Ingrese lugar de destino: "))
    destinoGrafo = graphAlgorithms.encontrarDestinoCercano(destino,data)
    destinoGrafo = str((destinoGrafo[1],destinoGrafo[0]))
    path, totalDistance = graphAlgorithms.shortest_path(origenGrafo,destinoGrafo,grafo)
    mapRoute.graficarMapa(path)

main()



