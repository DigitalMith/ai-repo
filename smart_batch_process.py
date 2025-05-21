import os
import json
import argparse
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import face_recognition

INPUT_DIR = "input"
OUTPUT_DIR = "output"
DEFAULT_CONFIG = {
    "SHARPNESS_FACTOR": 1.3,
    "BRIGHTNESS_FACTOR": 1.05,
    "CONTRAST_FACTOR": 1.1,
    "FACE_CROP_PADDING": 0.2,
    "CROP_ENABLED": True,
    "MAX_DIM": 2048,
    "FORMAT": "jpg"
}


def load_config(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}


def crop_face(img, padding):
    img_np = np.array(img)
    face_locations = face_recognition.face_locations(img_np)
    if not face_locations:
        return img
    top, right, bottom, left = face_locations[0]
    h, w = img_np.shape[:2]
    pad_h = int((bottom - top) * padding)
    pad_w = int((right - left) * padding)
    top = max(0, top - pad_h)
    bottom = min(h, bottom + pad_h)
    left = max(0, left - pad_w)
    right = min(w, right + pad_w)
    return img.crop((left, top, right, bottom))


def enhance_image(pil_img, sharpness, brightness, contrast):
    pil_img = ImageEnhance.Sharpness(pil_img).enhance(sharpness)
    pil_img = ImageEnhance.Brightness(pil_img).enhance(brightness)
    pil_img = ImageEnhance.Contrast(pil_img).enhance(contrast)
    return pil_img


def resize_image(img, max_dim):
    img.thumbnail((max_dim, max_dim), Image.LANCZOS)
    return img


def process_image(path, output_path, config):
    try:
        img = Image.open(path).convert("RGB")
        if config.get("CROP_ENABLED", True):
            img = crop_face(img, config.get("FACE_CROP_PADDING", 0.2))
        img = enhance_image(
            img,
            config.get("SHARPNESS_FACTOR", 1.3),
            config.get("BRIGHTNESS_FACTOR", 1.05),
            config.get("CONTRAST_FACTOR", 1.1)
        )
        img = resize_image(img, config.get("MAX_DIM", 2048))
        img.save(output_path, config.get("FORMAT", "jpg").upper(), quality=90)
        print(f"✓ Processed: {os.path.basename(path)}")
    except Exception as e:
        print(f"✗ Failed: {path} — {e}")


def parse_args():
    parser = argparse.ArgumentParser(description="Batch image enhancer")
    parser.add_argument('--config', type=str, default='session_config.json', help='Path to config file')
    parser.add_argument('--crop', type=str, choices=['yes', 'no'], help='Enable or disable face crop')
    parser.add_argument('--sharpness', type=float, help='Sharpness factor override')
    parser.add_argument('--brightness', type=float, help='Brightness factor override')
    parser.add_argument('--contrast', type=float, help='Contrast factor override')
    parser.add_argument('--max-dim', type=int, help='Max image dimension')
    parser.add_argument('--format', type=str, choices=['jpg', 'png'], help='Output file format')
    return parser.parse_args()


def batch_process():
    args = parse_args()
    config = DEFAULT_CONFIG.copy()
    config.update(load_config(args.config))

    # Apply overrides
    if args.crop:
        config['CROP_ENABLED'] = args.crop.lower() == 'yes'
    if args.sharpness:
        config['SHARPNESS_FACTOR'] = args.sharpness
    if args.brightness:
        config['BRIGHTNESS_FACTOR'] = args.brightness
    if args.contrast:
        config['CONTRAST_FACTOR'] = args.contrast
    if args.max_dim:
        config['MAX_DIM'] = args.max_dim
    if args.format:
        config['FORMAT'] = args.format

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = [f for f in os.listdir(INPUT_DIR)
             if f.lower().endswith(("jpg", "jpeg", "png"))]

    if not files:
        print("[!] No images found in input folder.")
        return

    for fname in files:
        in_path = os.path.join(INPUT_DIR, fname)
        out_name = os.path.splitext(fname)[0] + f".{config['FORMAT']}"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        process_image(in_path, out_path, config)


if __name__ == "__main__":
    print("[⚙️] Running smart batch processor...")
    batch_process()
    print("[✅] Done. Check the 'output' folder.")
