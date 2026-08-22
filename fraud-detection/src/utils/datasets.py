from enum import StrEnum
from pathlib import Path

import kagglehub
import pandas as pd

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
	variant: DatasetVariant = DatasetVariant.BASE,
	output_dir: Path = DATA_PATH / "raw",
) -> pd.DataFrame:
	"""
	Returns the pandas DataFrame containing the requested variant of the NeurIPS 2022 fraud detection dataset.
	if all the variants are requested, the Base.csv one is returned.
	"""
	csv = Path(DatasetVariant.BASE if variant is DatasetVariant.FULL else variant).name
	if not (output_dir / csv).exists():
		kagglehub.dataset_download(
			NEURIPS_DOWNLOAD_URL,
			path=csv if variant is not DatasetVariant.FULL else None,
			output_dir=str(output_dir),
		)

	return pd.read_csv(output_dir / csv)
