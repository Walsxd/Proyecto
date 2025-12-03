import unittest
from src.algoritmos import es_arbol, kruskal, prim

class TestArboles(unittest.TestCase):

    def test_es_arbol_valido(self):
        # A-B-C
        grafo = {
            'A': [('B', 1)],
            'B': [('A', 1), ('C', 1)],
            'C': [('B', 1)]
        }
        es_valido, _ = es_arbol(grafo)
        self.assertTrue(es_valido)

    def test_es_arbol_ciclo(self):
        # A-B-C-A (ciclo)
        grafo = {
            'A': [('B', 1), ('C', 1)],
            'B': [('A', 1), ('C', 1)],
            'C': [('B', 1), ('A', 1)]
        }
        es_valido, _ = es_arbol(grafo)
        self.assertFalse(es_valido)

    def test_es_arbol_desconectado(self):
        # A-B, C
        grafo = {
            'A': [('B', 1)],
            'B': [('A', 1)],
            'C': []
        }
        es_valido, _ = es_arbol(grafo)
        self.assertFalse(es_valido)

    def test_kruskal(self):
        # A-B(1), B-C(2), A-C(10)
        # MST: A-B, B-C (peso 3)
        grafo = {
            'A': [('B', 1), ('C', 10)],
            'B': [('A', 1), ('C', 2)],
            'C': [('A', 10), ('B', 2)]
        }
        mst, peso = kruskal(grafo)
        self.assertEqual(peso, 3)
        self.assertEqual(len(mst), 2)
        # Verificar aristas (ordenadas)
        aristas = sorted([(u, v) for u, v, w in mst])
        self.assertIn(('A', 'B'), aristas)
        self.assertIn(('B', 'C'), aristas)

    def test_prim(self):
        # Mismo grafo
        grafo = {
            'A': [('B', 1), ('C', 10)],
            'B': [('A', 1), ('C', 2)],
            'C': [('A', 10), ('B', 2)]
        }
        mst, peso = prim(grafo, 'A')
        self.assertEqual(peso, 3)
        self.assertEqual(len(mst), 2)

if __name__ == '__main__':
    unittest.main()
