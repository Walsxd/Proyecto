import unittest
from src.algoritmos import es_bipartito

class TestBipartito(unittest.TestCase):

    def test_grafo_bipartito_simple(self):
        # Cuadrado: 1-2-3-4-1
        grafo = {
            '1': [('2', 1), ('4', 1)],
            '2': [('1', 1), ('3', 1)],
            '3': [('2', 1), ('4', 1)],
            '4': [('3', 1), ('1', 1)]
        }
        es_bip, set_a, set_b = es_bipartito(grafo)
        self.assertTrue(es_bip)
        # Verificar que los sets son disjuntos y cubren todos los nodos
        self.assertTrue(set_a.isdisjoint(set_b))
        self.assertEqual(set_a | set_b, {'1', '2', '3', '4'})
        # Verificar que nodos adyacentes tienen colores distintos
        # 1 y 3 en un set, 2 y 4 en el otro
        if '1' in set_a:
            self.assertIn('3', set_a)
            self.assertIn('2', set_b)
            self.assertIn('4', set_b)
        else:
            self.assertIn('3', set_b)
            self.assertIn('2', set_a)
            self.assertIn('4', set_a)

    def test_grafo_no_bipartito_triangulo(self):
        # Triángulo: 1-2-3-1
        grafo = {
            '1': [('2', 1), ('3', 1)],
            '2': [('1', 1), ('3', 1)],
            '3': [('1', 1), ('2', 1)]
        }
        es_bip, _, _ = es_bipartito(grafo)
        self.assertFalse(es_bip)

    def test_grafo_desconectado_bipartito(self):
        # Dos componentes bipartitas
        # 1-2
        # 3-4
        grafo = {
            '1': [('2', 1)],
            '2': [('1', 1)],
            '3': [('4', 1)],
            '4': [('3', 1)]
        }
        es_bip, set_a, set_b = es_bipartito(grafo)
        self.assertTrue(es_bip)
        self.assertEqual(set_a | set_b, {'1', '2', '3', '4'})

    def test_grafo_vacio(self):
        grafo = {}
        es_bip, set_a, set_b = es_bipartito(grafo)
        self.assertTrue(es_bip)
        self.assertEqual(len(set_a), 0)
        self.assertEqual(len(set_b), 0)

if __name__ == '__main__':
    unittest.main()
