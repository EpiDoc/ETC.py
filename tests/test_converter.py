from chetc import Epigraph2Markup
from unittest import TestCase


class TestClauss(TestCase):
    def setUp(self):
        with open("test.txt") as f:
            lines = [x for x in f.readlines()]
            self.tests_strings = zip(*[lines[i::3] for i in range(3)])
        self.converter = Epigraph2Markup()
        self.debug = False
        self.maxDiff = 10000

    def test_automatic(self):
        for text_info, line, output in self.tests_strings:
            self.assertEqual(
                self.converter.convert(line, debug=self.debug).replace("\n", ""), output.replace("\n", ""),
                "{} fails".format(text_info)
            )
            self.converter.reset()
