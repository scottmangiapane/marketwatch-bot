from html.parser import HTMLParser

class StatusParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.orders = []
        self.recording = 0
        self.rawStats = []

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            try:
                link = attrs[0][1]
                if 'cancelorder' in link:
                    self.orders.append(link)
            except IndexError:
                pass
        if tag == 'ul':
            for name, value in attrs:
                if value == 'cubby worth':
                    self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'ul':
            self.recording -= 1

    def handle_data(self, data):
        if self.recording and data.strip() != '':
            self.rawStats.append(data.strip())

    def get_data(self):
        stats = {}
        tags = ['Net Worth',
                'Overall Gains',
                'Overall Returns',
                'Today\'s Gains',
                'Buying Power',
                'Cash Remaining',
                'Cash Borrowed',
                'Short Reserve']
        for i in range(0, len(self.rawStats)):
            if self.rawStats[i] in tags:
                try:
                    value = float(self.rawStats[i + 1].strip('$%,').replace(',', ''))
                except ValueError:
                    value = 0.0
                stats[self.rawStats[i]] = value
        return {'stats': stats, 'orders': self.orders}
