"""Columns at every node and beams on every V-axis segment of a grid, placed by Placement: element = placement * local."""

from compas.geometry import Box
from compas.geometry import Frame
from compas_grid import Grid
from compas_grid import Placement

grid = Grid.from_spacings(u=[6.0, 6.0], v=[4.0], levels=[3.2])
column = Box(0.2, 0.2, 2.7, Frame([0, 0, 1.35], [1, 0, 0], [0, 1, 0]))  # authored at its own origin, standing on z = 0
beam = Box(6.0, 0.15, 0.5, Frame([3.0, 0, -0.25], [1, 0, 0], [0, 1, 0]))  # along its x-axis, top at z = 0

columns = [column.transformed(Placement((u, v, "L0")).transformation(grid)) for u, v in grid.intersections()]
beams = [beam.transformed(Placement(a + ("L1",), toward=b).transformation(grid)) for a, b in grid.segments("v")]

print(len(columns), "columns,", len(beams), "beams")
print("column at C-2:", columns[-1].frame.point)
print("beam B-2 to C-2:", beams[-1].frame.point, beams[-1].frame.xaxis)
