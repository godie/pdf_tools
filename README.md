Here's the README and Setup in English:

-----

# 🚀 Cross-Platform PDF Tool with Tkinter and `pypdf`

A simple and easy-to-use desktop application for performing basic operations with PDF files, such as merging, extracting pages, and compressing. Developed in Python with `tkinter` for the cross-platform user interface and `pypdf` for PDF processing.

-----

## ✨ Features

  * **Merge PDFs:** Combine multiple PDF files or specific page ranges from several PDFs into a single document.
  * **Extract/Crop Pages:** Select and save specific pages from a PDF into a new file.
  * **Compress PDF (Basic):** Attempts to reduce the size of a PDF file by applying internal compression (FlateDecode).
  * **Page Count Display:** Shows the total number of pages for each selected PDF.
  * **Preview:** Opens the selected PDF with your operating system's default application for a quick review.
  * **Intuitive Graphical Interface:** Simple and clear user interface built with `tkinter`.
  * **Cross-Platform:** Compatible with Windows, macOS, and Linux.

-----

## 🛠️ Setup

Follow these steps to set up and run the application on your system.

### Prerequisites

Make sure you have Python 3.x installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### 📦 Installation

1.  **Clone or download the repository:**
    If you use Git:
  
    ```bash
    git clone https://github.com/godie/pdf_tools.git
    cd pdf_tools # For example, cd pdf-tool
    ```

    Or simply download the [pdf_tool.py](/pdf_tool.py) file and place it in a folder of your choice.

2.  **Create a virtual environment (recommended):**
    It's good practice to create a virtual environment to manage your project's dependencies.

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

      * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
      * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    The application requires the `pypdf` library. Install it using `pip`:

    ```bash
    pip install pypdf
    ```

    **Important\!** Make sure you have the **latest version of `pypdf`** (v3.0.0 or higher) for the basic compression functionality (`compress=True`) to work correctly and avoid errors. If you already have it installed, upgrade it:

    ```bash
    pip install --upgrade pypdf
    ```

-----

## 🚀 Usage

1.  **Run the application:**
    Once you have completed the `Setup` and activated your virtual environment (if you created one), you can run the application from your terminal:

    ```bash
    python pdf_tool_app.py
    ```

    (Make sure `pdf_tool_app.py` is the name of your main file).

2.  **Navigate the interface:**
    The main application window will be divided into three main sections:

      * **1. Merge PDFs:**

          * Click "Select PDFs to Merge" to choose one or more files.
          * The list will display the selected files with their page count.
          * **Double-click** on a file in the list to preview it.
          * Specify the pages to merge from EACH PDF (e.g., `1-5, 8, 10-last` or `All`).
          * Click "Merge Selected PDFs" and choose where to save the new PDF.

      * **2. Crop/Extract PDF Pages:**

          * Click "Select PDF to Crop" to choose the source file.
          * Use "Preview PDF" to open it.
          * Specify the pages to extract (e.g., `1-5, 8, 10-last` or `All`).
          * Click "Extract Pages" and choose where to save the resulting PDF.

      * **3. Compress PDF:**

          * Click "Select PDF to Compress" to choose the file.
          * Use "Preview PDF" to open it.
          * Click "Compress PDF" and choose where to save the compressed version. The application will inform you about the size reduction.

-----

## ⚠️ Important Notes on Compression

The compression functionality in this tool is basic and uses `pypdf`'s native capabilities to optimize internal PDF streams.

  * **Light Compression:** It only applies `FlateDecode` compression to objects that are not already compressed. This can help if the original PDF has a lot of uncompressed data (text, simple vector graphics).
  * **No Image Optimization:** This tool **does not reduce the quality or resolution of embedded images** in the PDF. If your PDF is large due to high-resolution images, the size reduction will be limited.
  * **For Greater Compression:** For more aggressive compression (including image resampling, removal of unused fonts, etc.), it is recommended to use external and more powerful tools like **Ghostscript** (which you would need to install separately and run via command line or integrate into your script) or online PDF compression services.

-----

## 👨‍💻 Contributions

If you wish to improve this tool, contributions are welcome\! You can open an *issue* to report bugs or suggest new features, or submit a *pull request* with your changes.

-----

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

-----