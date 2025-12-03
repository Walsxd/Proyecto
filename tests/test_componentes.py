import unittest
from src.algoritmos import obtener_componentes_conexas, kosaraju

class TestComponentes(unittest.TestCase):

    def test_componentes_conexas_undirected(self):
        # Grafo no dirigido: A-B, C (aislado)
        # Representación interna: A->B, B->A, C->[]
        grafo = {
            'A': [('B', 1)],
            'B': [('A', 1)],
            'C': []
        }
        componentes = obtener_componentes_conexas(grafo)
        # Esperamos [['A', 'B'], ['C']] (ordenado)
        self.assertEqual(len(componentes), 2)
        self.assertIn(['A', 'B'], componentes)
        self.assertIn(['C'], componentes)

    def test_kosaraju_scc(self):
        # Grafo dirigido: A->B->A (ciclo), C->A
        # SCCs: {A, B}, {C}
        grafo = {
            'A': [('B', 1)],
            'B': [('A', 1)],
            'C': [('A', 1)]
        }
        sccs = kosaraju(grafo)
        self.assertEqual(len(sccs), 2)
        self.assertIn(['A', 'B'], sccs)
        self.assertIn(['C'], sccs)

    def test_kosaraju_complex(self):
        # Grafo: 0->1->2->0 (ciclo), 1->3->4
        # SCCs: {0, 1, 2}, {3}, {4}
        grafo = {
            '0': [('1', 1)],
            '1': [('2', 1), ('3', 1)],
            '2': [('0', 1)],
            '3': [('4', 1)],
            '4': []
        }
        sccs = kosaraju(grafo)
        self.assertEqual(len(sccs), 3)
        self.assertIn(['0', '1', '2'], sccs)
        self.assertIn(['3'], sccs)
        self.assertIn(['4'], sccs)

if __name__ == '__main__':
    unittest.main()
