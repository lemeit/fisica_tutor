import pytesseract
from PIL import Image
import pdfplumber
import os
import io

# Rutas
PDF_SOURCE_DIR = "pdfs_fuente"
OUTPUT_DIR = "docs_limpios"
PDF_TO_PROCESS = "clase_01_vectores.pdf" # Solo para probar

# 1. Función de limpieza de errores de LaTeX más comunes
def clean_text(text):
    # Intentamos limpiar los caracteres obvios después del OCR
    text = text.replace('\n', ' ') # OCR suele meter muchos saltos de línea
    text = text.replace('cdot', '\cdot')
    text = text.replace('textm', '\text{m}')
    return text

def extract_and_structure_pdf_ocr():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    pdf_path = os.path.join(PDF_SOURCE_DIR, PDF_TO_PROCESS)

    if not os.path.exists(pdf_path):
        print(f"❌ ERROR: No se encontró el archivo PDF: {pdf_path}")
        return

    chapter_name = PDF_TO_PROCESS.replace(".pdf", "")
    output_file_path = os.path.join(OUTPUT_DIR, f"{chapter_name}_ocr.myst")

    full_text_ocr = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"   -> Procesando {len(pdf.pages)} páginas con OCR...")

            # Agregar el título
            full_text_ocr += f"# {chapter_name.replace('_', ' ').title()}\n\n"

            for page in pdf.pages:
                # Extraer la imagen de la página (esto requiere una librería PDF adicional si el PDFplumber falla)
                # Si esto falla, necesitamos otra librería como PyMuPDF, pero intentemos con Tesseract primero

                # Para Tesseract, el método más robusto es convertir el PDF a una imagen temporal
                # PERO: Simplificamos usando la conversión directa de Tesseract (pdf_to_text) si es un PDF limpio.
                # Si el PDF es un escaneo, esto es lo que funciona mejor:

                # Tesseract PDF a texto (usa OCR)
                page_text = pytesseract.image_to_string(pdf_path, lang='spa')

                # Si el texto se obtiene (significa que Tesseract procesó todo el archivo):
                if page_text:
                    full_text_ocr += clean_text(page_text)
                    break # Salimos del loop de páginas si Tesseract procesa el PDF completo de golpe

            if not full_text_ocr:
                print("❌ ERROR: Tesseract no pudo extraer el texto. El PDF está muy dañado o es solo imagen.")
                return

            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(full_text_ocr)

            print(f"   ✅ Texto (OCR) guardado en: {output_file_path}")

    except Exception as e:
        print(f"❌ Ocurrió un error (Tesseract): {e}")

# Ejecutar el proceso
extract_and_structure_pdf_ocr()
