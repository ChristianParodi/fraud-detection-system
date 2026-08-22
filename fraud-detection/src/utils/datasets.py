from enum import StrEnum
from pathlib import Path

import kagglehub

from .constants import DATA_PATH, NEURIPS_DOWNLOAD_URL


class DatasetVariant(StrEnum):
    BASE = "./Base.csv"
    VARIANT_1 = "./Variant I.csv"
    VARIANT_2 = "./Variant II.csv"
    VARIANT_3 = "./Variant III.csv"
    VARIANT_4 = "./Variant IV.csv"
    VARIANT_5 = "./Variant V.csv"
    FULL = ""


def get_neurips_fraud_dataset(
    variant: DatasetVariant = DatasetVariant.FULL,
    output_dir: Path = DATA_PATH / "raw",
) -> None:
    path = kagglehub.dataset_download(
        NEURIPS_DOWNLOAD_URL,
        path=variant,
        output_dir=str(output_dir),
    )
    print("Path to dataset files:", path)
