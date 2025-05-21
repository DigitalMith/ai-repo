import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import face_recognition

INPUT_DIR = "input"
OUTPUT_DIR = "output"
MAX_DIM = 2048
SHARPNESS_FACTOR = 1.3
BRIGHTNESS_FACTOR = 1.05
CONTRAST_FACTOR = 1.1
FACE_CROP_PADDING = 0.2  # % padding around face box


def enhance_image(pil_img):
    # Auto-adjust gamma using histogram equalization on value channel
    img = np.array(pil_img.convert('RGB'))
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    hsv[:, :, 2] = cv2.equalizeHist(hsv[:, :, 2])
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    pil_img = Image.fromarray(img)

    # Apply sharpness, contrast, brightness
    pil_img = ImageEnhance.Sharpness(pil_img).enhance(SHARPNESS_FACTOR)
    pil_img = ImageEnhance.Contrast(pil_img).enhance(CONTRAST_FACTOR)
    pil_img = ImageEnhance.Brightness(pil_img).enhance(BRIGHTNESS_FACTOR)

    return pil_img


def resize_preserve_aspect(img):
    img.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)
    return img


def crop_around_face(img):
    img_np = np.array(img)
    face_locations = face_recognition.face_locations(img_np)

    if not face_locations:
        return img  # no face found

    top, right, bottom, left = face_locations[0]
    h, w = img_np.shape[:2]

    # Expand box with padding
    pad_h = int((bottom - top) * FACE_CROP_PADDING)
    pad_w = int((right - left) * FACE_CROP_PADDING)
    top = max(0, top - pad_h)
    bottom = min(h, bottom + pad_h)
    left = max(0, left - pad_w)
    right = min(w, right + pad_w)

    cropped = img.crop((left, top, right, bottom))
    return cropped


def process_image(image_path, output_path):
    try:
        img = Image.open(image_path)
        img = enhance_image(img)
        img = crop_around_face(img)
        img = resize_preserve_aspect(img)
        img.save(output_path, "JPEG", quality=92, optimize=True)
        print(f"? Processed: {os.path.basename(image_path)}")
    except Exception as e:
        print(f"? Failed: {image_path} — {e}")


def batch_process():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = [f for f in os.listdir(INPUT_DIR)
             if f.lower().endswith(('jpg', 'jpeg', 'png'))]

    if not files:
        print("[!] No images found in input folder.")
        return

    for filename in files:
        in_path = os.path.join(INPUT_DIR, filename)
        out_path = os.path.join(OUTPUT_DIR, os.path.splitext(filename)[0] + ".jpg")
        process_image(in_path, out_path)


if __name__ == "__main__":
    print("[??] Starting batch image enhancement...")
    batch_process()
    print("[?] Done. Check the 'output' folder.")
