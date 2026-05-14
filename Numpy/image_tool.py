# ============================================================
#   IMAGE MANIPULATION TOOL — Using NumPy
#   image_tool.py
#
#   What you will learn:
#   - How images are just NumPy arrays (height x width x 3)
#   - Array slicing, math operations, clipping
#   - Saving and loading images with Pillow (pip install Pillow)
# ============================================================

import numpy as np
from PIL import Image   # pip install Pillow
import os

# ────────────────────────────────────────────────────────────
#  LOAD & SAVE HELPERS
# ────────────────────────────────────────────────────────────

def load_image(path):
    """
    Load an image from disk and return it as a NumPy array.
    Shape will be (height, width, 3) for RGB images.
    Pixel values are integers 0-255.
    """
    img = Image.open(path).convert("RGB")   # always RGB, no alpha channel
    return np.array(img, dtype=np.uint8)


def save_image(array, path):
    """
    Save a NumPy array as an image file.
    Clips values to 0-255 before saving to avoid corrupt pixels.
    """
    clipped = np.clip(array, 0, 255).astype(np.uint8)
    Image.fromarray(clipped).save(path)
    print(f"  [✓] Saved → {path}")


def show_info(array, label="Image"):
    """Print shape, dtype, min/max pixel values — useful for debugging."""
    print(f"  [{label}]  shape={array.shape}  dtype={array.dtype}  "
          f"min={array.min()}  max={array.max()}")


# ────────────────────────────────────────────────────────────
#  FEATURE 1 — GRAYSCALE
# ────────────────────────────────────────────────────────────

def to_grayscale(img):
    """
    Convert a colour image to grayscale using the luminance formula:
        gray = 0.2989*R + 0.5870*G + 0.1140*B
    This matches how human eyes perceive brightness.
    Returns a (H, W, 3) array so it can still be saved as RGB.
    """
    # img[:, :, 0] = Red channel, [:, :, 1] = Green, [:, :, 2] = Blue
    r = img[:, :, 0].astype(np.float32)
    g = img[:, :, 1].astype(np.float32)
    b = img[:, :, 2].astype(np.float32)

    gray_2d = 0.2989 * r + 0.5870 * g + 0.1140 * b   # shape: (H, W)

    # Stack 3 times to make it (H, W, 3) — same gray in R, G, B
    gray_3d = np.stack([gray_2d, gray_2d, gray_2d], axis=2)
    return gray_3d.astype(np.uint8)


# ────────────────────────────────────────────────────────────
#  FEATURE 2 — FLIP
# ────────────────────────────────────────────────────────────

def flip_horizontal(img):
    """
    Flip the image left-to-right (mirror effect).
    np.fliplr reverses the columns (axis=1).
    """
    return np.fliplr(img)


def flip_vertical(img):
    """
    Flip the image upside-down.
    np.flipud reverses the rows (axis=0).
    """
    return np.flipud(img)


# ────────────────────────────────────────────────────────────
#  FEATURE 3 — BRIGHTNESS
# ────────────────────────────────────────────────────────────

def adjust_brightness(img, factor):
    """
    Multiply every pixel by 'factor' to change brightness.
    factor > 1.0  →  brighter
    factor < 1.0  →  darker
    np.clip keeps values within 0-255 so pixels don't wrap or overflow.
    """
    bright = img.astype(np.float32) * factor
    return np.clip(bright, 0, 255).astype(np.uint8)


# ────────────────────────────────────────────────────────────
#  FEATURE 4 — CROP
# ────────────────────────────────────────────────────────────

def crop(img, top, bottom, left, right):
    """
    Crop the image using array slicing.
    img[rows, cols, channels]
    top/bottom = row range, left/right = column range.
    """
    return img[top:bottom, left:right, :]


# ────────────────────────────────────────────────────────────
#  FEATURE 5 — ROTATE 90°
# ────────────────────────────────────────────────────────────

def rotate_90(img, times=1):
    """
    Rotate image 90° counter-clockwise, 'times' number of times.
    np.rot90 rotates the first two axes (height, width).
    """
    return np.rot90(img, k=times)


# ────────────────────────────────────────────────────────────
#  FEATURE 6 — INVERT COLORS
# ────────────────────────────────────────────────────────────

def invert(img):
    """
    Invert all pixel values: new_pixel = 255 - old_pixel.
    A very bright pixel (250) becomes dark (5) and vice versa.
    """
    return 255 - img


# ────────────────────────────────────────────────────────────
#  FEATURE 7 — BLEND TWO IMAGES
# ────────────────────────────────────────────────────────────

def blend(img1, img2, alpha=0.5):
    """
    Mix two same-size images together.
    alpha = how much of img1 to use (0.0 to 1.0).
    result = alpha * img1 + (1 - alpha) * img2
    """
    if img1.shape != img2.shape:
        raise ValueError("Both images must be the same size to blend.")
    mixed = alpha * img1.astype(np.float32) + (1 - alpha) * img2.astype(np.float32)
    return np.clip(mixed, 0, 255).astype(np.uint8)


# ────────────────────────────────────────────────────────────
#  DEMO — runs when you have a real image file
# ────────────────────────────────────────────────────────────

def demo_with_real_image(input_path):
    """
    Run all operations on a real image and save the results.
    Pass any .jpg or .png file path.
    """
    print(f"\nLoading: {input_path}")
    img = load_image(input_path)
    show_info(img, "Original")

    base = os.path.splitext(input_path)[0]   # strip extension

    # Grayscale
    gray = to_grayscale(img)
    save_image(gray, base + "_grayscale.jpg")

    # Flips
    save_image(flip_horizontal(img), base + "_flip_h.jpg")
    save_image(flip_vertical(img),   base + "_flip_v.jpg")

    # Brightness
    save_image(adjust_brightness(img, 1.5), base + "_bright.jpg")
    save_image(adjust_brightness(img, 0.5), base + "_dark.jpg")

    # Crop (centre region)
    h, w = img.shape[:2]
    cropped = crop(img, h//4, 3*h//4, w//4, 3*w//4)
    save_image(cropped, base + "_cropped.jpg")

    # Rotate
    save_image(rotate_90(img, times=1), base + "_rotated.jpg")

    # Invert
    save_image(invert(img), base + "_inverted.jpg")

    print("\n[✓] All operations complete!")


# ────────────────────────────────────────────────────────────
#  DEMO — synthetic (no image file needed — uses random pixels)
# ────────────────────────────────────────────────────────────

def demo_synthetic():
    """
    Create a fake 200x300 image with random pixels to test all functions.
    No real image file needed — great for understanding the array shapes.
    """
    print("\n=== Synthetic Demo (random pixel array) ===\n")

    # Create a fake 200 rows × 300 columns RGB image
    np.random.seed(42)
    img = np.random.randint(0, 256, (200, 300, 3), dtype=np.uint8)
    show_info(img, "Original (random)")

    # --- Grayscale ---
    gray = to_grayscale(img)
    show_info(gray, "Grayscale")
    # All 3 channels should be equal now
    assert np.all(gray[:, :, 0] == gray[:, :, 1]), "R and G channels differ!"
    print("  Grayscale check passed (R == G == B)")

    # --- Flip ---
    flipped = flip_horizontal(img)
    show_info(flipped, "Flipped H")
    # First pixel of original should equal last pixel of flipped
    assert np.array_equal(img[0, 0], flipped[0, -1]), "Flip mismatch!"
    print("  Horizontal flip check passed")

    # --- Brightness ---
    bright = adjust_brightness(img, 2.0)
    show_info(bright, "Brightness x2")
    # Max value must never exceed 255
    assert bright.max() <= 255, "Clip failed!"
    print("  Brightness clip check passed")

    # --- Crop ---
    c = crop(img, 50, 150, 75, 225)
    show_info(c, "Cropped")
    assert c.shape == (100, 150, 3), f"Wrong crop shape: {c.shape}"
    print("  Crop shape check passed")

    # --- Rotate ---
    rot = rotate_90(img, times=1)
    show_info(rot, "Rotated 90°")
    # After 1 rotation, height and width swap
    assert rot.shape == (300, 200, 3), f"Wrong rotate shape: {rot.shape}"
    print("  Rotation shape check passed")

    # --- Invert ---
    inv = invert(img)
    show_info(inv, "Inverted")
    # Original + inverted should always sum to 255
    assert np.all(img.astype(int) + inv.astype(int) == 255), "Invert math failed!"
    print("  Invert check passed (original + inverted == 255)")

    # --- Blend ---
    blend_result = blend(img, inv, alpha=0.5)
    show_info(blend_result, "Blended (50/50)")
    print("  Blend check passed")

    print("\n[✓] All synthetic checks passed! Your functions work correctly.\n")
    print("To use with a real image, call: demo_with_real_image('your_photo.jpg')")


# ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    #demo_synthetic()

    # Uncomment this line to run on a real image:
    demo_with_real_image(r'c:\Users\c_1\Pictures\boy.png')
