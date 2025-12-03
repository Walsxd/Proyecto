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
    
    # Mapear nodo -> índice
    mapa = {nodo: i for i, nodo in enumerate(indices)}
    
    for u, vecinos in graph.items():
        for v, peso in vecinos:
            i, j = mapa[u], mapa[v]
            matriz[i][j] = 1
            
    return matriz, indices


## Debe retornar la matriz de incidencia del grafo y luego en tupla un arreglo con los indices.
def matriz_incidencia(graph):
    nodos_set = set(graph.keys())
    aristas = []
    
    # Recolectar todas las aristas y nodos
    for u, vecinos in graph.items():
        for v, peso in vecinos:
            nodos_set.add(v)
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
    costos_minimos = {inicio: 0} 

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


def generar_grafo_aleatorio(num_nodos, num_aristas, dirigido=False, min_peso=1, max_peso=10, con_pesos=True):
    import random
    import string

    if num_nodos < 1:
        return {}

    etiquetas = []
    for i in range(num_nodos):
        if i < 26:
            etiquetas.append(string.ascii_uppercase[i])
        else:
            etiquetas.append(f"N{i}")
            
    # Asegurar conectividad
    aristas = set()
    nodos_conectados = {etiquetas[0]}
    nodos_disponibles = set(etiquetas[1:])
    
    while nodos_disponibles:
        u = random.choice(list(nodos_conectados))
        v = random.choice(list(nodos_disponibles))
        
        aristas.add((u, v))
        nodos_conectados.add(v)
        nodos_disponibles.remove(v)
        
        if not dirigido:
            aristas.add((v, u))
            
    # Agregar aristas restantes
    aristas_actuales = len(aristas) if dirigido else len(aristas) // 2
    intentos = 0
    max_intentos = num_nodos * num_nodos * 2 # Evitar bucle infinito
    
    while aristas_actuales < num_aristas and intentos < max_intentos:
        u = random.choice(etiquetas)
        v = random.choice(etiquetas)
        
        if u == v: # Evitar bucles simples
            intentos += 1
            continue
            
        if (u, v) not in aristas:
            aristas.add((u, v))
            if not dirigido:
                aristas.add((v, u))
            aristas_actuales += 1
        else:
            intentos += 1
            
    # Convertir a formato de lista de adyacencia
    grafo = {nodo: [] for nodo in etiquetas}
    
    # Asignar pesos aleatorios
    aristas_procesadas = set()
    
    for u, v in aristas:
        if not dirigido and (v, u) in aristas_procesadas:
            continue 
        if con_pesos:
            peso = random.randint(min_peso, max_peso)
        else:
            peso = 0
            
        grafo[u].append((v, peso))
        if not dirigido:
            grafo[v].append((u, peso))
            aristas_procesadas.add((u, v))
            
    return grafo


def bfs_componentes(graph, start, visitados):
    """
    Realiza un BFS para encontrar todos los nodos alcanzables desde start.
    Retorna un conjunto de nodos que forman la componente conexa.
    """
    componente = set()
    cola = deque([start])
    visitados.add(start)
    componente.add(start)
    
    while cola:
        nodo = cola.popleft()
        vecinos = graph.get(nodo, [])
        for vecino, _ in vecinos:
            if vecino not in visitados:
                visitados.add(vecino)
                componente.add(vecino)
                cola.append(vecino)
    return componente


def obtener_componentes_conexas(graph):
    """
    Encuentra todas las componentes conexas de un grafo no dirigido.
    Retorna una lista de listas, donde cada sublista contiene los nodos de una componente.
    """
    visitados = set()
    componentes = []
    
    # Obtener todos los nodos
    nodos = list(graph.keys())
    
    for nodo in nodos:
        if nodo not in visitados:
            comp = bfs_componentes(graph, nodo, visitados)
            componentes.append(sorted(list(comp)))
            
    return componentes


def kosaraju(graph):
    """
    Encuentra las Componentes Fuertemente Conexas (SCC) usando el algoritmo de Kosaraju.
    Retorna una lista de listas de nodos.
    """
    # 1. DFS para obtener orden de finalización (stack)
    visitados = set()
    stack = []
    
    def dfs_fill_order(u):
        visitados.add(u)
        for v, _ in graph.get(u, []):
            if v not in visitados:
                dfs_fill_order(v)
        stack.append(u)
        
    for nodo in graph:
        if nodo not in visitados:
            dfs_fill_order(nodo)
            
    # 2. Transponer el grafo (invertir aristas)
    grafo_t = {u: [] for u in graph}
    for u in graph:
        for v, _ in graph[u]:
            grafo_t[v].append((u, 0)) # Peso irrelevante para conectividad
            
    # 3. DFS en el grafo transpuesto siguiendo el orden inverso del stack
    visitados.clear()
    sccs = []
    
    def dfs_scc(u, current_scc):
        visitados.add(u)
        current_scc.append(u)
        for v, _ in grafo_t.get(u, []):
            if v not in visitados:
                dfs_scc(v, current_scc)
                
    while stack:
        nodo = stack.pop()
        if nodo not in visitados:
            componente_actual = []
            dfs_scc(nodo, componente_actual)
            sccs.append(sorted(componente_actual))
            
    return sccs


class UnionFind:
    def __init__(self, elements):
        self.parent = {e: e for e in elements}
        self.rank = {e: 0 for e in elements}

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, item1, item2):
        root1 = self.find(item1)
        root2 = self.find(item2)

        if root1 != root2:
            if self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            elif self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1
            return True
        return False


def es_arbol(graph, es_dirigido=False):
    """
    Determina si un grafo es un árbol.
    Condiciones:
    1. No dirigido (aunque se puede adaptar, la definición clásica es para no dirigidos).
    2. Conexo.
    3. Sin ciclos (implícito si es conexo y |E| = |V| - 1).
    4. |E| = |V| - 1.
    """
    if es_dirigido:
        return False, "Los árboles (en este contexto) son grafos no dirigidos."
    
    nodos = list(graph.keys())
    if not nodos:
        return True, "Grafo vacío es trivialmente un árbol (o bosque vacío)."
        
    # Verificar conectividad
    visitados = set()
    comp = bfs_componentes(graph, nodos[0], visitados)
    if len(comp) != len(nodos):
        return False, "El grafo no es conexo."
        
    # Contar aristas
    num_aristas = 0
    for u in graph:
        num_aristas += len(graph[u])
    
    # En representación de lista de adyacencia para no dirigido, cada arista aparece 2 veces
    num_aristas //= 2
    
    if num_aristas != len(nodos) - 1:
        return False, f"Número de aristas incorrecto. Tiene {num_aristas}, debería tener {len(nodos) - 1}."
        
    return True, "Es un árbol."


def kruskal(graph):
    """
    Algoritmo de Kruskal para MST.
    Retorna (aristas_mst, peso_total).
    aristas_mst es una lista de tuplas (u, v, peso).
    """
    # Recolectar todas las aristas
    aristas = []
    procesados = set()
    
    for u in graph:
        for v, peso in graph[u]:
            # Ordenar para evitar duplicados en no dirigido
            edge = tuple(sorted((u, v)))
            if edge not in procesados:
                aristas.append((u, v, peso))
                procesados.add(edge)
                
    # Ordenar por peso
    aristas.sort(key=lambda x: x[2])
    
    uf = UnionFind(graph.keys())
    mst = []
    peso_total = 0
    
    for u, v, peso in aristas:
        if uf.union(u, v):
            mst.append((u, v, peso))
            peso_total += peso
            
    return mst, peso_total


def prim(graph, start_node):
    """
    Algoritmo de Prim para MST.
    Retorna (aristas_mst, peso_total).
    """
    import heapq
    
    mst = []
    peso_total = 0
    visitados = set([start_node])
    
    # Cola de prioridad: (peso, u, v) -> arista de u a v con peso
    edges = []
    for v, peso in graph.get(start_node, []):
        heapq.heappush(edges, (peso, start_node, v))
        
    while edges:
        peso, u, v = heapq.heappop(edges)
        
        if v not in visitados:
            visitados.add(v)
            mst.append((u, v, peso))
            peso_total += peso
            
            for next_v, next_peso in graph.get(v, []):
                if next_v not in visitados:
                    heapq.heappush(edges, (next_peso, v, next_v))
                    
    return mst, peso_total
