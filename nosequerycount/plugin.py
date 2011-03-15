import codecs
from collections import defaultdict
from django.conf import settings
from nosequerycount.utils import ColoredString
try:
    from nose.plugins import Plugin
except ImportError:
    Plugin = object
try:
    from django.db import connections
except:
    from django.db import connection

    class ConnectionDict(dict):
        """
        Compatibility with Django < 1.2
        """
        all = dict.values

    connections = ConnectionDict()
    connections['default'] = connection


class DjangoQueryCountPlugin(Plugin):
    """
    Counts SQL queries for each test.
    """
    name = 'querycount'
    data = defaultdict(dict)
    output_stream = None
    data_columns = {} # dictionary with data column width for table view

    def __init__(self, *args, **kwargs):
        super(DjangoQueryCountPlugin, self).__init__(*args, **kwargs)
        for name in connections:
            self.data_columns[name] = len(name) + 2

    def options(self, parser, env):
        """
        Add options to command line.
        """
        super(DjangoQueryCountPlugin, self).options(parser, env)
        parser.add_option('--querycount-threshold', action='store',
                          default=env.get('NOSE_QUERYCOUNT_THRESHOLD'),
                          dest='threshold',
                          help='Set query count threshold for each test'
                          '[NOSE_QUERYCOUNT_THRESHOLD]')

    def configure(self, options, conf):
        # Save a reference to the `Config` to access its `stream` in case
        # setOutputStream isn't called.
        self.config = conf
        if Plugin is not object:
            super(DjangoQueryCountPlugin, self).configure(options, conf)
        try:
            self.threshold = int(options.threshold)
        except (TypeError, ValueError):
            self.threshold = 0

    def startTest(self, test):
        """
        Reset query list before each test and enable DEBUG
        """
        for conn in connections.all():
            conn.queries = []
        settings.DEBUG = True

    def stopTest(self, test):
        """
        Set DEBUG off and count queries
        """
        settings.DEBUG = False
        for name in connections:
            query_count = len(connections[name].queries)
            self.data[str(test.id())][name] = query_count

            # update data column width
            if len(str(query_count)) > self.data_columns[name]:
                self.data_columns[name] = len(query_count) + 2

    def setOutputStream(self, stream):
        self.output_stream = stream

    def report(self, result):
        """
        Show query count report in table
        """
        total = 0
        output_stream = self.output_stream or self.config.stream
        if str is not unicode:
            output_stream = codecs.getwriter('utf-8')(output_stream)
        # column with calculation
        first_col_width = len(max(self.data.keys() or ['Tests'], key=len))
        total_width = first_col_width + sum(self.data_columns.values())

        # output table header
        output_stream.write('\n')
        output_stream.write('Tests'.ljust(first_col_width))
        for name, width in self.data_columns.iteritems():
            output_stream.write(name.rjust(width))
        output_stream.write('\n')
        output_stream.write('-' * total_width)
        output_stream.write('\n')

        for test_name, results in self.data.iteritems():
            output_stream.write(test_name.ljust(first_col_width))

            for name, count in results.iteritems():
                result = str(count).rjust(self.data_columns[name])
                if self.threshold and count > self.threshold:
                    result = ColoredString(result, ColoredString.RED)
                output_stream.write(result)
                total += count

            output_stream.write('\n')

        output_stream.write('-' * total_width)
        output_stream.write('\n')
        output_stream.write('TOTAL')
        output_stream.write(('%d queries' % total).rjust(total_width - 5))
        output_stream.write('\n\n')
