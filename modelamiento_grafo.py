import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

df_limpio = pd.read_csv('dataset_nodos.csv')
df_aristas = pd.read_csv('dataset_aristas.csv')

# 2. Inicializar y cargar el grafo
G = nx.Graph()

for _, row in df_limpio.iterrows():
  G.add_node(
      row['codigo'],
      pos=(float(row['x']), float(row['y'])),
      categoria=row['categoria'],
      nombre=row['nombre'],
  )

for _, row in df_aristas.iterrows():
  G.add_edge(row['Nodo1'], row['Nodo2'], weight=float(row['peso']))

pos = nx.get_node_attributes(G, 'pos')


fig, ax = plt.subplots(figsize=(14, 10), facecolor='#0f172a')
ax.set_facecolor('#0f172a')
nx.draw_networkx_edges(
    G, pos, edge_color='#334155', width=0.8, alpha=0.6, ax=ax
)
# Separar listas de nodos
nodos_inicio = [
    n for n, d in G.nodes(data=True) if d.get('categoria') == 'INICIO'
]
nodos_cabeceras = [
    n
    for n, d in G.nodes(data=True)
    if d.get('categoria') in ['Pasillo', 'Salida']
]
nodos_productos = [
    n
    for n, d in G.nodes(data=True)
    if d.get('categoria') not in ['INICIO', 'Pasillo', 'Salida']
]
# Guardar referencias de todas las capas de bolitas
scatter_productos = nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=nodos_productos,
    node_size=6,
    node_color='#38bdf8',
    alpha=0.7,
    ax=ax,
)
scatter_cabeceras = nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=nodos_cabeceras,
    node_size=35,
    node_color='#fb923c',
    ax=ax,
)

scatter_inicio = nx.draw_networkx_nodes(
    G, pos, nodelist=nodos_inicio, node_size=120, node_color='#4ade80', ax=ax
)

# Etiquetas fijas para la vista panorámica
labels_cabeceras_dict = {n: n for n in nodos_cabeceras + nodos_inicio}
textos_estaticos = nx.draw_networkx_labels(
    G,
    pos,
    labels=labels_cabeceras_dict,
    font_size=6,
    font_color='#f8fafc',
    ax=ax,
)

# Leyenda con cuadros
cuadro_verde = mpatches.Patch(
    color='#4ade80', label='Despacho / Punto inicio (I)'
)
cuadro_naranja_in = mpatches.Patch(
    color='#fb923c', label='A1 - A20 / Entradas de pasillos'
)
cuadro_naranja_out = mpatches.Patch(
    color='#f97316', label='FA1 - FA20 / Salidas de pasillos'
)
cuadro_azul = mpatches.Patch(
    color='#38bdf8', label='Artículos / Nodos de picking'
)

ax.legend(
    handles=[cuadro_verde, cuadro_naranja_in, cuadro_naranja_out, cuadro_azul],
    loc='lower left',
    bbox_to_anchor=(0.02, 0.03),
    facecolor='#1e293b',
    edgecolor='#334155',
    fontsize=9.5,
    framealpha=0.8,
    labelcolor='#f8fafc',
    handlelength=1.1,
    handleheight=1.1,
    borderpad=0.8,
    labelspacing=0.6,
)

plt.title(
    'Plano Topológico del Almacén',
    color='#f8fafc',
    fontsize=14,
    fontweight='bold',
    pad=15,
)
plt.axis('off')

# -------------------------------------------------------------
# 4. GESTIÓN DINÁMICA DE ZOOM (Reemplazo total de bolitas por códigos)
# -------------------------------------------------------------
elementos_dinamicos = []
def actualizar_vista(event_ax):
  global elementos_dinamicos

  for elem in elementos_dinamicos:
    elem.remove()
  elementos_dinamicos.clear()

  xlim = ax.get_xlim()
  ylim = ax.get_ylim()
  ancho_vista = abs(xlim[1] - xlim[0])
  alto_vista = abs(ylim[1] - ylim[0])

  zoom_cercano = ancho_vista < 130 and alto_vista < 300

  if zoom_cercano:
    #Ocultar bolitas y textos panorámicos
    scatter_productos.set_visible(False)
    scatter_cabeceras.set_visible(False)
    scatter_inicio.set_visible(False)
    for txt in textos_estaticos.values():
      txt.set_visible(False)

    # 1. Dibujar códigos centrados en (x, y)
    for n, (x, y) in pos.items():
      if xlim[0] <= x <= xlim[1] and ylim[0] <= y <= ylim[1]:
        cat = G.nodes[n].get('categoria', '')

        if cat == 'INICIO':
          color_borde = '#4ade80'
          tamano_letra = 9
        elif cat in ['Pasillo', 'Salida']:
          color_borde = '#fb923c'
          tamano_letra = 8.5
        else:
          color_borde = '#38bdf8'
          tamano_letra = 8

        txt = ax.text(
            x,
            y,
            str(n),
            fontsize=tamano_letra,
            color=color_borde,
            fontweight='bold',
            ha='center',
            va='center',
            bbox=dict(
                boxstyle='round,pad=0.25',
                facecolor='#0f172a',
                edgecolor=color_borde,
                linewidth=0.8,
                alpha=0.95,
            ),
            zorder=4,
        )
        elementos_dinamicos.append(txt)

    # 2. Dibujar pesos cargados desde dataset_aristas.csv
    for u, v, data in G.edges(data=True):
      x1, y1 = pos[u]
      x2, y2 = pos[v]
      if (xlim[0] <= x1 <= xlim[1] and ylim[0] <= y1 <= ylim[1]) or (
          xlim[0] <= x2 <= xlim[1] and ylim[0] <= y2 <= ylim[1]
      ):
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        peso = data.get('weight', '')
        txt = ax.text(
            mx,
            my,
            f'{peso}',
            fontsize=6.8,
            color='#facc15',
            ha='center',
            va='center',
            bbox=dict(
                boxstyle='round,pad=0.15',
                facecolor='#020617',
                edgecolor='#facc15',
                linewidth=0.6,
                alpha=0.95,
            ),
            zorder=3,
        )
        elementos_dinamicos.append(txt)
  else:
    # Restaurar vista completa
    scatter_productos.set_visible(True)
    scatter_cabeceras.set_visible(True)
    scatter_inicio.set_visible(True)
    for txt in textos_estaticos.values():
      txt.set_visible(True)

  fig.canvas.draw_idle()


ax.callbacks.connect('xlim_changed', actualizar_vista)
ax.callbacks.connect('ylim_changed', actualizar_vista)

plt.tight_layout()
plt.show()


print(df_limpio)