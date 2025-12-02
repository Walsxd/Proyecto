import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from algoritmos import *
from modelo import Grafo

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: white;'>Proyecto Estructuras Computacionales.</h1> <br><br>", unsafe_allow_html=True)
col_no1, col_izq, col_cen, col_der, col_no2 = st.columns([1,3, 1, 3,1])

# Inicializar variable de estado para el camino resaltado
if 'camino_resaltado' not in st.session_state:
    st.session_state.camino_resaltado = []

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
    st.subheader("Grafo seleccionado: ")

    G = graph.obtener_datos_visuales()
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Usar layout circular o spring si se prefiere
    pos = nx.circular_layout(G)
    
    # --- LOGICA DE COLOREADO ---
    camino = st.session_state.camino_resaltado
    
    # Colores por defecto
    colores_nodos = []
    colores_aristas = []
    
    # Definir colores de nodos
    for node in G.nodes():
        if node in camino:
            colores_nodos.append('red') # Nodo en el camino
        else:
            colores_nodos.append('lightblue') # Nodo normal
            
    # Definir colores de aristas
    aristas_camino = []
    if len(camino) > 1:
        for i in range(len(camino) - 1):
            aristas_camino.append((camino[i], camino[i+1]))
            if not graph.es_dirigido(): # Si no es dirigido, agregar la inversa tambien para comparar
                 aristas_camino.append((camino[i+1], camino[i]))

    for u, v in G.edges():
        if (u, v) in aristas_camino:
            colores_aristas.append('red')
        else:
            colores_aristas.append('gray')
    
    # Dibujar el grafo
    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color=colores_nodos, # Usamos la lista de colores dinámica
        node_size=800,
        edge_color=colores_aristas, # Usamos la lista de colores dinámica
        font_size=10,
        font_weight='bold',
        width=2 if not camino else [2 if c == 'red' else 1 for c in colores_aristas], # Aristas rojas mas gruesas
    )
    
    es_sinpesos = all(w == 0 for u, v, w in G.edges(data='weight', default=0))
    if not es_sinpesos :
        etiquetas = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas, ax=ax, font_size=10, label_pos=0.3)

    fig.set_facecolor('lightgray')
    st.pyplot(fig)


if not graph.obtener_lista_adyacencia():
    with (col_izq):
        st.warning("Aún no se ha agregado ninguna arista al grafo.")
else:
    with (col_izq):
        programs = ["Matriz de adyacencia","Lista de adyacencia","Matriz de incidencia","BFS", "DFS", "Bellman-Ford", "Dijkstra", "Floyd-Warshall"]
        selected_Option = st.selectbox("Seleccione un programa: ", programs)
        
        # Resetear camino si cambiamos a visualizaciones estáticas
        if selected_Option in ["Matriz de adyacencia", "Lista de adyacencia", "Matriz de incidencia"]:
             if st.session_state.camino_resaltado:
                 st.session_state.camino_resaltado = []
                 st.rerun()

        if selected_Option == "BFS":
            st.header("Búsqueda en Anchura (BFS)")
            st.write("")

            start_node = st.text_input("Nodo inicial:", "A")
            if start_node.islower() or len(start_node) != 1 or not start_node.isalpha():
                st.error("El nodo ingresado no es valido.")
            else:
                result = BFS(graph.obtener_lista_adyacencia(), start_node)
                st.write("Nodos visitados en orden:")
                st.code(" -> ".join(result), language="text")

        if selected_Option == "DFS":
            st.header("Búsqueda en Profundidad (DFS)")
            st.write("")

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

           st.write("Calcula la ruta más corta entre dos nodos.")
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
                       st.success(f"¡Ruta encontrada! Costo total: {costo}")
                       st.write(f"**Camino:** {' → '.join(camino)}")
                       st.session_state.camino_resaltado = camino
                       st.rerun() # Recargar para pintar
                   else:
                       st.warning("No existe un camino.")
                       st.session_state.camino_resaltado = []

        if selected_Option == "Bellman-Ford":
            st.header("Algoritmo de Bellman-Ford")
            st.write("")
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
                        st.write("No existe un camino.")
                        st.session_state.camino_resaltado = []
                    else:
                        st.success(f"¡Ruta encontrada! Costo total: {costo}")
                        st.code(" → ".join(camino), language="text")
                        st.session_state.camino_resaltado = camino
                        st.rerun()

        if selected_Option == "Floyd-Warshall":
            st.header("Algoritmo de Floyd-Warshall")
            st.write("")
            
            datos_grafo = graph.obtener_lista_adyacencia()
            start_node = st.text_input("Nodo inicial:", "A", key="floyd_start")
            end_node = st.text_input("Nodo final:", "C", key="floyd_end")
            
            if st.button("Calcular Floyd"):
                if (start_node not in datos_grafo or end_node not in datos_grafo):
                    st.error("Nodos no válidos.")
                else:
                    camino, costo = floyd_warshall(graph.obtener_lista_adyacencia(), start_node, end_node)
                    if not camino:
                        st.write("No existe un camino.")
                        st.session_state.camino_resaltado = []
                    else:
                        st.success(f"¡Ruta encontrada! Costo total: {costo}")
                        st.code(" → ".join(camino), language="text")
                        st.session_state.camino_resaltado = camino
                        st.rerun()

