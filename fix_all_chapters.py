import fileinput
import sys
import glob
import os

# --- 1. CONFIGURACIÓN DE CORRECCIÓN ---
# **¡IMPORTANTE!** USTED DEBE COMPLETAR ESTE DICCIONARIO CON SUS ERRORES MÁS COMUNES.
SINTAXIS_ROTA = {
    # Su corrección de unidades, asegurando \mathrm{} (más robusto) y el signo $
    '1\\text{cm}': r'$1 \mathrm{cm}$',
    '10\\text{kg}': r'$10 \mathrm{kg}$',
    # 2. Correcciones de vectores (ejemplo)
    'V = (V ,V ,V ),': r'$\vec{V} = (V_x, V_y, V_z)$',
    # 3. Corregir cualquier instancia de solo un caracter \ que debería ser \\
    '\\frac{': r'$$\\frac{',
    '\\vec{': r'$$\\vec{',
    # AÑADIR AQUÍ TODOS LOS ERRORES (Clave: Rota, Valor: Correcta)
}

# --- 2. RUTAS Y LÓGICA DE PROCESAMIENTO ---
DIRECTORIOS_A_PROCESAR = ['docs/capitulos_guia', 'docs/clases_teoria']

def aplicar_correcciones(archivo_a_corregir):
    """Aplica las correcciones definidas en SINTAXIS_ROTA a un archivo."""
    corregido = False
    try:
        with fileinput.FileInput(archivo_a_corregir, inplace=True, encoding='utf-8') as archivo:
            for linea in archivo:
                linea_corregida = linea
                for rota, correcta in SINTAXIS_ROTA.items():
                    if rota in linea_corregida:
                        linea_corregida = linea_corregida.replace(rota, correcta)
                        corregido = True

                sys.stdout.write(linea_corregida)

        return "✅ Corregido" if corregido else "☑️ Sin cambios"

    except Exception as e:
        return f"❌ ERROR al procesar: {e}"

if __name__ == "__main__":
    print("--- ⚙️ Iniciando Corrección Masiva de LaTeX ---")

    for directorio in DIRECTORIOS_A_PROCESAR:
        patron_busqueda = os.path.join(directorio, '*.myst')
        archivos_a_procesar = glob.glob(patron_busqueda)

        if not archivos_a_procesar:
            print(f"⚠️ Advertencia: No se encontraron archivos en '{directorio}'.")
            continue

        print(f"\nProcesando {len(archivos_a_procesar)} archivos en: {directorio}")
        for archivo in archivos_a_procesar:
            nombre_archivo = os.path.basename(archivo)
            resultado = aplicar_correcciones(archivo)
            print(f"[{nombre_archivo:25}] {resultado}")

    print("--- Proceso completado. ---")
