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
## y el nodo inicial como un string 'A'
def matriz_adyacencia(graph):
    return [[0, 1, 0], [1, 0, 1], [0, 1, 0]], ['A', 'B', 'C']

def dijkstra(grafo, inicio, fin):
    """
    Calcula la distancia más corta desde un nodo inicio hasta un nodo fin.
    Retorna la ruta y la distancia total.
    """
    # 1. Cola de prioridad: Guarda (distancia_acumulada, nodo_actual, camino_recorrido)
    queue = [(0, inicio, [inicio])]
    
    # 2. Visited: Para no procesar nodos repetidos innecesariamente
    visitados = set()

    while queue:
        # Sacamos el nodo con la MENOR distancia acumulada (gracias a heapq)
        (costo, nodo_actual, camino) = heapq.heappop(queue)

        # Si llegamos al destino, retornamos el resultado
        if nodo_actual == fin:
            return camino, costo

        if nodo_actual not in visitados:
            visitados.add(nodo_actual)

            # Revisamos los vecinos
            # .get() es para evitar errores si el nodo no tiene vecinos
            vecinos = grafo.get(nodo_actual, {})
            
            for vecino, peso in vecinos.items():
                if vecino not in visitados:
                    # Calculamos el nuevo costo total y actualizamos el camino
                    nuevo_costo = costo + peso
                    nuevo_camino = camino + [vecino]
                    heapq.heappush(queue, (nuevo_costo, vecino, nuevo_camino))

    return None, float('inf') # Si no hay camino