import svgwrite

MARKS = ['A+++', 'A++', 'A+', 'A', 'B', 'C', 'D', 'E', 'F']


def color(marks, index):
    steps_of_color = int(256 / len(marks) * 2) - 1
    index_of_yellow_label = int(len(marks) / 2)

    if index < index_of_yellow_label:
        r = abs(0 - index) * steps_of_color
        g = 255
        return 'fill:rgb({} {} {});'.format(r, g, 0)

    elif index > index_of_yellow_label:
        g = 255 - abs(index_of_yellow_label - index) * steps_of_color
        r = 255
        return 'fill:rgb({} {} {});'.format(r, g, 0)
    return 'fill:rgb({} {} {});'.format(255, 255, 0)  # yellow label


def generate_labels(height, width, marks, index, filename='labels.svg'):
    steps_of_width = width / (2 * len(marks))  # first label has half of width
    steps_of_height = height / (2 * len(marks) - 1)
    height_of_labels = steps_of_height - height / 100

    w_str = "{}pt".format(width)
    h_str = "{}pt".format(height)
    dwg = svgwrite.Drawing(filename, (w_str, h_str))
    label = dwg.add(dwg.g(id='labels', stroke='black'))
    #width /= 2
    for i in range(0, len(marks)):
        points = [
            [width / 100, 0 + i * steps_of_height],
            [width / 4 + i * steps_of_width, 0 + i * steps_of_height],
            [width / 4 + i * steps_of_width + width / 33, height_of_labels / 2 + i * steps_of_height],
            [width / 4 + i * steps_of_width, height_of_labels + i * steps_of_height],
            [width / 100, height_of_labels + i * steps_of_height],
            [width / 100, 0 + i * steps_of_height]
        ]

        polygon = svgwrite.shapes.Polygon(points=points, style=color(marks, i))

        text = svgwrite.text.Text(marks[i], (width / 20, height_of_labels / 2 + i * steps_of_height + 5))

        label.add(polygon)
        label.add(text)
    pointer = [
        [width / 4 + index * steps_of_width + width/33 * 3, steps_of_height * index],
        [width / 4 + index * steps_of_width + width/33 * 2, steps_of_height * index + height_of_labels / 2],
        [width / 4 + index * steps_of_width + width/33 * 3, steps_of_height * index + height_of_labels],
        [width, steps_of_height * index + height_of_labels],
        [width, steps_of_height * index]
    ]

    pointer = svgwrite.shapes.Polygon(points=pointer, style='fill:black;')
    label.add(pointer)

    border = dwg.add(dwg.g(id='border', stroke='white'))
    border.add(svgwrite.text.Text(
        marks[index],
        (
            width / 4 + index * steps_of_width + width / 33 * 2 + (width - width / 4 + index * steps_of_width + width / 33)/25  ,
            steps_of_height * index + height_of_labels / 2 + 5
        ),
        style='fill:white;'
    )
    )
    dwg.save()


generate_labels(1000, 1000, MARKS, 0)
