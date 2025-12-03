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

    def to_dict(self):
        """Convierte el grafo a un diccionario serializable."""
        aristas = []
        # Usamos grafo_nx para obtener las aristas de manera consistente
        for u, v, data in self.grafo_nx.edges(data=True):
            aristas.append({
                "u": u,
                "v": v,
                "peso": data.get("weight", 1)
            })
        
        return {
            "tipo": "Dirigido" if self.dirigido else "No dirigido",
            "nodos": list(self.nodos),
            "aristas": aristas
        }

    @classmethod
    def from_dict(cls, data):
        """Crea una instancia de Grafo desde un diccionario."""
        es_dirigido = data.get("tipo") == "Dirigido"
        grafo = cls(dirigido=es_dirigido)
        
        # Agregar nodos primero (para asegurar nodos aislados si los hubiera)
        for nodo in data.get("nodos", []):
            if nodo not in grafo.lista_adyacencia:
                grafo.lista_adyacencia[nodo] = []
                grafo.nodos.add(nodo)
                grafo.grafo_nx.add_node(nodo)
        
        # Agregar aristas
        for arista in data.get("aristas", []):
            grafo.agregar_arista(arista["u"], arista["v"], arista.get("peso", 1))
            
        return grafo

    def calcular_densidad(self):
        """Calcula la densidad del grafo."""
        return nx.density(self.grafo_nx)

    def es_conexo(self):
        """Verifica si el grafo es conexo (o fuertemente conexo si es dirigido)."""
        if self.dirigido:
            return nx.is_strongly_connected(self.grafo_nx)
        return nx.is_connected(self.grafo_nx)

    def calcular_diametro(self):
        """Calcula el diámetro ponderado (suma de pesos)."""
        try:
            # 1. Obtener todas las longitudes de caminos más cortos considerando el peso
            path_lengths = dict(nx.all_pairs_dijkstra_path_length(self.grafo_nx, weight='weight'))
            
            # 2. Encontrar la distancia máxima
            diametro = 0
            for source, targets in path_lengths.items():
                if not targets: 
                    continue
                max_dist_from_source = max(targets.values())
                if max_dist_from_source > diametro:
                    diametro = max_dist_from_source
            
            return diametro

        except nx.NetworkXError:
            return None

    def calcular_radio(self):
        """Calcula el radio ponderado."""
        try:
            path_lengths = dict(nx.all_pairs_dijkstra_path_length(self.grafo_nx, weight='weight'))
            
            # La excentricidad es la distancia máxima desde un nodo a cualquier otro
            excentricidades = {}
            for source, targets in path_lengths.items():
                if not targets: 
                    continue
                excentricidades[source] = max(targets.values())
            
            # El radio es la excentricidad mínima
            if not excentricidades:
                return 0
            return min(excentricidades.values())
            
        except ValueError:
            return None

    def calcular_centro(self):
        """Calcula el centro del grafo (requiere ser conexo)."""
        try:
            return nx.center(self.grafo_nx)
        except nx.NetworkXError:
            return None