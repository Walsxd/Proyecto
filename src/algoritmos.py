from collections import deque
import math

## Debe retornar una lista de nodos en el orden que fueron visitados.
def BFS(graph, start):
    visitados = set()
    cola = deque([start])
    orden = []
    
    visitados.add(start)
    
    while cola:
        nodo = cola.popleft()
        orden.append(nodo)
        
        # graph.get(nodo, []) devuelve la lista de tuplas (vecino, peso)
        # Ordenamos los vecinos alfabéticamente para consistencia visual
        vecinos = sorted(graph.get(nodo, []), key=lambda x: x[0])
        
        for vecino, peso in vecinos:
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)
                
    return orden

## Debe retornar una lista de nodos en el orden que fueron visitados.
def DFS(graph, start):
    visitados = set()
    pila = [start]
    orden = []
    
    while pila:
        nodo = pila.pop()
        if nodo not in visitados:
            visitados.add(nodo)
            orden.append(nodo)
            
            # Agregamos vecinos a la pila. 
            # Invertimos el orden para que al hacer pop salga en orden alfabetico
            vecinos = sorted(graph.get(nodo, []), key=lambda x: x[0], reverse=True)
            for vecino, peso in vecinos:
                if vecino not in visitados:
                    pila.append(vecino)
                    
    return orden

## Debe retornar la matriz de adyacencia del grafo y luego en tupla un arreglo con los indices.
def matriz_adyacencia(graph):
    # Obtenemos todos los nodos únicos y los ordenamos
    nodos = set(graph.keys())
    for vecinos in graph.values():
        for v, w in vecinos:
            nodos.add(v)
    indices = sorted(list(nodos))
    n = len(indices)
    
    # Crear matriz n x n llena de ceros
    matriz = [[0] * n for _ in range(n)]
    
    # Mapear nodo -> índice (ej: 'A' -> 0)
    mapa = {nodo: i for i, nodo in enumerate(indices)}
    
    for u, vecinos in graph.items():
        for v, peso in vecinos:
            i, j = mapa[u], mapa[v]
            matriz[i][j] = 1 # O se puede poner 'peso' si prefieres mostrar el peso
            
    return matriz, indices


## Debe retornar la matriz de incidencia del grafo y luego en tupla un arreglo con los indices.
def matriz_incidencia(graph):
    nodos_set = set(graph.keys())
    aristas = []
    
    # Recolectar todas las aristas y nodos
    for u, vecinos in graph.items():
        for v, peso in vecinos:
            nodos_set.add(v)
            # Para evitar duplicados en grafos no dirigidos, guardamos ordenado si es no dirigido
            # Pero como tu estructura duplica aristas en no dirigido (A->B y B->A), 
            # trataremos todo como dirigido para la matriz o filtraremos.
            # Asumiremos formato standard: cada entrada en la lista es una arista.
            aristas.append((u, v))
            
    indices = sorted(list(nodos_set))
    num_nodos = len(indices)
    num_aristas = len(aristas)
    
    matriz = [[0] * num_aristas for _ in range(num_nodos)]
    mapa = {nodo: i for i, nodo in enumerate(indices)}
    
    for col, (u, v) in enumerate(aristas):
        fila_u = mapa[u]
        fila_v = mapa[v]
        
        # En incidencia: Salida = 1, Entrada = -1 (o 1 si es no dirigido, pero usaremos convención dirigida)
        # Si u y v son iguales (bucle), es un caso especial, pero pondremos 1.
        matriz[fila_u][col] = 1
        matriz[fila_v][col] = -1 if u != v else 1
        
    return matriz, indices
  
  
## Dado el grafo y dos nodos, debe retornar el camino mas corto.
def bellman_ford(graph, start, end):
    # Inicialización
    distancias = {nodo: float('inf') for nodo in graph}
    predecesores = {nodo: None for nodo in graph}
    
    # Asegurar que todos los nodos destino posibles estén en el diccionario
    for vecinos in graph.values():
        for v, w in vecinos:
            if v not in distancias:
                distancias[v] = float('inf')
                predecesores[v] = None
                
    distancias[start] = 0
    nodos = list(distancias.keys())
    
    # Relajación de aristas |V| - 1 veces
    for _ in range(len(nodos) - 1):
        hubo_cambio = False
        for u in graph:
            for v, peso in graph[u]:
                if distancias[u] != float('inf') and distancias[u] + peso < distancias[v]:
                    distancias[v] = distancias[u] + peso
                    predecesores[v] = u
                    hubo_cambio = True
        if not hubo_cambio:
            break
            
    # Reconstrucción del camino
    camino = []
    actual = end
    if distancias[end] == float('inf'):
        return [], 0
        
    while actual is not None:
        camino.insert(0, actual)
        actual = predecesores[actual]
        
    if camino[0] != start: # No hay conexión real
        return [], 0
        
    return camino, distancias[end]

## Dado el grafo y dos nodos, debe retornar el camino mas corto.
def floyd_warshall(graph, start, end):
    # Obtener todos los nodos
    nodos = set(graph.keys())
    for vecinos in graph.values():
        for v, w in vecinos:
            nodos.add(v)
    nodos = sorted(list(nodos))
    n = len(nodos)
    mapa = {nodo: i for i, nodo in enumerate(nodos)}
    
    # Matriz de distancias y matriz de siguientes pasos para reconstruir camino
    dist = [[float('inf')] * n for _ in range(n)]
    siguiente = [[None] * n for _ in range(n)]
    
    # Inicializar con 0 la diagonal
    for i in range(n):
        dist[i][i] = 0
        
    # Inicializar con pesos del grafo
    for u, vecinos in graph.items():
        for v, peso in vecinos:
            i, j = mapa[u], mapa[v]
            # Nos quedamos con el menor peso si hay multiaristas
            if peso < dist[i][j]:
                dist[i][j] = peso
                siguiente[i][j] = v # Guardamos el NOMBRE del nodo siguiente
                
    # Algoritmo Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                    nuevo_peso = dist[i][k] + dist[k][j]
                    if nuevo_peso < dist[i][j]:
                        dist[i][j] = nuevo_peso
                        siguiente[i][j] = siguiente[i][k]
                        
    # Reconstruir camino
    if start not in mapa or end not in mapa:
        return [], 0
        
    u_idx, v_idx = mapa[start], mapa[end]
    if dist[u_idx][v_idx] == float('inf'):
        return [], 0
        
    camino = [start]
    curr = start
    while curr != end:
        curr_idx = mapa[curr]
        target_idx = mapa[end]
        nxt = siguiente[curr_idx][target_idx]
        if nxt is None:
            return [], 0
        camino.append(nxt)
        curr = nxt
        
    return camino, dist[u_idx][v_idx]


def dijkstra(grafo, inicio, fin):
    import heapq
    
    queue = [(0, inicio, [inicio])]
    visitados = set()
    costos_minimos = {inicio: 0} # Para optimización

    while queue:
        (costo, nodo_actual, camino) = heapq.heappop(queue)

        if nodo_actual == fin:
            return camino, costo

        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)
            
        vecinos = grafo.get(nodo_actual, [])
            
        for vecino, peso in vecinos:
            nuevo_costo = costo + peso
            # Solo agregamos si encontramos un camino más barato o si no lo hemos visto
            if vecino not in visitados: 
                 if nuevo_costo < costos_minimos.get(vecino, float('inf')):
                    costos_minimos[vecino] = nuevo_costo
                    nuevo_camino = camino + [vecino]
                    heapq.heappush(queue, (nuevo_costo, vecino, nuevo_camino))

    return None, float('inf')

