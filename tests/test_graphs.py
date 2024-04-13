import pytest
from bot.graphs_and_stats import *

def test_cumulative_graph():
    assert isinstance(cumululative_graph(), File)