# 🚀 Herramienta de PDF Multiplataforma con Tkinter y `pypdf`

Una aplicación de escritorio simple y fácil de usar para realizar operaciones básicas con archivos PDF, como unir, extraer páginas y comprimir. Desarrollada en Python con `tkinter` para la interfaz de usuario multiplataforma y `pypdf` para el procesamiento de PDF.

-----

## ✨ Características

  * **Unir PDFs:** Combina múltiples archivos PDF o rangos específicos de páginas de varios PDFs en un único documento.
  * **Extraer/Recortar Páginas:** Selecciona y guarda páginas específicas de un PDF en un nuevo archivo.
  * **Comprimir PDF (básico):** Intenta reducir el tamaño de un archivo PDF aplicando compresión interna (FlateDecode).
  * **Visualización de Páginas:** Muestra el número total de páginas para cada PDF seleccionado.
  * **Previsualización:** Abre el PDF seleccionado con la aplicación predeterminada de tu sistema operativo para una revisión rápida.
  * **Interfaz Gráfica Intuitiva:** Interfaz de usuario simple y clara construida con `tkinter`.
  * **Multiplataforma:** Compatible con Windows, macOS y Linux.

-----

## 🛠️ Setup (Configuración)

Sigue estos pasos para configurar y ejecutar la aplicación en tu sistema.

### Voraussetzungen (Requisitos)

Asegúrate de tener Python 3.x instalado en tu sistema. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).

### 📦 Instalación

1.  **Clona o descarga el repositorio:**
    Si usas Git:

    ```bash
    git clone <URL_DEL_REPOSITORIO> # Reemplaza con la URL de tu repositorio si lo tienes
    cd <nombre_de_tu_carpeta> # Por ejemplo, cd herramienta-pdf
    ```

    O simplemente descarga el archivo `pdf_tool_app.py` y colócalo en una carpeta de tu elección.

2.  **Crea un entorno virtual (recomendado):**
    Es una buena práctica crear un entorno virtual para gestionar las dependencias de tu proyecto.

    ```bash
    python -m venv venv
    ```

3.  **Activa el entorno virtual:**

      * **En Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
      * **En macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Instala las dependencias:**
    La aplicación requiere la librería `pypdf`. Instálala usando `pip`:

    ```bash
    pip install pypdf
    ```

    **¡Importante\!** Asegúrate de tener la **última versión de `pypdf`** (v3.0.0 o superior) para que la funcionalidad de compresión básica (`compress=True`) funcione correctamente y evite errores. Si ya lo tenías instalado, actualízalo:

    ```bash
    pip install --upgrade pypdf
    ```

-----

## 🚀 Uso

1.  **Ejecuta la aplicación:**
    Una vez que hayas completado el `Setup` y tengas activado tu entorno virtual (si lo creaste), puedes ejecutar la aplicación desde tu terminal:

    ```bash
    python pdf_tool_app.py
    ```

    (Asegúrate de que `pdf_tool_app.py` es el nombre de tu archivo principal).

2.  **Navega por la interfaz:**
    La ventana principal de la aplicación se dividirá en tres secciones principales:

      * **1. Unir PDFs:**

          * Haz clic en "Seleccionar PDFs para Unir" para elegir uno o más archivos.
          * La lista mostrará los archivos seleccionados con su número de páginas.
          * **Doble clic** en un archivo en la lista para previsualizarlo.
          * Especifica las páginas a unir de cada PDF (ej: `1-5, 8, 10-última` o `Todas`).
          * Haz clic en "Unir PDFs Seleccionados" y elige dónde guardar el nuevo PDF.

      * **2. Recortar/Extraer Páginas de PDF:**

          * Haz clic en "Seleccionar PDF para Recortar" para elegir el archivo fuente.
          * Usa "Previsualizar PDF" para abrirlo.
          * Especifica las páginas a extraer (ej: `1-5, 8, 10-última` o `Todas`).
          * Haz clic en "Extraer Páginas" y elige dónde guardar el PDF resultante.

      * **3. Comprimir PDF:**

          * Haz clic en "Seleccionar PDF para Comprimir" para elegir el archivo.
          * Usa "Previsualizar PDF" para abrirlo.
          * Haz clic en "Comprimir PDF" y elige dónde guardar la versión comprimida. La aplicación te informará sobre la reducción de tamaño.

-----

## ⚠️ Notas Importantes sobre la Compresión

La funcionalidad de compresión en esta herramienta es básica y utiliza las capacidades nativas de `pypdf` para optimizar los flujos internos del PDF.

  * **Compresión Ligera:** Solo aplica la compresión `FlateDecode` a objetos que no están ya comprimidos. Esto puede ayudar si el PDF original tiene muchos datos sin comprimir (texto, gráficos vectoriales simples).
  * **No Optimización de Imágenes:** Esta herramienta **no reduce la calidad o la resolución de las imágenes** incrustadas en el PDF. Si tu PDF es grande debido a imágenes de alta resolución, la reducción de tamaño será limitada.
  * **Para Mayor Compresión:** Para una compresión más agresiva (que incluya reescalado de imágenes, eliminación de fuentes no usadas, etc.), se recomienda el uso de herramientas externas y más potentes como **Ghostscript** (que deberías instalar por separado y ejecutar vía línea de comandos o integrarlo en tu script) o servicios de compresión de PDF online.

-----

## 👨‍💻 Contribuciones

Si deseas mejorar esta herramienta, ¡las contribuciones son bienvenidas\! Puedes abrir un *issue* para reportar errores o sugerir nuevas características, o enviar un *pull request* con tus cambios.

-----

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

-----