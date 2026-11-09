# COMPAS Grid

Structural grids and placements for building design tools in COMPAS.

A `Grid` is a set of tagged U axes, V axes and levels in its own frame, like `IfcGrid`. It gives intersections, nodes, segments, bays and their geometry, keyed by tags such as `("B", "2", "L1")`. A `Placement` locates something on a grid by a node, offsets and an optional direction, like `IfcGridPlacement`, and resolves to a frame and a transformation. An element on the grid has `element.transformation = placement.transformation(grid) * local`.

The package depends on `compas` only and has no element classes: element libraries, analysis models and IFC adapters use it. The `GridModel` and the elements of version 0.6.7 are at tag `v0.6.7`.

~~~python
from compas_grid import Grid, Placement

grid = Grid.from_spacings(u=[6.0, 6.0], v=[4.0], levels=[3.2, 3.2])
grid.point("B", "2", "L1")  # Point(6, 4, 3.2)
grid.bays()  # [(("A", "1"), ("B", "2")), (("B", "1"), ("C", "2"))]
beam = Placement(("A", "1", "L1"), offset=(0, 0, -0.25), toward=("B", "1"))
beam.transformation(grid)
~~~
