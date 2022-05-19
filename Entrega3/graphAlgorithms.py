import heapq
import math
import collections
def createPath(parent, j,path):
    if parent[j] == -1:
        path.append(j)
        return
    createPath(parent , parent[j],path)
    path.append(j)
 
def numNodes(parent, j):
	if parent[j] == -1 :
		return 0
	else: return 1+numNodes(parent , parent[j])

def shortest_path(origin, target, graph):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[origin] = 0
    parent={vertex: -1 for vertex in graph}
    pq = [(0, origin)]
    while len(pq) > 0:
        current_distance, current_vertex = heapq.heappop(pq)
        if current_vertex is target: break
        if current_distance > distances[current_vertex]:
            continue
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight[0]
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parent[neighbor] = current_vertex
                heapq.heappush(pq, (distance, neighbor))
    path = []                
    createPath(parent,target,path)
    print()
    return path,distances[target]


def safest_path(origin, target, graph):
    risks = {vertex: float('infinity') for vertex in graph}
    risks[origin] = 0
    parent={vertex: -1 for vertex in graph}
    pq = [(0, origin )]
    while len(pq) > 0:
        current_risk, current_vertex = heapq.heappop(pq)
        if current_vertex is target: break
        if current_risk > risks[current_vertex]:
            continue
        for neighbor, weight in graph[current_vertex].items():
            risk = current_risk + weight[1]
            if risk < risks[neighbor]:
                risks[neighbor] = risk
                parent[neighbor] = current_vertex
                heapq.heappush(pq, (risk, neighbor))
    path = []
    createPath(parent,target,path)
    print()
    return path , risks[target]/numNodes(parent,target)
 
def shortest_and_safest_path(origin, target, graph): #Returns the path, where the distance * harassment risk is the minimum
    weights = {vertex: float('infinity') for vertex in graph}
    weights[origin] = 0
    parent={vertex: -1 for vertex in graph}
    pq = [(0,origin)]
    while len(pq) > 0:
        current_weight, current_vertex = heapq.heappop(pq)
        if current_vertex is target: break
        if current_weight > weights[current_vertex]:
            continue
        for neighbor, weight in graph[current_vertex].items():
            total = current_weight + (weight[0]*weight[1])
            if total < weights[neighbor]:
                weights[neighbor] = total
                parent[neighbor] = current_vertex
                heapq.heappush(pq, (total, neighbor))
    path = []
    createPath(parent,target,path)
    print()
    return path,weights[target]

def no_exceed_risk(origin,target,graph,max_risk):
    distances = {v: float('infinity') for v in graph}
    parent={vertex: -1 for vertex in graph}
    risks = {v: float('infinity') for v in graph}
    distances[origin] = 0
    risks[origin] = 0
    pq = [(0, 0, origin)]
    while len(pq) > 0:
        current_distance, current_risk, current_vertex= heapq.heappop(pq)
        if current_vertex is target:
            break
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight[0]   
            if distance < distances[neighbor]:
                riskk = current_risk + (weight[0]*weight[1])
                average_risk = riskk/distance 
                if average_risk <= max_risk: 
                    parent[neighbor] = current_vertex
                    distances[neighbor]= distance
                    risks[neighbor] = average_risk
                    heapq.heappush(pq, (distance, riskk, neighbor))
    path = []
    createPath(parent,target,path)
    print()                
    return path,distances[target]

def no_exceed_distance(origin,target,graph,max_distance):
    distances = {v: float('infinity') for v in graph}
    parent={vertex: -1 for vertex in graph}
    risks = {v: float('infinity') for v in graph}
    distances[origin] = 0
    risks[origin] = 0
    pq = [(0, 0, origin)]
    while len(pq) > 0:
        current_risk, current_distance, current_vertex= heapq.heappop(pq)
        if current_vertex is target:
            break
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight[0]   
            if distance < distances[neighbor] and distance < max_distance:
                riskk = current_risk + (weight[0]*weight[1])
                average_risk = riskk/distance 
                if average_risk <= risks[neighbor]: 
                    parent[neighbor] = current_vertex
                    distances[neighbor]= distance
                    risks[neighbor] = average_risk
                    heapq.heappush(pq, (riskk, distance, neighbor))
    path = []
    createPath(parent,target,path)
    print()                
    return path,risks[target],distances[target]

def distance(origin, destination):
    """
    Calculate the Haversine distance.
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

def nearestOrigin(origin,data):
    dist = 1000000
    nearest = ()
    for coord in data['origin']:
        long,lat = list(map(float,coord[1:-1].split(',')))
        currDist = distance(origin,(lat,long))
        if currDist < dist:
            dist = currDist
            nearest = (lat,long)
    return nearest  

def nearestDestination(destination,data):
    dist = 1000000
    nearest = ()
    for coord in data['destination']:
        long,lat = list(map(float,coord[1:-1].split(',')))
        currDist = distance(destination,(lat,long))
        if currDist < dist:
            dist = currDist
            nearest = (lat,long)
    return nearest     
