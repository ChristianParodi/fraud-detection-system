import random
import time
from collections.abc import Iterator

import pandas as pd

from .datasets import get_neurips_fraud_dataset


def streaming_delay(rate_per_second: float = 10, verbose: bool = False):
	delay = random.expovariate(rate_per_second)
	if verbose:
		print(f"{delay=}")
	time.sleep(delay)


def simulate_streaming(
	df: pd.DataFrame, rate_per_second: float = 10, verbose: bool = False
) -> Iterator[dict]:
	"""
	Yields the dataframe one row at a time, spacing rows with exponentially
	distributed gaps (Poisson arrivals).

	### Parameters
		df: the dataframe to stream, one dict per row
		rate_per_second: mean arrival rate; gaps average 1 / rate_per_second
	### Returns
		An iterator over the rows of the dataframe supplied
	"""
	columns = df.columns
	# avoid building the namedtuple, so a row is just values without keys for now
	for row in df.itertuples(index=False, name=None):
		streaming_delay(rate_per_second=rate_per_second, verbose=verbose)
		# associate keys (columns) with values (rows), raising an error if the length is not the same (strict=True)
		yield dict(zip(columns, row, strict=True))


if __name__ == "__main__":
	df = get_neurips_fraud_dataset()
	max_example_rows = 10
	for row, n_row in zip(
		simulate_streaming(df, rate_per_second=10, verbose=True),
		range(1, max_example_rows),
	):
		print(f"{n_row=}")
		print(row)
