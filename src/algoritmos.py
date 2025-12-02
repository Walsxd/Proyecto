## Debe retornar una lista de nodos en el orden que fueron visitados.
## Los datos de ingreso son el grafo expresado como un diccionario {'A': {'B': 1}, 'B': {'A': 1}}
## y el nodo inicial como un string 'A'
def BFS(graph, start):
    return ["A", "B", "C", "D", "E", "F"]

## Debe retornar una lista de nodos en el orden que fueron visitados.
## Los datos de ingreso son el grafo expresado como un diccionario {'A': {'B': 1}, 'B': {'A': 1}}
## y el nodo inicial como un string 'A'
def DFS(graph, start):
    return ["A", "B", "C", "D", "E", "F"]

## Debe retornar la matriz de adyacencia del grafo y luego en tupla un arreglo con los indices.
## Los datos de ingreso son el grafo expresado como un diccionario {'A': {'B': 1}, 'B': {'A': 1}}
def matriz_adyacencia(graph):
    return [[0, 1, 0], [1, 0, 1], [0, 1, 0]], ['A', 'B', 'C']


## Debe retornar la matriz de incidencia del grafo y luego en tupla un arreglo con los indices.
## Los datos de ingreso son el grafo expresado como un diccionario {'A': {'B': 1}, 'B': {'A': 1}}
def matriz_incidencia(graph):
    return [[0, 1, 0], [1, 0, 1], [0, 1, 0]], ['A', 'B', 'C']

## Dado el grafo y dos nodos, debe retornar el camino mas corto entre ambos nodos.
## Los datos de ingreso son el grafo expresado como un diccionario {'A': {'B': 1}, 'B': {'A': 1}}
## y los nodos inicial y final como strings 'A', 'C'
## Se debe retornar una arreglo con el camino mas corto
## En caso de que no exista camino, retornar un arreglo vacio []
def dijkstra(graph, start, end):
    return ["A", "B", "C"]

## Dado el grafo y dos nodos, debe retornar el camino mas corto entre ambos nodos.
## Los datos de ingreso son el grafo expresado como un diccionario {'A': {'B': 1}, 'B': {'A': 1}}
## y los nodos inicial y final como strings 'A', 'C'
## Se debe retornar una arreglo con el camino mas corto
## En caso de que no exista camino, retornar un arreglo vacio []
def bellman_ford(graph, start, end):
    return ["A", "B", "C"]

## Dado el grafo y dos nodos, debe retornar el camino mas corto entre ambos nodos.
## Los datos de ingreso son el grafo expresado como un diccionario {'A': {'B': 1}, 'B': {'A': 1}}
## y los nodos inicial y final como strings 'A', 'C'
## Se debe retornar una arreglo con el camino mas corto
## En caso de que no exista camino, retornar un arreglo vacio []
def floyd_warshall(graph, start, end):
    return ["A", "B", "C"]


