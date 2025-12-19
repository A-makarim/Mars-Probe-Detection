"""
This module contains preprocessing functions for the Mars Probe Detection project.

remove_empty_labels: bool
"""

from pathlib import Path


def remove_empty_labels(data_dir: str):
    """
    Remove label files that are empty and their corresponding image files if subject was constantly in view.
    """
    data_path = Path(data_dir)
    labels_dir = data_path / 'labels'
    images_dir = data_path / 'images'

    # remove any files with empty labels and corresponding images

    for label_file in labels_dir.glob('*.txt'):
        with open(label_file, 'r') as f:
            lines = f.readlines()
        
        if len(lines) == 0:
            print(f"Removing empty label file: {label_file}")
            image_file = images_dir / f"{label_file.stem}.jpg"  # assuming .jpg images
            if image_file.exists():
                print(f"Removing corresponding image file: {image_file}")
                image_file.unlink() 
            label_file.unlink()


remove_empty_labels('data/')
print("Empty label files and corresponding images removed.")
