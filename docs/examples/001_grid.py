"""A grid of 2 x 1 bays and 2 storeys, rotated by 30 degrees: tags, nodes, lines and bays."""

import math

from compas.geometry import Frame
from compas.geometry import Rotation
from compas_grid import Grid

frame = Frame.worldXY().transformed(Rotation.from_axis_and_angle([0, 0, 1], math.radians(30)))
grid = Grid.from_spacings(u=[6.0, 6.0], v=[4.0], levels=[3.2, 3.2], level_tags=["S0", "S1", "Roof"], frame=frame)

print(grid.u_tags, grid.v_tags, grid.level_tags)
print("intersections:", grid.intersections())
print("bays:", grid.bays())
print("B-2 on S1:", grid.point("B", "2", "S1"))
print("column B-1, S0 to S1:", grid.line(("B", "1", "S0"), ("B", "1", "S1")))
print("beams on the U axes:", len(grid.segments("u")), "on the V axes:", len(grid.segments("v")))
print("bay A1-B2 on Roof:", grid.bay_polygon((("A", "1"), ("B", "2")), "Roof"))
