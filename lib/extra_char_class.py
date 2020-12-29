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
        self.pattern_compile = r'(?P<start>re\.compile\(\n*\s*r[\'"].*?)(?P<offender>\[\\?.\])(?P<end>\n*\s*.*?[\'"].*?\n*\s*\))'
        self.pattern_match = r'(?P<start>re\.match\(\n*\s*r[\'"].*?)(?P<offender>\[\\?.\])(?P<end>.*\n*\s*,\s)'
        self.pattern_list = [self.pattern_compile,
                             self.pattern_match]
        self.prog_list = [re.compile(pattern) for pattern in self.pattern_list]

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
            new_file_string = None
            for prog in self.prog_list:
                if prog.search(file_string):
                    while prog.search(file_string):
                        file_string = prog.sub(self.replacer, file_string)
                    new_file_string = file_string

        if new_file_string is not None:
            with open(filepath, 'w') as outfile:
                outfile.write(new_file_string)
