import networkx as nx

## Estructura basica del grafo como clase

class Grafo:
    def __init__(self, dirigido=False):
        self.dirigido = dirigido
        self.grafo_nx = nx.DiGraph() if dirigido else nx.Graph()
        self.lista_adyacencia = {}
        self.nodos = set()

    def agregar_arista(self, u, v, peso=1):
        if u not in self.lista_adyacencia:
            self.lista_adyacencia[u] = []
            self.nodos.add(u)
            self.grafo_nx.add_node(u)

        if v not in self.lista_adyacencia:
            self.lista_adyacencia[v] = []
            self.nodos.add(v)
            self.grafo_nx.add_node(v)

        self.lista_adyacencia[u].append((v, peso))
        self.grafo_nx.add_edge(u, v, weight=peso)

        if not self.dirigido:
            self.lista_adyacencia[v].append((u, peso))

    def es_dirigido(self):
        return self.dirigido

    def obtener_lista_adyacencia(self):
        return self.lista_adyacencia

    def obtener_datos_visuales(self):
        return self.grafo_nx