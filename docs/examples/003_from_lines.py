"""A grid read from drawn lines (as exported from CAD), then its topology as a CellNetwork."""

from compas.geometry import Line
from compas_grid import Grid

posts = [Line([x, y, 0], [x, y, 3.0]) for x in (0, 6) for y in (0, 4)]
beams = [Line([0, 0, 3], [6, 0, 3.0002]), Line([0, 4, 3], [6, 4, 3]), Line([0, 0, 3], [0, 4, 3]), Line([6, 0, 3], [6, 4, 3])]

grid = Grid.from_lines(posts + beams, tolerance=0.001, level_tags=["S0", "Roof"])
print("u", grid.u, "v", grid.v, "levels", [round(z, 4) for z in grid.levels])

network = grid.to_cellnetwork()  # the topology of the whole grid, not the drawn members: beam edges on every level
print("vertices", network.number_of_vertices())
print("columns", len(list(network.edges_where(is_column=True))), "beams", len(list(network.edges_where(is_beam=True))))
print("beams on Roof", len(list(network.edges_where(is_beam=True, level="Roof"))))
print("floors", len(list(network.faces_where(is_floor=True))))
