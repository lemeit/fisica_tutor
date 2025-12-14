import fileinput
import sys

SINTAXIS_ROTA = {
    # Error 1: Vector con componentes (falta el vector, subíndices y delimitadores)
    'V = (V ,V ,V ),': r'$\vec{V} = (V_x, V_y, V_z)$',
    # Error 2: Módulo o Intensidad (falta raíz cuadrada, superíndices, y delimitadores de bloque)
    'V = V2 +V2. | | x y q': r'$$V = \sqrt{V^2_x + V^2_y}$$',
    # Error 3: Suma de Vectores (falta el vector, subíndices, y delimitadores de bloque)
    'V +V = (V +V ,V +V +,V +V ),': r'$$\vec{V}_1 + \vec{V}_2 = (V_{1x} + V_{2x}, V_{1y} + V_{2y}, V_{1z} + V_{2z})$$'
}

archivo_a_corregir = 'docs/clase_01_vectores.myst'

try:
    # Abre el archivo para reemplazar el contenido 'in place' (directamente)
    with fileinput.FileInput(archivo_a_corregir, inplace=True, encoding='utf-8') as archivo:
        for linea in archivo:
            linea_corregida = linea
            for rota, correcta in SINTAXIS_ROTA.items():
                linea_corregida = linea_corregida.replace(rota, correcta)

            sys.stdout.write(linea_corregida) # Escribe la línea corregida

    print(f"✅ ¡Éxito! Sintaxis corregida en: {archivo_a_corregir}")
except FileNotFoundError:
    print(f"❌ Error: Archivo {archivo_a_corregir} no encontrado. Mueva el archivo o corrija la ruta.")
