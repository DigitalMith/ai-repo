import os
import json
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import face_recognition

SAMPLE_INPUT_DIR = "sample_input"
PREVIEW_OUTPUT_DIR = "preview_output"
CONFIG_OUTPUT_FILE = "session_config.json"

SHARPNESS_VALUES = [1.0, 1.3, 1.6]
BRIGHTNESS_VALUES = [1.0, 1.1, 1.2]
CONTRAST_VALUES = [1.0, 1.1, 1.2]
CROP_PADDING = [0.1, 0.2, 0.3]  # used for face-aware crops


def measure_sharpness(img_np):
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()


def measure_brightness(img_np):
    hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
    return np.mean(hsv[:, :, 2])


def measure_contrast(img_np):
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    return np.std(gray)


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


def enhance(img, sharpness, brightness, contrast):
    img = ImageEnhance.Sharpness(img).enhance(sharpness)
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    return img


def generate_previews():
    os.makedirs(PREVIEW_OUTPUT_DIR, exist_ok=True)
    files = [f for f in os.listdir(SAMPLE_INPUT_DIR)
             if f.lower().endswith(("jpg", "jpeg", "png"))]

    all_metrics = []

    for fname in files:
        base = os.path.splitext(fname)[0]
        img_path = os.path.join(SAMPLE_INPUT_DIR, fname)
        img = Image.open(img_path).convert("RGB")
        img_np = np.array(img)

        sharp_val = measure_sharpness(img_np)
        bright_val = measure_brightness(img_np)
        contrast_val = measure_contrast(img_np)
        all_metrics.append((sharp_val, bright_val, contrast_val))

        for s in SHARPNESS_VALUES:
            for b in BRIGHTNESS_VALUES:
                for c in CONTRAST_VALUES:
                    for pad in CROP_PADDING:
                        crop = crop_face(img, pad)
                        result = enhance(crop.copy(), s, b, c)
                        outname = f"{base}_sharp{s}_bright{b}_cont{c}_pad{pad}.jpg"
                        outpath = os.path.join(PREVIEW_OUTPUT_DIR, outname)
                        result.save(outpath, "JPEG", quality=90)

    # Metric summary
    avg_sharp = np.mean([m[0] for m in all_metrics])
    avg_bright = np.mean([m[1] for m in all_metrics])
    avg_contrast = np.mean([m[2] for m in all_metrics])

    print("\n📊 Sample Analysis Results:")
    print(f"  Avg Sharpness: {avg_sharp:.2f} (Laplace var)")
    print(f"  Avg Brightness: {avg_bright:.2f} (0–255 HSV V channel)")
    print(f"  Avg Contrast: {avg_contrast:.2f} (std of grayscale)")

    config = {}

    print("\n🧠 Suggested Enhancements:")
    if avg_sharp < 250:
        config["SHARPNESS_FACTOR"] = 1.5
    else:
        config["SHARPNESS_FACTOR"] = 1.2
    print(f"  SHARPNESS_FACTOR = {config['SHARPNESS_FACTOR']}")

    if avg_bright < 120:
        config["BRIGHTNESS_FACTOR"] = 1.2
    elif avg_bright > 180:
        config["BRIGHTNESS_FACTOR"] = 0.9
    else:
        config["BRIGHTNESS_FACTOR"] = 1.0
    print(f"  BRIGHTNESS_FACTOR = {config['BRIGHTNESS_FACTOR']}")

    if avg_contrast < 50:
        config["CONTRAST_FACTOR"] = 1.2
    else:
        config["CONTRAST_FACTOR"] = 1.0
    print(f"  CONTRAST_FACTOR = {config['CONTRAST_FACTOR']}")

    config["FACE_CROP_PADDING"] = 0.2
    print(f"  FACE_CROP_PADDING = {config['FACE_CROP_PADDING']}")

    with open(CONFIG_OUTPUT_FILE, "w") as f:
        json.dump(config, f, indent=2)
        print(f"\n💾 Saved config to {CONFIG_OUTPUT_FILE}")


if __name__ == "__main__":
    print("[🧪] Generating preview grid with enhancement variations...")
    generate_previews()
    print("[✅] Done. Check the 'preview_output' folder for results.")
