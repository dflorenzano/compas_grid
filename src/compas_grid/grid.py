from compas.data import Data
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Transformation

LETTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ"  # I and O are left out: they read as 1 and 0


def letters(n):
    """The first ``n`` letter tags of a grid: A to Z without I and O, then AA, AB, ...

    Parameters
    ----------
    n : int
        Number of tags.

    Returns
    -------
    list[str]

    """
    tags = []
    size = len(LETTERS)
    for i in range(n):
        tag = ""
        k = i
        while k >= 0:
            tag = LETTERS[k % size] + tag
            k = k // size - 1
        tags.append(tag)
    return tags


def _check(name, values, tags):
    if len(values) < 1:
        raise ValueError("{} needs at least one position.".format(name))
    if any(b <= a for a, b in zip(values, values[1:])):
        raise ValueError("{} positions must increase strictly: {}".format(name, values))
    if len(tags) != len(values):
        raise ValueError("{} has {} positions but {} tags.".format(name, len(values), len(tags)))
    if len(set(tags)) != len(tags):
        raise ValueError("{} tags must be unique: {}".format(name, tags))


class Grid(Data):
    """An orthogonal structural grid: named axes in two plan directions and named levels.

    The grid lives in its own ``frame``. In that frame, a U axis is the line ``x = u[i]`` (it runs along y),
    a V axis is the line ``y = v[j]`` (it runs along x), and a level is the plane ``z = levels[k]``.
    This matches ``IfcGrid`` (``UAxes``, ``VAxes``, ``IfcGridAxis.AxisTag``) with storey elevations as levels.
    A rotated or moved grid is a grid with another frame.

    Every entity is identified by tags, not by indices, so keys stay valid when an axis is inserted:

    - intersection: ``(u_tag, v_tag)``, e.g. ``("B", "2")``;
    - node: ``(u_tag, v_tag, level_tag)``, e.g. ``("B", "2", "L1")``;
    - segment: two intersections next to each other on one axis, e.g. ``(("A", "1"), ("A", "2"))``;
    - bay: its lower and upper corner intersections, e.g. ``(("A", "1"), ("B", "2"))``.

    Parameters
    ----------
    u : list[float]
        Positions of the U axes along the frame's x-axis, strictly increasing.
    v : list[float]
        Positions of the V axes along the frame's y-axis, strictly increasing.
    levels : list[float], optional
        Elevations of the levels along the frame's z-axis, strictly increasing. Default ``[0.0]``.
    u_tags : list[str], optional
        Tags of the U axes. Default A, B, C, ... (no I, no O).
    v_tags : list[str], optional
        Tags of the V axes. Default 1, 2, 3, ...
    level_tags : list[str], optional
        Tags of the levels. Default L0, L1, L2, ...
    frame : :class:`compas.geometry.Frame`, optional
        Placement of the grid in the world. Default ``Frame.worldXY()``.
    name : str, optional
        Name of the grid.

    Examples
    --------
    >>> grid = Grid(u=[0, 6, 12], v=[0, 4], levels=[0.0, 3.2, 6.4])
    >>> grid.point("B", "2", "L1")
    Point(x=6.000, y=4.000, z=3.200)
    >>> grid.bays()
    [(('A', '1'), ('B', '2')), (('B', '1'), ('C', '2'))]

    """

    @property
    def __data__(self):
        return {
            "u": self.u,
            "v": self.v,
            "levels": self.levels,
            "u_tags": self.u_tags,
            "v_tags": self.v_tags,
            "level_tags": self.level_tags,
            "frame": self.frame,
            "name": self.name,
        }

    def __init__(self, u, v, levels=None, u_tags=None, v_tags=None, level_tags=None, frame=None, name=None):
        super(Grid, self).__init__(name=name)
        self.u = [float(x) for x in u]
        self.v = [float(y) for y in v]
        self.levels = [float(z) for z in (levels if levels is not None else [0.0])]
        self.u_tags = [str(t) for t in u_tags] if u_tags is not None else letters(len(self.u))
        self.v_tags = [str(t) for t in v_tags] if v_tags is not None else [str(j + 1) for j in range(len(self.v))]
        self.level_tags = [str(t) for t in level_tags] if level_tags is not None else ["L{}".format(k) for k in range(len(self.levels))]
        self.frame = frame or Frame.worldXY()
        _check("u", self.u, self.u_tags)
        _check("v", self.v, self.v_tags)
        _check("levels", self.levels, self.level_tags)

    def __repr__(self):
        return "Grid(u={!r}, v={!r}, levels={!r}, u_tags={!r}, v_tags={!r}, level_tags={!r}, frame={!r})".format(
            self.u, self.v, self.levels, self.u_tags, self.v_tags, self.level_tags, self.frame
        )

    @classmethod
    def from_spacings(cls, u, v, levels=None, **kwargs):
        """Make a grid from the spacings between axes and the heights between levels, starting at 0.

        Parameters
        ----------
        u : list[float]
            Spacings between consecutive U axes (bay widths along x).
        v : list[float]
            Spacings between consecutive V axes (bay depths along y).
        levels : list[float], optional
            Heights between consecutive levels (storey heights). Default: one level at 0.
        **kwargs
            Tags, frame and name, as for :class:`Grid`.

        Returns
        -------
        :class:`Grid`

        Examples
        --------
        >>> Grid.from_spacings([6, 6], [4], [3.2, 3.2]).levels
        [0.0, 3.2, 6.4]

        """

        def running(spacings):
            values = [0.0]
            for s in spacings:
                values.append(values[-1] + s)
            return values

        return cls(running(u), running(v), running(levels or []), **kwargs)

    # =============================================================================
    # Tags and indices
    # =============================================================================

    def _tags(self, direction):
        if direction == "u":
            return self.u_tags
        if direction == "v":
            return self.v_tags
        if direction == "w":
            return self.level_tags
        raise ValueError("direction must be 'u', 'v' or 'w', not {!r}".format(direction))

    def index(self, direction, tag):
        """Index of a U axis, V axis or level (``direction`` ``"u"``, ``"v"`` or ``"w"``) from its tag."""
        tags = self._tags(direction)
        if tag not in tags:
            raise KeyError("No {} axis tagged {!r}.".format(direction, tag))
        return tags.index(tag)

    def position(self, direction, tag):
        """Position of a U axis (x), V axis (y) or level (z, ``direction="w"``) in the grid's frame."""
        i = self.index(direction, tag)
        return {"u": self.u, "v": self.v, "w": self.levels}[direction][i]

    # =============================================================================
    # Topology
    # =============================================================================

    def intersections(self):
        """The intersections of the U and V axes, as ``(u_tag, v_tag)``, row by row from the first V axis."""
        return [(ut, vt) for vt in self.v_tags for ut in self.u_tags]

    def nodes(self, level=None):
        """The intersections on every level (or on one ``level``), as ``(u_tag, v_tag, level_tag)``."""
        levels = self.level_tags if level is None else [self.level_tags[self.index("w", level)]]
        return [(ut, vt, lt) for lt in levels for (ut, vt) in self.intersections()]

    def segments(self, direction=None):
        """The axis pieces between two intersections next to each other.

        Parameters
        ----------
        direction : {"u", "v", None}, optional
            ``"u"``: segments on the U axes (they run along y); ``"v"``: on the V axes (they run along x); ``None``: both.

        Returns
        -------
        list[tuple[tuple[str, str], tuple[str, str]]]

        """
        found = []
        if direction in (None, "u"):
            found += [((ut, a), (ut, b)) for ut in self.u_tags for a, b in zip(self.v_tags, self.v_tags[1:])]
        if direction in (None, "v"):
            found += [((a, vt), (b, vt)) for vt in self.v_tags for a, b in zip(self.u_tags, self.u_tags[1:])]
        if direction not in (None, "u", "v"):
            raise ValueError("direction must be 'u', 'v' or None, not {!r}".format(direction))
        return found

    def bays(self):
        """The bays, as their lower and upper corner intersections, row by row from the first V axis."""
        return [((u0, v0), (u1, v1)) for v0, v1 in zip(self.v_tags, self.v_tags[1:]) for u0, u1 in zip(self.u_tags, self.u_tags[1:])]

    # =============================================================================
    # Geometry
    # =============================================================================

    @property
    def transformation(self):
        """:class:`compas.geometry.Transformation` from the grid's frame to the world."""
        return Transformation.from_frame(self.frame)

    def local_point(self, u, v, level=None):
        """Point of a node in the grid's own frame (no ``level``: the first level)."""
        z = self.levels[0] if level is None else self.position("w", level)
        return Point(self.position("u", u), self.position("v", v), z)

    def point(self, u, v, level=None):
        """Point of a node in the world (no ``level``: the first level)."""
        return self.local_point(u, v, level).transformed(self.transformation)

    def line(self, start, end):
        """Line between two nodes ``(u_tag, v_tag, level_tag)``: a column line between levels, a beam line on a segment."""
        return Line(self.point(*start), self.point(*end))

    def axis_line(self, direction, tag, level=None, overhang=0.0):
        """The whole U or V axis at a level, extended by ``overhang`` past the outer axes at both ends."""
        z = self.levels[0] if level is None else self.position("w", level)
        if direction == "u":
            x = self.position("u", tag)
            a, b = Point(x, self.v[0] - overhang, z), Point(x, self.v[-1] + overhang, z)
        elif direction == "v":
            y = self.position("v", tag)
            a, b = Point(self.u[0] - overhang, y, z), Point(self.u[-1] + overhang, y, z)
        else:
            raise ValueError("direction must be 'u' or 'v', not {!r}".format(direction))
        return Line(a.transformed(self.transformation), b.transformed(self.transformation))

    def bay_polygon(self, bay, level=None):
        """The outline of a bay at a level, counter-clockwise from its lower corner."""
        (u0, v0), (u1, v1) = bay
        return Polygon([self.point(u0, v0, level), self.point(u1, v0, level), self.point(u1, v1, level), self.point(u0, v1, level)])
