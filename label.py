import svgwrite

MARKS = ['A+++', 'A++', 'A+', 'A', 'B', 'C', 'D', 'E', 'F']


def color(marks, index):
    """
    function generating color

    :param marks:
    :param index:
    :return: string of color
    """
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


def generate_labels(height, width, marks, index, container_px=0, container_py=0):
    """
    :param height:
    :param width:
    :param marks: list of marks
    :param index: which label to point in marks
    :param container_px: x position of container
    :param container_py: y position of container
    :return: container which contains paramaters of generated labels
    """
    steps_of_width = width / (2 * len(marks))  # first label has half of width
    steps_of_height = height / (2 * len(marks) - 1)
    height_of_labels = steps_of_height - height / 100

    container = Element([(container_px, container_py)], 'container', '')
    # width /= 2
    for i in range(0, len(marks)):
        points = [
            [0, 0 + i * steps_of_height],
            [width / 4 + i * steps_of_width, 0 + i * steps_of_height],
            [width / 4 + i * steps_of_width + width / 33, height_of_labels / 2 + i * steps_of_height],
            [width / 4 + i * steps_of_width, height_of_labels + i * steps_of_height],
            [0, height_of_labels + i * steps_of_height],
            [0, 0 + i * steps_of_height]
        ]
        print(points)

        # polygon = svgwrite.shapes.Polygon(points=points, style=color(marks, i))
        polygon = Element(points, 'polygon', style=color(marks, i) + 'stroke:black;stroke-width:2;')
        # text = svgwrite.text.Text(marks[i], (width / 20, height_of_labels / 2 + i * steps_of_height + 5))
        text = Element([(width / 20, height_of_labels / 2 + i * steps_of_height + 5)], 'text', '', text=marks[i])
        container.add(polygon)
        container.add(text)
    pointer = [
        [width / 4 + index * steps_of_width + width / 33 * 3, steps_of_height * index],
        [width / 4 + index * steps_of_width + width / 33 * 2, steps_of_height * index + height_of_labels / 2],
        [width / 4 + index * steps_of_width + width / 33 * 3, steps_of_height * index + height_of_labels],
        [width, steps_of_height * index + height_of_labels],
        [width, steps_of_height * index]
    ]

    # pointer = svgwrite.shapes.Polygon(points=pointer, style='fill:black;', transform='translate(-36 45.5)')
    pointer = Element(pointer, 'polygon', style='fill:black;')
    # print(pointer.attribs)
    container.add(pointer)

    container.add(Element(
        [(
            width / 4 + index * steps_of_width + width / 33 * 2 + (
                    width - width / 4 + index * steps_of_width + width / 33) / 25,
            steps_of_height * index + height_of_labels / 2 + 5
        )], 'text', 'white', text=marks[index]
    )
    )

    #
    # border.add(svgwrite.text.Text(
    #   "your skill score: {} ".format(score)
    # ))
    ymax = height_of_labels + (len(marks) - 1) * steps_of_height
    return container, ymax


class RootElement:
    """
    Class to implement behavior of relative axis in svg.
    """
    id = 0

    def __init__(self, x=1000, y=1000, constructor=svgwrite.Drawing, filename='labels.svg'):
        """

        :param x: x size of svg element in svg
        :param y: y size of svg element in svg
        :param constructor: constructor of library svgwrite for element
        :param filename: filename or path to save
        """
        self.constructor = constructor
        self.x = x
        self.y = y
        self.points = [(x, y)]
        # print(self.points)
        self.elements = []
        self.type = 'svg'
        self.filename = filename
        self.id = 1 + RootElement.id
        RootElement.id += 1
        # print(self.id)

    def __getitem__(self, item):
        return self.elements[item]

    # def __setitem__(self, key, value):
    #     assert type(key) is int, 'index must be number'
    #     self.elements[key] = value

    def append(self, element):
        """
        adds element to list of elements
        :param element: instance of Element
        :type element: Element
        """
        # assert type(element) is Element, 'not Element object'
        self.elements.append(element)

    def add(self, element):
        """
        calls append and set element.parent_element to self
        :param element: instance of Element
        :type element: Element
        """
        self.append(element)
        # print(element)
        # print(self)
        element.parent_element = self
        # print(element)

    def build(self):
        """
        generate svg document
        """
        dwg = self.constructor(self.filename, ("{}pt".format(self.y), "{}pt".format(self.y)))

        for element in self.elements:
            element.build(dwg)
        dwg.save()

    def __str__(self):
        return 'id: {} size: {} elements: {}'.format(self.id, self.points, self.elements)


class Element(RootElement):


    """
    Class to implement behavior of relative axis in svg.
    """
    def __init__(self, points, type_of_element, style, relative=True, text=None, parent_element=None):
        """
        :param self:
        :param points: tuple or list of x points and y points
        :type points: ((int),(int))
        :param type_of_element: tells which element of svg, you want to create
        :type type_of_element: str
        :param style: style of element to pass
        :type style: str
        :param relative: if set to True, object will calculate absolute axis.
        :param text: text for text element in svg, leave None if type_of_element is not 'text'
        :param parent_element: element from which will be generated absolute axis
        :type relative: bool
        """

        self.type = type_of_element
        self.elements = []
        self.parent_element = parent_element
        self.points = points
        # print(points)
        self.relative = relative
        self.style = style
        self.text = text
        RootElement.id += 1
        self.id = RootElement.id
        # print(self.id)

    def count_real_x_y(self):
        """counts absolute axis if self.realative is set to True"""
        if not self.relative:
            return
        if self.parent_element.type == 'svg':
            xmin = 0
            ymin = 0
        else:
            xmin = self.parent_element.points[0][0]
            ymin = self.parent_element.points[0][0]

            for x, y in self.parent_element.points:
                # print(xmin)
                # print(x)
                if xmin > x:
                    xmin = x
                if ymin > y:
                    ymin = y
        # print(self.points)
        points = [(x + xmin, y + ymin) for x, y in self.points]
        self.points = points

    def build(self, dwg):
        """ generate svg document
        :param dwg: object of swgwrite.Drawing
        :type dwg: swgwrite.Drawing
        """
        self.count_real_x_y()
        if self.type != 'container' or self.type == 'table':

            if self.type == 'polygon':
                new_el = svgwrite.shapes.Polygon(points=self.points, style=self.style)

            elif self.type == 'text':
                new_el = svgwrite.text.Text(self.text, (self.points[0][0], self.points[0][1]), fill=self.style)

            dwg.add(new_el)
        for element in self.elements:
            # print(element)
            element.build(dwg)

    def __len__(self):
        return len(self.elements)


class Table(Element):
    """
    Class which implements Tables in svg
    """
    def __init__(self, points, length_of_row, length_of_column, padding=5, stroke_width=2, parent_element=None,
                 relative=True):
        """

        :param points: tuple of starting position of the table
        :type points: (int,int)
        :param length_of_row: length of row
        :param length_of_column: length of column
        :param padding: padding of text in table
        :param stroke_width: border width of table
        :type stroke_width: int, float
        :param parent_element: instance of Element or RootElement
        :type parent_element: Element, RootElement
        :param relative: if set to True, object will calculate absolute axis.
        :type relative: bool
        """
        self.elements = []  # rows
        self.points = points
        self.length_of_row = length_of_row
        self.length_of_column = length_of_column
        self.padding = padding
        self.type = 'table'
        self.stroke_width = stroke_width
        self.parent_element = parent_element
        self.relative = relative
        self.id = 1 + RootElement.id
        RootElement.id += 1

    def build(self, dwg):
        """
        generate svg document
        :param dwg: object of swgwrite.Drawing
        :type dwg: swgwrite.Drawing
        """
        self.count_real_x_y()
        print(self.points)
        # for paramater, score, counter in enumerate(self.elements):
        counter = 0
        for paramater, score in self.elements.items():  # todo add atribute font-size
            paramater = svgwrite.text.Text(paramater, (self.points[0][0] + 0.1 * self.length_of_column,
                                                       self.points[0][1] + (0.5 + counter) * self.length_of_row + 5
                                                       )
                                           )

            score = svgwrite.text.Text(score, (self.points[0][0] + 1.1 * self.length_of_column,
                                               self.points[0][1] + (0.5 + counter) * self.length_of_row + 5
                                               )
                                       )

            x = self.points[0][0]
            y = self.points[0][1]
            points = [
                (x, y + counter * self.length_of_row),
                (x + self.length_of_column, y + counter * self.length_of_row),
                (x + self.length_of_column, y + (counter + 1) * self.length_of_row),
                (x, y + (counter + 1) * self.length_of_row),
                (x, y + counter * self.length_of_row)
            ]
            first_column = svgwrite.shapes.Polygon(points, style='fill:none; stroke:black;stroke-width:{};'.format(
                self.stroke_width))

            points = [  # todo write list comprehnsion
                (x + self.length_of_column, y + counter * self.length_of_row),
                (x + self.length_of_column * 2, y + counter * self.length_of_row),
                (x + self.length_of_column * 2, y + (counter + 1) * self.length_of_row),
                (x + self.length_of_column, y + (counter + 1) * self.length_of_row),
                (x + self.length_of_column, y + counter * self.length_of_row)
            ]

            second_column = svgwrite.shapes.Polygon(points, style='fill:none; stroke:black;stroke-width:{};'.format(
                self.stroke_width))

            dwg.add(paramater)
            dwg.add(score)
            dwg.add(first_column)
            dwg.add(second_column)
            counter += 1
    # def build(self, dwg): # todo generating n*n tables
    #     rows = len(self.elements)
    #     columns = len(self.elements[0])
    #     super().build(dwg)
    #     x = self.points[0]
    #     y = self.points[1]
    #     for r in range(rows):
    #         points = [
    #             (x, y + r * self.length_of_row),
    #             (x + columns * self.length_of_column, y + r * self.length_of_row),
    #             (x + columns * self.length_of_column, y + (r + 1) * self.length_of_row),
    #             (x, y + (r + 1) * self.length_of_row),
    #             (x, y + r * self.length_of_row)
    #         ]
    #         dwg.add(svgwrite.shapes.Polygon(points,
    #                                         style='fill:none; stroke:black;stroke-width:{};'.format(self.stroke_width)))
    #     for c in range(columns):
    #         points = [
    #             (x + c * self.length_of_column, y),
    #             (x + (c + 1) * self.length_of_column, y),
    #             (x + (c + 1) * self.length_of_column, y + rows * self.length_of_row),
    #             (x + c * self.length_of_column, y + rows * self.length_of_row),
    #             (x + c * self.length_of_column, y)
    #         ]
    #         dwg.add(svgwrite.shapes.Polygon(points,
    #                                         style='fill:none; stroke:black;stroke-width:{};'.format(self.stroke_width)))


# test = RelElement(svgwrite.Drawing())
# print(test.params)

# generate_labels(1000, 1000, MARKS, 0)


drawing = RootElement()
container, ymax = generate_labels(500, 500, MARKS, 2, 50, 50)

table = Table([(0, ymax)], 50, 250)  # length_of_columns should be half of width
text = Element([(1000, 500)], 'text', '', text='test')
table.elements = {'test': 'test', 'score': '59'}
container.add(table)
drawing.add(container)
drawing.build()
