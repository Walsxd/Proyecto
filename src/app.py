import streamlit as st
import networkx as nx
import matplotlib as plt
from algoritmos import *
from modelo import Grafo

st.title("Proyecto Estructuras Computacionales.")

st.subheader("Ingrese el grafo a utilizar: ")


# Seleccion de Grafo para seguir con el programa
# Deberia ir la logica para colocar un grafo en una clase (no creada aun) grafo.
# Deberia ser un diccionario de listas de adyacencia

# PROVISIONALMENTE tenemos este grafo
graph = Grafo(dirigido = True)
graph.agregar_arista("A", "B")
graph.agregar_arista("A", "C")
graph.agregar_arista("B", "D")
graph.agregar_arista("B", "E")
graph.agregar_arista("C", "F")
graph.agregar_arista("E", "F")

programs = ["Matriz de adyacencia","Lista de adyacencia","Matriz de incidencia","BFS", "DFS"]
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



