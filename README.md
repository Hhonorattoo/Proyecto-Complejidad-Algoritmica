# Optimización y Modelamiento Topológico de Almacén para *Order Picking*

Este repositorio contiene la implementación en Python para la representación topológica, visualización interactiva y análisis de complejidad algorítmica enfocados en la optimización de rutas de preparación de pedidos (*Order Picking*) en un almacén logístico.

El proyecto traduce la planta física de un almacén a un **grafo ponderado y no dirigido** $G = (V, E, W)$ de 1,542 nodos y 1,579 aristas, implementando un control de **Nivel de Detalle Dinámico (LOD)** para la exploración interactiva y un estudio gráfico del costo computacional de ruteo.

---

## 🚀 Características Principales

* **Modelamiento Topológico:** Representación formal de pasillos, conexiones, puntos de picking y zona de despacho.
* **Control Interactivo LOD (Level of Detail):** 
  * *Vista Panorámica:* Muestra la estructura general del almacén segmentada por colores.
  * *Vista en Acercamiento (Zoom):* Oculta los puntos de alta densidad y despliega dinámicamente las cajas con los códigos de cada producto y los pesos métricos (distancias) en cada arista[cite: 2, 3].
* **Análisis de Complejidad Computacional:** Evaluación comparativa en escalas lineal y logarítmica entre la solución por **Fuerza Bruta** $O(n!)$ y **Programación Dinámica / Held-Karp** $O(n^2 \cdot 2^n)$.

---

## 📁 Estructura del Repositorio

```text
.
├── dataset_nodos.csv       # Dataset con 1,542 nodos (código, nombre, categoría, x, y)
├── dataset_aristas.csv     # Dataset con 1,579 aristas (Nodo1, Nodo2, peso)
├── modelamiento_grafo.py   # Script de visualización e interacción LOD del grafo
├── Creacion_imagen.py      # Script para generar la gráfica comparativa de complejidad
└── README.md               # Documentación del proyecto

