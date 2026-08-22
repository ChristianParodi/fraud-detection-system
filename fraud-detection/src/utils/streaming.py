import random
import time
from collections.abc import Iterator

import pandas as pd

from .datasets import get_neurips_fraud_dataset


def streaming_delay(max_delay_seconds: float = 1, verbose: bool = False) -> None:
	"""
	Simulates a delay between 0 and max_delay_seconds
	### Parameters
		max_delay_seconds: the maximum delay to sample in seconds
	"""
	delay = random.uniform(0, max_delay_seconds)
	if verbose:
		print(f"{delay=}")
	time.sleep(delay)


def simulate_streaming(df: pd.DataFrame, verbose: bool = False) -> Iterator[dict]:
	"""
	The dataframe is returned row by row with lazy loading, plus
	a small delay to simulate streaming

	### Parameters
		df: the dataframe to stream, one dict per row
	### Returns
		A single lazy-loaded row of the dataframe supplied
	"""
	for row in df.to_dict("records"):
		streaming_delay(verbose)
		yield row


if __name__ == "__main__":
	df = get_neurips_fraud_dataset()
	for row in simulate_streaming(df, verbose=True):
		print(row)
