compas_grid
===========

Structural grids and placements for building design tools in COMPAS.

- `Grid`: tagged U axes, V axes and levels in its own frame (as `IfcGrid`). Intersections, nodes, segments and bays, keyed by tags such as `("B", "2", "L1")`; points, lines, axis lines and bay polygons in the world. `Grid.from_spacings`, `Grid.from_lines` (drawn input), `Grid.to_cellnetwork`.
- `Placement`: a node of a grid, offsets along u, v, w and an optional direction toward another intersection (as `IfcGridPlacement`). `placement.frame(grid)`, `placement.transformation(grid)`; an element on the grid has `element.transformation = placement.transformation(grid) * local`.

`compas_grid` depends on `compas` only. It has no element classes. The `GridModel` and the elements of version 0.6.7 are at tag `v0.6.7`.

~~~python
from compas_grid import Grid, Placement

grid = Grid.from_spacings(u=[6.0, 6.0], v=[4.0], levels=[3.2, 3.2])
grid.point("B", "2", "L1")                      # Point(6, 4, 3.2)
grid.bays()                                     # [(("A", "1"), ("B", "2")), (("B", "1"), ("C", "2"))]
beam = Placement(("A", "1", "L1"), offset=(0, 0, -0.25), toward=("B", "1"))
beam.transformation(grid)
~~~

Installation
------------

To install the latest version for development:

~~~bash
git clone https://github.com/dflorenzano/compas_grid.git
cd compas_grid
pip install -e ".[dev]"
~~~

Tests
-----

~~~bash
pytest --doctest-modules src tests
~~~

Examples
--------

`docs/examples/001_grid.py`, `002_placement.py`, `003_from_lines.py`.
