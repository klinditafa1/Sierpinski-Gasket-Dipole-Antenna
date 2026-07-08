import FreeCAD as App
import Part
from FreeCAD import Vector
import math

doc = App.newDocument("Sierpinski_Dipole")

# =====================================
# PARAMETERS
# =====================================

WIDTH_TOTAL = 88.0
HEIGHT_TOTAL = 48.68

GAP = 2.0
COPPER = 0.035

ITERATION = 2

# =====================================
# LEFT TRIANGLE DIMENSIONS
# =====================================

SIDE = HEIGHT_TOTAL / (math.sqrt(3)/2)

# =====================================
# SIERPINSKI CUTS
# =====================================

cuts = []

def sierpinski_holes(p1,p2,p3,depth):

    if depth == 0:
        return

    m12 = (
        (p1[0]+p2[0])/2,
        (p1[1]+p2[1])/2
    )

    m23 = (
        (p2[0]+p3[0])/2,
        (p2[1]+p3[1])/2
    )

    m31 = (
        (p3[0]+p1[0])/2,
        (p3[1]+p1[1])/2
    )

    cuts.append((m12,m23,m31))

    sierpinski_holes(p1,m12,m31,depth-1)
    sierpinski_holes(m12,p2,m23,depth-1)
    sierpinski_holes(m31,m23,p3,depth-1)

# =====================================
# LEFT MAIN TRIANGLE
# =====================================

h = HEIGHT_TOTAL

p1 = (0,0)
p2 = (0,h)
p3 = (SIDE*math.sqrt(3)/2,h/2)

wire = Part.makePolygon([
    Vector(*p1,0),
    Vector(*p2,0),
    Vector(*p3,0),
    Vector(*p1,0)
])

left_face = Part.Face(wire)

# =====================================
# CREATE HOLES
# =====================================

cuts.clear()

sierpinski_holes(
    p1,
    p2,
    p3,
    ITERATION
)

for tri in cuts:

    poly = Part.makePolygon([
        Vector(tri[0][0],tri[0][1],0),
        Vector(tri[1][0],tri[1][1],0),
        Vector(tri[2][0],tri[2][1],0),
        Vector(tri[0][0],tri[0][1],0)
    ])

    hole = Part.Face(poly)

    left_face = left_face.cut(hole)

# =====================================
# EXTRUDE
# =====================================

left_shape = left_face.extrude(
    Vector(0,0,COPPER)
)

# =====================================
# POSITION LEFT
# =====================================

left_shape.translate(
    Vector(
        WIDTH_TOTAL/2 - GAP/2 - p3[0],
        0,
        0
    )
)

# =====================================
# RIGHT SIDE
# =====================================

right_shape = left_shape.mirror(
    Vector(WIDTH_TOTAL/2,0,0),
    Vector(1,0,0)
)

# =====================================
# FEED PADS
# =====================================

feed_w = 1.5
feed_h = 4.0

feed1 = Part.makeBox(
    feed_w,
    feed_h,
    COPPER
)

feed1.translate(
    Vector(
        WIDTH_TOTAL/2 - GAP/2 - feed_w,
        HEIGHT_TOTAL/2 - feed_h/2,
        0
    )
)

feed2 = Part.makeBox(
    feed_w,
    feed_h,
    COPPER
)

feed2.translate(
    Vector(
        WIDTH_TOTAL/2 + GAP/2,
        HEIGHT_TOTAL/2 - feed_h/2,
        0
    )
)

# =====================================
# COMBINE
# =====================================

antenna = left_shape.fuse(right_shape)
antenna = antenna.fuse(feed1)
antenna = antenna.fuse(feed2)

obj = doc.addObject(
    "Part::Feature",
    "SierpinskiDipole"
)

obj.Shape = antenna

doc.recompute()

print("Sierpinski Dipole Generated")