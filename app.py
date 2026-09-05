import os
import tkinter as tk
from tkinter import filedialog, messagebox
import img2pdf
from pdf2image import convert_from_path

THEME = {
    "bg": "#F5F7FA",
    "card_bg": "#FFFFFF",
    "primary": "#825799",
    "text": "#333333",
    "font_family": "Century Gothic",
}

class ConverterApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image & PDF Converter")
        self.root.geometry("450x420")
        self.root.resizable(False, False)
        self.root.configure(bg=THEME["bg"])

        self.current_mode = "img_to_pdf"
        self.files = []

        self._setup_ui()

    def _setup_ui(self):
        title_label = tk.Label(
            self.root,
            text="Image & PDF Converter",
            font=(THEME["font_family"], 18, "bold"),
            bg=THEME["primary"],
            fg="white",
            pady=15,
        )
        title_label.pack(fill=tk.X)

        content_frame = tk.Frame(self.root, bg=THEME["bg"], padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        self.mode_btn = tk.Button(
            content_frame,
            text="Mode: Image ➔ PDF",
            font=(THEME["font_family"], 11, "bold"),
            bg="#E1E8ED",
            fg=THEME["text"],
            relief=tk.FLAT,
            pady=8,
            command=self._change_mode,
        )
        self.mode_btn.pack(fill=tk.X, pady=(0, 15))

        self.upload_btn = tk.Button(
            content_frame,
            text="Select Images",
            font=(THEME["font_family"], 11),
            bg="#FFFFFF",
            fg=THEME["text"],
            relief=tk.GROOVE,
            pady=8,
            command=self._upload_files,
        )
        self.upload_btn.pack(fill=tk.X, pady=5)

        self.status_label = tk.Label(
            content_frame,
            text="No files selected",
            font=(THEME["font_family"], 9, "italic"),
            bg=THEME["bg"],
            fg="#7F8C8D",
            wraplength=380,
        )
        self.status_label.pack(pady=10)

        self.convert_btn = tk.Button(
            content_frame,
            text="Start Conversion",
            font=(THEME["font_family"], 12, "bold"),
            bg=THEME["primary"],
            fg="white",
            relief=tk.FLAT,
            pady=10,
            command=self._convert,
        )
        self.convert_btn.pack(fill=tk.X, pady=(15, 0))

        info_label = tk.Label(
            self.root,
            text="Haiaka",
            font=(THEME["font_family"], 9),
            bg=THEME["bg"],
            fg="#BDC3C7",
        )
        info_label.pack(side=tk.BOTTOM, anchor=tk.SE, padx=15, pady=10)

    def _change_mode(self):
        self.files = []
        self.status_label.config(text="No files selected")

        if self.current_mode == "img_to_pdf":
            self.current_mode = "pdf_to_img"
            self.mode_btn.config(text="Mode: PDF ➔ Image")
            self.upload_btn.config(text="Select PDF File")
        else:
            self.current_mode = "img_to_pdf"
            self.mode_btn.config(text="Mode: Image ➔ PDF")
            self.upload_btn.config(text="Select Images")

    def _upload_files(self):
        if self.current_mode == "img_to_pdf":
            filetypes = [
                ("Image files", "*.png *.jpg *.jpeg"),
                ("All files", "*.*"),
            ]
            selected = filedialog.askopenfilenames(
                title="Select Images", filetypes=filetypes
            )
        else:
            filetypes = [("PDF files", "*.pdf"), ("All files", "*.*")]
            selected = filedialog.askopenfilenames(
                title="Select PDF", filetypes=filetypes
            )

        if selected:
            self.files = list(selected)
            self.status_label.config(
                text=f"Selected {len(self.files)} file(s)"
            )

    def _convert(self):
        if not self.files:
            messagebox.showerror("Error", "Please select file(s) first.")
            return

        try:
            if self.current_mode == "img_to_pdf":
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF file", "*.pdf")],
                    title="Save PDF As",
                )
                if save_path:
                    with open(save_path, "wb") as f:
                        f.write(img2pdf.convert(self.files))
                    messagebox.showinfo(
                        "Success", "Successfully converted to PDF!"
                    )

            else:
                output_dir = filedialog.askdirectory(
                    title="Select Output Folder"
                )
                if output_dir:
                    for pdf_file in self.files:
                        images = convert_from_path(pdf_file)
                        base_name = os.path.splitext(
                            os.path.basename(pdf_file)
                        )[0]
                        for i, image in enumerate(images):
                            image.save(
                                os.path.join(
                                    output_dir, f"{base_name}_page_{i+1}.png"
                                ),
                                "PNG",
                            )
                    messagebox.showinfo(
                        "Success", "Successfully extracted pages as images!"
                    )

        except Exception as e:
            messagebox.showerror(
                "Conversion Error", f"An error occurred:\n{str(e)}"
            )

if __name__ == "__main__":
    app = ConverterApp()
    app.root.mainloop()