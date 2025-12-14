import json
import os
import re

def clean_and_load_json(file_path, content):
    """Intenta limpiar caracteres de control JSON inválidos y recarga."""
    print("   ⚠️ Intentando limpieza automática de caracteres de control...")
    # Eliminar cualquier carácter de control no válido en JSON (excepto \n, \r, \t)
    cleaned_content = re.sub(r'[\x00-\x1f]', '', content)

    try:
        data = json.loads(cleaned_content)

        # Sobrescribir el archivo original con el contenido limpio
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"   ✅ ¡{os.path.basename(file_path)} limpiado y guardado correctamente!")
        return True
    except json.JSONDecodeError:
        print("   ❌ Fallo la limpieza automática. El error es más complejo.")
        return False
    except Exception as e:
        print(f"   ❌ Fallo la limpieza automática por error desconocido: {e}")
        return False


def check_file(filename):
    file_path = os.path.join('json_capitulos', filename)
    print(f"\n--- Comprobando {filename} ---")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            data = json.loads(content)

        print(f"✅ ¡{filename} es un archivo JSON válido!")
        return True

    except FileNotFoundError:
        print(f"❌ Error: Archivo no encontrado en la ruta esperada: {file_path}")
        return False

    except json.JSONDecodeError as e:
        print(f"❌ ERROR CRÍTICO de sintaxis JSON en {filename}:")
        print(f"  Mensaje: {e.msg}")

        if e.lineno > 0:
            lines = content.split('\n')
            if e.lineno <= len(lines):
                 error_line = lines[e.lineno - 1]
                 print(f"  Línea {e.lineno}: {error_line.strip()}")
                 print("  " + " " * (e.colno - 1) + "^")

        # Llamar a la función de limpieza solo si detectamos un error JSON
        if clean_and_load_json(file_path, content):
            return True # Retorna verdadero si la limpieza tuvo éxito
        else:
            return False # Si la limpieza falló, retorna falso

    except Exception as e:
        print(f"❌ ERROR desconocido: {e}")
        return False

if __name__ == "__main__":
    if not os.path.isdir('json_capitulos'):
        print("El directorio 'json_capitulos' no existe. Deteniendo.")
    else:
        # Nota: El 20 ya está limpio, lo comprobaremos de nuevo
        check_file('capitulo_20.json')
        check_file('capitulo_22.json')
