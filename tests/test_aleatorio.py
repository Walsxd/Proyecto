import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.algoritmos import generar_grafo_aleatorio

class TestGrafoAleatorio(unittest.TestCase):
    def test_generar_grafo_aleatorio_no_dirigido(self):
        num_nodos = 5
        num_aristas = 6
        grafo = generar_grafo_aleatorio(num_nodos, num_aristas, dirigido=False)
        
        # Verificar numero de nodos
        self.assertEqual(len(grafo), num_nodos)
        
        # Verificar conectividad (no hay nodos aislados)
        # En nuestra implementacion, cada nodo debe tener al menos una arista
        for nodo, vecinos in grafo.items():
            self.assertTrue(len(vecinos) > 0, f"El nodo {nodo} esta aislado")
            
        # Verificar numero de aristas (aprox, ya que en no dirigido se duplican)
        total_aristas = sum(len(vecinos) for vecinos in grafo.values())
        # En no dirigido, cada arista aparece 2 veces (u->v y v->u)
        self.assertEqual(total_aristas, num_aristas * 2)

    def test_generar_grafo_aleatorio_dirigido(self):
        num_nodos = 5
        num_aristas = 7
        grafo = generar_grafo_aleatorio(num_nodos, num_aristas, dirigido=True)
        
        self.assertEqual(len(grafo), num_nodos)
        
        # Verificar numero de aristas
        total_aristas = sum(len(vecinos) for vecinos in grafo.values())
        self.assertEqual(total_aristas, num_aristas)

if __name__ == '__main__':
    unittest.main()
