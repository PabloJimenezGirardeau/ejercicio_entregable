# Metro Madrid - Optimización de Rutas

Este proyecto es una aplicación interactiva que permite calcular rutas óptimas en el sistema de metro de Madrid (lineas 1-10). Utilizando algoritmos como Dijkstra, optimiza la ruta entre dos estaciones, ya sea por el menor tiempo de trayecto o por la menor cantidad de transbordos.
He descubierto que al haber puestos tiempos aleatorios entre estaciones, si filtras la ruta por tiempo aveces te da una ruta que no tiene mucho sentido. Aun asi siguen siendo validas

## 📄 Descripción del proyecto

### Funcionalidades principales:
- **Cálculo de la ruta más corta**: Utilizando el algoritmo de Dijkstra, el programa calcula la ruta más corta entre dos estaciones optimizando por tiempo o por transbordos.
- **Visualización del mapa del metro**: La aplicación permite mostrar una imagen del mapa del metro de Madrid.
- **Optimización por tiempo o transbordos**: Puedes elegir si deseas optimizar la ruta para que tarde lo menos posible o para tener la menor cantidad de transbordos.

### Interfaz gráfica:
La interfaz está construida usando **Tkinter**. En ella puedes:

- Seleccionar la estación de origen.
- Seleccionar la estación de destino.
- Elegir si prefieres optimizar la ruta por **tiempo** o por **transbordos**.
- Mostrar el mapa del metro de Madrid en una ventana emergente.

## 📊 Análisis de Complejidad

El análisis de la complejidad del programa se encuentra en el archivo [complejidad.md](complejidad.md).

