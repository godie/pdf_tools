import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter
import os
import sys # Para abrir archivos con la aplicación predeterminada

class PDFToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Herramienta de PDF")
        self.root.geometry("650x850") # Tamaño inicial de la ventana ajustado

        self.selected_merge_files = []
        self.selected_extract_file = None
        self.selected_compress_file = None

        self._create_widgets()

    def _create_widgets(self):
        # --- Sección Unir PDFs ---
        merge_frame = tk.LabelFrame(self.root, text="1. Unir PDFs", padx=10, pady=10)
        merge_frame.pack(padx=10, pady=5, fill="x")

        tk.Button(merge_frame, text="Seleccionar PDFs para Unir", command=self._select_merge_pdfs).pack(pady=5)

        # Listbox para mostrar archivos seleccionados y su número de páginas
        self.merge_files_listbox = tk.Listbox(merge_frame, height=6, selectmode=tk.MULTIPLE, relief=tk.SUNKEN, bd=2)
        self.merge_files_listbox.pack(fill="x", padx=5, pady=5)
        self.merge_files_listbox.bind("<Double-Button-1>", self._open_pdf_for_preview) # Abrir al doble click

        tk.Label(merge_frame, text="Páginas a unir de CADA PDF (Ej: 1-5, 8, 10-última). Escribe 'Todas' para todas las páginas:").pack(pady=(5,0))
        self.merge_pages_entry = tk.Entry(merge_frame, bd=2, relief=tk.GROOVE)
        self.merge_pages_entry.pack(fill="x", padx=5, pady=5)
        self.merge_pages_entry.insert(0, "Todas") # Valor por defecto

        tk.Button(merge_frame, text="Unir PDFs Seleccionados", command=self._merge_pdfs, bg="#4CAF50", fg="white").pack(pady=10)

        # --- Sección Recortar/Extraer Páginas de PDF ---
        extract_frame = tk.LabelFrame(self.root, text="2. Recortar/Extraer Páginas de PDF", padx=10, pady=10)
        extract_frame.pack(padx=10, pady=5, fill="x")

        tk.Button(extract_frame, text="Seleccionar PDF para Recortar", command=self._select_extract_pdf).pack(pady=5)

        self.extract_file_label = tk.Label(extract_frame, text="Archivo seleccionado: Ninguno", anchor="w")
        self.extract_file_label.pack(pady=5, fill="x")
        
        # Botón para previsualizar el PDF de extracción
        tk.Button(extract_frame, text="Previsualizar PDF", command=lambda: self._open_pdf_for_preview(self.selected_extract_file)).pack(pady=5)

        tk.Label(extract_frame, text="Páginas a extraer (Ej: 1-5, 8, 10-última). Escribe 'Todas' para todas las páginas:").pack(pady=(5,0))
        self.extract_pages_entry = tk.Entry(extract_frame, bd=2, relief=tk.GROOVE)
        self.extract_pages_entry.pack(fill="x", padx=5, pady=5)
        self.extract_pages_entry.insert(0, "Todas") # Valor por defecto

        tk.Button(extract_frame, text="Extraer Páginas", command=self._extract_pages, bg="#2196F3", fg="white").pack(pady=10)

        # --- Sección Comprimir PDF ---
        compress_frame = tk.LabelFrame(self.root, text="3. Comprimir PDF", padx=10, pady=10)
        compress_frame.pack(padx=10, pady=5, fill="x")

        tk.Button(compress_frame, text="Seleccionar PDF para Comprimir", command=self._select_compress_pdf).pack(pady=5)

        self.compress_file_label = tk.Label(compress_frame, text="Archivo seleccionado: Ninguno", anchor="w")
        self.compress_file_label.pack(pady=5, fill="x")
        
        # Botón para previsualizar el PDF de compresión
        tk.Button(compress_frame, text="Previsualizar PDF", command=lambda: self._open_pdf_for_preview(self.selected_compress_file)).pack(pady=5)

        tk.Button(compress_frame, text="Comprimir PDF", command=self._compress_pdf, bg="#FFC107", fg="black").pack(pady=10)

        # --- Barra de estado ---
        self.status_label = tk.Label(self.root, text="Listo", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 9))
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def _update_status(self, message):
        """Actualiza el mensaje en la barra de estado."""
        self.status_label.config(text=message)
        self.root.update_idletasks() # Forzar la actualización visual

    def _get_pdf_page_count(self, filepath):
        """Obtiene el número total de páginas de un PDF."""
        try:
            reader = PdfReader(filepath)
            return len(reader.pages)
        except Exception:
            return 0 # En caso de error, devuelve 0 páginas

    def _open_pdf_for_preview(self, filepath_or_event):
        """
        Abre el PDF seleccionado con la aplicación predeterminada del sistema.
        Puede recibir un filepath directamente o un objeto de evento de Tkinter (para listbox).
        """
        if isinstance(filepath_or_event, str):
            filepath = filepath_or_event
        else: # Es un evento del listbox
            selected_indices = self.merge_files_listbox.curselection()
            if not selected_indices:
                return
            # Obtener el filepath real del elemento seleccionado en el listbox
            # Asumimos que los elementos del listbox corresponden a self.selected_merge_files
            filepath = self.selected_merge_files[selected_indices[0]]

        if filepath and os.path.exists(filepath):
            try:
                if sys.platform == "win32":
                    os.startfile(filepath)
                elif sys.platform == "darwin": # macOS
                    os.system(f"open \"{filepath}\"")
                else: # Linux y otros Unix-like
                    os.system(f"xdg-open \"{filepath}\"")
                self._update_status(f"Abriendo '{os.path.basename(filepath)}' para previsualizar.")
            except Exception as e:
                messagebox.showerror("Error de Previsualización", f"No se pudo abrir el archivo para previsualizar: {e}")
                self._update_status(f"Error al abrir '{os.path.basename(filepath)}'.")
        else:
            self._update_status("No hay archivo seleccionado para previsualizar.")

    def _parse_page_ranges(self, page_string, total_pages):
        """
        Parsea una cadena de rangos de páginas (Ej: "1-5, 8, 10-última")
        y devuelve una lista ordenada de índices de página (0-indexados).
        Valida que las páginas estén dentro del rango del PDF.
        """
        pages = set()
        page_string = page_string.strip()

        if not page_string or page_string.lower() == "todas":
            return list(range(total_pages))

        parts = page_string.split(',')
        for part in parts:
            part = part.strip()
            if not part: # Ignorar partes vacías
                continue

            try:
                if '-' in part:
                    start_str, end_str = part.split('-')
                    start = int(start_str) - 1 # Convertir a 0-indexado
                    end = total_pages - 1 if end_str.lower() == 'última' else int(end_str) - 1

                    # Asegurar que los rangos son válidos y dentro de los límites
                    start = max(0, start)
                    end = min(total_pages - 1, end)

                    if start <= end:
                        pages.update(range(start, end + 1))
                else:
                    page = int(part) - 1 # Convertir a 0-indexado
                    if 0 <= page < total_pages: # Solo añadir si la página existe
                        pages.add(page)
            except ValueError:
                # Ignorar partes mal formadas o no numéricas
                continue
        return sorted(list(pages))

    def _select_merge_pdfs(self):
        """Abre un diálogo para seleccionar múltiples archivos PDF para unir y muestra su número de páginas."""
        files = filedialog.askopenfilenames(
            title="Seleccionar archivos PDF para unir",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
        )
        if files:
            self.selected_merge_files = list(files)
            self.merge_files_listbox.delete(0, tk.END)
            for f in self.selected_merge_files:
                page_count = self._get_pdf_page_count(f)
                self.merge_files_listbox.insert(tk.END, f"{os.path.basename(f)} ({page_count} páginas)")
            self._update_status(f"Seleccionados {len(files)} archivos para unir.")
        else:
            self._update_status("Selección de archivos de unión cancelada.")

    def _merge_pdfs(self):
        """Une los PDFs seleccionados en un único archivo, respetando los rangos de páginas."""
        if not self.selected_merge_files:
            messagebox.showwarning("Advertencia", "Por favor, selecciona al menos un archivo PDF para unir.")
            return

        output_filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar PDF unificado como"
        )
        if not output_filepath:
            self._update_status("Operación de unión cancelada.")
            return

        writer = PdfWriter()
        total_merged_pages = 0
        self._update_status("Uniendo PDFs...")

        pages_to_add_str = self.merge_pages_entry.get().strip()

        for filepath in self.selected_merge_files:
            try:
                reader = PdfReader(filepath)
                current_pdf_total_pages = len(reader.pages)
                
                pages_to_add_indices = self._parse_page_ranges(pages_to_add_str, current_pdf_total_pages)
                
                if not pages_to_add_indices and pages_to_add_str.lower() != "todas":
                    # Si el parseo no encontró páginas válidas y no se pidió "Todas", preguntar al usuario.
                    if messagebox.askyesno("Páginas no válidas", 
                                           f"Las páginas especificadas ('{pages_to_add_str}') para '{os.path.basename(filepath)}' son inválidas o no existen. ¿Deseas añadir todas las páginas de este archivo?"):
                        pages_to_add_indices = list(range(current_pdf_total_pages))
                    else:
                        self._update_status(f"Omitiendo '{os.path.basename(filepath)}' por páginas inválidas.")
                        continue # Omitir este archivo si el usuario no quiere añadir todas

                # Si aún no hay páginas a añadir (ej. PDF vacío o usuario no quiso añadir todas)
                if not pages_to_add_indices:
                    self._update_status(f"No se añadieron páginas de '{os.path.basename(filepath)}'.")
                    continue

                for page_num_0_indexed in pages_to_add_indices:
                    writer.add_page(reader.pages[page_num_0_indexed])
                    total_merged_pages += 1
            except Exception as file_e:
                messagebox.showerror("Error al procesar archivo", f"No se pudo procesar el archivo '{os.path.basename(filepath)}': {file_e}. Este archivo será omitido.")
                self._update_status(f"Error con '{os.path.basename(filepath)}'. Omitiendo.")
                continue # Continuar con el siguiente archivo

        if total_merged_pages == 0:
            messagebox.showwarning("Advertencia", "No se añadieron páginas de ningún PDF. Archivo de salida no creado.")
            self._update_status("Unión cancelada: No se añadieron páginas.")
            return

        try:
            with open(output_filepath, "wb") as f:
                writer.write(f)
            
            self._update_status(f"PDFs unidos exitosamente en '{os.path.basename(output_filepath)}' con {total_merged_pages} páginas.")
            messagebox.showinfo("Éxito", f"PDFs unidos y guardados como '{os.path.basename(output_filepath)}'.")
        except Exception as e:
            self._update_status(f"Error al guardar PDF unificado: {e}")
            messagebox.showerror("Error", f"Ocurrió un error al guardar el PDF unificado: {e}")


    def _select_extract_pdf(self):
        """Abre un diálogo para seleccionar un único archivo PDF para extraer páginas y muestra su número de páginas."""
        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo PDF para recortar",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
        )
        if filepath:
            self.selected_extract_file = filepath
            page_count = self._get_pdf_page_count(filepath)
            self.extract_file_label.config(text=f"Archivo seleccionado: {os.path.basename(filepath)} ({page_count} páginas)")
            self._update_status(f"Archivo '{os.path.basename(filepath)}' seleccionado para extraer páginas.")
        else:
            self._update_status("Selección de archivo para extraer cancelada.")

    def _extract_pages(self):
        """Extrae las páginas especificadas del PDF seleccionado en un nuevo archivo."""
        if not self.selected_extract_file:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo PDF para extraer páginas.")
            return

        output_filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar PDF recortado como"
        )
        if not output_filepath:
            self._update_status("Operación de extracción cancelada.")
            return

        self._update_status("Extrayendo páginas...")
        try:
            reader = PdfReader(self.selected_extract_file)
            writer = PdfWriter()
            total_pages = len(reader.pages)
            
            pages_to_extract_str = self.extract_pages_entry.get().strip()
            pages_to_extract_indices = self._parse_page_ranges(pages_to_extract_str, total_pages)

            if total_pages == 0:
                messagebox.showwarning("Advertencia", "El PDF seleccionado no contiene páginas.")
                self._update_status("Extracción fallida: PDF sin páginas.")
                return
            
            if not pages_to_extract_indices:
                messagebox.showwarning("Advertencia", "No se especificaron páginas válidas o el rango es incorrecto. No se extrajo nada.")
                self._update_status("Extracción cancelada: no hay páginas válidas para extraer.")
                return

            extracted_count = 0
            for page_num_0_indexed in pages_to_extract_indices:
                writer.add_page(reader.pages[page_num_0_indexed])
                extracted_count += 1
            
            if extracted_count == 0:
                messagebox.showwarning("Advertencia", "Las páginas especificadas no existen en el PDF o no se pudieron extraer. No se extrajo nada.")
                self._update_status("Extracción fallida: páginas no válidas.")
                return

            with open(output_filepath, "wb") as f:
                writer.write(f)
            
            self._update_status(f"Páginas extraídas exitosamente en '{os.path.basename(output_filepath)}' ({extracted_count} páginas).")
            messagebox.showinfo("Éxito", f"Páginas extraídas y guardadas como '{os.path.basename(output_filepath)}'.")

        except Exception as e:
            self._update_status(f"Error al extraer páginas: {e}")
            messagebox.showerror("Error", f"Ocurrió un error al extraer las páginas: {e}")

    def _select_compress_pdf(self):
        """Abre un diálogo para seleccionar un único archivo PDF para comprimir y muestra su número de páginas."""
        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo PDF para comprimir",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
        )
        if filepath:
            self.selected_compress_file = filepath
            page_count = self._get_pdf_page_count(filepath)
            self.compress_file_label.config(text=f"Archivo seleccionado: {os.path.basename(filepath)} ({page_count} páginas)")
            self._update_status(f"Archivo '{os.path.basename(filepath)}' seleccionado para comprimir.")
        else:
            self._update_status("Selección de archivo para comprimir cancelada.")

    def _compress_pdf(self):
        """Intenta comprimir el PDF seleccionado usando pypdf y proporciona feedback detallado."""
        if not self.selected_compress_file:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo PDF para comprimir.")
            return

        if not os.path.exists(self.selected_compress_file):
            messagebox.showerror("Error", "El archivo seleccionado para comprimir no existe.")
            self._update_status("Error: Archivo no encontrado para comprimir.")
            return
        
        output_filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar PDF comprimido como"

        )
        if not output_filepath:
            self._update_status("Operación de compresión cancelada.")
            return

        self._update_status("Comprimiendo PDF (esto puede tomar un momento)...")
        try:
            original_size = os.path.getsize(self.selected_compress_file)
            reader = PdfReader(self.selected_compress_file)
            writer = PdfWriter(clone_from=self.selected_compress_file)

            if len(reader.pages) == 0:
                messagebox.showwarning("Advertencia", "El PDF seleccionado no contiene páginas. No se puede comprimir.")
                self._update_status("Compresión fallida: PDF sin páginas.")
                return

            # Añadir todas las páginas del PDF original al nuevo escritor
            for page in writer.pages:
                page.compress_content_streams(level=6)

            # Intentar escribir con la compresión habilitada.
            # El argumento `compress=True` de pypdf aplica FlateDecode a los streams
            # no comprimidos. Esto no es una compresión tan agresiva como la que
            # realizan herramientas dedicadas (que pueden reescalar imágenes,
            # eliminar fuentes, etc.), pero puede ofrecer cierta reducción.
            with open(output_filepath, "wb") as f:
                writer.write(f) 

            new_size = os.path.getsize(output_filepath)
            size_reduction_bytes = original_size - new_size
            size_reduction_percent = (size_reduction_bytes / original_size) * 100 if original_size > 0 else 0

            status_message = (
                f"PDF comprimido exitosamente en '{os.path.basename(output_filepath)}'.\n"
                f"Tamaño original: {original_size / (1024*1024):.2f} MB, "
                f"Tamaño nuevo: {new_size / (1024*1024):.2f} MB.\n"
                f"Reducción: {size_reduction_bytes / 1024:.2f} KB ({size_reduction_percent:.2f}%)."
            )
            self._update_status(status_message)
            messagebox.showinfo(
                "Éxito de Compresión",
                f"PDF comprimido y guardado como '{os.path.basename(output_filepath)}'.\n"
                f"Reducción de tamaño: {size_reduction_percent:.2f}%.\n\n"
                "Nota: La compresión con esta herramienta es básica. Para una compresión más agresiva (por ejemplo, reducir la calidad de las imágenes o eliminar elementos no esenciales), se recomiendan herramientas externas como Ghostscript o compresores de PDF online."
            )

        except Exception as e:
            self._update_status(f"Error al comprimir PDF: {e}")
            messagebox.showerror("Error", f"Ocurrió un error al comprimir el PDF: {e}\n"
                                          "Asegúrate de que el archivo no esté corrupto o protegido.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToolApp(root)
    root.mainloop()