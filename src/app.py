import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from algoritmos import *
from modelo import Grafo

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: white;'>Proyecto Estructuras Computacionales.</h1> <br><br>", unsafe_allow_html=True)
col_no1, col_izq, col_cen, col_der, col_no2 = st.columns([1,3, 1, 3,1])

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

    with c2:
        if st.button("Eliminar grafo"):
            if 'graph' in st.session_state:
                reiniciar_grafo()
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
    except ValueError:
        st.error("Por favor ingrese los nodos en el formato correcto: 'A, B'")

with col_der:
    st.subheader("Grafo seleccionado: ")
    G = graph.obtener_datos_visuales()
    fig, ax = plt.subplots(figsize=(8, 8))
    pos = nx.spring_layout(G, seed=40)
    nx.draw(G,
            pos,
            ax = ax,
            with_labels=True,
            node_color='lightblue',
            node_size=500,
            edge_color='lightgreen',
            font_size=12,
            font_weight='bold',
            )

    etiquetas = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas, ax=ax, font_size=10)
    fig.set_facecolor('Gray')
    st.pyplot(fig)


with col_izq:
    programs = ["Matriz de adyacencia", "Lista de adyacencia", "Matriz de incidencia", "BFS", "DFS", "Dijkstra"]
    selected_Option = st.selectbox("Seleccione un programa: ", programs)
    if selected_Option == "BFS":
        st.header("Búsqueda en Anchura (BFS)")
        ## Descripcion breve de BFS
        st.write("")

        start_node = st.text_input("Nodo inicial:", "A")
        if start_node.islower() or len(start_node) != 1 or not start_node.isalpha():
            st.error("El nodo ingresado no es valido.")
        else:
            result = BFS(graph.obtener_lista_adyacencia(), start_node)
            st.write("Nodos visitados en orden:", " -> ".join(result))

    if selected_Option == "DFS":
        st.header("Búsqueda en Anchura (DFS)")
        ## Descripcion breve de DFS
        st.write("")

        start_node = st.text_input("Nodo inicial:", "A")
        if start_node.islower() or len(start_node) != 1 or not start_node.isalpha():
            st.error("El nodo ingresado no es valido.")
        else:
            result = DFS(graph.obtener_lista_adyacencia(), start_node)
            st.write("Nodos visitados en orden:", " -> ".join(result))


    if selected_Option == "Lista de adyacencia":
        st.header("Lista de adyacencia")

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
        
    if selected_Option == "Dijkstra":
        st.header("Algoritmo de Dijkstra")
        st.write("Calcula la ruta más corta entre dos nodos.")

        # Inputs para nodo inicio y fin
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            start_node = st.text_input("Nodo de Inicio:", "A")
        with col_d2:
            end_node = st.text_input("Nodo Destino:", "F")

        if st.button("Calcular Ruta"):
            # Obtenemos los datos del grafo actual
            datos_grafo = graph.obtener_lista_adyacencia()
            
            # Verificamos si los nodos existen
            if start_node not in datos_grafo or end_node not in datos_grafo:
                st.error(f"Error: Revisa que los nodos '{start_node}' y '{end_node}' existan en el grafo.")
            else:
                # Llamamos a tu función dijkstra que importamos de algoritmos.py
                camino, costo = dijkstra(datos_grafo, start_node, end_node)

                if camino:
                    st.success(f"¡Ruta encontrada! Costo total: {costo}")
                    st.write(f"**Camino:** {' → '.join(camino)}")
                else:
                    st.warning("No existe un camino entre estos dos nodos.")


