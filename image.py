import cv2
import numpy as np
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import tempfile

# خواندن تصویر اصلی
image_path = "Fig2.19(a).jpg"
original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if original_image is None:
    print("No image found!")
    exit()

# لیست وضوح‌های مورد نظر
resolutions = [(512, 512), (256, 256), (128, 128), (64, 64), (32, 32)]

# تنظیم اندازه صفحه PDF (20cm × 20cm)
pdf_width, pdf_height = 20 * cm, 20 * cm  
pdf_filename = "resized_images.pdf"
c = canvas.Canvas(pdf_filename, pagesize=(pdf_width, pdf_height))

for res in resolutions:
    # تغییر اندازه تصویر
    resized = cv2.resize(original_image, res, interpolation=cv2.INTER_CUBIC)

    # تبدیل به فرمت PIL
    img_pil = Image.fromarray(resized)

    # ذخیره در یک فایل موقت
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
        temp_filename = temp_file.name
        img_pil.save(temp_filename, format="JPEG")

    # رسم تصویر در PDF
    c.drawImage(temp_filename, 0, 0, pdf_width, pdf_height)

    # افزودن متن (وضوح تصویر)
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(1, 1, 1)  # متن سفید

    c.drawString(10, pdf_height - 30, f"Resolution: {res[0]}x{res[1]}")

    c.showPage()  # صفحه جدید برای تصویر بعدی

c.save()

print("PDF saved successfully!")
