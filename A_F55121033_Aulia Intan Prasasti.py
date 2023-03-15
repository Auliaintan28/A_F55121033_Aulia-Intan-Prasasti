import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

class ImageProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        self.contrast_stretching_button = tk.Button(self.root, text="Contrast Stretching", command=self.contrast_stretching)
        self.contrast_stretching_button.pack()

        self.histogram_equalization_button = tk.Button(self.root, text="Histogram Equalization", command=self.histogram_equalization)
        self.histogram_equalization_button.pack()

        self.save_button = tk.Button(self.root, text="Save Image", command=self.save_image)
        self.save_button.pack()

        self.image = None
        self.image_path = None
        self.modified_image = None

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])

        self.image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        self.image = cv2.resize(self.image, (500, 500))
        self.modified_image = self.image.copy()
        image = Image.fromarray(self.image)
        image = ImageTk.PhotoImage(image)
        self.image_label.config(image=image)
        self.image_label.image = image

    def contrast_stretching(self):
        p2, p98 = np.percentile(self.image, (2, 98))
        self.modified_image = (self.image - p2) * 255.0 / (p98 - p2)
        self.modified_image = np.clip(self.modified_image, 0, 255).astype(np.uint8)

        image = Image.fromarray(self.modified_image)
        image = ImageTk.PhotoImage(image)
        self.image_label.config(image=image)
        self.image_label.image = image

    def histogram_equalization(self):
        self.modified_image = cv2.equalizeHist(self.image)

        image = Image.fromarray(self.modified_image)
        image = ImageTk.PhotoImage(image)
        self.image_label.config(image=image)
        self.image_label.image = image

    def save_image(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".png")

        cv2.imwrite(save_path, self.modified_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessor(root)
    root.mainloop()
