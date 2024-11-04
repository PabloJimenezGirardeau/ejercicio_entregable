import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import networkx as nx
import pandas as pd
import unicodedata
import os  # Importar os para trabajar con rutas relativas

# Definir la ruta relativa para el archivo CSV
csv_path = os.path.join(os.path.dirname(__file__), 'mapa_metro.csv')
metro_data = pd.read_csv(csv_path)

# Crear el grafo desde los datos del CSV y agregar conexiones bidireccionales
G = nx.DiGraph()
for _, row in metro_data.iterrows():
    origen = row['origen']
    destino = row['destino']
    tiempo = row['tiempo']
    linea = row['linea']
    G.add_edge(origen, destino, weight=tiempo, linea=linea)
    G.add_edge(destino, origen, weight=tiempo, linea=linea)

# Función para normalizar el texto (elimina acentos y convierte a minúsculas)
def normalizar_texto(texto):
    texto = texto.lower()
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if unicodedata.category(c) != 'Mn')

# Función para mostrar el mapa del metro
def mostrar_mapa_metro():
    # Definir la ruta relativa para la imagen del mapa
    imagen_mapa_path = os.path.join(os.path.dirname(__file__), 'Madrid_metro_map.png')
    
    # Crear una nueva ventana para mostrar el mapa
    mapa_ventana = tk.Toplevel(root)
    mapa_ventana.title("Mapa del Metro de Madrid")
    
    # Cargar y mostrar la imagen
    imagen_mapa = Image.open(imagen_mapa_path)
    imagen_mapa = imagen_mapa.resize((800, 800), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(imagen_mapa)
    etiqueta_mapa = tk.Label(mapa_ventana, image=img_tk)
    etiqueta_mapa.image = img_tk  # Mantener la referencia
    etiqueta_mapa.pack()

# Función para buscar la ruta más corta usando Dijkstra
def buscar_ruta_mas_corta(grafo, origen, destino):
    try:
        ruta = nx.dijkstra_path(grafo, origen, destino, weight='weight')
        tiempo_total = nx.dijkstra_path_length(grafo, origen, destino, weight='weight')
        return ruta, tiempo_total
    except nx.NetworkXNoPath:
        return None, None

# Función para buscar la ruta con menos transbordos y optimizar también por tiempo
def buscar_ruta_menos_transbordos_con_tiempo(grafo, origen, destino):
    try:
        rutas = list(nx.all_shortest_paths(grafo, origen, destino))
        mejor_ruta = None
        mejor_tiempo = float('inf')

        for ruta in rutas:
            tiempo_total = sum(grafo[ruta[i]][ruta[i+1]]['weight'] for i in range(len(ruta) - 1))
            if tiempo_total < mejor_tiempo:
                mejor_ruta = ruta
                mejor_tiempo = tiempo_total
        
        return mejor_ruta, mejor_tiempo
    except nx.NetworkXNoPath:
        return None, None

# Función para detectar transbordos y generar la ruta con cambios de línea
def mostrar_ruta_con_transbordos(ruta):
    resultado_texto = ""
    linea_actual = None

    for i in range(len(ruta) - 1):
        estacion_actual = ruta[i]
        estacion_siguiente = ruta[i + 1]
        linea_siguiente = G[estacion_actual][estacion_siguiente]['linea']
        
        if linea_actual is None:
            resultado_texto += f"Inicia en {estacion_actual} (Toma la {linea_siguiente})\n"
            linea_actual = linea_siguiente
        elif linea_actual != linea_siguiente:
            resultado_texto += f"Llega a {estacion_actual}, haz transbordo a la {linea_siguiente}\n"
            linea_actual = linea_siguiente
        else:
            resultado_texto += f"Continúa en la {linea_actual}, pasa por {estacion_actual}\n"
    
    resultado_texto += f"Llega a {ruta[-1]}\n"  # Llegada al destino
    return resultado_texto

# Función para buscar la ruta más corta y mostrarla con transbordos
def buscar_ruta():
    origen = normalizar_texto(origen_entry.get())  # Normalizar la entrada del origen
    destino = normalizar_texto(destino_entry.get())  # Normalizar la entrada del destino
    optimizacion = optimizacion_var.get()  # Obtener si se optimiza por tiempo o transbordos
    
    estaciones_grafo = {normalizar_texto(estacion): estacion for estacion in G.nodes}
    
    if origen not in estaciones_grafo or destino not in estaciones_grafo:
        resultado_label.config(text="Estaciones no válidas")
        return
    
    origen_real = estaciones_grafo[origen]
    destino_real = estaciones_grafo[destino]
    
    if optimizacion == "Tiempo":
        ruta, tiempo_total = buscar_ruta_mas_corta(G, origen_real, destino_real)
    else:
        ruta, tiempo_total = buscar_ruta_menos_transbordos_con_tiempo(G, origen_real, destino_real)
    
    if ruta is None:
        resultado_label.config(text="No hay una ruta válida entre las estaciones.")
    else:
        resultado_texto = f"Ruta optimizada por {optimizacion} (Tiempo total: {tiempo_total:.2f} minutos):\n"
        resultado_texto += mostrar_ruta_con_transbordos(ruta)
        resultado_label.config(text=resultado_texto)

# Crear la ventana principal de la GUI
root = tk.Tk()
root.title("Ruta en el Metro de Madrid")

# Lista de estaciones para el autocompletado
estaciones = list(G.nodes)

# Crear los elementos de la interfaz
origen_label = ttk.Label(root, text="Estación de Origen:")
origen_label.grid(row=0, column=0, padx=5, pady=5)
origen_entry = ttk.Combobox(root, values=estaciones)
origen_entry.grid(row=0, column=1, padx=5, pady=5)

destino_label = ttk.Label(root, text="Estación de Destino:")
destino_label.grid(row=1, column=0, padx=5, pady=5)
destino_entry = ttk.Combobox(root, values=estaciones)
destino_entry.grid(row=1, column=1, padx=5, pady=5)

# Opción para seleccionar la optimización
optimizacion_label = ttk.Label(root, text="Optimizar por:")
optimizacion_label.grid(row=2, column=0, padx=5, pady=5)
optimizacion_var = tk.StringVar(value="Tiempo")
optimizacion_menu = ttk.Combobox(root, textvariable=optimizacion_var, values=["Tiempo", "Transbordos"])
optimizacion_menu.grid(row=2, column=1, padx=5, pady=5)

# Botón para buscar la ruta
buscar_button = ttk.Button(root, text="Buscar Ruta", command=buscar_ruta)
buscar_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Área para mostrar los resultados
resultado_label = ttk.Label(root, text="", justify="left")
resultado_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Botón para mostrar el mapa del metro
mapa_button = ttk.Button(root, text="Mostrar Mapa del Metro", command=mostrar_mapa_metro)
mapa_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Iniciar la interfaz
root.mainloop()
