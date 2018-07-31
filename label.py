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
    def __init__(self, x=1000, y=1000, constructor=svgwrite.Drawing, elements=[], filename='labels.svg'):
        self.constructor = constructor
        self.x = x
        self.y = y
        self.points = [(x, y)]
        self.elements = elements
        self.type = 'svg'
        self.filename = filename

    def __getitem__(self, item):
        return self.elements[item]

    def __setitem__(self, key, value):
        assert type(key) is int, 'index must be number'
        self.elements[key] = value

    def append(self, element):
        assert type(element) is Element, 'not Element object'
        self.elements.append(element)

    def add(self, element):
        element.parent_element = self
        self.append(element)

    def build(self):
        dwg = self.constructor(self.filename, ("{}pt".format(self.y), "{}pt".format(self.y)))

        for element in self.elements:
            element.build(dwg)
        dwg.save()


class Element(RootElement):
    def __init__(self, points, type_of_element, style, elements=[], relative=True, text=None, parent_element=None):
        self.type = type_of_element
        self.elements = elements
        self.parent_element = parent_element
        self.points = points
        self.relative = relative
        self.style = style
        self.text = text

    def count_real_x_y(self):
        if not self.relative:
            return
        if self.parent_element.type == 'svg':
            xmin=0
            ymin=0
        else:
            xmin = self.parent_element.points[0][0]
            ymin = self.parent_element.points[0][0]

            for x, y in self.parent_element.points:
                print(xmin)
                print(x)
                if xmin > x:
                    xmin = x
                if ymin > y:
                    ymin = y
        points = [(x + xmin, y + ymin) for x, y in self.points]
        self.points = points


    def build(self, dwg):
        self.count_real_x_y()
        if self.type == 'polygon':
            new_el = svgwrite.shapes.Polygon(points=self.points, style=self.style)

        else:
            new_el = svgwrite.text.Text(self.text, self.points)

        dwg.add(new_el)
        for element in self.elements:
            element.build(dwg)

# test = RelElement(svgwrite.Drawing())
# print(test.params)

# generate_labels(1000, 1000, MARKS, 0)


drawing = RootElement()
points = [
    [50, 50],
    [100, 50],
    [100, 100],
    [50, 100],
    [50,50]
]

element = Element(points, 'polygon', style=color(MARKS, 3))
drawing.add(element)
points = [(x / 4, y / 4) for x, y in points]
print(points)
nested_Element = Element(points, 'text', 'fill:black;', text='Hello')
element.add(nested_Element)
drawing.build()
