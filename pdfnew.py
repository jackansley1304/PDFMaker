import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image
import os

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        self.root.geometry("400x400")
        self.images = []

        self.select_button = tk.Button(root, text="Select Images", command=self.select_images)
        self.select_button.pack(pady=10)

        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.listbox.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.move_up_button = tk.Button(root, text="Move Up", command=self.move_up)
        self.move_up_button.pack(pady=2)

        self.move_down_button = tk.Button(root, text="Move Down", command=self.move_down)
        self.move_down_button.pack(pady=2)

        self.delete_button = tk.Button(root, text="Delete from List", command=self.delete_selected)
        self.delete_button.pack(pady=2)

        self.convert_button = tk.Button(root, text="Convert to PDF", command=self.convert_to_pdf)
        self.convert_button.pack(pady=10)

    def select_images(self):
        filetypes = [("Image files", "*.jpg;*.jpeg;*.png")]
        selected_files = filedialog.askopenfilenames(title="Select Images", filetypes=filetypes)

        for file in selected_files:
            if file not in self.images:
                self.images.append(file)
                self.listbox.insert(tk.END, os.path.basename(file))

    def move_up(self):
        index = self.listbox.curselection()
        if index and index[0] > 0:
            idx = index[0]
            self.images[idx - 1], self.images[idx] = self.images[idx], self.images[idx - 1]
            self.update_listbox(idx, idx - 1)

    def move_down(self):
        index = self.listbox.curselection()
        if index and index[0] < len(self.images) - 1:
            idx = index[0]
            self.images[idx + 1], self.images[idx] = self.images[idx], self.images[idx + 1]
            self.update_listbox(idx, idx + 1)

    def delete_selected(self):
        index = self.listbox.curselection()
        if index:
            idx = index[0]
            del self.images[idx]
            self.listbox.delete(idx)

    def update_listbox(self, old_idx, new_idx):
        item = self.listbox.get(old_idx)
        self.listbox.delete(old_idx)
        self.listbox.insert(new_idx, item)
        self.listbox.select_set(new_idx)

    def convert_to_pdf(self):
        if not self.images:
            messagebox.showwarning("No Images", "Please select images first.")
            return

        try:
            pil_images = [Image.open(img).convert("RGB") for img in self.images]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{e}")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save PDF as",
            initialfile="converted.pdf"
        )

        if save_path:
            pil_images[0].save(save_path, save_all=True, append_images=pil_images[1:])
            messagebox.showinfo("Success", f"PDF saved to:\n{save_path}")

            # Ask to delete original images
            if messagebox.askyesno("Delete Originals", "Do you want to permanently delete the original image files?"):
                for img in self.images:
                    try:
                        os.remove(img)
                    except Exception as e:
                        messagebox.showwarning("Delete Error", f"Could not delete {os.path.basename(img)}:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToPDFConverter(root)
    root.mainloop()
