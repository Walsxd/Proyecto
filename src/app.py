import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os

from algoritmos import *
from modelo import Grafo

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: white;'>Proyecto Estructuras Computacionales.</h1> <br><br>", unsafe_allow_html=True)
col_no1, col_izq, col_cen, col_der, col_no2 = st.columns([1,3, 1, 3,1])

# Inicializar variable de estado para el camino resaltado
if 'camino_resaltado' not in st.session_state:
    st.session_state.camino_resaltado = []

if 'mensaje_costo' not in st.session_state:
    st.session_state.mensaje_costo = None

# Paletas de colores
PALETAS = {
    "Azul": {"nodo": "#97c2fc", "resaltado": "#ff4d4d", "texto": "white"}, # Azul -> Rojo suave
    "Rojo": {"nodo": "#ff9999", "resaltado": "#4d4dff", "texto": "white"}, # Rojo -> Azul fuerte
    "Verde": {"nodo": "#99ff99", "resaltado": "#ff00ff", "texto": "black"}, # Verde -> Magenta
    "Amarillo": {"nodo": "#ffff99", "resaltado": "#0000ff", "texto": "black"}, # Amarillo -> Azul
    "Gris": {"nodo": "#dddddd", "resaltado": "#ff0000", "texto": "black"}, # Gris -> Rojo
    "Naranja": {"nodo": "#ffcc99", "resaltado": "#0000ff", "texto": "black"}, # Naranja -> Azul
}

with col_izq:
    st.subheader("Ingrese el grafo a utilizar: ")

    c1, c2, c3 = st.columns(3, vertical_alignment='bottom')

    with c1:
        st.markdown("""
            <div style="margin-top: 15px; margin-bottom: 5px; font-size: 14px;">
                Nodos A y B (A &rarr; B):
            </div>
        """, unsafe_allow_html=True)
        a1, a2 = st.columns(2)
        with a1:
            nodo_u = st.text_input("", "A", label_visibility="collapsed")
        with a2:
            nodo_v = st.text_input("", "B", label_visibility="collapsed")
    with c2:
        peso = st.number_input("Peso de la arista:", step=1)
    with c3:
        agregar = st.button("Agregar arista")

    c1,c2 = st.columns([5,2], vertical_alignment='bottom')

    def reiniciar_grafo():
        if 'graph' in st.session_state:
            del st.session_state.graph
        st.session_state.camino_resaltado = [] # Limpiar camino al reiniciar

    with c2:
        if st.button("Eliminar grafo"):
            if 'graph' in st.session_state:
                reiniciar_grafo()
                st.rerun()
    with c1:
        tipo = st.selectbox(
            "Tipo de grafo: ",
            ["Dirigido", "No dirigido"],
            on_change=reiniciar_grafo
        )

if 'graph' not in st.session_state:
    st.session_state.graph = Grafo(dirigido = True if tipo == "Dirigido" else False)
graph = st.session_state.graph

if agregar:
    try:
        u, v = nodo_u, nodo_v
        if (u.islower() or len(u) != 1 or not u.isalpha()) or (v.islower() or len(v) != 1 or not v.isalpha()):
            st.error("Los nodos ingresados no son validos.")
        else:
            graph.agregar_arista(u, v, peso)
            st.session_state.camino_resaltado = [] # Limpiar camino al modificar grafo
    except ValueError:
        st.error("Por favor ingrese los nodos en el formato correcto: 'A, B'")

with col_der:

    c_header, c_color = st.columns([2, 1])
    with c_header:
        st.subheader("Grafo seleccionado: ")
    with c_color:
        color_seleccionado = st.selectbox("Color:", list(PALETAS.keys()))
        colores = PALETAS[color_seleccionado]

    G = graph.obtener_datos_visuales()
    
    # --- LOGICA DE COLOREADO ---
    camino = st.session_state.camino_resaltado
    
    try:
        nt = Network(height="500px", width="500px", bgcolor="#ffffff", font_color="black", directed=graph.es_dirigido())
        
        # Añadir nodos manualmente para asegurar control
        for node in G.nodes():
            color_nodo = colores["resaltado"] if node in camino else colores["nodo"]
            size_nodo = 25 if node in camino else 20
            # shape='circle' pone la etiqueta adentro
            # font color depende de la paleta para contraste
            font_color = "white" if colores.get("texto") == "white" else "black"
            
            nt.add_node(node, label=str(node), color=color_nodo, size=size_nodo, shape='circle', 
                        font={'color': font_color, 'size': 20, 'face': 'arial'})

        # Añadir aristas manualmente para asegurar pesos
        aristas_camino_set = set()
        if len(camino) > 1:
             for i in range(len(camino) - 1):
                 u, v = camino[i], camino[i+1]
                 aristas_camino_set.add((u, v))
                 if not graph.es_dirigido():
                     aristas_camino_set.add((v, u))

        for u, v, data in G.edges(data=True):
            color_arista = colores["resaltado"] if (u, v) in aristas_camino_set else 'gray'
            width_arista = 3 if (u, v) in aristas_camino_set else 1
            w = data.get('weight', 0)
            label_arista = str(w) if w != 0 else ""
            
            nt.add_edge(u, v, color=color_arista, width=width_arista, label=label_arista)

        # Opciones de física ajustadas para evitar "explosiones" y zoom excesivo
        nt.set_options("""
        var options = {
          "physics": {
            "barnesHut": {
              "gravitationalConstant": -3000,
              "centralGravity": 0.5,
              "springLength": 95,
              "springConstant": 0.04,
              "damping": 0.09,
              "avoidOverlap": 0.1
            },
            "minVelocity": 0.75,
            "solver": "barnesHut",
            "stabilization": {
              "enabled": true,
              "iterations": 1000,
              "updateInterval": 100,
              "onlyDynamicEdges": false,
              "fit": true
            }
          },
          "interaction": {
            "dragNodes": true,
            "hideEdgesOnDrag": false,
            "hideNodesOnDrag": false,
            "zoomView": true
          }
        }
        """)
        
        # Guardar y mostrar
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            nt.save_graph(tmp_file.name)
            tmp_file.seek(0)
            html_content = tmp_file.read().decode('utf-8')
            
            html_content = html_content.replace('</head>', '<style>body, html { margin: 0; padding: 0; overflow: hidden; } #mynetwork { width: 500px; height: 500px; display: block; border: 1px solid lightgray; } canvas { display: block; }</style></head>')
            
        components.html(html_content, height=500, width=500, scrolling=False)
        
    except Exception as e:
        st.error(f"Error al generar grafo interactivo: {e}")
        # Fallback a matplotlib si falla algo (aunque no deberia)
        fig, ax = plt.subplots(figsize=(8, 8))
        pos = nx.circular_layout(G)
        nx.draw(G, pos, ax=ax, with_labels=True)
        st.pyplot(fig)

    with st.expander("Generar Grafo Aleatorio"):
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            tipo_aleatorio = st.radio("Tipo:", ["Dirigido", "No dirigido"], horizontal=True)
            num_nodos = st.number_input("Nodos:", min_value=2, max_value=20, value=5)
            con_pesos = st.checkbox("Con Pesos", value=True)
        with col_r2:
            # Max aristas
            max_edges = num_nodos * (num_nodos - 1)
            if tipo_aleatorio == "No dirigido":
                max_edges //= 2
            num_aristas = st.number_input("Aristas:", min_value=num_nodos-1, max_value=max_edges, value=num_nodos)
            
            if con_pesos:
                c_min, c_max = st.columns(2)
                with c_min:
                    min_p = st.number_input("Min Peso", value=1, min_value=1)
                with c_max:
                    max_p = st.number_input("Max Peso", value=10, min_value=min_p)
            else:
                min_p, max_p = 1, 1
            
        if st.button("Generar Aleatorio"):
            reiniciar_grafo()
            # Crear grafo nuevo
            st.session_state.graph = Grafo(dirigido = True if tipo_aleatorio == "Dirigido" else False)
            
            # Generar datos
            datos_aleatorios = generar_grafo_aleatorio(
                num_nodos, 
                num_aristas, 
                dirigido=(tipo_aleatorio=="Dirigido"),
                min_peso=min_p,
                max_peso=max_p,
                con_pesos=con_pesos
            )
            
            # Cargar en el objeto Grafo
            for u, vecinos in datos_aleatorios.items():
                 for v, peso in vecinos:
                     if tipo_aleatorio == "Dirigido":
                         st.session_state.graph.agregar_arista(u, v, peso)
                     else:
                         if u < v: 
                             st.session_state.graph.agregar_arista(u, v, peso)
                         elif u == v:
                             st.session_state.graph.agregar_arista(u, v, peso)
            st.rerun()


if not graph.obtener_lista_adyacencia():
    with (col_izq):
        st.warning("Aún no se ha agregado ninguna arista al grafo.")
else:
    with (col_izq):
        programs = ["~", "Matriz de adyacencia","Lista de adyacencia","Matriz de incidencia","BFS", "DFS", "Bellman-Ford", "Dijkstra", "Floyd-Warshall"]
        selected_Option = st.selectbox("Seleccione un programa: ", programs)
        
        # Calcular si es sin pesos para las advertencias
        es_sinpesos = all(w == 0 for u, v, w in G.edges(data='weight', default=0))

        # Resetear camino si cambiamos a visualizaciones estáticas o vacía
        if selected_Option == "~":
             if st.session_state.mensaje_costo or st.session_state.camino_resaltado:
                 st.session_state.mensaje_costo = None
                 st.session_state.camino_resaltado = []
                 st.rerun()

        if selected_Option in ["Matriz de adyacencia", "Lista de adyacencia", "Matriz de incidencia"]:
             if st.session_state.camino_resaltado:
                 st.session_state.camino_resaltado = []
                 st.rerun()

        if selected_Option == "BFS":
            st.header("Búsqueda en Anchura (BFS)")
            st.markdown("""
            **Descripción:** Explora el grafo nivel por nivel (capas). Útil para encontrar el camino más corto en grafos no ponderados.
            - **Complejidad Temporal:** $O(V + E)$
            - **Complejidad Espacial:** $O(V)$
            """)

            start_node = st.text_input("Nodo inicial:", "A")
            if start_node.islower() or len(start_node) != 1 or not start_node.isalpha():
                st.error("El nodo ingresado no es valido.")
            else:
                result = BFS(graph.obtener_lista_adyacencia(), start_node)
                st.write("Nodos visitados en orden:")
                st.code(" -> ".join(result), language="text")

        if selected_Option == "DFS":
            st.header("Búsqueda en Profundidad (DFS)")
            st.markdown("""
            **Descripción:** Explora tanto como sea posible a lo largo de cada rama antes de retroceder.
            - **Complejidad Temporal:** $O(V + E)$
            - **Complejidad Espacial:** $O(V)$
            """)

            start_node = st.text_input("Nodo inicial:", "A")
            if start_node.islower() or len(start_node) != 1 or not start_node.isalpha():
                st.error("El nodo ingresado no es valido.")
            else:
                result = DFS(graph.obtener_lista_adyacencia(), start_node)
                st.write("Nodos visitados en orden:")
                st.code(" -> ".join(result), language="text")


        if selected_Option == "Lista de adyacencia":
            lista_adyacencia = graph.obtener_lista_adyacencia()
            cols = st.columns(len(lista_adyacencia)) if len(lista_adyacencia) < 4 else [None]

            for nodo, vecinos in lista_adyacencia.items():
                with st.expander(f"Nodo {nodo}", expanded=False):
                    if not vecinos:
                        st.caption("Sin conexiones salientes")
                    for vecino, peso in vecinos:
                        st.write(f"{nodo} ➡ **{vecino}** , Peso: `{peso}`")

        if selected_Option == "Matriz de adyacencia":
            st.header("Matriz de adyacencia")
            matriz, letras = matriz_adyacencia(graph.obtener_lista_adyacencia())
            df = pd.DataFrame(matriz, index=letras, columns=letras)

            estilos_css = [
                {'selector': 'th', 'props': [('text-align', 'center')]},
                {'selector': 'td', 'props': [('text-align', 'center')]},
            ]

            df_algo = df.style.set_table_styles(estilos_css)
            st.table(df_algo)

        if selected_Option == "Matriz de incidencia":
            st.header("Matriz de incidencia")
            matriz, letras = matriz_incidencia(graph.obtener_lista_adyacencia())
            # Ajustar columnas a número de aristas
            columnas_aristas = [f"e{i+1}" for i in range(len(matriz[0]))] if matriz else []
            df = pd.DataFrame(matriz, index=letras, columns=columnas_aristas)

            estilos_css = [
                {'selector': 'th', 'props': [('text-align', 'center')]},
                {'selector': 'td', 'props': [('text-align', 'center')]},
            ]

            df_algo = df.style.set_table_styles(estilos_css)
            st.table(df_algo)

        if selected_Option == "Dijkstra":
           st.header("Algoritmo de Dijkstra")
           st.write("")
           if es_sinpesos:
               st.info("Dijkstra no es adecuado para grafos sin pesos.")

           st.markdown("""
           **Descripción:** Encuentra el camino más corto desde un nodo origen a todos los demás en un grafo con pesos positivos.
           - **Complejidad Temporal:** $O(E \log V)$ (usando cola de prioridad)
           - **Complejidad Espacial:** $O(V + E)$
           """)
           col_d1, col_d2 = st.columns(2)
           with col_d1:
               start_node = st.text_input("Nodo de Inicio:", "A")
           with col_d2:
               end_node = st.text_input("Nodo Destino:", "F")
           
           if st.button("Calcular Ruta"):
               datos_grafo = graph.obtener_lista_adyacencia()

               if start_node not in datos_grafo or end_node not in datos_grafo:
                   st.error(f"Error: Revisa nodos.")
               else:
                   camino, costo = dijkstra(datos_grafo, start_node, end_node)
                   if camino:
                        st.session_state.camino_resaltado = camino
                        st.session_state.mensaje_costo = f"¡Ruta encontrada! Costo total: {costo}"
                        st.rerun()
                   else:
                        st.session_state.camino_resaltado = []
                        st.session_state.mensaje_costo = "No existe un camino entre estos nodos."
                        st.rerun()

        if selected_Option == "Bellman-Ford":
            st.header("Algoritmo de Bellman-Ford")
            st.markdown("""
            **Descripción:** Calcula caminos más cortos y es capaz de detectar ciclos negativos. Es más lento que Dijkstra.
            - **Complejidad Temporal:** $O(V \cdot E)$
            - **Complejidad Espacial:** $O(V)$
            """)
            if es_sinpesos:
                st.info("Info: Bellman-Ford funciona, pero es lento para grafos sin pesos negativos.")

            start_node = st.text_input("Nodo inicial:", "A", key="bellman_start")
            end_node = st.text_input("Nodo final:", "C", key="bellman_end")
            
            if st.button("Calcular Bellman"):
                datos_grafo = graph.obtener_lista_adyacencia()
                if (start_node not in datos_grafo or end_node not in datos_grafo):
                    st.error("Nodos no válidos.")
                else:
                    camino, costo = bellman_ford(graph.obtener_lista_adyacencia(), start_node, end_node)
                    if not camino:
                        st.session_state.camino_resaltado = []
                        st.session_state.mensaje_costo = "No existe un camino entre estos nodos."
                        st.rerun()
                    else:
                        st.session_state.camino_resaltado = camino
                        st.session_state.mensaje_costo = f"¡Ruta encontrada! Costo total: {costo}"
                        st.rerun()

        if selected_Option == "Floyd-Warshall":
            st.header("Algoritmo de Floyd-Warshall")
            st.markdown("""
            **Descripción:** Programación dinámica para encontrar caminos más cortos entre **todos** los pares de nodos.
            - **Complejidad Temporal:** $O(V^3)$
            - **Complejidad Espacial:** $O(V^2)$
            """)
            
            datos_grafo = graph.obtener_lista_adyacencia()
            start_node = st.text_input("Nodo inicial:", "A", key="floyd_start")
            end_node = st.text_input("Nodo final:", "C", key="floyd_end")
            
            if st.button("Calcular Floyd"):
                if (start_node not in datos_grafo or end_node not in datos_grafo):
                    st.error("Nodos no válidos.")
                else:
                    camino, costo = floyd_warshall(graph.obtener_lista_adyacencia(), start_node, end_node)
                    if not camino:
                        st.session_state.camino_resaltado = []
                        st.session_state.mensaje_costo = "No existe un camino entre estos nodos."
                        st.rerun()
                    else:
                        st.session_state.camino_resaltado = camino
                        st.session_state.mensaje_costo = f"¡Ruta encontrada! Costo total: {costo}"
                        st.rerun()

        if st.session_state.mensaje_costo:
            st.write("---")
            if "No existe" in st.session_state.mensaje_costo:
                st.warning(st.session_state.mensaje_costo)
            else:
                st.success(st.session_state.mensaje_costo)
                if st.session_state.camino_resaltado:
                    st.write(f"**Camino:** {' → '.join(st.session_state.camino_resaltado)}")