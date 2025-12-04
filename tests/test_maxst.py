import unittest
from src.algoritmos import kruskal_maximo

class TestMaxST(unittest.TestCase):

    def test_kruskal_maximo_simple(self):
        # Grafo simple:
        # A - (10) - B
        # |          |
        # (1)        (5)
        # |          |
        # C - (2) -- D
        #
        # Aristas: (A,B,10), (B,D,5), (C,D,2), (A,C,1)
        # MaxST debería tomar: (A,B,10), (B,D,5), (C,D,2) -> Total 17
        # (A,C,1) formaría ciclo A-B-D-C-A
        
        grafo = {
            'A': [('B', 10), ('C', 1)],
            'B': [('A', 10), ('D', 5)],
            'C': [('A', 1), ('D', 2)],
            'D': [('B', 5), ('C', 2)]
        }
        
        mst, peso = kruskal_maximo(grafo)
        self.assertEqual(peso, 17)
        self.assertEqual(len(mst), 3)
        
        # Verificar aristas específicas
        aristas_esperadas = {tuple(sorted(('A', 'B'))), tuple(sorted(('B', 'D'))), tuple(sorted(('C', 'D')))}
        aristas_obtenidas = {tuple(sorted((u, v))) for u, v, p in mst}
        self.assertEqual(aristas_obtenidas, aristas_esperadas)

    def test_kruskal_maximo_desconectado(self):
        # Dos componentes
        # A-B (10)
        # C-D (5)
        grafo = {
            'A': [('B', 10)],
            'B': [('A', 10)],
            'C': [('D', 5)],
            'D': [('C', 5)]
        }
        mst, peso = kruskal_maximo(grafo)
        self.assertEqual(peso, 15)
        self.assertEqual(len(mst), 2)

    def test_kruskal_maximo_ciclo_pesado(self):
        # Triángulo con pesos altos
        # A-B (100), B-C (100), C-A (1)
        # MaxST debe descartar C-A
        grafo = {
            'A': [('B', 100), ('C', 1)],
            'B': [('A', 100), ('C', 100)],
            'C': [('B', 100), ('A', 1)]
        }
        mst, peso = kruskal_maximo(grafo)
        self.assertEqual(peso, 200)
        self.assertEqual(len(mst), 2)
        
        aristas_obtenidas = {tuple(sorted((u, v))) for u, v, p in mst}
        self.assertNotIn(tuple(sorted(('A', 'C'))), aristas_obtenidas)

if __name__ == '__main__':
    unittest.main()
