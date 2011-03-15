import unittest
from nose.plugins.plugintest import PluginTester
from nosequerycount.plugin import DjangoQueryCountPlugin, connections


def pass_func():
    connections['default'].queries = ['query'] * 2
    assert True


def fail_func():
    connections['default'].queries = ['query'] * 3
    assert False
    connections['default'].queries = ['query'] * 3


def error_func():
    connections['default'].queries = ['query'] * 4
    raise Exception


def error_test(exception):

    def error_func():
        raise exception
    return unittest.FunctionTestCase(error_func)
error_test.__test__ = False

PASS = unittest.FunctionTestCase(pass_func)
FAIL = unittest.FunctionTestCase(fail_func)
ERROR = unittest.FunctionTestCase(error_func)


class TestPlugin(PluginTester, unittest.TestCase):
    activate = '--with-querycount'
    args = ['--querycount-threshold=']
    tests = [PASS, FAIL, ERROR]

    def setUp(self):
        self.plugin = DjangoQueryCountPlugin()
        self.plugins = [self.plugin]
        PluginTester.setUp(self)

    def makeSuite(self):
        return self.tests
