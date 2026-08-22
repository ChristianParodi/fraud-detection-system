import asyncio
import random
from collections.abc import AsyncIterator

import pandas as pd

from .datasets import get_neurips_fraud_dataset


async def simulate_stream_delay(rate_per_second: float = 10, verbose: bool = False):
	if rate_per_second <= 0:
		raise ValueError("rate_per_second must be > 0")

	delay = random.expovariate(rate_per_second)
	if verbose:
		print(f"{delay=:.6f}")
	await asyncio.sleep(delay)


async def simulate_data_stream(
	df: pd.DataFrame, rate_per_second: float = 10, verbose: bool = False
) -> AsyncIterator[dict]:
	"""
	Yields the dataframe one row at a time, spacing rows with exponentially
	distributed gaps (Poisson arrivals).

	### Parameters
		df: the dataframe to stream, one dict per row
		rate_per_second: mean arrival rate; gaps average 1 / rate_per_second
	### Returns
		An async iterator over the rows of the dataframe supplied
	"""
	# avoid building the namedtuple, so a row is just values without keys for now
	for row in df.itertuples(index=False, name=None):
		await simulate_stream_delay(rate_per_second=rate_per_second, verbose=verbose)
		# associate keys (columns) with values (rows), raising an error if the length is not the same (strict=True)
		yield dict(zip(df.columns, row, strict=True))


async def consume_data_stream(
	stream: AsyncIterator[dict],
	max_n_rows: int | None = None,
):
	"""
	consumer function for the async stream simulator
	"""
	if max_n_rows is not None and max_n_rows <= 0:
		raise ValueError("max_rows must be strictly positive.")

	n_row = 0

	async for row in stream:
		n_row += 1

		print(f"{n_row=}")
		print(row)

		if max_n_rows is not None and n_row == max_n_rows:
			break


async def _main():
	df = get_neurips_fraud_dataset()
	stream = simulate_data_stream(df, rate_per_second=10, verbose=True)
	await consume_data_stream(stream, max_n_rows=10)


if __name__ == "__main__":
	asyncio.run(_main())
