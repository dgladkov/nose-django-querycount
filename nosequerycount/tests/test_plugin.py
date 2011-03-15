from nose.plugins import Plugin
from helpers import TestPlugin


class TestDisabledPlugin(TestPlugin):
    activate = ''

    def test_is_plugin(self):
        self.assert_(isinstance(self.plugin, Plugin))

    def test_name_is_achievements(self):
        self.assertEqual(self.plugin.name, 'querycount')

    def test_is_not_enabled_by_default(self):
        self.assert_(not self.plugin.enabled)


class TestEnabledPlugin(TestPlugin):

    def test_is_enabled(self):
        self.assert_(self.plugin.enabled)

    def test_report(self):
        self.assertTrue('fail_func         3' in self.output)
        self.assertTrue('error_func        4' in self.output)
        self.assertTrue('pass_func         2' in self.output)
        self.assertTrue('TOTAL     9 queries' in self.output)


class TestWithThreshold(TestPlugin):
    args = ['--querycount-threshold=3']

    def test_is_enabled(self):
        self.assert_(self.plugin.enabled)

    def test_colored_report(self):
        self.assertTrue('fail_func         3' in self.output)
        self.assertTrue('pass_func         2' in self.output)
        self.assertTrue('error_func\x1b[1;31m        4\x1b[0m' in self.output)
        self.assertTrue('TOTAL     9 queries' in self.output)
