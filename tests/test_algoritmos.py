import sys
import os

# Agregar el directorio src al path para poder importar algoritmos
sys.path.append(os.path.join(os.getcwd(), 'src'))

from algoritmos import BFS, DFS

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
        print("✅ BFS Correcto")
    else:
        print(f"❌ BFS Incorrecto. Esperado: {esperado_bfs}")
except Exception as e:
    print(f"❌ Error en BFS: {e}")

print("\n--- Test DFS (Estructura Correcta) ---")
try:
    ruta_dfs = DFS(grafo, 'A')
    print(f"Resultado DFS: {ruta_dfs}")
    esperado_dfs = ['A', 'B', 'D', 'E', 'C', 'F'] 
    if ruta_dfs == esperado_dfs:
        print("✅ DFS Correcto")
    else:
        print(f"❌ DFS Incorrecto. Esperado: {esperado_dfs}")
except Exception as e:
    print(f"❌ Error en DFS: {e}")
