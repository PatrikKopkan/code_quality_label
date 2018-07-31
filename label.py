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
    # width /= 2
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
        [width / 4 + index * steps_of_width + width / 33 * 3, steps_of_height * index],
        [width / 4 + index * steps_of_width + width / 33 * 2, steps_of_height * index + height_of_labels / 2],
        [width / 4 + index * steps_of_width + width / 33 * 3, steps_of_height * index + height_of_labels],
        [width, steps_of_height * index + height_of_labels],
        [width, steps_of_height * index]
    ]

    pointer = svgwrite.shapes.Polygon(points=pointer, style='fill:black;', transform='translate(-36 45.5)')
    # print(pointer.attribs)
    label.add(pointer)

    border = dwg.add(dwg.g(id='border', stroke='white'))
    border.add(svgwrite.text.Text(
        marks[index],
        (
            width / 4 + index * steps_of_width + width / 33 * 2 + (
                    width - width / 4 + index * steps_of_width + width / 33) / 25,
            steps_of_height * index + height_of_labels / 2 + 5
        ),
        style='fill:white;'
    )
    )
    #
    # border.add(svgwrite.text.Text(
    #   "your skill score: {} ".format(score)
    # ))
    dwg.save()

class RootElement:
    def __init__(self, x=1000, y=1000, constructor=svgwrite.Drawing(), elements=[], filename='labels.svg'):
        self.constructor = constructor
        self.x = x
        self.y = y
        self.elements = elements
        self.type = 'svg'
        self.filename= filename

    def __getitem__(self, item):
        return self.elements[item]

    def __setitem__(self, key, value):
        assert type(key) is int, 'index must be number'
        self.elements[key] = value

    def append(self, element):
        self.elements.append(element)

    def add(self, element):
        self.append(element)

    def build(self):
        dwg = self.constructor(self.filename, ("{}pt".format(self.y), "{}pt".format(self.y)))
        for element in self.elements:
            element.build(dwg)

class Element:
    def __init__(self, points, type_of_element, parent_element, style,elements=[], relative=True):
        self.type = type_of_element
        self.elements = elements
        self.parent_element = parent_element
        self.axis = self.count_real_x_y(points, relative)
        self.style = style

    def append(self, element):
        self.elements.append(element)

    def add(self, element):
        self.append(element)

    def __getitem__(self, item):
        return self.elements[item]

    def __setitem__(self, key, value):
        assert type(key) is int, 'index must be number'
        self.elements[key] = value

    def count_real_x_y(self, points, relative):
        if not relative:
            return points
        if self.parent_element.type_of_element == 'polygon':
            xmin = None
            xmax = None
            ymin = None
            ymax = None

            for x, y in self.parent_element.points:
                if xmin > x:
                    xmin = x
                if xmax < x:
                    xmax = x
                if ymin > y:
                    ymin = y
                if ymax < y:
                    ymax = y

            return [(x + self.parent_element.x, y + self.parent_element.y) for x, y in points]

        elif self.parent_element.type_of_element != 'polygon':

    def build(self, dwg):
        if self.type == 'polygon':
            new_el = svgwrite.shapes.Polygon(points=self.points, style=self.style)
            dwg.add(new_el)
            for element in self.elements:
                element.build(dwg)


# test = RelElement(svgwrite.Drawing())

# print(test.params)
generate_labels(1000, 1000, MARKS, 0)
