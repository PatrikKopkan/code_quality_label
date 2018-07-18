import svgwrite
from svgwrite import px
MARKS = ['A+++', 'A++', 'A+', 'A','B','C','D']

def color(marks, index):
    steps_of_color = int(256/len(marks)*2) - 1
    index_of_green_label = 0
    index_of_yellow_label = int(len(marks)/2)
    index_of_red_label = len(marks)-1

    if index < index_of_yellow_label:
        r = abs(0 - index) * steps_of_color
        g = 255
        return r, g, 0

    elif index > index_of_yellow_label:
        g = 255 - abs(index_of_yellow_label - index) * steps_of_color
        r = 255
        return r, g, 0
    return 255, 255, 0 # yellow label

def generate_labels(height, width, marks):

    steps_of_width = width/(2 * len(marks)) # first label has half of width
    steps_of_height = height / ((2*len(marks) - 1))
    height_of_labels = steps_of_height

    w_str = "{}pt".format(width)
    h_str = "{}pt".format(height)
    dwg = svgwrite.Drawing('labels.svg', (w_str, h_str))
    label = dwg.add(dwg.g(id='label', stroke='green'))
    i = 1
    points = [
        [0, 0],
        [width/2, 0],
        [width/2 + 30, height_of_labels/2],
        [width/2, height_of_labels],
        [0, height_of_labels],
        [0, 0]
    ]

    polygon = svgwrite.shapes.Polygon(points=points)
    label.add(dwg.line(start=(0*px, 0*px), end=(200*px, 200*px)))
    label.add(polygon)
    dwg.save()

generate_labels(1000,1000,MARKS)

