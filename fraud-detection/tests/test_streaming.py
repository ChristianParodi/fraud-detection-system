import asyncio
import random

import pandas as pd
import pytest
from src.utils import streaming
from src.utils.streaming import consume_data_stream, simulate_data_stream


@pytest.fixture
def slept(monkeypatch):
	"""Records every sleep instead of performing it, so tests never wait."""
	recorded = []

	async def fake_sleep(delay):
		recorded.append(delay)

	monkeypatch.setattr(streaming.asyncio, "sleep", fake_sleep)
	return recorded


async def collect(stream):
	return [row async for row in stream]


def test_yields_one_dict_per_row_preserving_column_names():
	df = pd.DataFrame({"income": [0.1, 0.2], "amount (EUR)": [10, 20]})

	rows = asyncio.run(collect(simulate_data_stream(df)))

	assert rows == [
		{"income": 0.1, "amount (EUR)": 10},
		{"income": 0.2, "amount (EUR)": 20},
	]


def test_sleeps_once_per_row_with_exponential_gaps(slept):
	df = pd.DataFrame({"income": [0.1, 0.2, 0.3]})

	random.seed(0)
	asyncio.run(collect(simulate_data_stream(df, rate_per_second=100)))

	random.seed(0)
	assert slept == [random.expovariate(100) for _ in range(3)]


def test_consumer_stops_early_without_paying_for_remaining_rows(slept):
	df = pd.DataFrame({"income": [0.1, 0.2, 0.3]})

	asyncio.run(consume_data_stream(simulate_data_stream(df), max_n_rows=1))

	assert len(slept) == 1


def test_rejects_non_positive_rate():
	df = pd.DataFrame({"income": [0.1]})

	with pytest.raises(ValueError):
		asyncio.run(collect(simulate_data_stream(df, rate_per_second=0)))


def test_rejects_non_positive_max_rows():
	df = pd.DataFrame({"income": [0.1]})

	with pytest.raises(ValueError):
		asyncio.run(consume_data_stream(simulate_data_stream(df), max_n_rows=0))
