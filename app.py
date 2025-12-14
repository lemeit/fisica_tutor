import streamlit as st
import json
import os

# --- 1. CONFIGURACIÓN DE PÁGINA (Tema Moderno y Ancho Completo) ---
st.set_page_config(
    page_title="Guía de Física: Serway & Jewett",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 2. CONSTANTES Y CONFIGURACIÓN DE ARCHIVOS ---
BASE_PATH = "json_capitulos"

# Estructura del libro Serway Vol. 1 para la navegación
CAPITULO_GRUPOS = {
    "📚 PARTE 1: Mecánica (Caps. 1-14)": list(range(1, 15)),
    "🌊 PARTE 2: Oscilaciones y Ondas Mecánicas (Caps. 15-18)": list(range(15, 19)),
    "🔥 PARTE 3: Termodinámica (Caps. 19-22)": list(range(19, 23))
}

# Diccionario de títulos para la barra lateral
TITULOS_CAPITULOS = {
    1: "Capítulo 1: Medición y Vectores", 2: "Capítulo 2: Movimiento en Una Dimensión",
    3: "Capítulo 3: Vectores y Movimiento en Dos Dimensiones", 4: "Capítulo 4: Dinámica: Leyes de Newton",
    5: "Capítulo 5: Aplicaciones de las Leyes de Newton", 6: "Capítulo 6: Trabajo y Energía Cinética",
    7: "Capítulo 7: Energía Potencial y Conservación", 8: "Capítulo 8: Momentum Lineal y Colisiones",
    9: "Capítulo 9: Rotación de Cuerpos Rígidos", 10: "Capítulo 10: Momento Angular",
    11: "Capítulo 11: Equilibrio Estático y Elasticidad", 12: "Capítulo 12: Gravitación Universal",
    13: "Capítulo 13: Mecánica de Fluidos", 14: "Capítulo 14: Movimiento Oscilatorio",
    15: "Capítulo 15: Movimiento Ondulatorio", 16: "Capítulo 16: Ondas Sonoras",
    17: "Capítulo 17: Sobreposición y Ondas Estacionarias", 18: "Capítulo 18: Temperatura, Calor y 1ra Ley",
    19: "Capítulo 19: Teoría Cinética de Gases", 20: "Capítulo 20: Máquinas Térmicas y 2da Ley",
    21: "Capítulo 21: Entropía", 22: "Capítulo 22: Tópicos de Termodinámica",
}

# Diccionario de Prompts/URLs de imágenes
IMAGENES_CAPITULOS = {
    5: {
        "url": "",
        "prompt": "Diagrama de cuerpo libre técnico de un bloque sobre un plano inclinado con fuerzas N, W, y f_k rotuladas."
    },
    13: {
        "url": "",
        "prompt": "Diagrama técnico de un tubo Venturi mostrando la Ecuación de Bernoulli: flujo de fluido más rápido en la sección estrecha (baja presión) y más lento en la sección ancha (alta presión)."
    },
    14: {
        "url": "",
        "prompt": "Gráfico de la posición vs tiempo para el Movimiento Armónico Simple (MAS) de un sistema masa-resorte, mostrando Amplitud (A), Periodo (T) y fase (phi)."
    },
}

# --- 3. FUNCIÓN DE CARGA DE DATOS ---
@st.cache_data
def load_chapter_data(chapter_id):
    """Carga y parsea el archivo JSON del capítulo especificado."""
    file_path = os.path.join(BASE_PATH, f"capitulo_{chapter_id:02d}.json")
    if not os.path.exists(file_path):
        return None, f"Archivo no encontrado: {file_path}"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data, None
    except json.JSONDecodeError as e:
        error_msg = f"Error de formato JSON en el Capítulo {chapter_id} (Posición: {e.pos}). Revise cuidadosamente las barras invertidas ('\\\\' para LaTeX)."
        return None, error_msg
    except Exception as e:
        return None, f"Error desconocido al cargar el capítulo {chapter_id}: {e}"

# --- Manejo del estado para la selección del capítulo (Inicialización) ---
if 'selected_chapter' not in st.session_state:
    st.session_state.selected_chapter = 1
if 'selected_part_key' not in st.session_state:
    # Determinar la clave de la parte inicial (Mecánica)
    st.session_state.selected_part_key = list(CAPITULO_GRUPOS.keys())[0]

# --- 4. BARRA LATERAL (NAVEGACIÓN MEJORADA) ---
st.sidebar.title("📚 Guía de Física Serway")
st.sidebar.markdown("---")

# 4.1. Selector de Parte del Libro (Selectbox)
part_keys = list(CAPITULO_GRUPOS.keys())

# Determinar el índice actual para la selección
try:
    current_part_index = part_keys.index(st.session_state.selected_part_key)
except ValueError:
    current_part_index = 0 # Default a la primera parte

selected_part_key = st.sidebar.selectbox(
    "Seleccionar **Parte del Libro**:",
    options=part_keys,
    index=current_part_index,
    key='part_selector'
)
st.session_state.selected_part_key = selected_part_key # Actualiza el estado

# 4.2. Obtener Capítulos de la Parte Seleccionada
current_chapter_ids = CAPITULO_GRUPOS[selected_part_key]
current_options = {id: TITULOS_CAPITULOS.get(id, f"Capítulo {id} (Título no disponible)") for id in current_chapter_ids}

# 4.3. Selector de Capítulo (Radio Button)
try:
    # Verifica si el capítulo seleccionado anteriormente pertenece a esta nueva parte
    default_index = current_chapter_ids.index(st.session_state.selected_chapter)
except ValueError:
    # Si no, selecciona el primer capítulo de esta nueva parte automáticamente
    st.session_state.selected_chapter = current_chapter_ids[0]
    default_index = 0

def chapter_radio_callback():
    st.session_state.selected_chapter = st.session_state.chapter_radio_key

st.sidebar.markdown("---")
st.sidebar.markdown("### Seleccionar Capítulo")

st.sidebar.radio(
    "Capítulos:",
    options=current_chapter_ids,
    format_func=lambda x: current_options[x],
    key='chapter_radio_key',
    index=default_index,
    on_change=chapter_radio_callback
)

capitulo_seleccionado = st.session_state.selected_chapter

st.sidebar.markdown("---")
st.sidebar.info("⚛️ Guía de Estudio Basada en Serway & Jewett, Volumen 1.")


# --- 5. ÁREA PRINCIPAL (RENDERIZADO DEL CONTENIDO) ---
if capitulo_seleccionado:
    data, error = load_chapter_data(capitulo_seleccionado)

    if error:
        st.error(error)
        st.warning("El archivo JSON del capítulo contiene un error de sintaxis. Por favor, asegúrese de que **todas** las ecuaciones de LaTeX estén delimitadas por `$$` y que las barras invertidas sean dobles (`\\\\`).")
    elif data:

        # 5.1. Título y Subtítulo (Diseño Solicitado)

        # Extraer el nombre de la parte (e.g., "PARTE 3: Termodinámica (Caps. 19-22)")
        part_key_display = selected_part_key.replace("📚 ", "").replace("🌊 ", "").replace("🔥 ", "")

        # Título Grande: Capítulo X: Título (Diseño solicitado)
        st.title(f"{data['titulo']}")

        # Subtítulo: Parte X: Nombre de la Parte
        st.subheader(f"{part_key_display}")

        st.markdown("---")

        # Implementación del Diseño Moderno con PESTAÑAS
        tab_teoria, tab_ejercicios = st.tabs(["📘 Teoría y Conceptos Clave", "🧠 Ejercicios Resueltos"])

        # --- Pestaña de Teoría ---
        with tab_teoria:
            if data['secciones'] and data['secciones'][0]['tipo'] == 'teoria':
                teoria = data['secciones'][0]
                st.header(teoria['titulo'])

                st.markdown(teoria['contenido_markdown'])

                img_data = IMAGENES_CAPITULOS.get(capitulo_seleccionado)

                if img_data:
                    st.markdown("### 🖼️ Diagrama Clave del Concepto")
                    if img_data['url']:
                        st.image(img_data['url'], caption=img_data['prompt'])
                    else:
                        st.warning("Diagrama Faltante: Integre esta imagen para mejor visualización.")
                        st.code(f"Prompt para generación de IA: {img_data['prompt']}", language='text')

            else:
                st.warning("Contenido de teoría no estructurado correctamente en el JSON.")

        # --- Pestaña de Ejercicios ---
        with tab_ejercicios:
            if len(data['secciones']) > 1 and data['secciones'][1]['tipo'] == 'ejercicios':
                ejercicios_seccion = data['secciones'][1]
                st.header(ejercicios_seccion['titulo'])
                ejercicios = ejercicios_seccion['ejercicios']

                for ejercicio in ejercicios:
                    with st.expander(f"**{ejercicio['enunciado']}**"):
                        st.markdown("---")
                        st.markdown("#### ✅ Solución Detallada")
                        st.markdown(ejercicio['solucion_markdown'])
                        st.markdown("---")

            else:
                st.info("Este capítulo no contiene ejercicios resueltos.")
