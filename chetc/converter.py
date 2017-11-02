from .configs import Clauss
import re


SPACES = re.compile("\s+")
GLOBALS = re.compile("%g\d")
LINE_SPLIT = re.compile("\s+=\s+")
MAKE_ID = re.compile("(%mkID\d+)")
MAKE_ID_LB = re.compile("%mkIDlb(\d)")
MAKE_ID_W = re.compile("%mkIDW")
DOLLAR_TARGET = re.compile("($\d)+")


class Converter(object):
    """ Leiden convention style to epidoc converter


    :param replacement_model: Class with replacements patterns
    :type replacement_model: chetc.configs.base.ConverterReplacementModel

    """

    def __init__(self, replacement_model=None):
        if replacement_model is None:
            self.__replacement_model__ = Clauss()
        else:
            self.__replacement_model__ = replacement_model
        self.lineNum = 0
        self.wNum = 0
        self.id = 0
        self.ignoreLB = False

        self.__replacements__ = list(self.replacement_model.replacements())

    @property
    def replacement_model(self):
        """ ReplacementModel instance used for configuration

        :rtype: chetc.configs.base.ConverterReplacementModel
        """
        return self.__replacement_model__

    @property
    def replacements(self):
        """ Yields tuples made of a RegexObject and a Replacement string

        """
        return self.__replacements__

    def reset(self):
        """ Reset the current object for a new document
        """
        self.lineNum = 0
        self.id = 0
        self.wNum = 0

    def count(self, text, find):
        """ Count the number of match of find in text or the length of characters of find

        :param text:
        :param find:
        :return:
        """
        if text == find:
            return len(SPACES.sub("", text))
        else:
            return text.count(find)

    def lb(self, *args):
        """ Makes and a register a line beginning ID

        :return: New line number
        :rtype: str
        """
        self.lineNum += 1
        return str(self.lineNum)

    def w(self, *args):
        """ Makes and register a word ID

        :return: New word number
        :rtype: str
        """
        self.wNum += 1
        return str(self.wNum)

    def replace(self, replacement_string):
        """ Create a temporary function that replace variables in the code depending on the current class

        :param replacement_string: String that will be used for replacement
        :type replacement_string: str
        :return: New function
        :rtype: callable
        """
        def temp(sub_output):
            output = ""+replacement_string
            groups = sub_output.groups()
            for i in range(len(groups)):
                output = output.replace("$"+str(i+1), groups[i] or "")
            return output
        return temp

    def convert(self, text, debug=False):
        """ Convert given string written in Leiden Convention to Epidoc XML

        :param text: The text to convert.
        :type text: str
        :param debug: Whether to print or not the results as things advance
        :type debug: bool
        :return: Epidoc XML encoded string
        :rtype: str
        """
        result = "" + text
        for pattern, replacement in self.replacements:  # For each replacement
            result = pattern.sub(self.replace(replacement), result)

            _ = [unit for match in MAKE_ID.findall(result) for unit in match.groups() if unit is not None]
            if debug is True:
                print(result)

        result = MAKE_ID_W.sub(self.w, result)
        result = MAKE_ID_LB.sub(self.lb, result)
        return result

    def multiple_convert(self, texts, debug=False):
        """ Convert a list of given string written in Leiden Convention to Epidoc XML

        :param texts: The text to convert.
        :type texts: iterable
        :param debug: Whether to print or not the results as things advance
        :type debug: bool
        :yield: Yield each Epidoc XML encoded string
        """
        for text in texts:
            yield self.convert(text, debug=debug)
            self.reset()
