********************************************************************************
compas_grid
********************************************************************************

.. rst-class:: lead

.. figure:: /_images/compas_grid.jpg
   :figclass: figure
   :class: figure-img img-fluid


COMPAS Grid gives structural grids and placements for building design tools in COMPAS. A ``Grid`` is a set of tagged U axes, V axes and levels in its own frame, like ``IfcGrid``: it gives intersections, nodes, segments, bays and their geometry, keyed by tags (``("B", "2", "L1")``). A ``Placement`` locates something on a grid by a node, offsets and an optional direction, like ``IfcGridPlacement``, and resolves to a frame and a transformation. The package depends on ``compas`` only and has no element classes: element libraries, analysis models and IFC adapters use it.


Table of Contents
=================

.. toctree::
   :maxdepth: 3
   :titlesonly:

   Introduction <self>
   installation
   tutorial
   examples
   api
   license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
