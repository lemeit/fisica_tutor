import os
import re
import json

BASE_PATH = "json_capitulos"

def fix_latex_delimiters_in_string(content):
    """
    Versión para limpiar y envolver unidades, y asegurar el doble escape.
    """

    # 1. Limpieza de residuos comunes de errores de corrección (como 'text' suelto)
    content = content.replace('\\text{m}', '$$\\text{m}$$')
    content = content.replace('text{m}', '$$\\text{m}$$')

    # 2. Asegurar que las ecuaciones grandes (frac, Delta, color) sigan envueltas
    # Usa la versión robusta que funcionó antes
    latex_commands = ['frac', 'Delta', 'sum', 'int', 'sqrt', 'text', 'color']
    pattern = r'([^$])(\\\\(?:' + '|'.join(latex_commands) + r')\s*\\{.*?)\\}'
    content = re.sub(r'([^$])(\\\\(?:frac|Delta|sum|int|sqrt|text|color).*?)', r'\1$$\2$$', content, flags=re.IGNORECASE)

    # 3. Limpiar cualquier resto de 'tex' suelto que no pertenezca a un comando
    # Esto busca "tex" que no está escapado, asumiendo que es basura de una corrección fallida
    # Lo reemplazaremos por el correcto \text{unidad} dentro de $$
    content = re.sub(r'\\tex(m|kg|s|A|K|mol|cd)', r'\\text{\1}', content, flags=re.IGNORECASE) # Arregla \text{m}
    content = re.sub(r'tex(m|kg|s|A|K|mol|cd)', r'\\text{\1}', content, flags=re.IGNORECASE) # Arregla texm

    # 4. Envolver unidades comunes que se quedaron fuera del paso 2 (solo si parecen estar en una tabla o párrafo)
    # Buscamos unidades SI comunes que no estén envueltas en $$ y las envolvemos en \text{unit} y $$
    units_to_wrap = ['m', 'kg', 's', 'A', 'K', 'mol', 'cd', 'cm', 'N', 'J', 'W', 'Hz', 'V', 'C']
    for unit in units_to_wrap:
        # Busca la unidad que no esté precedida por $ o \ (para no tocar comandos existentes)
        # Esto es muy peligroso, lo usaremos solo para el caso exacto de la tabla de SI
        if 'Unidades SI' in content:
            content = content.replace(f'| {unit}', f'| $${unit}$$')

    # 5. Limpiar posibles dobles $$ y restos de saltos de línea \\n/\\r
    content = content.replace('$$$$', '$$')
    content = content.replace('$$$$$$', '$$')
    content = content.replace('\\\\n', '\n')
    content = content.replace('\\\\r', '\r')

    return content

# El resto del script sigue siendo el mismo (process_file_for_latex_fix y __main__)

def process_file_for_latex_fix(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        modified = False

        for section in data.get('secciones', []):
            if 'contenido_markdown' in section:
                original_content = section['contenido_markdown']
                new_content = fix_latex_delimiters_in_string(original_content)
                if original_content != new_content:
                    section['contenido_markdown'] = new_content
                    modified = True

            if section.get('tipo') == 'ejercicios':
                for ejercicio in section.get('ejercicios', []):
                    original_solucion = ejercicio['solucion_markdown']
                    new_solucion = fix_latex_delimiters_in_string(original_solucion)
                    if original_solucion != new_solucion:
                        ejercicio['solucion_markdown'] = new_solucion
                        modified = True

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return f"✅ Archivo '{os.path.basename(file_path)}' corregido."
        else:
            return f"☑️ Archivo '{os.path.basename(file_path)}' sin cambios."

    except json.JSONDecodeError:
        return f"❌ ERROR: '{os.path.basename(file_path)}' tiene un error de sintaxis JSON. ¡Corrija esto ANTES de ejecutar el script!"
    except Exception as e:
        return f"❌ ERROR al procesar '{os.path.basename(file_path)}': {e}"

if __name__ == "__main__":
    print("--- ⚙️ Iniciando Corrector Automático de LaTeX en JSON (Versión Unidades) ---")

    if not os.path.exists(BASE_PATH):
        print(f"❌ ERROR: El directorio '{BASE_PATH}' no fue encontrado.")
    else:
        file_list = sorted([f for f in os.listdir(BASE_PATH) if f.endswith('.json')])

        if not file_list:
            print(f"⚠️ Advertencia: No se encontraron archivos JSON en '{BASE_PATH}'.")
        else:
            print(f"🔎 Se encontraron {len(file_list)} archivos. Iniciando corrección...")
            for filename in file_list:
                file_path = os.path.join(BASE_PATH, filename)
                result = process_file_for_latex_fix(file_path)
                print(result)
            print("--- Proceso completado. Reinicie Streamlit. ---")
