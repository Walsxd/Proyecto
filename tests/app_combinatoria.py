import streamlit as st
import pandas as pd
import itertools

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="Algoritmos Combinatorios")

# --- FUNCIONES LÓGICAS (ALGORITMOS) ---
def generar_permutaciones(elementos):
    # Usamos itertools para eficiencia en la web, pero la lógica es O(n * n!)
    return list(itertools.permutations(elementos))

def generar_cadenas_binarias_rec(n):
    if n == 0:
        return [""]
    cadenas = []
    for cadena in generar_cadenas_binarias_rec(n - 1):
        cadenas.append(cadena + "0")
        cadenas.append(cadena + "1")
    return cadenas

def generar_conjunto_potencia(elementos):
    n = len(elementos)
    total_combinaciones = 1 << n
    potencia = []
    for i in range(total_combinaciones):
        subconjunto = []
        for j in range(n):
            if (i >> j) & 1:
                subconjunto.append(elementos[j])
        potencia.append(subconjunto)
    return potencia

def obtener_datos_correspondencia(elementos):
    n = len(elementos)
    total_combinaciones = 1 << n
    data = []
    
    for i in range(total_combinaciones):
        # Generar binario (padding con ceros a la izquierda)
        binario = bin(i)[2:].zfill(n)
        
        # Generar subconjunto basado en el binario
        subconjunto = []
        # Leemos de izquierda a derecha para alinear con la lista visualmente
        for idx, char in enumerate(binario):
            if char == '1':
                subconjunto.append(elementos[idx])
        
        # Formatear el subconjunto como string para la tabla
        sub_str = "{" + ", ".join(subconjunto) + "}" if subconjunto else "∅"
        
        data.append([i, binario, sub_str])
        
    return data

# --- INTERFAZ GRÁFICA ---

st.markdown("<h1 style='text-align: center; color: white;'>Laboratorio de Estructuras Discretas</h1> <br>", unsafe_allow_html=True)

col_izq, col_espacio, col_der = st.columns([1, 0.2, 2])

with col_izq:
    st.markdown("### ⚙️ Configuración")
    
    opciones = [
        "1. Permutaciones",
        "2. Conjunto Potencia",
        "3. Cadenas Binarias",
        "4. Correspondencia (Binario ↔ Potencia)"
    ]
    seleccion = st.selectbox("Seleccione un algoritmo:", opciones)
    
    st.divider()
    
    # Inputs dinámicos según la selección
    elementos = []
    n = 0
    
    if "3. Cadenas Binarias" in seleccion:
        n = st.number_input("Tamaño de cadena (n):", min_value=1, max_value=20, value=3, step=1)
        st.info(f"Se generarán $2^{n} = {2**n}$ cadenas.")
    else:
        raw_input = st.text_input("Ingrese elementos (separados por coma o espacio):", "A, B, C")
        # Limpieza de entrada
        elementos = [x.strip() for x in raw_input.replace(',', ' ').split() if x.strip()]
        n = len(elementos)
        
        if n > 0:
            st.caption(f"Elementos detectados ({n}): {elementos}")
            if n > 10:
                st.warning("⚠️ Cuidado: Muchos elementos pueden alentar el navegador.")

with col_der:
    st.markdown("### 📊 Resultados y Visualización")
    
    # --- LOGICA DE VISUALIZACIÓN ---
    
    if "1. Permutaciones" in seleccion:
        st.subheader("Generador de Permutaciones")
        st.markdown(r"**Complejidad:** $O(n \cdot n!)$")
        
        if n > 0:
            perms = generar_permutaciones(elementos)
            df = pd.DataFrame(perms, columns=[f"Pos {i+1}" for i in range(n)])
            df.index += 1  # Empezar índice en 1
            
            st.write(f"Total de permutaciones: **{len(perms)}**")
            st.dataframe(df, use_container_width=True, height=400)
        else:
            st.info("Ingrese elementos para comenzar.")

    elif "2. Conjunto Potencia" in seleccion:
        st.subheader("Conjunto Potencia")
        st.markdown(r"**Complejidad:** $O(n \cdot 2^n)$")
        
        if n > 0:
            potencia = generar_conjunto_potencia(elementos)
            # Formatear para visualización limpia
            potencia_fmt = ["{" + ", ".join(p) + "}" if p else "∅ (Conjunto Vacío)" for p in potencia]
            
            df = pd.DataFrame(potencia_fmt, columns=["Subconjuntos"])
            st.write(f"Total de subconjuntos: **{len(potencia)}**")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Ingrese elementos para comenzar.")

    elif "3. Cadenas Binarias" in seleccion:
        st.subheader(f"Cadenas Binarias de tamaño {n}")
        st.markdown(r"**Complejidad:** $O(n \cdot 2^n)$")
        
        cadenas = generar_cadenas_binarias_rec(n)
        
        # Visualización en columnas para ahorrar espacio vertical
        col1, col2 = st.columns(2)
        half = len(cadenas) // 2
        
        with col1:
            st.table(pd.DataFrame(cadenas[:half], columns=["Cadenas (Parte 1)"]))
        with col2:
            st.table(pd.DataFrame(cadenas[half:], columns=["Cadenas (Parte 2)"]))

    elif "4. Correspondencia" in seleccion:
        st.subheader("Correspondencia Binaria ↔ Subconjuntos")
        st.markdown(r"**Complejidad:** $O(n \cdot 2^n)$")
        st.write("Este algoritmo demuestra cómo cada número binario actúa como una 'máscara' para seleccionar elementos.")
        
        if n > 0:
            datos = obtener_datos_correspondencia(elementos)
            df = pd.DataFrame(datos, columns=["Índice Decimal", "Máscara Binaria", "Subconjunto Resultante"])
            
            # Estilizar la tabla
            st.table(df)
            
            # Explicación visual
            st.info("Nota: Un '1' en la máscara binaria significa que el elemento en esa posición es incluido en el subconjunto.")
        else:
            st.info("Ingrese elementos para comenzar.")

# Footer simple
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>Proyecto Estructuras Computacionales - Algoritmos Combinatorios</div>", unsafe_allow_html=True)