import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'src'))

from modelo import Grafo
from algoritmos import matriz_adyacencia

def test_matriz_adyacencia():
    g = Grafo(dirigido=True)
    g.agregar_arista('A', 'B', 1)
    g.agregar_arista('B', 'C', 2)
    
    matriz, indices = matriz_adyacencia(g.obtener_lista_adyacencia())
    
    print(f"Indices: {indices}")
    print("Matriz:")
    for fila in matriz:
        print(fila)
        
    expected_indices = ['A', 'B', 'C']
    # A -> B (1), B -> C (1)
    #    A  B  C
    # A  0  1  0
    # B  0  0  1
    # C  0  0  0
    expected_matriz = [
        [0, 1, 0],
        [0, 0, 1],
        [0, 0, 0]
    ]
    
    assert indices == expected_indices, f"Indices incorrectos. Esperado: {expected_indices}, Obtenido: {indices}"
    assert matriz == expected_matriz, f"Matriz incorrecta. Esperado: {expected_matriz}, Obtenido: {matriz}"
    print("Test Matriz Adyacencia: PASSED")

if __name__ == "__main__":
    try:
        test_matriz_adyacencia()
    except AssertionError as e:
        print(f"Test FAILED: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
