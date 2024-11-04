## 📊 Análisis de Complejidad

### 1. Algoritmo de Dijkstra

El algoritmo de Dijkstra se utiliza para encontrar la ruta más corta en el sistema de metro de Madrid, optimizando por tiempo.

- **Big O (O)**: \( O((V + E) \log V) \)
- **Theta (Θ)**: \( Θ((V + E) \log V) \)
- **Omega (Ω)**: \( Ω((V + E) \log V) \)

Donde:
- \( V \) es el número de estaciones.
- \( E \) es el número de conexiones (aristas) entre estaciones.

### 2. Búsqueda de Transbordos

Una vez que se ha calculado la ruta más corta, se recorre la lista de estaciones para detectar transbordos. Este recorrido tiene una complejidad lineal.

- **Big O (O)**: \( O(n) \)
- **Theta (Θ)**: \( Θ(n) \)
- **Omega (Ω)**: \( Ω(n) \)

Donde:
- \( n \) es el número de estaciones en la ruta.

### 3. Complejidad Total del Programa

El tiempo total de ejecución del programa está dominado por el algoritmo de Dijkstra, por lo que la complejidad global del programa es:

- **Big O (O)**: \( O((V + E) \log V) \)
- **Theta (Θ)**: \( Θ((V + E) \log V) \)
- **Omega (Ω)**: \( Ω((V + E) \log V) \)
