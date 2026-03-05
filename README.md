# Astart_pathfinding
Código en py, con funcionamiento del algoritmo y representación
# 🏎️ A* RACING: Pathfinding Engine
### Desarrollado por **Adrián Pavón**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-ffffff?style=for-the-badge&logo=matplotlib&logoColor=black)

**A* Racing** es un simulador de navegación autónoma que implementa el algoritmo **A-Star (A*)** para encontrar la trayectoria óptima en circuitos de carreras complejos. El motor calcula en milisegundos la ruta más corta evitando colisiones con muros y chicanes, visualizando el proceso mediante una interfaz de alto rendimiento.



## 🎯 Visión General
A diferencia de otros buscadores de caminos, este proyecto utiliza una **heurística de distancia Euclídea** combinada con **costos de movimiento diferenciados**:
* **Movimiento Ortogonal:** Costo $1.0$
* **Movimiento Diagonal:** Costo $\sqrt{2} \approx 1.414$

Esto permite que la "moto" trace curvas realistas y trayectorias fluidas, simulando el comportamiento de un piloto real que busca el ápice de la curva.

## 🛠️ Stack Tecnológico
* **Core:** `Python` con `heapq` (Binary Heaps) para una complejidad $O(\log n)$ en la extracción del nodo mínimo.
* **Matemáticas:** `NumPy` para la manipulación de la rejilla (grid) como tensores.
* **UI/UX:** `Streamlit` con inyección de **CSS personalizado** para una estética *Cyber-Racing*.
* **Renderizado:** `Matplotlib` con efectos de trazado de ruta (`PathEffects`) y parches vectoriales dinámicos para representar la moto y la meta.



## 🧠 El Algoritmo en Detalle

El motor de búsqueda evalúa cada nodo $n$ basándose en la función de costo total:

$$f(n) = g(n) + h(n)$$

Donde:
* **$g(n)$**: Es el costo real acumulado desde el nodo de inicio hasta el nodo actual $n$.
* **$h(n)$**: Es la **Heurística**, una estimación del costo desde $n$ hasta el destino. En este proyecto usamos la distancia euclídea:
    $$\text{dist} = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$$

### Características Especiales:
* **Detección de Colisiones:** El sistema valida la integridad de la ruta y asegura que los puntos de inicio/fin no estén bloqueados antes de iniciar.
* **Exploración Visual:** Se muestran las celdas analizadas (Open Set) en azul para entender cómo el algoritmo "descarta" caminos ineficientes.
* **Editor Dinámico:** Permite crear circuitos personalizados activando o desactivando muros mediante un editor de datos integrado.

## 🚀 Instalación y Despliegue

1.  **Clonar el repositorio:**
    ```bash
   git clone [https://github.com/apavalc3108/Astart_pathfinding.git](https://github.com/apavalc3108/Astart_pathfinding.git)
   cd Astart_pathfinding
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install streamlit numpy matplotlib
    ```

3.  **Lanzar el motor:**
    ```bash
    python -m streamlit run path nombre_archivo.py
    ```

## 📊 Panel de Telemetría
Al ejecutar la simulación, el sistema devuelve métricas críticas de rendimiento en tarjetas visuales:
* **Nodos en Ruta:** Cantidad de pasos que componen el camino final.
* **Distancia Total:** Longitud exacta considerando tramos diagonales.
* **Celdas Visitadas:** Indica qué tan eficiente fue la búsqueda.
* **Tiempo de Cálculo:** Latencia del algoritmo medida con precisión de microsegundos.

---

## 👨‍💻 Autor
**Adrián Pavón**
*MASTER DE ESPECIALIZACIÓN EN IA Y BIG DATA*

---
> "La línea más corta entre dos puntos es el A* bien implementado."
