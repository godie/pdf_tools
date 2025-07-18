from PyPDF2 import PdfReader, PdfWriter
import os
import argparse

def extraer_paginas_pdf_interactivo(ruta_pdf_entrada):
    """
    Extrae páginas específicas de un archivo PDF de forma interactiva.
    Permite al usuario seleccionar páginas individuales o rangos.

    Args:
        ruta_pdf_entrada (str): La ruta al archivo PDF de entrada.
    """
    if not os.path.exists(ruta_pdf_entrada):
        print(f"Error: El archivo de entrada '{ruta_pdf_entrada}' no existe.")
        return

    try:
        lector_pdf = PdfReader(ruta_pdf_entrada)
        num_paginas = len(lector_pdf.pages)

        print(f"\nEl PDF '{os.path.basename(ruta_pdf_entrada)}' tiene {num_paginas} página(s).")
        print("¿Qué página(s) deseas extraer?")
        print("Puedes especificar:")
        print("  - Una sola página (ej: 5)")
        print("  - Múltiples páginas separadas por comas (ej: 1,3,7)")
        print("  - Un rango de páginas (ej: 2-5)")
        print("  - Una combinación (ej: 1,3-5,8)")

        entrada_usuario = input("Introduce el/los número(s) de página(s): ")
        paginas_a_extraer = set() # Usamos un set para evitar duplicados y mantener el orden

        # Procesar la entrada del usuario
        partes = entrada_usuario.replace(" ", "").split(',')
        for parte in partes:
            if '-' in parte:
                try:
                    inicio, fin = map(int, parte.split('-'))
                    if inicio > fin:
                        print(f"Advertencia: El rango '{parte}' es inválido (inicio > fin). Se ignorará.")
                        continue
                    for i in range(inicio, fin + 1):
                        paginas_a_extraer.add(i)
                except ValueError:
                    print(f"Advertencia: Formato de rango inválido '{parte}'. Se ignorará.")
            else:
                try:
                    pagina = int(parte)
                    paginas_a_extraer.add(pagina)
                except ValueError:
                    print(f"Advertencia: Formato de página inválido '{parte}'. Se ignorará.")

        if not paginas_a_extraer:
            print("No se seleccionaron páginas válidas para extraer. Saliendo.")
            return

        # Filtrar páginas válidas y ordenarlas
        paginas_validas = sorted([p for p in paginas_a_extraer if 1 <= p <= num_paginas])

        if not paginas_validas:
            print("Ninguna de las páginas seleccionadas es válida o está dentro del rango del PDF. Saliendo.")
            return

        escritor_pdf = PdfWriter()
        for pagina_num in paginas_validas:
            # PyPDF2 usa indexación base 0, por lo que restamos 1 al número de hoja
            escritor_pdf.add_page(lector_pdf.pages[pagina_num - 1])

        # Construir el nombre del archivo de salida
        nombre_base, extension = os.path.splitext(os.path.basename(ruta_pdf_entrada))
        if len(paginas_validas) == 1:
            pdf_salida = f"{nombre_base}_pagina_{paginas_validas[0]}{extension}"
        else:
            # Si son múltiples páginas, podemos dar un nombre genérico o más descriptivo
            pdf_salida = f"{nombre_base}_paginas_extraidas{extension}"

        # Asegurarse de que el archivo de salida no sobrescriba uno existente sin preguntar
        contador = 1
        nombre_original_salida = pdf_salida
        while os.path.exists(pdf_salida):
            print(f"El archivo '{pdf_salida}' ya existe.")
            respuesta = input("¿Deseas sobrescribirlo? (s/n): ").lower()
            if respuesta == 's':
                break
            else:
                pdf_salida = f"{os.path.splitext(nombre_original_salida)[0]}_{contador}{extension}"
                contador += 1
                print(f"Intentando guardar como '{pdf_salida}'.")


        with open(pdf_salida, 'wb') as salida:
            escritor_pdf.write(salida)

        print(f"\nLas páginas {', '.join(map(str, paginas_validas))} han sido extraídas y guardadas en '{pdf_salida}'.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

# --- Ejemplo de uso ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrae hojas de tus PDFs.")
    parser.add_argument(
        "--pdf_file",
        type=str,
        default="my.pdf", # Valor por defecto
        help="Ruta al archivo pdf "
    )
    args = parser.parse_args()
    if not os.path.exists(args.pdf_file):
        print(f"Error: El archivo de trades '{args.pdf_file}' no se encontró. Por favor, verifica la ruta.")
        exit(1) # Salir del script con un código de error
    # Pide al usuario la ruta del archivo PDF
   
    extraer_paginas_pdf_interactivo(args.pdf_file)