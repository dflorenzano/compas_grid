import math

import pytest

from compas.data import json_dumps
from compas.data import json_loads
from compas.geometry import Box
from compas.geometry import Frame
from compas.geometry import Rotation
from compas.geometry import Translation
from compas.tolerance import TOL
from compas_grid import Grid
from compas_grid import Placement


@pytest.fixture
def grid():
    return Grid(u=[0, 6, 12], v=[0, 4], levels=[0.0, 3.2])


def test_node_placement_is_grid_frame_at_node(grid):
    frame = Placement(("B", "2", "L1")).frame(grid)
    assert frame.point == [6, 4, 3.2]
    assert TOL.is_allclose(frame.xaxis, [1, 0, 0]) and TOL.is_allclose(frame.yaxis, [0, 1, 0])


def test_offsets_are_eccentricities_along_u_v_w(grid):
    frame = Placement(("B", "1", "L1"), offset=(0.1, -0.2, -0.5)).frame(grid)
    assert TOL.is_allclose(frame.point, [6.1, -0.2, 2.7])


def test_toward_points_x_along_the_segment(grid):
    along_v = Placement(("A", "1", "L1"), toward=("B", "1")).frame(grid)
    along_u = Placement(("A", "1", "L1"), toward=("A", "2")).frame(grid)
    assert TOL.is_allclose(along_v.xaxis, [1, 0, 0])
    assert TOL.is_allclose(along_u.xaxis, [0, 1, 0]) and TOL.is_allclose(along_u.zaxis, [0, 0, 1])
    with pytest.raises(ValueError):
        Placement(("A", "1", "L1"), toward=("A", "1")).frame(grid)


def test_rotated_grid():
    frame = Frame([10, 20, 0], [1, 0, 0], [0, 1, 0]).transformed(Rotation.from_axis_and_angle([0, 0, 1], math.radians(90), point=[10, 20, 0]))
    grid = Grid(u=[0, 6], v=[0, 4], levels=[0, 3], frame=frame)
    placed = Placement(("B", "1", "L1"), offset=(0, 0.5, 0)).frame(grid)
    assert TOL.is_allclose(placed.point, [9.5, 26, 3])
    assert TOL.is_allclose(placed.xaxis, [0, 1, 0])


def test_element_transformation_is_placement_times_local(grid):
    box = Box(0.2, 0.2, 3.0, Frame([0, 0, 1.5], [1, 0, 0], [0, 1, 0]))  # a column authored at its own origin, standing on z = 0
    local = Translation.from_vector([0, 0, 0.0])
    placement = Placement(("C", "2", "L0"))
    placed = box.transformed(placement.transformation(grid) * local)
    assert TOL.is_allclose(placed.frame.point, [12, 4, 1.5])


def test_data_roundtrip():
    placement = Placement(("A", "2", "L1"), offset=(0, 0, -0.25), toward=("B", "2"), name="beam")
    other = json_loads(json_dumps(placement))
    assert isinstance(other, Placement)
    assert other.__data__ == placement.__data__
    assert Placement.__from_data__(Placement(("A", "1", "L0")).__data__).toward is None


def test_invalid_placements(grid):
    with pytest.raises(ValueError):
        Placement(("A", "1"))
    with pytest.raises(ValueError):
        Placement(("A", "1", "L0"), offset=(1, 2))
    with pytest.raises(ValueError):
        Placement(("A", "1", "L0"), toward=("A",))
    with pytest.raises(KeyError):
        Placement(("A", "9", "L0")).frame(grid)
