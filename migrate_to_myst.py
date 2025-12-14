import json
import os
import re

# --- CONFIGURACIÓN ---
INPUT_DIR = "json_capitulos"
OUTPUT_DIR = "docs"
# ---------------------

def clean_markdown_content(markdown_text):
    """
    Realiza limpieza final: corrige saltos de línea y asegura el formato de ecuaciones.
    """
    if not markdown_text:
        return ""

    # 1. Asegurar saltos de línea de Markdown (doble salto para párrafo)
    # Streamlit usa \n, pero Sphinx/MyST prefiere párrafos separados por líneas en blanco.
    # Reemplazamos todos los \n (salto de línea JSON) que no estén precedidos por otro \n con doble salto.
    # Sin embargo, evitamos romper el formato interno de tablas y listas.

    # Reemplazar \\n (JSON escaped newline) por \n
    content = markdown_text.replace('\\n', '\n')

    # 2. Limpieza de comandos Latex incompletos que pudieran quedar
    content = content.replace('textm', r'\text{m}')
    content = content.replace('textcm', r'\text{cm}')

    # 3. Eliminar caracteres que Python o JSON pueden haber insertado
    content = content.replace('$$$$', '$$')
    content = content.replace('\\cdot', ' \cdot ')

    # 4. Asegurar que las ecuaciones de una línea ($$ecuación$$) no tengan líneas en blanco extra dentro
    # Esto es complejo, pero simplificamos eliminando saltos de línea alrededor de $$ si no son parte de un bloque

    return content.strip()

def process_chapter(file_path):
    """Procesa un archivo JSON de capítulo y lo convierte a formato MyST."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error de sintaxis JSON en {file_path}: {e}")
        return None

    capitulo_id = data.get('capitulo_id', 'XX')
    titulo = data.get('titulo', 'Título sin nombre')

    # Cabecera MyST del archivo
    myst_content = f"({'capitulo_'}{capitulo_id})=\n"  # Etiqueta MyST para referencias
    myst_content += f"# {titulo}\n\n"
    myst_content += f"*Parte: {data.get('parte', 'General')}*\n"
    myst_content += f"*Fecha: {data.get('fecha_generacion', 'Desconocida')}*\n\n"

    for section in data.get('secciones', []):
        section_type = section.get('tipo', 'teoria')
        section_title = section.get('titulo', 'Sección sin título')

        # Título de la sección (Subtítulo h2 o h3)
        myst_content += f"## {section_title}\n\n"

        if section_type == 'teoria':
            markdown = section.get('contenido_markdown', '')
            myst_content += clean_markdown_content(markdown) + "\n\n"

        elif section_type == 'ejercicios':
            for i, ejercicio in enumerate(section.get('ejercicios', [])):
                enunciado = ejercicio.get('enunciado_markdown', f"Problema {i+1} sin enunciado.")
                solucion = ejercicio.get('solucion_markdown', 'Solución no disponible.')

                # Título del ejercicio
                myst_content += f"### Problema {i + 1}: {enunciado.splitlines()[0]}\n\n"

                # Enunciado (el resto del texto)
                myst_content += clean_markdown_content(enunciado) + "\n\n"

                # Solución oculta usando una directiva MyST (Sphinx) para expandir
                # Esto es ideal para una guía interactiva/wiki
                myst_content += ".. dropdown:: Mostrar Solución\n\n"
                # Añadir sangría de 3 espacios a la solución para que funcione dentro de dropdown
                solution_lines = clean_markdown_content(solucion).split('\n')
                indented_solution = '\n'.join('   ' + line for line in solution_lines)

                myst_content += indented_solution + "\n\n"

    return myst_content

def migrate():
    """Función principal para orquestar la migración."""
    if not os.path.exists(INPUT_DIR):
        print(f"❌ ERROR: El directorio '{INPUT_DIR}' no existe. Asegúrese de que los JSONs están ahí.")
        return

    # Crear el directorio de salida si no existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Leer todos los archivos JSON de capítulo
    json_files = sorted([f for f in os.listdir(INPUT_DIR) if f.startswith('capitulo_') and f.endswith('.json')])

    print(f"🔎 Encontrados {len(json_files)} capítulos JSON para migrar.")

    toc_entries = []

    for filename in json_files:
        file_path = os.path.join(INPUT_DIR, filename)

        # Procesar el capítulo y obtener el contenido MyST
        myst_content = process_chapter(file_path)

        if myst_content:
            # Nombrar el archivo de salida con el mismo nombre base (.myst)
            output_filename = filename.replace('.json', '.myst')
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(myst_content)

            print(f"✅ Migrado {filename} a {output_filename}")

            # Preparar la tabla de contenido (toctree)
            toc_entries.append(output_filename.replace('.myst', ''))

    # Crear el archivo principal (index.myst) con el índice de la guía
    create_index_file(toc_entries)

    print("\n--- ¡MIGRACIÓN COMPLETADA! ---")
    print(f"Los archivos .myst están en el directorio '{OUTPUT_DIR}'.")
    print("El siguiente paso es configurar Sphinx y construir la documentación.")

def create_index_file(toc_entries):
    """Crea el archivo principal index.myst con la tabla de contenido."""
    index_content = "# Guía Completa de Física y Matemáticas\n\n"
    index_content += "Esta es una guía completa de conceptos y ejercicios resueltos de Física.\n\n"
    index_content += ".. toctree::\n"
    index_content += "   :maxdepth: 2\n"
    index_content += "   :caption: Capítulos\n\n"

    # Agregar las entradas de los capítulos
    for entry in toc_entries:
        index_content += f"   {entry}\n"

    index_path = os.path.join(OUTPUT_DIR, "index.myst")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)

    print(f"✅ Creado el índice (index.myst) para la tabla de contenido.")


if __name__ == "__main__":
    migrate()
