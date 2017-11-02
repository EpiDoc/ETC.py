import re
from .base import ConverterReplacementModel


class Clauss(ConverterReplacementModel):
    """ Conversion class for the Clauss database

    :param word_numbering: Includes a word number every time a new word is found
    :type word_numbering: bool
    """
    word_matcher_regularization = "[\w\(\)\?\!]"
    word_matcher_plus_square_brkcts = "[\w\[\]\?\!]"

    def replacements(self):
        """ Generates replacements patterns and substring

        :yield: Replacements and their substring
        """
        x = [
            ##########################################
            # Normalization Phase
            ##########################################

            # When a line ends with an unknown content
            ("(\[\s*\/)", "[?] /"),

            # When a line ends with a provided character and an unknown loss
            ("(\[(" + Clauss.word_matcher_regularization + "*)\s*\/)",
                "[$1] [?] /"),
            ("\[(" + Clauss.word_matcher_regularization + "+)\s*$",
                "[$1] [?]"),

            # When a line starts with an unknown content
            ('(\/\s*\])',
                '/ [?]'),

            # When a line starts with a provided character and an unknown content
            ('(\/\s*(' + Clauss.word_matcher_regularization + '*)\])',
                '/ [?] [$1]'),
            ('^(\s*(' + Clauss.word_matcher_regularization + '*)\])',
                '[?] [$1]'),

            # When two words are spanning inside the same provided lacuna : [abc(ade!) abc(e)x(z!)]
            ('\[(' + Clauss.word_matcher_regularization + '+) (' + Clauss.word_matcher_regularization + '+)\]',
                '[$1] [$2]'),

            # When three words are spanning inside the same provided lacuna : [abc(ade!) abc(e)x(z!) abc(e)x(z!)]
            ('\[(' + Clauss.word_matcher_regularization + '+) (' + Clauss.word_matcher_regularization + '+) (' + Clauss.word_matcher_regularization + '+)\]',
                '[$1] [$2] [$3]'),

            # Replace angular bracket by curved bracked
            ("<", "«"),
            (">", "»"),

        ]
        ##########################################
        # Word and line tagging
        ##########################################
        if self.word_numbering:
            x += [
                # Tag a word
                ('([^\s/]+)',
                    '<w n="%mkIDW">$1</w>')
            ]
        x += [
            # Tag the first line
            ('^(.){0}',
                '<lb n="%mkIDlb1"/>'),
            # Tag multiple lines
            ('(\/{2})(?!\w\>)',
             '<lb n="%mkIDlb1"/><gap extent="unknown" reason="lost" unit="line" />'),
            # Tag a line
            ('(\/)(?![\w\>]+)',
                '<lb n="%mkIDlb1"/>'),

            ##########################################
            # Angular bracket markup
            ##########################################

            # Correction
            ("«(\w+)=(\w+)»",
                "<choice><corr>$1</corr><sic>$2</sic></choice>"),

            # Here texts are listed that have been created to fill erased passages
            ("««([\w\(\)\?\!])»»",
                "<del>$1</del>"), # Not so sure about this one [Meaning of the legend]

            # Here text have been erased and something was filled by an ancient hand
            ("««\[\[([\w\(\)\?\!])\]\]»»}",
                "<add place=\"overstrike\">$1</add>"),

            ##########################################
            # Curly brackets
            ##########################################

            # Replace curly brackets
            ("\{((?:\w|\s)+)\}",
                "<sic>$1</sic>"),

            ##########################################
            # Parentheses in Brackets
            ##########################################

            # Abbreviation inside Parentheses, even with supplied inside
            ("\[(" + Clauss.word_matcher_plus_square_brkcts + "*)\((\w+)\)(" + Clauss.word_matcher_plus_square_brkcts + "*)\]",
                "<supplied reason=\"lost\"><expan><abbr>$1</abbr><ex>$2</ex><abbr>$3</abbr></expan></supplied>"),

            ##########################################
            # Parentheses
            ##########################################

            # Parentheses, even with supplied inside
            ("(" + Clauss.word_matcher_plus_square_brkcts + "*)\((\w+)\)(" + Clauss.word_matcher_plus_square_brkcts + "*)",
                "<expan><abbr>$1</abbr><ex>$2</ex><abbr>$3</abbr></expan>"),

            # Parentheses with uncertain
            ("(" + Clauss.word_matcher_plus_square_brkcts + "*)\((\w+)(?:(?:\?)|(?:\(\?\)))\)(" + Clauss.word_matcher_plus_square_brkcts + "*)",
                "<expan><abbr>$1</abbr><ex cert=\"low\">$2</ex><abbr>$3</abbr></expan>"),

            # Parentheses with unextented parentheses
            ("(" + Clauss.word_matcher_plus_square_brkcts + "*)\(\)(" + Clauss.word_matcher_plus_square_brkcts + "*)",
                "<expan><abbr>$1</abbr><abbr>$2</abbr></expan>"),

            ##########################################
            # Brackets
            ##########################################

            # When the loss' extent is unknown
            ("\[\?\]",
                '<gap reason="lost" extent="unknown" unit="character"/>'),

            # When the loss' extent is quantified
            ("\[(\d+)\]",
                '<gap reason="lost" extent="$1" unit="character"/>'),

            # When the loss' extent is quantified but unsure
            ("\[(\d+)\?\]",
                '<gap reason="lost" extent="$1" unit="character" cert="low"/>'),
            ("\[(\d+)\(\?\)\]",
                '<gap reason="lost" extent="$1" unit="character" cert="low"/>'),

            # When we supply an uncertain replacement
            ("\[(" + Clauss.word_matcher_regularization + "+)\?\]",
             '<supplied reason="lost" cert="low">$1</supplied>'),
            ("\[(" + Clauss.word_matcher_regularization + "+)\(\?\)\]",
             '<supplied reason="lost" cert="low">$1</supplied>'),
            ("(\w*)\[(" + Clauss.word_matcher_regularization + "+)\](\w*)\(\?\)",
             '$1<supplied reason="lost" cert="low">$2</supplied>$3'),

            # When we supply a replacement
            ("\[(" + Clauss.word_matcher_regularization + "+)\]",
                '<supplied reason="lost">$1</supplied>'),

            ##########################################
            # Clean Up
            ##########################################
            ("(<abbr></abbr>)", "")

        ]
        for pattern, replacement in x:
            yield re.compile(pattern), replacement