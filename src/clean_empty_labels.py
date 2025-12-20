"""
clean_empty_labels.py

Remove empty YOLO label files and their corresponding images.
Use ONLY if the subject is always in view.

how this helps? 
training data will provide false ground truth
data is labelled by sam3 segmentation model
this is not human annotated dataset liek COCO or VOC

"""

from pathlib import Path

IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp")


def is_empty_label(label_path: Path) -> bool:
    """Return True if label file is empty or whitespace-only."""
    try:
        return label_path.stat().st_size == 0 or label_path.read_text().strip() == ""
    except Exception:
        return False


def find_matching_image(images_dir: Path, stem: str) -> Path | None:
    """Find image with same stem and known extensions."""
    for ext in IMAGE_EXTS:
        img = images_dir / f"{stem}{ext}"
        if img.exists():
            return img
    return None


def clean_empty_labels(labels_dir: str = "data/sam_output/labels", images_dir: str = "data/sam_output/images", delete: bool = True) -> int:
    """
    Remove empty label files and their matching images.
    """
    labels_dir = Path(labels_dir)
    images_dir = Path(images_dir)

    if not labels_dir.exists() or not images_dir.exists():
        print("Labels or images directory not found.")
        return 0

    removed = 0

    for label in sorted(labels_dir.glob("*.txt")):
        if is_empty_label(label):
            img = find_matching_image(images_dir, label.stem)

            if delete:
                try:
                    label.unlink()
                except Exception:
                    pass
                if img and img.exists():
                    try:
                        img.unlink()
                    except Exception:
                        pass
                removed += 1
                print(f"Removed empty label: {label.name}")
            else:
                if img:
                    print(f"Would remove: {label.name} and {img.name}")
                else:
                    print(f"Would remove: {label.name} (no matching image)")

    print(f"\nDone. Removed {removed} empty label(s).")
    return removed


if __name__ == "__main__":
    # preserve simple CLI behaviour: delete by default
    clean_empty_labels()
