import math

import pytest

from compas.data import json_dumps
from compas.data import json_loads
from compas.geometry import Frame
from compas.geometry import Rotation
from compas.geometry import Translation
from compas.tolerance import TOL
from compas_grid import Grid
from compas_grid import letters


@pytest.fixture
def grid():
    return Grid(u=[0, 6, 12], v=[0, 4], levels=[0.0, 3.2, 6.4])


def test_default_tags(grid):
    assert grid.u_tags == ["A", "B", "C"]
    assert grid.v_tags == ["1", "2"]
    assert grid.level_tags == ["L0", "L1", "L2"]


def test_letters_skip_i_and_o():
    tags = letters(26)
    assert "I" not in tags and "O" not in tags
    assert tags[7:9] == ["H", "J"]
    assert tags[23:26] == ["Z", "AA", "AB"]


def test_counts(grid):
    assert len(grid.intersections()) == 6
    assert len(grid.nodes()) == 18
    assert len(grid.nodes("L1")) == 6
    assert len(grid.segments("u")) == 3  # A, B, C each from 1 to 2
    assert len(grid.segments("v")) == 4  # 1 and 2 each A-B, B-C
    assert len(grid.segments()) == 7
    assert grid.bays() == [(("A", "1"), ("B", "2")), (("B", "1"), ("C", "2"))]


def test_irregular_axes_and_spacings():
    a = Grid(u=[0, 5, 12], v=[0, 4, 7], levels=[0, 3, 7])
    b = Grid.from_spacings(u=[5, 7], v=[4, 3], levels=[3, 4])
    assert a.u == b.u and a.v == b.v and a.levels == b.levels
    assert a.point("C", "3", "L2") == [12, 7, 7]


def test_point_line_and_bay(grid):
    assert grid.point("B", "2", "L1") == [6, 4, 3.2]
    assert grid.point("B", "2") == [6, 4, 0]
    column = grid.line(("B", "1", "L0"), ("B", "1", "L1"))
    assert TOL.is_close(column.length, 3.2)
    assert grid.axis_line("u", "B", "L1", overhang=1.0).start == [6, -1, 3.2]
    polygon = grid.bay_polygon((("B", "1"), ("C", "2")), "L2")
    assert TOL.is_close(polygon.area, 24.0)
    assert polygon.points[0] == [6, 0, 6.4]


def test_custom_tags_are_stable_keys():
    a = Grid(u=[0, 6], v=[0, 4], u_tags=["A", "C"])
    b = Grid(u=[0, 3, 6], v=[0, 4], u_tags=["A", "B", "C"])  # an axis inserted between A and C
    assert a.point("C", "2") == b.point("C", "2")
    assert a.index("u", "C") == 1 and b.index("u", "C") == 2


def test_rotated_and_moved_frame():
    frame = Frame([10, 20, 1], [1, 0, 0], [0, 1, 0]).transformed(Rotation.from_axis_and_angle([0, 0, 1], math.radians(90), point=[10, 20, 1]))
    grid = Grid(u=[0, 6], v=[0, 4], levels=[0, 3], frame=frame)
    assert grid.point("A", "1", "L0") == [10, 20, 1]
    assert TOL.is_allclose(grid.point("B", "1", "L1"), [10, 26, 4])  # u runs along world y after 90 degrees
    assert TOL.is_allclose(grid.point("A", "2", "L0"), [6, 20, 1])
    moved = grid.transformation * Translation.from_vector([6, 4, 3])
    assert TOL.is_allclose(Frame.worldXY().transformed(moved).point, grid.point("B", "2", "L1"))


def test_data_roundtrip(grid):
    grid.frame = Frame([1, 2, 3], [0, 1, 0], [-1, 0, 0])
    other = json_loads(json_dumps(grid))
    assert isinstance(other, Grid)
    assert other.__data__ == grid.__data__
    assert other.point("C", "2", "L2") == grid.point("C", "2", "L2")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"u": [], "v": [0]},
        {"u": [0, 0], "v": [0]},
        {"u": [6, 0], "v": [0]},
        {"u": [0, 6], "v": [0], "u_tags": ["A"]},
        {"u": [0, 6], "v": [0], "u_tags": ["A", "A"]},
        {"u": [0], "v": [0], "levels": [3, 0]},
    ],
)
def test_invalid_grids(kwargs):
    with pytest.raises(ValueError):
        Grid(**kwargs)


def test_unknown_tag_and_direction(grid):
    with pytest.raises(KeyError):
        grid.point("Z", "1")
    with pytest.raises(ValueError):
        grid.index("x", "A")
    with pytest.raises(ValueError):
        grid.segments("w")
