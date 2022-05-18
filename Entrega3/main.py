import pandas as pd
import JsonApi
import mapRoute
import graphAlgorithms
import webbrowser
data = pd.read_csv('calles_de_medellin_con_acoso.csv', sep = ';',)
data.harassmentRisk = data.harassmentRisk.fillna(data.harassmentRisk.mean())
graph= {}
unique_origins = data.origin.unique()

# The graph is represented as a dict of dicts
# Keys are the origins and at first their values are empty dicts.
for i in range(len(unique_origins)):
    graph[unique_origins[i]] = {}

# The values are filled.
# The keys are the destinations and the values are the distance, and
# harassment risk for each destination.
for i in data.index:
    if data["oneway"][i]==False:
        graph[data["origin"][i]][data["destination"][i]]=(data["length"][i],data["harassmentRisk"][i])
    else:
        graph[data["origin"][i]][data["destination"][i]]=(data["length"][i],data["harassmentRisk"][i])
        try:
            graph[data["destination"][i]][data["origin"][i]]=(data["length"][i],data["harassmentRisk"][i])
        except KeyError:#  This error happens when 'oneway' is True and the destination must be as a key in the dict as a origin.
                        # In some cases, this coordinates where not presented as a origin in the dataframe.
            graph[data['destination'][i]]={data["origin"][i]:(data["length"][i],data["harassmentRisk"][i])}


def main():
    print('Por favor, sea muy específico al ingresar los lugares...')
    print("Recuerde que la ruta roja es la más rápida, la azul la más balanceada entre acoso y distancia, y la verde es la más segura.")
    origin = graphAlgorithms.nearestOrigin(JsonApi.strToCoordinates(input("Ingrese lugar de origen: ")),data)
    origin = str((origin[1],origin[0]))
    destination = graphAlgorithms.nearestDestination(JsonApi.strToCoordinates(input("Ingrese lugar de destino: ")),data)
    destination = str((destination[1],destination[0]))
    path1, totalDistance = graphAlgorithms.safest_path(origin,destination,graph)
    path2, totalDistance2 = graphAlgorithms.shortest_and_safest_path(origin,destination,graph)
    path3, totalDistance3 = graphAlgorithms.shortest_path(origin,destination,graph)
    
    mapRoute.createMap(path1,path2,path3)
    webbrowser.open_new_tab('map.html')

main()


