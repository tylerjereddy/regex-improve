"""
Regular expressions for policing the inefficient
usage of character classes to hold single 
(meta)characters.

This is an efficiency issue noted in Chapter 6 of:
Friedl, Jeffrey. Mastering Regular Expressions. 3rd ed.,
O’Reilly Media, 2009.

See section: 'Don’t use superfluous character classes'

In particular, there's an overhead associated with placement
of the single (meta)characters in the class.
"""

import re

class FileOperatorExtraCharClass:
    def __init__(self):
        self.pattern = r'(?P<start>re\.compile\(.*?)(?P<offender>\[\\?.\])(?P<end>.*?[\'"].*?\))'
        self.prog = re.compile(self.pattern)

    def replacer(self, match):
        # even if [\w], always start at second
        # position and go to second last to
        # find the element to be removed from
        # class
        single_char = match.group('offender')[1:-1]
        if single_char in '.*+?()[]|':
            single_char = '\\' + single_char
        return match.group('start') + single_char + match.group('end')

    def per_file_operator(self, filepath):
        with open(filepath, 'r') as infile:
            file_string = infile.read()
            while self.prog.search(file_string):
                file_string = self.prog.sub(self.replacer, file_string)
            new_file_string = file_string

        with open(filepath, 'w') as outfile:
            outfile.write(new_file_string)
