"""
colour augmentation functions
3D model was printed wihth yellow filament
we want to augment images to simulate different lighting conditions
"""


"""
Colour augmentation utilities.

Purpose:
- Simulate different probe filament colours and lighting conditions
- Force the model to rely on shape, not colour
- Avoid Mars-like background hues (reds / browns)

This operates on images ONLY.
Labels remain unchanged.
"""

import cv2
import numpy as np
import random


# OpenCV HSV hue range: 0–179
# Mars background is mostly reds/oranges/browns → avoid these
FORBIDDEN_HUE_RANGES = [
    (0, 15),     # red / orange
    (160, 179),  # deep red
]


def _random_valid_hue():
    """Sample a hue that is NOT Mars-like."""
    while True:
        h = random.uniform(0, 179)
        if not any(lo <= h <= hi for lo, hi in FORBIDDEN_HUE_RANGES):
            return h


def colour_augment(img: np.ndarray, hue_strength: float = 1.0, sat_range=(0.7, 1.4), val_range=(0.7, 1.3)) -> np.ndarray:
    """
    Apply colour augmentation to an image.

    Parameters
    ----------
    img : np.ndarray
        BGR image (OpenCV format)
    hue_strength : float
        0.0 → no hue change
        1.0 → full random hue replacement
        0.3–0.6 recommended
    sat_range : tuple
        Saturation multiplier range
    val_range : tuple
        Brightness multiplier range
    """

    assert img.dtype == np.uint8, "Image must be uint8"

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)

    # Hue augmentation
    if hue_strength > 0:
        new_hue = _random_valid_hue()
        hsv[..., 0] = (
            (1 - hue_strength) * hsv[..., 0]
            + hue_strength * new_hue
        )

    # Saturation
    sat_mult = random.uniform(*sat_range)
    hsv[..., 1] *= sat_mult

    # Brightness (Value)
    val_mult = random.uniform(*val_range)
    hsv[..., 2] *= val_mult

    hsv = np.clip(hsv, 0, 255).astype(np.uint8)
    out = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return out


def main():
    pass


if __name__ == "__main__":
    main()
