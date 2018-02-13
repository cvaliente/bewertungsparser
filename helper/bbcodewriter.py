def bbcode(tag, string, value=None):
    """Return a text(string) enclosed by the bbcode tags"""
    tag = str(tag)
    string = str(string)
    if value:
        value = str(value)
        return '[' + tag + '=' + value + ']' + string + '[/' + tag + ']'
    else:
        return '[' + tag + ']' + string + '[/' + tag + ']'


def make_url(url_string, url_name):
    """Return an bbcode url format for given url and description"""
    return bbcode('url', url_name, url_string)


def font_bold(text):
    """Return the text with a bbcode bold tag"""
    return bbcode(tag='b', string=text)


def true_type(text):
    """Return the text with a bbcode tt tag"""
    return bbcode(tag='tt', string=text)


def table_cell(text):
    """Return the text with a td tag"""
    return bbcode(tag='td', string=text)


def table_row(text):
    """Return the text with a td tag"""
    return bbcode(tag='tr', string=text)


class BBTable:
    """creates the frame of a bbcode table"""

    def __init__(self, rows):
        """needs the rows as input for this table"""
        self.elements = rows

    @staticmethod
    def tablify(rows):
        """adds start and end tags for tables"""
        return str('[table]\r\n' + rows + '[/table]')

    def __str__(self):
        """prints table in bbcode format"""
        return self.tablify(''.join(str(row) for row in self.elements))


class TableRow:
    """creates a bbcode table row with correct tags"""

    def __init__(self, fields, is_header=False):
        """needs the rows as input for this table"""
        self.elements = fields
        self.is_header = is_header

    def make_cell(self, row_field):
        """encloses cells with correct tags"""
        if self.is_header:
            row_field = font_bold(row_field) + true_type('   ')
        return table_cell(row_field)

    @staticmethod
    def make_row(cells):
        """encloses rows with the correct tags"""
        return table_row(cells) + '\r\n'

    def __str__(self):
        """adds cell and row tags to elements"""
        return self.make_row(''.join(self.make_cell(field) for field in self.elements))


def generate_table(bewertungs_threads):
    """"generate a table for the threads"""
    return BBTable([TableRow(['Platz', 'Bewertung', 'Stimmen', 'Produkt'], True)]
                   + [TableRow([index + 1, element.durchschnitt, element.stimmen, make_url(element.url, element.name)])
                      for index, element in bewertungs_threads])
