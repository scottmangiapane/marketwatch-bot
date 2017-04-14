from html.parser import HTMLParser

class StockParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.raw = []

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for name, value in attrs:
                if value == 'row first cubby':
                    self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'ul':
            self.recording -= 1

    def handle_data(self, data):
        if self.recording and data.strip() != '':
            self.raw.append(data.strip())

    def get_data(self):
        data = 0.0
        for i in range(0, len(self.raw)):
            if self.raw[i] == '$':
                try:
                    data = float(self.raw[i + 1].replace(',', ''))
                except:
                    pass
        return data

    def reset(self):
        HTMLParser.reset(self)
        self.recording = 0
        self.raw = []
