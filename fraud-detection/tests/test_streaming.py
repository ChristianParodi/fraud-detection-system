import random
import time

import pandas as pd
import pytest
from src.utils.streaming import simulate_streaming


@pytest.fixture
def slept(monkeypatch):
	"""Records every sleep instead of performing it, so tests never wait."""
	recorded = []
	# every function calling time.sleep(<arg>) in this test suite will call recorded.append(<arg>)
	monkeypatch.setattr(time, "sleep", recorded.append)
	return recorded


def test_yields_one_dict_per_row_preserving_column_names():
	df = pd.DataFrame({"income": [0.1, 0.2], "amount (EUR)": [10, 20]})

	rows = list(simulate_streaming(df))

	assert rows == [
		{"income": 0.1, "amount (EUR)": 10},
		{"income": 0.2, "amount (EUR)": 20},
	]


def test_sleeps_once_per_row_with_exponential_gaps(slept):
	df = pd.DataFrame({"income": [0.1, 0.2, 0.3]})

	random.seed(0)
	list(simulate_streaming(df, rate_per_second=100))

	random.seed(0)
	assert slept == [random.expovariate(100) for _ in range(3)]


def test_stops_early_without_paying_for_remaining_rows(slept):
	df = pd.DataFrame({"income": [0.1, 0.2, 0.3]})

	next(simulate_streaming(df))

	assert len(slept) == 1
