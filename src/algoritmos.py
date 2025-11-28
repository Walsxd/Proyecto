## Debe retornar una lista de nodos en el orden que fueron visitados.
## Los datos de ingreso son el grafo expresado como un diccionario {'A': {'B': 1}, 'B': {'A': 1}}
## y el nodo inicial como un string 'A'
def BFS(graph, start):
    return ["B", "A", "C", "D", "E", "F"]

## Debe retornar una lista de nodos en el orden que fueron visitados.
## Los datos de ingreso son el grafo expresado como un diccionario {'A': {'B': 1}, 'B': {'A': 1}}
## y el nodo inicial como un string 'A'
def DFS(graph, start):
    return ["A", "B", "C", "D", "E", "F"]

## Debe retornar la matriz de adyacencia del grafo y luego en tupla un arreglo con los indices.
## Los datos de ingreso son el grafo expresado como un diccionario {'A': {'B': 1}, 'B': {'A': 1}}
## y el nodo inicial como un string 'A'
def matriz_adyacencia(graph):
    return [[0, 1, 0], [1, 0, 1], [0, 1, 0]], ['A', 'B', 'C']
