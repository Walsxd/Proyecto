import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os
import json
import io

from algoritmos import *
from modelo import Grafo

st.set_page_config(layout="wide", page_title="Proyecto Grafos")

st.markdown("""
    <style>
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        .main-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            padding: 0.5rem 2rem;
            z-index: 1000000; 
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
            height: 3.5rem; 
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .main-header h1 {
            color: white;
            margin: 0;
            font-size: 1.5rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .main .block-container {
            padding-top: 4.5rem !important;
        }
        
        .streamlit-expanderHeader {
            background-color: rgba(59, 130, 246, 0.1);
            border-radius: 8px;
            border-left: 4px solid #3b82f6;
            font-weight: 500;
        }
        
        .stButton > button {
            border-radius: 8px;
            border: 1px solid rgba(59, 130, 246, 0.3);
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        .stButton > button:hover {
            border-color: #3b82f6;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
            transform: translateY(-1px);
        }
        
        iframe {
            border-radius: 12px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
    </style>
    
    <div class="main-header">
        <h1>Proyecto Estructuras Computacionales</h1>
    </div>
""", unsafe_allow_html=True)
col_no1, col_izq, col_cen, col_der, col_no2 = st.columns([1,3, 1, 3,1])

# Inicializar variable de estado para el camino resaltado
if 'camino_resaltado' not in st.session_state:
    st.session_state.camino_resaltado = []

if 'aristas_resaltadas' not in st.session_state:
    st.session_state.aristas_resaltadas = []

if 'colores_nodos' not in st.session_state:
    st.session_state.colores_nodos = {}

if 'mensaje_costo' not in st.session_state:
    st.session_state.mensaje_costo = None

# Inicializar variable de estado para fullscreen
if 'fullscreen' not in st.session_state:
    st.session_state.fullscreen = False

# Inicializar selector de programa
if 'program_selector' not in st.session_state:
    st.session_state.program_selector = "~"

# Inicializar opción previa para detectar cambios
if 'previous_program' not in st.session_state:
    st.session_state.previous_program = "~"

# Inicializar selector de color
if 'selector_color' not in st.session_state:
    st.session_state.selector_color = "Azul"

# Paletas de colores
PALETAS = {
    "Azul": {"nodo": "#97c2fc", "resaltado": "#ff4d4d", "texto": "white"}, # Azul -> Rojo suave
    "Rojo": {"nodo": "#ff9999", "resaltado": "#4d4dff", "texto": "white"}, # Rojo -> Azul fuerte
    "Verde": {"nodo": "#99ff99", "resaltado": "#ff00ff", "texto": "black"}, # Verde -> Magenta
    "Amarillo": {"nodo": "#ffff99", "resaltado": "#0000ff", "texto": "black"}, # Amarillo -> Azul
    "Gris": {"nodo": "#dddddd", "resaltado": "#ff0000", "texto": "black"}, # Gris -> Rojo
    "Naranja": {"nodo": "#ffcc99", "resaltado": "#0000ff", "texto": "black"}, # Naranja -> Azul
}

OPCIONES_COLOR = ["Azul", "Rojo", "Verde", "Amarillo", "Gris", "Naranja"]

# Colores suaves para Bipartito (Set A, Set B)
COLORES_BIPARTITO = {
    "Azul": ("#97c2fc", "#ffb3b3"),     # Azul claro vs Rojo claro
    "Rojo": ("#ff9999", "#97c2fc"),     # Rojo claro vs Azul claro
    "Verde": ("#99ff99", "#ffccff"),    # Verde claro vs Magenta claro
    "Amarillo": ("#ffff99", "#ccccff"), # Amarillo claro vs Lavanda
    "Gris": ("#dddddd", "#ffb3b3"),     # Gris claro vs Rojo claro
    "Naranja": ("#ffcc99", "#99ccff"),  # Naranja claro vs Azul claro
}


# Modo Pantalla Completa
if st.session_state.get('fullscreen', False):
    if st.button("Salir de Pantalla Completa"):
        st.session_state.fullscreen = False
        st.rerun()
    
    # Asegurarse de que existe el grafo
    if 'graph' in st.session_state:
        graph_fs = st.session_state.graph
        G_fs = graph_fs.obtener_datos_visuales()
        camino_fs = st.session_state.camino_resaltado
        colores_nodos_fs = st.session_state.get('colores_nodos', {})
        
        # Usar colores por defecto o seleccionados
        nombre_color = st.session_state.selector_color
        colores_fs = PALETAS[nombre_color]
        
        try:
            nt_fs = Network(height="800px", width="100%", bgcolor="#ffffff", font_color="black", directed=graph_fs.es_dirigido())
            
            for node in G_fs.nodes():
                # Prioridad: colores_nodos > camino_resaltado > color base
                if node in colores_nodos_fs:
                    color_nodo = colores_nodos_fs[node]
                elif node in camino_fs:
                    color_nodo = colores_fs["resaltado"]
                else:
                    color_nodo = colores_fs["nodo"]
                    
                nt_fs.add_node(node, label=str(node), color=color_nodo, size=30, shape='circle', 
                            font={'color': 'white', 'size': 24, 'face': 'arial'})

            aristas_camino_set_fs = set()
            
            # Prioridad a aristas_resaltadas (MST, etc)
            if 'aristas_resaltadas' in st.session_state and st.session_state.aristas_resaltadas:
                for u, v in st.session_state.aristas_resaltadas:
                    aristas_camino_set_fs.add((u, v))
                    if not graph_fs.es_dirigido():
                        aristas_camino_set_fs.add((v, u))
            # Si no, usar camino_resaltado (Dijkstra, BFS, etc)
            elif len(camino_fs) > 1:
                 for i in range(len(camino_fs) - 1):
                     u, v = camino_fs[i], camino_fs[i+1]
                     aristas_camino_set_fs.add((u, v))
                     if not graph_fs.es_dirigido():
                         aristas_camino_set_fs.add((v, u))

            for u, v, data in G_fs.edges(data=True):
                color_arista = colores_fs["resaltado"] if (u, v) in aristas_camino_set_fs else 'gray'
                width_arista = 4 if (u, v) in aristas_camino_set_fs else 2
                w = data.get('weight', 0)
                label_arista = str(w) if w != 0 else ""
                nt_fs.add_edge(u, v, color=color_arista, width=width_arista, label=label_arista)

            nt_fs.set_options("""
            var options = {
              "physics": {"barnesHut": {"gravitationalConstant": -3000, "centralGravity": 0.3, "springLength": 150}},
              "interaction": {"dragNodes": true, "zoomView": true}
            }
            """)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
                nt_fs.save_graph(tmp_file.name)
                tmp_file.seek(0)
                html_content = tmp_file.read().decode('utf-8')
                
            components.html(html_content, height=800, scrolling=False)
            
        except Exception as e:
            st.error(f"Error al generar grafo: {e}")
    
    st.stop()  # Importante: detener ejecución para no mostrar el resto

with col_izq:
    st.markdown("### Configuración del Grafo")

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
        st.session_state.aristas_resaltadas = [] # Limpiar aristas
        st.session_state.colores_nodos = {} # Limpiar colores de nodos
        st.session_state.mensaje_costo = None
        st.session_state.program_selector = "~" # Resetear selector
        st.session_state.previous_program = "~"

    with c2:
        if st.button("Eliminar grafo"):
            if 'graph' in st.session_state:
                reiniciar_grafo()
                st.rerun()
    with c1:
        # Determinar índice por defecto basado en el grafo actual
        default_index = 0
        if 'graph' in st.session_state:
            default_index = 0 if st.session_state.graph.es_dirigido() else 1

        # Inicializar estado si no existe
        if 'tipo_grafo_ui' not in st.session_state:
             st.session_state.tipo_grafo_ui = "Dirigido" if default_index == 0 else "No dirigido"

        st.write("Tipo de grafo:")
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            if st.button("Dirigido", type="primary" if st.session_state.tipo_grafo_ui == "Dirigido" else "secondary", use_container_width=True):
                if st.session_state.tipo_grafo_ui != "Dirigido":
                    st.session_state.tipo_grafo_ui = "Dirigido"
                    reiniciar_grafo()
                    st.rerun()
        
        with col_t2:
            if st.button("No dirigido", type="primary" if st.session_state.tipo_grafo_ui == "No dirigido" else "secondary", use_container_width=True):
                if st.session_state.tipo_grafo_ui != "No dirigido":
                    st.session_state.tipo_grafo_ui = "No dirigido"
                    reiniciar_grafo()
                    st.rerun()

        tipo = st.session_state.tipo_grafo_ui






    st.write("") 

    with st.expander("Generar Grafo Aleatorio"):
        col_rand1, col_rand2 = st.columns(2)
        with col_rand1:
            num_nodos_rand = st.number_input("Nodos", min_value=2, max_value=100, value=5, key="rand_nodos")
            min_peso_rand = st.number_input("Peso Mínimo", value=1, key="rand_min_peso")
        with col_rand2:
            # Estimación de aristas máximas
            max_aristas = num_nodos_rand * (num_nodos_rand - 1)
            if not (tipo == "Dirigido"):
                max_aristas //= 2
            
            num_aristas_rand = st.number_input("Aristas", min_value=num_nodos_rand-1, max_value=max_aristas, value=min(num_nodos_rand, max_aristas), key="rand_aristas")
            max_peso_rand = st.number_input("Peso Máximo", value=10, key="rand_max_peso")
            
        if st.button("Generar Aleatorio"):
            reiniciar_grafo()
            adj_aleatoria = generar_grafo_aleatorio(
                num_nodos_rand, 
                num_aristas_rand, 
                dirigido=(tipo == "Dirigido"),
                min_peso=min_peso_rand,
                max_peso=max_peso_rand
            )
            
            # Crear nuevo grafo y poblarlo
            nuevo_grafo = Grafo(dirigido=(tipo == "Dirigido"))
            

            added_edges = set()
            for u, vecinos in adj_aleatoria.items():
                for v, w in vecinos:
                    if tipo == "Dirigido":
                        nuevo_grafo.agregar_arista(u, v, w)
                    else:
                        # Para no dirigido, solo agregamos si no hemos procesado la arista (u, v) o (v, u)
                        edge = tuple(sorted((u, v)))
                        if edge not in added_edges:
                            nuevo_grafo.agregar_arista(u, v, w)
                            added_edges.add(edge)

            
            st.session_state.graph = nuevo_grafo
            st.rerun()

    with st.expander("Gestión de Archivos"):
        # Botón de descarga centrado
        if 'graph' in st.session_state:
            grafo_dict = st.session_state.graph.to_dict()
            json_str = json.dumps(grafo_dict, indent=2)
            st.download_button(
                label="Descargar Grafo Actual (JSON)",
                data=json_str,
                file_name="grafo.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.markdown("---")
        st.write("**Cargar Grafo desde Archivo:**")
        
        # Carga de archivo
        uploaded_file = st.file_uploader(
            "Arrastra y suelta tu archivo JSON aquí", 
            type=["json"], 
            label_visibility="visible"
        )
        
        if uploaded_file is not None:
            # Evitar recargas infinitas comprobando si es el mismo archivo
            if 'last_uploaded_file' not in st.session_state or st.session_state.last_uploaded_file != uploaded_file.name:
                try:
                    data = json.load(uploaded_file)
                    # Validar estructura básica
                    if "nodos" in data and "aristas" in data:
                        reiniciar_grafo()
                        st.session_state.graph = Grafo.from_dict(data)
                        
                        # Actualizamos el archivo cargado
                        st.session_state.last_uploaded_file = uploaded_file.name
                        
                        st.success("¡Grafo cargado correctamente!")
                        st.rerun()
                    else:
                        st.error("El archivo no tiene el formato correcto (faltan nodos o aristas).")
                except Exception as e:
                    st.error(f"Error al leer archivo: {e}")

        # Exportar Imagen PNG
        if 'graph' in st.session_state:
            st.markdown("---")
            st.write("**Exportar Imagen:**")
            
            try:
                G_export = st.session_state.graph.obtener_datos_visuales()
                
                # Calcular tamaño dinámico basado en el número de nodos
                num_nodos = len(G_export.nodes())
                # Tamaño base 12, aumenta con los nodos, tope en 50
                calc_size = max(12, min(50, num_nodos * 0.5))
                
                fig, ax = plt.subplots(figsize=(calc_size, calc_size), dpi=100)
                
                pos = nx.circular_layout(G_export)
                nx.draw_networkx_nodes(G_export, pos, ax=ax, node_size=700, node_color='#97c2fc', edgecolors='black')
                nx.draw_networkx_labels(G_export, pos, ax=ax, font_size=12, font_family="sans-serif")
                nx.draw_networkx_edges(G_export, pos, ax=ax, edge_color='gray', width=1.5, arrowsize=20)
                
                # Dibujar pesos de aristas
                edge_labels = nx.get_edge_attributes(G_export, 'weight')
                nx.draw_networkx_edge_labels(G_export, pos, edge_labels=edge_labels, font_size=10)
                
                plt.axis('off')
                
                buf = io.BytesIO()
                plt.savefig(buf, format="png", bbox_inches='tight', pad_inches=0.1)
                buf.seek(0)
                
                st.download_button(
                    label="Descargar Imagen (PNG)",
                    data=buf,
                    file_name="grafo.png",
                    mime="image/png",
                    use_container_width=True
                )
                plt.close(fig)
            except Exception as e:
                st.error(f"Error al generar imagen: {e}")

if 'graph' not in st.session_state:
    st.session_state.graph = Grafo(dirigido = True if tipo == "Dirigido" else False)
graph = st.session_state.graph
G = graph.obtener_datos_visuales() # DEFINIR G AQUI PARA QUE ESTE DISPONIBLE GLOBALMENTE

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

if not graph.obtener_lista_adyacencia():
    with (col_izq):
        st.info("Comienza agregando aristas para construir tu grafo")
else:
    with (col_izq):
        programs = ["~", "Matriz de adyacencia","Lista de adyacencia","Matriz de incidencia","Componentes Conexas", "Es Árbol?", "Es Bipartito?", "Pareo (Matching)", "Kruskal (MST)", "Reverse-Kruskal (MaxST)", "Prim (MST)", "BFS", "DFS", "Bellman-Ford", "Dijkstra", "Floyd-Warshall"]
        
        # Detectar cambio de programa para limpiar
        if st.session_state.program_selector != st.session_state.previous_program:
            st.session_state.mensaje_costo = None
            st.session_state.camino_resaltado = []
            st.session_state.aristas_resaltadas = []
            st.session_state.colores_nodos = {}
            st.session_state.previous_program = st.session_state.program_selector
            # No hacemos rerun aquí para dejar que el flujo continúe con el nuevo programa
            
        selected_Option = st.selectbox("Seleccione un programa: ", programs, key="program_selector")
        
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
            st.dataframe(df_algo, use_container_width=True)

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
            st.dataframe(df_algo, use_container_width=True)

        if selected_Option == "Componentes Conexas":
            st.header("Componentes Conexas")
            
            datos_grafo = graph.obtener_lista_adyacencia()
            es_dirigido = graph.es_dirigido()
            
            if es_dirigido:
                st.markdown("**Grafo Dirigido:** Buscando Componentes Fuertemente Conexas (SCC) usando Kosaraju.")
                componentes = kosaraju(datos_grafo)
            else:
                st.markdown("**Grafo No Dirigido:** Buscando Componentes Conexas.")
                componentes = obtener_componentes_conexas(datos_grafo)
                
            st.write(f"**Número de componentes encontradas:** {len(componentes)}")
            
            # Crear DataFrame para componentes
            data_comp = []
            for i, comp in enumerate(componentes):
                data_comp.append({
                    "Componente": i + 1,
                    "Nodos": ", ".join(comp),
                    "Tamaño": len(comp)
                })
            
            df_comp = pd.DataFrame(data_comp)
            df_comp.set_index("Componente", inplace=True)
            
            # Estilizar tabla
            estilos_css = [
                {'selector': 'th', 'props': [('text-align', 'center'), ('background-color', '#262730'), ('color', 'white')]},
                {'selector': 'td', 'props': [('text-align', 'center')]},
            ]
            st.table(df_comp.style.set_table_styles(estilos_css))

                
            # Opcional: Colorear componentes (si se desea en el futuro)
            # Por ahora solo mostramos la lista textual como se acordó.


        if selected_Option == "Es Árbol?":
            st.header("Validación de Árbol")
            datos_grafo = graph.obtener_lista_adyacencia()
            es_dirigido = graph.es_dirigido()
            
            es_arbol_val, razon = es_arbol(datos_grafo, es_dirigido)
            
            if es_arbol_val:
                st.success(f"✅ {razon}")
            else:
                st.error(f"❌ {razon}")

        if selected_Option == "Es Bipartito?":
            st.header("Validación de Grafo Bipartito")
            datos_grafo = graph.obtener_lista_adyacencia()
            
            es_bip, set_a, set_b = es_bipartito(datos_grafo)
            
            if es_bip:
                st.success("✅ El grafo ES bipartito.")
                # Preparar datos para la tabla
                lista_a = sorted(list(set_a), key=lambda x: (len(x), x))
                lista_b = sorted(list(set_b), key=lambda x: (len(x), x))
                
                # Igualar longitudes para el DataFrame
                max_len = max(len(lista_a), len(lista_b))
                lista_a += [""] * (max_len - len(lista_a))
                lista_b += [""] * (max_len - len(lista_b))
                
                df_bipartito = pd.DataFrame({
                    "Conjunto A": lista_a,
                    "Conjunto B": lista_b
                })
                
                # Estilizar la tabla
                estilos_css = [
                    {'selector': 'th', 'props': [('text-align', 'center'), ('background-color', '#262730'), ('color', 'white')]},
                    {'selector': 'td', 'props': [('text-align', 'center')]},
                ]
                df_bipartito.index = range(1, len(df_bipartito) + 1)
                st.table(df_bipartito.style.set_table_styles(estilos_css))

                
                # Asignar colores para visualización dinámicamente
                nombre_color = st.session_state.selector_color
                color_a, color_b = COLORES_BIPARTITO.get(nombre_color, ("#97c2fc", "#ffb3b3"))
                
                colores_map = {}
                for n in set_a:
                    colores_map[n] = color_a
                for n in set_b:
                    colores_map[n] = color_b
                
                st.session_state.colores_nodos = colores_map
                
            else:
                st.error("❌ El grafo NO es bipartito.")
                
        if selected_Option == "Pareo (Matching)":
            st.header("Pareo (Matching)")
            datos_grafo = graph.obtener_lista_adyacencia()
            
            tipo_pareo = st.radio("Tipo de Pareo:", ["Maximal (Greedy)", "Máximo (Hopcroft-Karp)"])
            
            if tipo_pareo == "Maximal (Greedy)":
                matching = matching_maximal(datos_grafo)
                st.write(f"**Tamaño del Matching:** {len(matching)}")
                # Crear DataFrame para matching
                df_matching = pd.DataFrame(list(matching), columns=["Nodo U", "Nodo V"])
                
                # Estilizar tabla
                estilos_css = [
                    {'selector': 'th', 'props': [('text-align', 'center'), ('background-color', '#262730'), ('color', 'white')]},
                    {'selector': 'td', 'props': [('text-align', 'center')]},
                ]
                df_matching.index = range(1, len(df_matching) + 1)
                st.table(df_matching.style.set_table_styles(estilos_css))


                
                st.session_state.aristas_resaltadas = matching
                
            else: # Máximo (Hopcroft-Karp)
                es_bip, matching = hopcroft_karp(datos_grafo)
                if not es_bip:
                    st.error("Hopcroft-Karp requiere un grafo bipartito.")
                else:
                    st.write(f"**Tamaño del Matching Máximo:** {len(matching)}")
                    # Crear DataFrame para matching
                    df_matching = pd.DataFrame(list(matching), columns=["Nodo U", "Nodo V"])
                    
                    # Estilizar tabla
                    estilos_css = [
                        {'selector': 'th', 'props': [('text-align', 'center'), ('background-color', '#262730'), ('color', 'white')]},
                        {'selector': 'td', 'props': [('text-align', 'center')]},
                    ]
                    df_matching.index = range(1, len(df_matching) + 1)
                    st.table(df_matching.style.set_table_styles(estilos_css))


                    
                    st.session_state.aristas_resaltadas = matching

        if selected_Option == "Kruskal (MST)":
            st.header("Árbol de Expansión Mínima (Kruskal)")
            datos_grafo = graph.obtener_lista_adyacencia()
            es_dirigido = graph.es_dirigido()
            
            if es_dirigido:
                st.warning("El algoritmo de Kruskal está diseñado para grafos no dirigidos.")
            else:
                # Verificar conectividad primero
                es_valido, _ = es_arbol(datos_grafo, es_dirigido)
                # Un MST existe si el grafo es conexo (aunque es_arbol pide que no haya ciclos, Kruskal funciona en cualquier conexo para dar un árbol)
                # Relajamos la condición: solo necesitamos que sea conexo.
                comp = obtener_componentes_conexas(datos_grafo)
                if len(comp) > 1:
                    st.error("El grafo no es conexo. No existe un MST único (sería un bosque).")
                else:
                    mst, peso_total = kruskal(datos_grafo)
                    st.write(f"**Peso Total del MST:** {peso_total}")
                    # Crear DataFrame para MST
                    df_mst = pd.DataFrame(mst, columns=["Origen", "Destino", "Peso"])
                    
                    # Estilizar tabla
                    estilos_css = [
                        {'selector': 'th', 'props': [('text-align', 'center'), ('background-color', '#262730'), ('color', 'white')]},
                        {'selector': 'td', 'props': [('text-align', 'center')]},
                    ]
                    df_mst.index = range(1, len(df_mst) + 1)
                    st.table(df_mst.style.set_table_styles(estilos_css))


                        
                    # Resaltar en el grafo
                    aristas_mst = []
                    nodos_mst = set()
                    for u, v, p in mst:
                        aristas_mst.append((u, v))
                        nodos_mst.add(u)
                        nodos_mst.add(v)
                    
                    st.session_state.aristas_resaltadas = aristas_mst
                    # st.session_state.camino_resaltado = list(nodos_mst) # No resaltar nodos para MST, solo aristas

        if selected_Option == "Reverse-Kruskal (MaxST)":
            st.header("Árbol de Expansión Máxima (Reverse-Kruskal)")
            datos_grafo = graph.obtener_lista_adyacencia()
            es_dirigido = graph.es_dirigido()
            
            if es_dirigido:
                st.warning("El algoritmo de Kruskal está diseñado para grafos no dirigidos.")
            else:
                # Verificar conectividad
                comp = obtener_componentes_conexas(datos_grafo)
                if len(comp) > 1:
                    st.error("El grafo no es conexo. No existe un MaxST único (sería un bosque).")
                else:
                    mst, peso_total = kruskal_maximo(datos_grafo)
                    st.write(f"**Peso Total del MaxST:** {peso_total}")
                    # Crear DataFrame para MaxST
                    df_mst = pd.DataFrame(mst, columns=["Origen", "Destino", "Peso"])
                    
                    # Estilizar tabla
                    estilos_css = [
                        {'selector': 'th', 'props': [('text-align', 'center'), ('background-color', '#262730'), ('color', 'white')]},
                        {'selector': 'td', 'props': [('text-align', 'center')]},
                    ]
                    df_mst.index = range(1, len(df_mst) + 1)
                    st.table(df_mst.style.set_table_styles(estilos_css))


                        
                    # Resaltar en el grafo
                    aristas_mst = []
                    for u, v, p in mst:
                        aristas_mst.append((u, v))
                    
                    st.session_state.aristas_resaltadas = aristas_mst

        if selected_Option == "Prim (MST)":
            st.header("Árbol de Expansión Mínima (Prim)")
            datos_grafo = graph.obtener_lista_adyacencia()
            es_dirigido = graph.es_dirigido()
            
            if es_dirigido:
                st.warning("El algoritmo de Prim está diseñado para grafos no dirigidos.")
            else:
                comp = obtener_componentes_conexas(datos_grafo)
                if len(comp) > 1:
                    st.error("El grafo no es conexo. Prim necesita un grafo conexo.")
                else:
                    start_node = st.text_input("Nodo inicial para Prim:", "A")
                    if start_node not in datos_grafo:
                         st.error("Nodo no válido.")
                    else:
                        mst, peso_total = prim(datos_grafo, start_node)
                        st.write(f"**Peso Total del MST:** {peso_total}")
                        # Crear DataFrame para MST
                        df_mst = pd.DataFrame(mst, columns=["Origen", "Destino", "Peso"])
                        
                        # Estilizar tabla
                        estilos_css = [
                            {'selector': 'th', 'props': [('text-align', 'center'), ('background-color', '#262730'), ('color', 'white')]},
                            {'selector': 'td', 'props': [('text-align', 'center')]},
                        ]
                        df_mst.index = range(1, len(df_mst) + 1)
                        st.table(df_mst.style.set_table_styles(estilos_css))



                        aristas_mst = []
                        nodos_mst = set()
                        for u, v, p in mst:
                            aristas_mst.append((u, v))
                            nodos_mst.add(u)
                            nodos_mst.add(v)

                        st.session_state.aristas_resaltadas = aristas_mst
                        # st.session_state.camino_resaltado = list(nodos_mst) # No resaltar nodos para MST, solo aristas



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

# --- MOVED col_der LOGIC HERE ---
with col_der:

    c_header, c_color, c_btn = st.columns([3, 1.5, 0.5], vertical_alignment="bottom")

    with c_header:
        st.subheader("Grafo seleccionado: ")

    with c_color:
        # 'label_visibility="collapsed"' oculta la etiqueta para ahorrar espacio
        # Usamos key para persistir y acceder en col_izq
        color_seleccionado = st.selectbox("Color", OPCIONES_COLOR, label_visibility="collapsed", key="selector_color")
        colores = PALETAS[color_seleccionado]

    if st.button("Ver en Pantalla Completa"):
        st.session_state.fullscreen = True
        st.rerun()

    # G YA ESTA DEFINIDO ARRIBA
    
    # --- LOGICA DE COLOREADO ---
    camino = st.session_state.camino_resaltado
    colores_nodos = st.session_state.get('colores_nodos', {})
    
    try:
        nt = Network(height="500px", width="500px", bgcolor="#ffffff", font_color="black", directed=graph.es_dirigido())
        
        # Añadir nodos manualmente para asegurar control
        for node in G.nodes():
            # Prioridad: colores_nodos > camino_resaltado > color base
            if node in colores_nodos:
                color_nodo = colores_nodos[node]
            elif node in camino:
                color_nodo = colores["resaltado"]
            else:
                color_nodo = colores["nodo"]
            
            size_nodo = 25 if node in camino or node in colores_nodos else 20
            font_color = "white" if colores.get("texto") == "white" else "black"
            
            nt.add_node(node, label=str(node), color=color_nodo, size=size_nodo, shape='circle', 
                        font={'color': font_color, 'size': 20, 'face': 'arial'})

        # Añadir aristas manualmente para asegurar pesos
        aristas_camino_set = set()
        
        # Prioridad a aristas_resaltadas (MST, etc)
        if 'aristas_resaltadas' in st.session_state and st.session_state.aristas_resaltadas:
            for u, v in st.session_state.aristas_resaltadas:
                aristas_camino_set.add((u, v))
                if not graph.es_dirigido():
                    aristas_camino_set.add((v, u))
        # Si no, usar camino_resaltado (Dijkstra, BFS, etc)
        elif len(camino) > 1:
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