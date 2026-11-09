from compas.data import Data
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.geometry import Vector
from compas.tolerance import TOL


class Placement(Data):
    """Where something sits on a grid: a node, offsets from it, and optionally a direction.

    A placement holds tags only, never the grid; it resolves against a grid with :meth:`frame` and :meth:`transformation`.
    This matches ``IfcGridPlacement``: ``at`` is the ``IfcVirtualGridIntersection`` (plus the level), ``offset`` its
    ``OffsetDistances``, ``toward`` the ``PlacementRefDirection``.

    The frame is the grid's frame, moved to the node plus ``offset``. With ``toward``, its x-axis points in plan from ``at``
    to that intersection (e.g. along a beam's segment); its z-axis stays the grid's z-axis. An element placed on the grid has
    ``element.transformation = placement.transformation(grid) * element_local_transformation``.

    Parameters
    ----------
    at : tuple[str, str, str]
        The node, as ``(u_tag, v_tag, level_tag)``.
    offset : tuple[float, float, float], optional
        Offsets (eccentricities) from the node along the grid's u, v and w directions. Default ``(0, 0, 0)``.
    toward : tuple[str, str], optional
        An intersection ``(u_tag, v_tag)`` the x-axis points to, in plan. Default: the grid's x-axis.
    name : str, optional
        Name of the placement.

    Examples
    --------
    >>> from compas_grid import Grid
    >>> grid = Grid(u=[0, 6], v=[0, 4], levels=[0, 3.2])
    >>> beam = Placement(("A", "1", "L1"), offset=(0, 0, -0.25), toward=("A", "2"))
    >>> beam.frame(grid)
    Frame(point=Point(x=0.000, y=0.000, z=2.950), xaxis=Vector(x=0.000, y=1.000, z=0.000), yaxis=Vector(x=-1.000, y=0.000, z=0.000))

    """

    @property
    def __data__(self):
        return {
            "at": list(self.at),
            "offset": list(self.offset),
            "toward": list(self.toward) if self.toward is not None else None,
            "name": self.name,
        }

    def __init__(self, at, offset=None, toward=None, name=None):
        super(Placement, self).__init__(name=name)
        if len(at) != 3:
            raise ValueError("at must be (u_tag, v_tag, level_tag), not {!r}".format(at))
        self.at = tuple(str(t) for t in at)
        self.offset = tuple(float(d) for d in (offset or (0.0, 0.0, 0.0)))
        if len(self.offset) != 3:
            raise ValueError("offset must have 3 values (u, v, w), not {!r}".format(offset))
        self.toward = tuple(str(t) for t in toward) if toward is not None else None
        if self.toward is not None and len(self.toward) != 2:
            raise ValueError("toward must be (u_tag, v_tag), not {!r}".format(toward))

    def __repr__(self):
        return "Placement(at={!r}, offset={!r}, toward={!r})".format(self.at, self.offset, self.toward)

    def frame(self, grid):
        """The frame of this placement on a grid, in the world.

        Parameters
        ----------
        grid : :class:`compas_grid.Grid`

        Returns
        -------
        :class:`compas.geometry.Frame`

        Raises
        ------
        KeyError
            If a tag is not in the grid.
        ValueError
            If ``toward`` is the intersection of ``at``.

        """
        u, v, level = self.at
        local = grid.local_point(u, v, level)
        du, dv, dw = self.offset
        origin = [local[0] + du, local[1] + dv, local[2] + dw]
        xaxis = Vector(1, 0, 0)
        if self.toward is not None:
            target = grid.local_point(self.toward[0], self.toward[1], level)
            xaxis = Vector(target[0] - local[0], target[1] - local[1], 0.0)
            if TOL.is_zero(xaxis.length):
                raise ValueError("toward {!r} is the intersection of at {!r}.".format(self.toward, self.at))
        yaxis = Vector(0, 0, 1).cross(xaxis)
        return Frame(origin, xaxis, yaxis).transformed(grid.transformation)

    def transformation(self, grid):
        """:class:`compas.geometry.Transformation` from the placement's frame on ``grid`` to the world."""
        return Transformation.from_frame(self.frame(grid))
