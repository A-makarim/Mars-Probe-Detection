from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing import split_dataset


def main():
	split_dataset(data_dir=str(PROJECT_ROOT / 'data'/ 'augmented'), train_ratio=0.7, val_ratio=0.2, seed=42)
	print("Dataset split into train, val, and test sets.")


if __name__ == "__main__":
	main()