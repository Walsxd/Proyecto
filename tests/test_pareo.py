import unittest
from src.algoritmos import matching_maximal, hopcroft_karp

class TestPareo(unittest.TestCase):

    def test_matching_maximal_simple(self):
        # A - B - C - D
        grafo = {
            'A': [('B', 1)],
            'B': [('A', 1), ('C', 1)],
            'C': [('B', 1), ('D', 1)],
            'D': [('C', 1)]
        }
        matching = matching_maximal(grafo)
        
        # Verificar que es un matching válido
        nodos_cubiertos = set()
        for u, v in matching:
            self.assertNotIn(u, nodos_cubiertos)
            self.assertNotIn(v, nodos_cubiertos)
            nodos_cubiertos.add(u)
            nodos_cubiertos.add(v)
            
        # Verificar que es maximal (no se pueden agregar más aristas)
        # En este caso A-B, C-D es maximal (size 2)
        # A-B es matching pero no maximal si queda C-D libre
        # B-C es maximal (size 1) porque bloquea todo
        
        # Nuestro algoritmo greedy depende del orden, pero debe ser maximal
        # Si elige B-C, ya no puede elegir nada más.
        # Si elige A-B, luego puede elegir C-D.
        
        # Verificamos que no hay aristas en el grafo que conecten dos nodos NO cubiertos
        for u in grafo:
            if u not in nodos_cubiertos:
                for v, _ in grafo[u]:
                    if v not in nodos_cubiertos:
                        self.fail(f"El matching no es maximal, se puede agregar la arista {u}-{v}")

    def test_hopcroft_karp_bipartito(self):
        # Grafo bipartito clásico
        # Set A: 1, 2, 3
        # Set B: 4, 5
        # 1-4, 1-5, 2-4, 3-5
        grafo = {
            '1': [('4', 1), ('5', 1)],
            '2': [('4', 1)],
            '3': [('5', 1)],
            '4': [('1', 1), ('2', 1)],
            '5': [('1', 1), ('3', 1)]
        }
        
        es_bip, matching = hopcroft_karp(grafo)
        self.assertTrue(es_bip)
        self.assertEqual(len(matching), 2) # Max matching size is 2 (e.g. 2-4, 3-5 leaves 1 matched to nothing or 1-4, 3-5 leaves 2 matched to nothing)
        # Wait, 1-4, 2-? No. 
        # 2-4, 3-5. 1 has edges to 4 and 5, both taken.
        # 1-5, 2-4. 3 has edge to 5, taken.
        # Max matching is indeed 2.

    def test_hopcroft_karp_bipartito_perfecto(self):
        # Cuadrado: A-B-C-D-A
        # A(0)-B(1)-C(0)-D(1)-A(0)
        # Matching perfecto: A-B, C-D (size 2)
        grafo = {
            'A': [('B', 1), ('D', 1)],
            'B': [('A', 1), ('C', 1)],
            'C': [('B', 1), ('D', 1)],
            'D': [('A', 1), ('C', 1)]
        }
        es_bip, matching = hopcroft_karp(grafo)
        self.assertTrue(es_bip)
        self.assertEqual(len(matching), 2)

    def test_hopcroft_karp_no_bipartito(self):
        # Triángulo
        grafo = {
            'A': [('B', 1), ('C', 1)],
            'B': [('A', 1), ('C', 1)],
            'C': [('A', 1), ('B', 1)]
        }
        es_bip, matching = hopcroft_karp(grafo)
        self.assertFalse(es_bip)
        self.assertEqual(len(matching), 0)

if __name__ == '__main__':
    unittest.main()
