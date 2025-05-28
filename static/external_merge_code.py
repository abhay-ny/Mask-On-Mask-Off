import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

class YUVImageReconstructor:
    def __init__(self, root):
        self.root = root
        self.root.title("YUV Image Reconstructor")

        self.Y_loaded = False
        self.U_loaded = False
        self.V_loaded = False
        self.displayed_image = None

        # Buttons to upload Y, U, and V component images
        tk.Button(root, text="Upload Y Component", command=self.upload_Y).pack()
        tk.Button(root, text="Upload U Component", command=self.upload_U).pack()
        tk.Button(root, text="Upload V Component", command=self.upload_V).pack()

        # Button to reconstruct and display the original image
        tk.Button(root, text="Reconstruct Image", command=self.reconstruct_image).pack()

    def upload_Y(self):
        file_path = filedialog.askopenfilename(title="Select Y Component Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.Y = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.Y_loaded = True
            messagebox.showinfo("Success", "Y Component Image Uploaded Successfully")

    def upload_U(self):
        file_path = filedialog.askopenfilename(title="Select U Component Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.U = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.U_loaded = True
            messagebox.showinfo("Success", "U Component Image Uploaded Successfully")

    def upload_V(self):
        file_path = filedialog.askopenfilename(title="Select V Component Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.V = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.V_loaded = True
            messagebox.showinfo("Success", "V Component Image Uploaded Successfully")

    def reconstruct_image(self):
        if not all((self.Y_loaded, self.U_loaded, self.V_loaded)):
            messagebox.showerror("Error", "Please upload all Y, U, and V component images")
            return

        # Merge Y, U, and V components to reconstruct the original image
        merged_image = cv2.merge((self.Y, self.U, self.V))

        # Convert merged image from YUV to RGB
        merged_image_rgb = cv2.cvtColor(merged_image, cv2.COLOR_YUV2RGB)

        # Display the reconstructed image
        self.display_image(merged_image_rgb)

        # Ask user for file name and location to save the merged image
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            # Convert merged image to RGB for saving
            merged_image_bgr = cv2.cvtColor(merged_image_rgb, cv2.COLOR_RGB2BGR)
            # Save the merged image
            cv2.imwrite(file_path, merged_image_bgr)
            messagebox.showinfo("Success", "Merged image saved successfully")

    def display_image(self, image):
        # Convert image to PIL format
        pil_image = Image.fromarray(image)

        # Convert PIL image to PhotoImage and keep a reference to avoid garbage collection
        self.displayed_image = ImageTk.PhotoImage(pil_image)

        # Display image using Tkinter
        label = tk.Label(self.root, image=self.displayed_image)
        label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = YUVImageReconstructor(root)
    root.mainloop()
