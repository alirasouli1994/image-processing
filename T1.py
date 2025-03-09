import cv2
import numpy as np
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import tempfile


image_path = "Fig2.19(a).jpg"
original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if original_image is None:
    print("No image found!")
    exit()


resolutions = [(512, 512), (256, 256), (128, 128), (64, 64), (32, 32)]


pdf_width, pdf_height = 20 * cm, 20 * cm  
pdf_filename = "resized_images.pdf"
c = canvas.Canvas(pdf_filename, pagesize=(pdf_width, pdf_height))

for res in resolutions:
   
    resized = cv2.resize(original_image, res, interpolation=cv2.INTER_CUBIC)

  
    img_pil = Image.fromarray(resized)

   
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
        temp_filename = temp_file.name
        img_pil.save(temp_filename, format="JPEG")

    c.drawImage(temp_filename, 0, 0, pdf_width, pdf_height)

   
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(1, 1, 1)  

    c.drawString(10, pdf_height - 30, f"Resolution: {res[0]}x{res[1]}")

    c.showPage() 

c.save()

print("PDF saved successfully!")
