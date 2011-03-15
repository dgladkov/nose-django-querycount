import unittest
from nosequerycount.utils import ColoredString


class TestColoredString(unittest.TestCase):
    colors = (
        'BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE',
    )

    def test_is_unicode_subclass(self):
        self.assert_(issubclass(ColoredString, unicode))

    def test_class_properties(self):
        for c, n in zip(self.colors, range(8)):
            self.assertTrue(hasattr(ColoredString, c))
            self.assertEqual(getattr(ColoredString, c), n)

    def test_colorize(self):
        for n in range(8):
            cs = ColoredString('mystring', n)
            self.assertEqual(str(cs), '\x1b[1;3%dmmystring\x1b[0m' % n)
