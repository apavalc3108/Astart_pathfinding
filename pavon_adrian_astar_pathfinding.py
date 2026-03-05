import heapq
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import streamlit as st
import time

# Si fuera necesario pip install streamlit numpy matplotlib

# Logica del ALGORITMO A*
# Clase que representa cada celda del grid como un nodo
class nodo:
    def __init__(self, x, y):
        self.x = x                  # Fila del nodo
        self.y = y                  # Columna del nodo
        self.G = float('inf')       # Costo desde el inicio hasta este nodo
        self.H = 0                  # Heuristica (distancia estimada al destino)
        self.f = float('inf')       # Costo total f = G + H
        self.padre_i = None         # Fila del nodo padre
        self.padre_j = None         # Columna del nodo padre

    # Permite comparar nodos en la cola de prioridad segun su valor f
    def __lt__(self, other):
        return self.f < other.f

# Dimensiones del grid
ROW = 9
COL = 10

# Verifica si una posicion esta dentro de los limites del grid
def es_valido(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

# Verifica si la celda no esta bloqueada (1 = libre, 0 = bloqueada)
def unlock(grid, row, col):
    return grid[row][col] == 1

# Verifica si la posicion actual es el destino
def es_destino(row, col, dest):
    return row == dest[0] and col == dest[1]

# Calcula la heuristica usando distancia mahattam
def calcular_valor_h(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

# Reconstruye el camino desde el destino hasta el origen usando los padres
def obtener_ruta(detalles, dest):
    path = []
    row, col = dest[0], dest[1]

    # Retrocede desde el destino hasta el nodo inicial
    while not (detalles[row][col].padre_i == row and detalles[row][col].padre_j == col):
        path.append((row, col))
        temp_row = detalles[row][col].padre_i
        temp_col = detalles[row][col].padre_j
        row, col = temp_row, temp_col

    # Anade el nodo inicial
    path.append((row, col))

    # Invierte la lista para que vaya desde el origen al destino
    path.reverse()
    return path

# Implementacion del algoritmo A*
def busqueda_a_estrella(grid, start, dest):

    # Verifica que origen y destino esten dentro del grid
    if not es_valido(start[0], start[1]) or not es_valido(dest[0], dest[1]):
        print("Origen o destino fuera de rango")
        return None

    # Verifica que origen y destino no esten bloqueados
    if not unlock(grid, start[0], start[1]) or not unlock(grid, dest[0], dest[1]):
        print("Origen o destino bloqueado")
        return None

    # Si el origen ya es el destino
    if es_destino(start[0], start[1], dest):
        print("Ya estamos en el destino")
        return [tuple(start)]

    lista_cerrada = set()  # Conjunto de nodos ya evaluados

    # Matriz de nodos con informacion detallada
    detalles = [[nodo(i, j) for j in range(COL)] for i in range(ROW)]

    # Inicializa el nodo de inicio
    i, j = start
    detalles[i][j].f = 0
    detalles[i][j].G = 0
    detalles[i][j].padre_i = i
    detalles[i][j].padre_j = j

    # Cola de prioridad (lista abierta)
    lista_abierta = []
    heapq.heappush(lista_abierta, (0, detalles[i][j]))

    # Mientras haya nodos por explorar
    while lista_abierta:

        # Extrae el nodo con menor f
        f, actual = heapq.heappop(lista_abierta)
        i, j = actual.x, actual.y

        # Lo agrega a la lista cerrada
        lista_cerrada.add((i, j))

        # Movimientos posibles (4 direcciones + diagonales)
        direcciones = [
            (0, 1), (0, -1), (1, 0), (-1, 0),      # Movimientos rectos
            (1, 1), (1, -1), (-1, 1), (-1, -1)     # Movimientos diagonales
        ]

        # Explora los vecinos
        for d in direcciones:
            ni, nj = i + d[0], j + d[1]

            # Verifica que sea valido, libre y no visitado
            if es_valido(ni, nj) and unlock(grid, ni, nj) and (ni, nj) not in lista_cerrada:

                # Si encontramos el destino
                if es_destino(ni, nj, dest):
                    detalles[ni][nj].padre_i = i
                    detalles[ni][nj].padre_j = j
                    print("Destino encontrado!")
                    return obtener_ruta(detalles, dest)

                else:
                    # Costo diagonal = 1.414 (aprox sqrt(2))
                    # Costo recto = 1
                    costo = 1.414 if abs(d[0]) + abs(d[1]) == 2 else 1.0

                    # Nuevo costo G
                    g_new = detalles[i][j].G + costo

                    # Nueva heuristica H
                    h_new = calcular_valor_h(ni, nj, dest)

                    # Nuevo costo total F
                    f_new = g_new + h_new

                    # Si es mejor camino o nunca se ha visitado
                    if detalles[ni][nj].f == float('inf') or detalles[ni][nj].f > f_new:
                        detalles[ni][nj].f = f_new
                        detalles[ni][nj].G = g_new
                        detalles[ni][nj].padre_i = i
                        detalles[ni][nj].padre_j = j

                        # Se anade a la lista abierta
                        heapq.heappush(lista_abierta, (f_new, detalles[ni][nj]))

    print("No se encontro camino")
    return None


# DATOS DE PRUEBA

# 1 = celda libre
# 0 = celda bloqueada
cuadricula = [
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 1, 0, 0, 1]
]

# Punto de inicio
origen = [8, 0]

# Punto de destino
destino = [0, 0]

# Ejecuta el algoritmo A*
camino_resultado = busqueda_a_estrella(cuadricula, origen, destino)

# Imprime el camino encontrado
print("Camino encontrado:", camino_resultado)



#  VISUALIZACION STREAMLIT
def busqueda_a_estrella_ui(grid, start, dest):
    """
    Wrapper del algoritmo A* que acepta grids de cualquier tamano
    y devuelve ademas la lista de celdas exploradas para visualizarlas.
    La logica interna es identica a busqueda_a_estrella.
    """
    grid = np.array(grid)
    R, C = grid.shape

    def _valido(r, c):   return 0 <= r < R and 0 <= c < C
    def _libre(r, c):    return grid[r][c] == 1
    def _destino(r, c):  return r == dest[0] and c == dest[1]
    def _h(r, c):        return ((r - dest[0]) ** 2 + (c - dest[1]) ** 2) ** 0.5

    if not _valido(*start) or not _valido(*dest): return None, []
    if not _libre(*start)  or not _libre(*dest):  return None, []
    if _destino(*start): return [tuple(start)], []

    cerrada  = set()
    detalles = [[nodo(i, j) for j in range(C)] for i in range(R)]
    i, j = start
    detalles[i][j].f = 0
    detalles[i][j].G = 0
    detalles[i][j].padre_i = i
    detalles[i][j].padre_j = j

    lista_abierta = []
    heapq.heappush(lista_abierta, (0, detalles[i][j]))
    exploradas = []

    direcciones = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    while lista_abierta:
        f, actual = heapq.heappop(lista_abierta)
        i, j = actual.x, actual.y
        cerrada.add((i, j))
        exploradas.append((i, j))

        for d in direcciones:
            ni, nj = i + d[0], j + d[1]
            if not _valido(ni, nj) or not _libre(ni, nj) or (ni, nj) in cerrada:
                continue
            if _destino(ni, nj):
                detalles[ni][nj].padre_i = i
                detalles[ni][nj].padre_j = j
                path = []
                r2, c2 = ni, nj
                while not (detalles[r2][c2].padre_i == r2 and detalles[r2][c2].padre_j == c2):
                    path.append((r2, c2))
                    tr, tc = detalles[r2][c2].padre_i, detalles[r2][c2].padre_j
                    r2, c2 = tr, tc
                path.append((r2, c2))
                path.reverse()
                return path, exploradas

            costo = 1.414 if abs(d[0]) + abs(d[1]) == 2 else 1.0
            g_new = detalles[i][j].G + costo
            f_new = g_new + _h(ni, nj)
            if detalles[ni][nj].f == float('inf') or detalles[ni][nj].f > f_new:
                detalles[ni][nj].f     = f_new
                detalles[ni][nj].G     = g_new
                detalles[ni][nj].padre_i = i
                detalles[ni][nj].padre_j = j
                heapq.heappush(lista_abierta, (f_new, detalles[ni][nj]))

    return None, exploradas


def circuito_default(rows, cols):
    # Genera un circuito de carreras con obstaculos predefinidos
    grid = np.ones((rows, cols), dtype=int)
    grid[0, :]      = 0
    grid[rows-1, :] = 0
    grid[:, 0]      = 0
    grid[:, cols-1] = 0
    
    mid_r, mid_c = rows // 2, cols // 2
    
    # Isla central
    for r in range(mid_r - 2, mid_r + 3):
        for c in range(mid_c - 3, mid_c + 4):
            if 0 < r < rows-1 and 0 < c < cols-1:
                grid[r][c] = 0
                
    # Chicanes
    for r in range(2, rows // 3):
        grid[r][cols // 4]     = 0
        grid[r][cols // 4 + 1] = 0
    for r in range(rows * 2 // 3, rows - 2):
        grid[r][cols * 3 // 4]     = 0
        grid[r][cols * 3 // 4 - 1] = 0
        
    # Curvas cerradas
    for c in range(2, cols // 3):
        grid[rows // 4][c] = 0
    for c in range(cols * 2 // 3, cols - 2):
        grid[rows * 3 // 4][c] = 0
        
    # --- NUEVA OBSTRUCCIÓN ESPECÍFICA ---
    grid[3, 6] = 0  # Fila 3, Columna 6 bloqueada
    
    # Asegurar inicio y fin libres
    sr, sc = rows // 2, 2
    gr, gc = rows // 2, cols - 3
    grid[sr][sc] = 1
    grid[gr][gc] = 1
    
    return grid, (sr, sc), (gr, gc)

#Genera la figura matplotlib del circuito con la ruta calculada.
def dibujar_circuito(grid, start, goal, path=None, exploradas=None):
    grid = np.array(grid, dtype=float)
    R, C = grid.shape

    # Construir imagen RGB celda por celda
    img = np.zeros((R, C, 3))
    for r in range(R):
        for c in range(C):
            img[r, c] = [0.05, 0.30, 0.08] if grid[r][c] == 0 else [0.12, 0.16, 0.22]

    if exploradas:
        for (r, c) in exploradas:
            if (r, c) != tuple(start) and (r, c) != tuple(goal):
                img[r, c] = [0.10, 0.25, 0.40]

    if path:
        for (r, c) in path:
            if (r, c) != tuple(start) and (r, c) != tuple(goal):
                img[r, c] = [0.96, 0.77, 0.26]

    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('#080c12')
    ax.set_facecolor('#080c12')
    ax.imshow(img, aspect='equal', interpolation='nearest')

    # Cuadricula sutil
    for r in range(R + 1):
        ax.axhline(r - 0.5, color='#ffffff08', linewidth=0.4)
    for c in range(C + 1):
        ax.axvline(c - 0.5, color='#ffffff08', linewidth=0.4)

    # Linea de ruta con halo
    if path and len(path) > 1:
        pr, pc = zip(*path)
        ax.plot(pc, pr, color='#f5c542', linewidth=2.5, alpha=0.6,
                path_effects=[pe.Stroke(linewidth=5, foreground='#f5c54230'), pe.Normal()])

    # Moto vectorial en el inicio (patches, evita problemas con emojis en matplotlib)
    sr, sc = start
    z = 12  # zorder base

    # Rueda trasera
    ax.add_patch(plt.Circle((sc - 0.28, sr + 0.28), 0.22, color='#cccccc', zorder=z))
    ax.add_patch(plt.Circle((sc - 0.28, sr + 0.28), 0.10, color='#444444', zorder=z+1))
    # Rueda delantera
    ax.add_patch(plt.Circle((sc + 0.28, sr + 0.28), 0.20, color='#cccccc', zorder=z))
    ax.add_patch(plt.Circle((sc + 0.28, sr + 0.28), 0.09, color='#444444', zorder=z+1))
    # Chasis
    ax.add_patch(mpatches.FancyBboxPatch(
        (sc - 0.28, sr - 0.18), 0.56, 0.28,
        boxstyle="round,pad=0.04",
        facecolor='#e8a200', edgecolor='#f5c542', linewidth=1.2, zorder=z+1
    ))
    # Manillar
    ax.plot([sc + 0.18, sc + 0.38], [sr - 0.18, sr - 0.30],
            color='#aaaaaa', linewidth=2, zorder=z+2)
    # Carenado superior (asiento)
    ax.add_patch(mpatches.FancyBboxPatch(
        (sc - 0.22, sr - 0.30), 0.30, 0.14,
        boxstyle="round,pad=0.03",
        facecolor='#cc3300', edgecolor='none', zorder=z+2
    ))
    # Piloto: cabeza y casco
    ax.add_patch(plt.Circle((sc + 0.05, sr - 0.42), 0.11, color='#ffcc88', zorder=z+3))
    ax.add_patch(mpatches.Arc(
        (sc + 0.05, sr - 0.42), 0.24, 0.22,
        angle=0, theta1=0, theta2=180,
        color='#cc3300', linewidth=4, zorder=z+4
    ))
    # Halo verde
    ax.add_patch(plt.Circle((sc, sr), 0.7, color='#00e5a0', fill=False,
                             linewidth=2.5, alpha=0.9, zorder=z+5))
    ax.text(sc, sr - 1.2, 'START', fontsize=7, color='#00e5a0',
            ha='center', va='center', fontfamily='monospace', fontweight='bold')

    # Bandera a cuadros en la meta
    gr2, gc2 = goal
    flag_size   = 0.45
    colors_flag = ['white', 'black']
    for fi in range(4):
        for fj in range(4):
            rect = mpatches.FancyBboxPatch(
                (gc2 - 0.9 + fj * flag_size, gr2 - 0.9 + fi * flag_size),
                flag_size, flag_size,
                boxstyle="square,pad=0",
                facecolor=colors_flag[(fi + fj) % 2],
                edgecolor='none', alpha=0.95, zorder=5
            )
            ax.add_patch(rect)
    ax.add_patch(plt.Circle((gc2, gr2), 0.7, color='#ff6b6b', fill=False,
                             linewidth=2.5, alpha=0.9))
    ax.text(gc2, gr2 + 1.3, 'FINISH', fontsize=7, color='#ff6b6b',
            ha='center', va='center', fontfamily='monospace', fontweight='bold')

    ax.set_xlim(-0.5, C - 0.5)
    ax.set_ylim(R - 0.5, -0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor('#f5c54230')
        spine.set_linewidth(1.5)
    ax.set_title('CIRCUITOS DE CARRERAS  —  RUTA A* DE ADRIÁN PAVÓN ', color='#f5c542',
                 fontsize=14, fontfamily='monospace', fontweight='bold', pad=16)
    plt.tight_layout()
    return fig


# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="A* CIRCUITO DE CARRERAS",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
/* Importación de fuentes */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@400;600&display=swap');

/* Fondo y textos generales */
html, body, [class*="css"], .stApp { 
    background-color: #000000 !important; 
    color: #e0e0e0; 
}

/* Hacemos el header transparente (sigue visible, pero sin molestar) */
header[data-testid="stHeader"] {
    background-color: transparent !important;
    border-bottom: none !important;
    box-shadow: none !important;
}

/* OCULTAR DEPLOY, MENÚ Y FOOTER */
.stDeployButton { display: none !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* Botón de expandir sidebar (el círculo verde) */
button[data-testid="stSidebarExpandButton"] {
    visibility: visible !important;
    background-color: #7CFC00 !important;
    box-shadow: 0 0 15px #7CFC00 !important;
}

/* TÍTULOS */
.title-main {
    font-family: 'Orbitron', sans-serif; 
    font-size: 2.8rem; font-weight: 900;
    background: linear-gradient(90deg, #fff 30%, #f5c542);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center; margin: 0;
}
.title-sub {
    font-family: 'Rajdhani', sans-serif; color: #f5c542;
    font-size: 1rem; letter-spacing: 6px; text-transform: uppercase;
    text-align: center;
}

/* TARJETAS DE INFORMACIÓN (CUADROS AMARILLOS) */
.stat-card {
    background-color: #f5c542;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(245, 197, 66, 0.3);
    border: 1px solid #e8a200;
}
.stat-value {
    font-family: 'Orbitron', sans-serif;
    color: #000000 !important;
    font-size: 1.8rem;
    font-weight: 900;
}
.stat-label {
    font-family: 'Rajdhani', sans-serif;
    color: #333333 !important;
    font-size: 0.9rem;
    font-weight: 700;
    text-transform: uppercase;
    margin-top: 5px;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #0a0a0a !important;
    border-right: 1px solid rgba(124, 252, 0, 0.2);
}
section[data-testid="stSidebar"] * { 
    color: #7CFC00 !important; 
}

/* Botones Dorados */
.stButton > button {
    font-family: 'Orbitron', sans-serif !important; 
    background: linear-gradient(135deg, #f5c542, #e8a200);
    color: #080c12; border: none; font-weight: bold;
}

/* Mensajes de éxito/error */
.success-box {
    padding: 10px; background-color: rgba(0, 229, 160, 0.2);
    border: 1px solid #00e5a0; color: #00e5a0;
    text-align: center; font-family: 'Orbitron', sans-serif; border-radius: 5px;
}
</style> """, unsafe_allow_html=True)

st.markdown("""
<div class="title-container">
    <p class="title-main">A* RACING - ADRIÁN PAVÓN </p>
    <p class="title-sub">PLAN DE RUTAS· CIRCUITO DE CARRERAS DE ADRIÁN PAVÓN</p>
</div>
""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Sidebar de configuracion

with st.sidebar:
    st.markdown("## CONFIGURACION")
    st.markdown("---")
    rows = st.slider("Filas del circuito", 8, 20, 12)
    cols = st.slider("Columnas del circuito", 10, 28, 18)
    st.markdown("---")
    st.markdown("### POSICION INICIO")
    start_row = st.number_input("Fila",    0, rows - 1, rows // 2, key="sr")
    start_col = st.number_input("Columna", 0, cols - 1, 2,         key="sc")
    st.markdown("### POSICION META")
    goal_row  = st.number_input("Fila",    0, rows - 1, rows // 2, key="gr")
    goal_col  = st.number_input("Columna", 0, cols - 1, cols - 3,  key="gc")
    st.markdown("---")
    usar_circuito = st.checkbox("Usar circuito predeterminado", value=True)
    st.markdown("---")
    st.markdown("""
    <div style='font-family:monospace; font-size:0.7rem; color:#00BFBF; line-height:1.9'>
    Pista libre    — azul oscuro<br>
    Muro / barrera — negro<br>
    Celdas exploradas — azul<br>
    Ruta optima    — dorado<br>
    Posicion inicio — verde (moto)<br>
    Linea de meta  — rojo (bandera)
    </div>
    """, unsafe_allow_html=True)
# Estado del grid
if usar_circuito:
    current_grid, _, _ = circuito_default(rows, cols)
else:
    if "grid" not in st.session_state or st.session_state.grid.shape != (rows, cols):
        st.session_state.grid = np.ones((rows, cols), dtype=int)
    current_grid = st.session_state.grid

start_pos = (start_row, start_col)
goal_pos  = (goal_row,  goal_col)

# Layout principal: mapa a la izquierda, controles a la derecha
col_map, col_ctrl = st.columns([3, 1])

with col_ctrl:
    st.markdown("### CONTROLES")
    ejecutar = st.button("EJECUTAR A*")
    limpiar  = st.button("LIMPIAR RUTA")
    st.markdown("---")
    
    if not usar_circuito:
        st.markdown("### EDITAR MAPA")
        st.caption("Desmarcado = LIBRE (1) | Marcado = MURO (0)")
        
        # 1. INVERSIÓN AL ENTRAR: 
        # Si el grid original tiene un 0 (muro), lo convertimos a True (marcado)
        df_para_editar = (st.session_state.grid == 0)
        
        grid_edit = st.data_editor(
            df_para_editar,
            column_config={
                str(i): st.column_config.CheckboxColumn(width="small") 
                for i in range(cols)
            },
            use_container_width=True,
            key="mi_editor_grid_invertido"
        )
        
        # 2. INVERSIÓN AL SALIR:
        # Si el usuario marca la casilla (True), guardamos un 0 (muro).
        # Si la deja vacía (False), guardamos un 1 (libre).
        st.session_state.grid = np.where(np.array(grid_edit), 0, 1)
        current_grid = st.session_state.grid

# Inicializar session state
if "path" not in st.session_state:
    st.session_state.path       = None
    st.session_state.exploradas = []
    st.session_state.stats      = None
    st.session_state.ejecutado  = False

if limpiar:
    st.session_state.path       = None
    st.session_state.exploradas = []
    st.session_state.stats      = None
    st.session_state.ejecutado  = False

if ejecutar:
    t0 = time.perf_counter()
    path, exploradas = busqueda_a_estrella_ui(current_grid, start_pos, goal_pos)
    t1 = time.perf_counter()
    st.session_state.path       = path
    st.session_state.exploradas = exploradas
    st.session_state.ejecutado  = True
    if path:
        dist = sum(
            1.414 if abs(path[k][0] - path[k-1][0]) + abs(path[k][1] - path[k-1][1]) == 2 else 1.0
            for k in range(1, len(path))
        )
        st.session_state.stats = {
            "nodos":      len(path),
            "dist":       round(dist, 2),
            "exploradas": len(exploradas),
            "tiempo":     round((t1 - t0) * 1000, 3)
        }
    else:
        st.session_state.stats = None

# Dibuja el circuito
with col_map:
    fig = dibujar_circuito(
        current_grid, start_pos, goal_pos,
        st.session_state.path,
        st.session_state.exploradas
    )
    st.pyplot(fig)
    plt.close(fig)

# Mensaje de resultado
if st.session_state.path:
    st.markdown('<div class="success-box">RUTA OPTIMA ENCONTRADA — LA MOTO LLEGA A META</div>',
                unsafe_allow_html=True)
elif st.session_state.get("ejecutado") and not st.session_state.path:
    st.markdown('<div class="error-box">SIN RUTA VALIDA — CIRCUITO BLOQUEADO</div>',
                unsafe_allow_html=True)

# Tarjetas de estadisticas
if st.session_state.stats:
    s = st.session_state.stats
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl in [
        (c1, s["nodos"],           "NODOS EN RUTA"),
        (c2, s["dist"],            "DISTANCIA TOTAL"),
        (c3, s["exploradas"],      "CELDAS VISITADAS"),
        (c4, f"{s['tiempo']} ms",  "TIEMPO CALCULO"),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{val}</div>
                <div class="stat-label">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)