# Changelog - Development Branch

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

* Added `compas_grid.Grid`: orthogonal grid of tagged U axes, V axes and levels in its own frame (rotated grids by frame), with intersections, nodes, segments, bays, points, lines, axis lines and bay polygons. Keys are axis tags, not indices.
* Added `Grid.from_spacings` and `compas_grid.letters`.
* Added `Grid.from_lines` (import adapter for drawn lines, merge tolerance) and `Grid.to_cellnetwork` (nodes, column and beam edges, bay faces).
* Added `compas_grid.Placement`: a node of a grid by tags, offsets (eccentricities) along u, v, w and an optional plan direction toward another intersection; `frame(grid)` and `transformation(grid)` resolve it (as `IfcGridPlacement`).
* Added `tests/test_grid.py`, `tests/test_placement.py` and examples `docs/examples/001_grid.py`, `002_placement.py`, `003_from_lines.py`.

### Changed

* Changed the README and the docs index to describe the grid and placement package.
* Changed the dependencies to `compas >= 2` only (no `compas_model`, no `compas_viewer`).

### Removed

* Removed `compas_grid.models` (`GridModel`) and `compas_grid.elements` (all element classes), their examples and `data/` files. They stay available at tag `v0.6.7`.


## [0.6.7] 2025-03-12

### Added

### Changed

### Removed

## [0.6.6] 2025-03-12

### Added

### Changed

- Test

### Removed


## [0.6.5] 2025-03-12

### Added

### Changed

- Test

### Removed


## [0.6.4] 2025-03-12

### Added

- Add transformation to gridmodel serialization.

### Changed

### Removed


## [0.6.3] 2025-03-12

### Added

### Changed

- Test

### Removed


## [0.6.1] 2025-03-12

### Added

### Changed

- Test

### Removed


## [0.6.0] 2025-03-12

### Added

### Changed

- Test

### Removed

## [0.5.0] 2025-03-12

### Added

### Changed
-   Alignment with compas_model transformations.

### Removed


## [0.3.0] 2025-01-22

### Added

### 

-   Preparation for CARBCOMN workshop.

### Removed


## [0.2.0] 2025-01-21

### Added

-   Added data-structures:`datastrucuture.cell_network`, `element_beam`, `element_column_head`, `element_column`, `element_plate`, `interface_cutter`, `model`.
-   Added shapes: `shape_column_head`
-   Added examples: `docs\examples\json_to_grid.py`

### Changed

### Removed

