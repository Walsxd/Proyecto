import sys
import os

# Agregar el directorio src al path para poder importar algoritmos
sys.path.append(os.path.join(os.getcwd(), 'src'))

from algoritmos import BFS, DFS, bellman_ford, floyd_warshall, dijkstra

# Grafo de prueba con la estructura CORRECTA (Lista de tuplas)
# A -> B, C
# B -> D, E
# C -> F
grafo = {
    'A': [('B', 1), ('C', 1)],
    'B': [('D', 1), ('E', 1)],
    'C': [('F', 1)],
    'D': [],
    'E': [],
    'F': []
}

print("--- Test BFS (Estructura Correcta) ---")
print("Grafo: A -> [B, C], B -> [D, E], C -> [F]")
try:
    ruta_bfs = BFS(grafo, 'A')
    print(f"Resultado BFS: {ruta_bfs}")
    esperado_bfs = ['A', 'B', 'C', 'D', 'E', 'F']
    if ruta_bfs == esperado_bfs:
        print("BFS Correcto")
    else:
        print(f"BFS Incorrecto. Esperado: {esperado_bfs}")
except Exception as e:
    print(f"Error en BFS: {e}")

print("\n--- Test DFS (Estructura Correcta) ---")
try:
    ruta_dfs = DFS(grafo, 'A')
    print(f"Resultado DFS: {ruta_dfs}")
    esperado_dfs = ['A', 'B', 'D', 'E', 'C', 'F'] 
    if ruta_dfs == esperado_dfs:
        print("DFS Correcto")
    else:
        print(f"DFS Incorrecto. Esperado: {esperado_dfs}")
except Exception as e:
    print(f"Error en DFS: {e}")


print("\n--- Test Dijkstra (Tu algoritmo) ---")
try:
    
    camino, costo = dijkstra(grafo, 'A', 'F')
    print(f"Resultado Dijkstra: {camino}, Costo: {costo}")
    
    esperado_camino = ['A', 'C', 'F']
    esperado_costo = 2
    
    if camino == esperado_camino and costo == esperado_costo:
        print("Dijkstra Correcto")
    else:
        print(f"Dijkstra Incorrecto. Esperado: {esperado_camino} con costo {esperado_costo}")
except Exception as e:
    print(f"Error en Dijkstra: {e}")

print("\n--- Test Bellman-Ford (Tu algoritmo) ---")
try:
    camino, costo = bellman_ford(grafo, 'A', 'F')
    print(f"Resultado Bellman-Ford: {camino}, Costo: {costo}")
    
    if camino == ['A', 'C', 'F'] and costo == 2:
        print("Bellman-Ford Correcto")
    else:
        print("Bellman-Ford Incorrecto")
except Exception as e:
    print(f"Error en Bellman-Ford: {e}")

print("\n--- Test Floyd-Warshall (Tu algoritmo) ---")
try:
    
    nodos = sorted(list(grafo.keys())) # ['A', 'B', 'C', 'D', 'E', 'F']
    idx_a = nodos.index('A')
    idx_f = nodos.index('F')
    
    matriz, lista_nodos = floyd_warshall(grafo)
    distancia_calculada = matriz[idx_a][idx_f]
    
    print(f"Distancia Floyd A->F: {distancia_calculada}")
    
    if distancia_calculada == 2:
        print("Floyd-Warshall Correcto")
    else:
        print(f"Floyd-Warshall Incorrecto. Esperado: 2, Recibido: {distancia_calculada}")
except Exception as e:
    print(f"Error en Floyd-Warshall: {e}")