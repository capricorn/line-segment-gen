from math import tan, atan, pi, dist
from random import randint
from PIL import Image, ImageDraw

im = Image.new('L', (500, 500), 256)
draw = ImageDraw.Draw(im)

# Initial line segment for seeding generation.
lines = [
    (
        (im.size[0]/8, im.size[0]/8),
        (im.size[0]-im.size[0]/8, im.size[1]-im.size[1]/8)
    )
]

def slope(point_a, point_b):
    xa, ya = point_a
    xb, yb = point_b

    if xb - xa == 0:
        print("Division by zero")
        return 1

    return (yb - ya) / (xb - xa)

def intersection_segment(segment, point):
    ''' Generate the normal line segment normal from point to segment '''

    start_point, end_point = segment
    seg_slope = slope(start_point, end_point)
    seg_line = lambda x: seg_slope*(x - end_point[0]) + end_point[1]

    normal_slope = tan((atan(seg_slope) + pi/2))
    normal_line = lambda x: normal_slope*(x - point[0]) + point[1]

    # Next, compute 'x' intersection point
    xi = (normal_slope*point[0] - point[1] - seg_slope*end_point[0] + end_point[1]) / \
        (normal_slope - seg_slope)

    return (point, (xi, normal_line(xi)))

def normal_to_segment(segment, point):
    ''' Returns true if point has a normal line intersection to segment '''

    segment_i = intersection_segment(segment, point)

    _, point_i = segment_i

    start_point, end_point = segment
    min_x = min(start_point[0], end_point[0])
    max_x = max(start_point[0], end_point[0])
    min_y = min(start_point[1], end_point[1])
    max_y = max(start_point[1], end_point[1])
    new_x, new_y = point_i
    in_bounds = (new_x >= min_x and new_x <= max_x) and \
        (new_y >= min_y and new_y <= max_y)

    return in_bounds

def generate_point():
    ''' Generate a random point that can normally intersect an existing segment '''
    new_point = (randint(0,im.size[0]-1), randint(0,im.size[1]-1))
    for segment in lines:
        if normal_to_segment(segment, new_point):
            return new_point

    return None

def add_line(lines):
    while True:
        new_point = generate_point()
        if new_point:
            break
                
    new_segments = []
    for segment in lines:
        # Important, otherwise out of bounds of existing segments
        if normal_to_segment(segment, new_point) == False:
            continue
        # The intersection segment
        new_segment = intersection_segment(segment, new_point)
        new_segments.append(new_segment)
    
    minimum = new_segments[0]
    for segment in new_segments:
        if dist(*segment) < dist(*minimum):
            minimum = segment
    
    return minimum

def point_tuple(point):
    ''' Expand a point of the form ((a,b),(c,d)) to (a,b,c,d) '''
    return (*point[0], *point[1])

images = []
draw.line(point_tuple(lines[0]))
for i in range(100):
    new_segment = add_line(lines)
    lines.append(new_segment)
    draw.line(point_tuple(new_segment))
    images.append(im.copy())

images[0].save('out.gif', save_all=True, append_images=images[1:])