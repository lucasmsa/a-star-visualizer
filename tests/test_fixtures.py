import json
from pathlib import Path

import pytest

from astar.grid import Grid
from astar.search import a_star

FIXTURES = sorted((Path(__file__).resolve().parents[1] / "fixtures").glob("*.json"))


@pytest.mark.parametrize("path", FIXTURES, ids=[p.stem for p in FIXTURES])
def test_golden_fixture_is_reproduced(path):
    data = json.loads(path.read_text())
    grid = Grid.from_strings(data["grid"])
    result = a_star(
        grid,
        tuple(data["start"]),
        tuple(data["goal"]),
        connectivity=data["connectivity"],
        heuristic=data["heuristic"],
    )
    assert result.found == data["found"]
    assert [list(p) for p in result.path] == data["path"]
    assert [list(p) for p in result.expansion_order] == data["expansionOrder"]
    assert result.cost == pytest.approx(data["cost"], abs=1e-9)


def test_there_are_three_fixtures():
    assert len(FIXTURES) == 3
