import subprocess
import argparse
import os

def pdf_to_html(input_pdf, output_html):
    command = ["pdf2htmlEX", input_pdf, output_html]
    try:
        subprocess.run(command, check=True)
        print(f"El archivo HTML se ha generado correctamente: {output_html}")
    except subprocess.CalledProcessError as e:
        print(f"Error al convertir el PDF a HTML: {e}")

def main():
    parser = argparse.ArgumentParser(description="Convertir PDF a HTML con formato.")
    parser.add_argument("input_pdf", help="Ruta del archivo PDF de entrada.")
    parser.add_argument(
        "output_html",
        nargs="?",
        help="Ruta del archivo HTML de salida (opcional). Si no se proporciona, se usa el nombre del archivo PDF con extensión .html."
    )

    args = parser.parse_args()

    # Si no se proporciona `output_html`, asignar el mismo nombre que `input_pdf` con extensión `.html`
    output_html = args.output_html or f"{os.path.splitext(args.input_pdf)[0]}.html"
    
    pdf_to_html(args.input_pdf, output_html)

if __name__ == "__main__":
    main()
