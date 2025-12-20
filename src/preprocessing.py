"""
This module contains preprocessing functions for the Mars Probe Detection project.


split_data: 
"""


from pathlib import Path
import random
import shutil



def split_dataset(data_dir: str, train_ratio=0.7, val_ratio=0.2, seed=42):

    """
    Split dataset into train, validation, and test sets.
    Yolo needs images and labels in separate folders for each split.
    """
    random.seed(seed)

    data_path = Path(data_dir)
    images = sorted((data_path / "images").glob("*.jpg"))
    labels = {p.stem: p for p in (data_path / "labels").glob("*.txt")}

    pairs = [(img, labels.get(img.stem)) for img in images]
    pairs = [p for p in pairs if p[1] is not None]


    print(f"Found {len(images)} images")
    print(f"Found {len(labels)} labels")
    print(f"Matched {len(pairs)} image–label pairs")


    random.shuffle(pairs)

    n = len(pairs)
    n_train = int(train_ratio * n)
    n_val = int(val_ratio * n)

    splits = {
        "train": pairs[:n_train],
        "val": pairs[n_train:n_train + n_val],
        "test": pairs[n_train + n_val:]
    }

    for split, items in splits.items():
        img_dir = data_path / split / "images"
        lbl_dir = data_path / split / "labels"

        img_dir.mkdir(parents=True, exist_ok=True)
        lbl_dir.mkdir(parents=True, exist_ok=True)

        print(f"Copying {len(items)} samples to {split} set")

        for i, (img, lbl) in enumerate(items, 1):
            shutil.copy(img, img_dir / img.name)
            shutil.copy(lbl, lbl_dir / lbl.name)

            if i % 25 == 0 or i == len(items):
                print(f"  {split}: {i}/{len(items)} copied", flush=True)


def main():
    split_dataset(data_dir="data/augmented", train_ratio=0.7, val_ratio=0.2, seed=42)
    print("SRC: Dataset split into train, val, and test sets.")


if __name__ == "__main__":
    main()


