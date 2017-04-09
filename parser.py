from html.parser import HTMLParser

class CustomParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.buying_power = ''
        self.recording = 0
        self.raw = []

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag == 'ul':
            for name, value in attrs:
                if value == 'cubby worth':
                    self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'ul':
            self.recording -= 1

    def handle_data(self, data):
        if self.recording and data.strip() != '':
            self.raw.append(data.strip())

    def get_data(self):
        data = {}
        tags = ['Net Worth',
                'Overall Gains',
                'Overall Returns',
                'Today\'s Gains',
                'Buying Power',
                'Cash Remaining',
                'Cash Borrowed',
                'Short Reserve']
        for i in range(0, len(self.raw)):
            if self.raw[i] in tags:
                data[self.raw[i]] = self.raw[i + 1]
        return data
