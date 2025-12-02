import heapq
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
def bellman_ford(graph, start, end):
    return ["A", "B", "C"]

## Dado el grafo y dos nodos, debe retornar el camino mas corto entre ambos nodos.
## Los datos de ingreso son el grafo expresado como un diccionario {'A': {'B': 1}, 'B': {'A': 1}}
## y los nodos inicial y final como strings 'A', 'C'
## Se debe retornar una arreglo con el camino mas corto
## En caso de que no exista camino, retornar un arreglo vacio []
def floyd_warshall(graph, start, end):
    return ["A", "B", "C"]


# --- Pega esto en src/algoritmos.py ---
def dijkstra(grafo, inicio, fin):
    import heapq
    
    # Cola de prioridad: (costo_acumulado, nodo_actual, camino_recorrido)
    queue = [(0, inicio, [inicio])]
    visitados = set()

    while queue:
        # Sacamos el nodo con el menor costo acumulado
        (costo, nodo_actual, camino) = heapq.heappop(queue)

        # Si llegamos al destino, retornamos el camino y el costo
        if nodo_actual == fin:
            return camino, costo

        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            
            # Obtenemos los vecinos (sin .items() porque es una lista de tuplas)
            vecinos = grafo.get(nodo_actual, [])
            
            for vecino, peso in vecinos:
                if vecino not in visitados:
                    nuevo_costo = costo + peso
                    nuevo_camino = camino + [vecino]
                    heapq.heappush(queue, (nuevo_costo, vecino, nuevo_camino))

    # Si se vacía la cola y no llegamos al destino
    return None, float('inf')
