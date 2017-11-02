class ConverterReplacementModel:
    """ Conversion class for the Clauss database

    :param word_numbering: Includes a word number every time a new word is found
    :type word_numbering: bool
    """
    word_matcher_regularization = "[\w\(\)\?\!]"
    word_matcher_plus_square_brkcts = "[\w\[\]\?\!]"

    def __init__(self, word_numbering=True):
        self.__word_numbering__ = word_numbering

    @property
    def word_numbering(self):
        """ Whether or not to apply word numbering

        :rtype: bool
        """
        return self.__word_numbering__

    def replacements(self):
        """ Generates replacements patterns and substring

        :yield: Replacements and their substring
        """
        raise NotImplementedError