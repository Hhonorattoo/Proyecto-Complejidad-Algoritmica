# Optimización y Modelamiento Topológico de Almacén para *Order Picking*

Este repositorio contiene la implementación en Python para la representación topológica, visualización interactiva y análisis de complejidad algorítmica enfocados en la optimización de rutas de preparación de pedidos (*Order Picking*) en un almacén logístico.

El proyecto traduce la planta física de un almacén a un **grafo ponderado y no dirigido** $G = (V, E, W)$ de 1,542 nodos y 1,579 aristas, implementando un control de **Nivel de Detalle Dinámico (LOD)** para la exploración interactiva y un estudio gráfico del costo computacional de ruteo.

---

## Características Principales

* **Modelamiento Topológico:** Representación formal de pasillos, conexiones, puntos de picking y zona de despacho.
* **Control Interactivo LOD (Level of Detail):** 
  * *Vista Panorámica:* Muestra la estructura general del almacén segmentada por colores.
  * *Vista en Acercamiento (Zoom):* Oculta los puntos de alta densidad y despliega dinámicamente las cajas con los códigos de cada producto y los pesos métricos (distancias) en cada arista.
* **Análisis de Complejidad Computacional:** Evaluación comparativa en escalas lineal y logarítmica entre la solución por **Fuerza Bruta** $O(n!)$ y **Programación Dinámica / Held-Karp** $O(n^2 \cdot 2^n)$.

---

## Estructura del Repositorio

```text
.
├── dataset_nodos.csv       # Dataset con 1,542 nodos (código, nombre, categoría, x, y)
├── dataset_aristas.csv     # Dataset con 1,579 aristas (Nodo1, Nodo2, peso)
├── modelamiento_grafo.py   # Script de visualización e interacción LOD del grafo
├── Creacion_imagen.py      # Script para generar la gráfica comparativa de complejidad
└── README.md               # Documentación del proyecto
```

## Estructura de los Datasets

### 1. `dataset_nodos.csv`
Almacena las entidades y atributos espaciales de la planta:
* **`codigo`**: Identificador alfanumérico único de cada nodo.
* **`nombre`**: Denominación del producto o ubicación en el almacén.
* **`categoria`**: Clasificación del punto (`INICIO`, `Pasillo`, `Salida`, o categoría de producto).
* **`x`, `y`**: Coordenadas cartesianas bidimensionales en el plano del almacén.

### 2. `dataset_aristas.csv`
Define las adyacencias y transitabilidad entre nodos:
* **`Nodo1`**: Código del extremo inicial.
* **`Nodo2`**: Código del extremo final.
* **`peso`**: Distancia euclidiana métrica entre ambos puntos.

---

## Clasificación Cromática de Nodos

| Categoría | Color en Grafo | Función en el Almacén |
| :--- | :--- | :--- |
| **`INICIO` (`I`)** | Verde (`#4ade80`) | Punto de despacho/salida y retorno obligatorio de rutas. |
| **`Pasillo` (`A1-A20`)** | Naranja (`#fb923c`) | Cabeceras de acceso e interconexión vial inferior. |
| **`Salida` (`FA1-FA20`)** | Naranja Intenso (`#f97316`) | Cabeceras superiores de evacuación entre pasillos. |
| **Artículos de Picking** | Azul (`#38bdf8`) | Puntos fijos de recolección de productos. |

---

## 🛠️ Requisitos e Instalación

### Requisitos Previos
* Python 3.8 o superior.

### Instalación de Librerías
Instala los paquetes necesarios ejecutando en tu terminal:

```bash
pip install pandas networkx matplotlib numpy
```

## 💻 Instrucciones de Ejecución

> **Nota:** Asegúrate de ejecutar los scripts desde la misma carpeta donde se encuentran los archivos `dataset_nodos.csv` y `dataset_aristas.csv`.

### 1. Visualización Interactiva del Almacén

```bash
python modelamiento_grafo.py
```

*   **Navegación:** Usa las herramientas de Zoom de la ventana de Matplotlib. Al acercarte a cualquier sección, la interfaz cambiará automáticamente de vista panorámica a vista detallada con códigos y distancias.

### 2. Generación del Gráfico de Complejidad Algorítmica

```bash
python Creacion_imagen.py
```
*   Despliega la comparación asintótica entre el enfoque por Fuerza Bruta $O(n!)$ y la optimización Held-Karp $O(n^2 \cdot 2^n)$[cite: 1].

## 🔬 Análisis de Complejidad y Algoritmos

Para resolver el problema del viajante de comercio (TSP) aplicado al *Order Picking*[cite: 1]:

*   Fuerza Bruta ($O(n!)$): Computacionalmente inviable cuando el número de productos por pedido supera $n > 10$, sobrepasando rápidamente los 3.6 millones de operaciones[cite: 1].
*   Held-Karp ($O(n^2 \cdot 2^n)$): Optimización mediante Programación Dinámica que reduce de manera exponencial los tiempos de procesamiento en listas intermedias de extracción[cite: 1].
