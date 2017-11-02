from chetc import Converter
from unittest import TestCase
import os
from chetc.configs import Clauss


class TestClauss(TestCase):
    def setUp(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_Clauss_now.txt")) as f:
            lines = [x for x in f.readlines()]
            self.tests_strings = zip(*[lines[i::3] for i in range(3)])
        self.converter = Converter(replacement_model=Clauss(word_numbering=False))
        self.debug = False
        self.maxDiff = 50000

    def test_automatic(self):
        for text_info, line, output in self.tests_strings:
            self.assertEqual(
                self.converter.convert(line, debug=self.debug).replace("\n", ""), output.replace("\n", ""),
                "{} fails".format(text_info)
            )
            self.converter.reset()
