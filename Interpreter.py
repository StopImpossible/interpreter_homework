"""
Description: The big homework of the complier
Time: 2015-11-19
Author: Koprvhdix
E-mail: koprvhdix@163.com

Usage:
    $ python Interpreter.py -f source_file
"""

from optparse import OptionParser
import turtle
import sys
import math
import re

keyword_token = ['FOR', 'FROM', 'STEP',
                 'DRAW', 'ORIGIN', 'ROT',
                 'SCALE', 'TO', 'COS',
                 'SIN', 'IS']

constant_token = {
    'PI' : 3.141592653589,
    'E' : 2.718281828459
}

special_symbols = [',', ';', '+',
                   '-', '*', '/',
                   '**', '(', ')']

annotation = ['--', '//']

token_list = []

class token(object):
    def __init__(self, token_str, row, col, is_confirm):
        self.token_str = token_str.upper()
        self.line_num = row
        self.col_num = col
        if is_confirm:
            mark = 0
            for item in special_symbols:
                if self.token_str == item:
                    self.token_value = self.token_str
                    self.token_type = 'SPECIAL_SYMBOLS'
                    mark += 1
                    break
            if mark == 0:
                for item in annotation:
                    if item == self.token_str:
                        self.token_value = self.token_str
                        self.token_type = 'ANNOTATION'
                        mark += 1
                        break
            if mark == 0:
                mark2 = self.token_str.find('.')
                if mark2 == -1:
                    self.token_value = int(self.token_str)
                    self.token_type = 'INT'
                else:
                    self.token_value = float(self.token_str)
                    self.token_type = 'FLOAT'
        else:
            self.token_type = self.get_token_type()

    def get_token_type(self):
        for item in keyword_token:
            if item == self.token_str:
                self.token_value = self.token_str
                return 'KEYWORD'
        for item in constant_token.keys():
            if item == self.token_str:
                self.token_value = constant_token[item]
                return 'CONSTANT'
        self.token_value = self.token_str
        return 'IDENTIFIER'

class Interpreter(object):
    def __init__(self, source_file):
        self.source_file = source_file
        self.token_list = []
        file_iter = open(self.source_file)
        self.source_code = []
        for line in file_iter:
            self.source_code.append(line.replace('\n', ' '))

    def dfa(self):
        pattern_word = re.compile(r'\w')
        pattern_num = re.compile(r'\d')
        pattern_spec = re.compile(r'[,|;|(|)|+]')
        pattern_spec2 = re.compile(r'[*|/|-]')
        line_num = 0
        current_state = 0
        for item in self.source_code:
            line_num += 1
            col_num = 1
            token_str = []
            for character in item:
                if current_state == 0:
                    matter = pattern_num.match(character)
                    if matter:
                        current_state = 2
                        token_str.append(character)
                        continue
                    matter = pattern_word.match(character)
                    if matter:
                        current_state = 1
                        token_str.append(character)
                        continue
                    matter = pattern_spec.match(character)
                    #maybe have error
                    if matter:
                        current_state = 0
                        if len(token_str) != 0:
                            token_str2 = ''
                            token_str2 = token_str2.join(token_str)
                            get_token = token(token_str2, line_num, col_num, False)
                            col_num += 1
                            token_list.append(get_token)
                        get_token = token(character, line_num, col_num, True)
                        token_list.append(get_token)
                        col_num += 1
                        token_str = []
                        continue
                    matter = pattern_spec2.match(character)
                    if matter:
                        current_state = 4
                        token_str.append(character)
                        continue
                    if character == ' ':
                        current_state = 0
                        continue
                    print "Error: unexpected character %s found at %s" % (character, line_num)
                    sys.exit("unexpected character")
                elif current_state == 1:
                    matter = pattern_word.match(character)
                    if matter:
                        current_state = 1
                        token_str.append(character)
                        continue
                    matter = pattern_spec.match(character)
                    if matter:
                        current_state = 0
                        token_str2 = ''
                        token_str2 = token_str2.join(token_str)
                        get_token = token(token_str2, line_num, col_num, False)
                        col_num += 1
                        token_list.append(get_token)
                        get_token = token(character, line_num, col_num, True)
                        token_list.append(get_token)
                        token_str = []
                        continue
                    matter = pattern_spec2.match(character)
                    if matter:
                        current_state = 4
                        token_str2 = ''
                        token_str2 = token_str2.join(token_str)
                        get_token = token(token_str2, line_num, col_num, False)
                        col_num += 1
                        token_list.append(get_token)
                        token_str = []
                        token_str.append(character)
                        continue
                    if character == ' ':
                        current_state = 0
                        token_str2 = ''
                        token_str2 = token_str2.join(token_str)
                        get_token = token(token_str2, line_num, col_num, False)
                        col_num += 1
                        token_list.append(get_token)
                        token_str = []
                        continue
                    print "Error: unexpected character %s found at %s" % (character, line_num)
                    sys.exit("unexpected character")
                elif current_state == 2:
                    matter = pattern_num.match(character)
                    if matter:
                        current_state = 2
                        token_str.append(character)
                        continue
                    matter = pattern_spec.match(character)
                    if matter:
                        current_state = 0
                        token_str2 = ''
                        token_str2 = token_str2.join(token_str)
                        get_token = token(token_str2, line_num, col_num, True)
                        token_list.append(get_token)
                        col_num += 1
                        get_token = token(character, line_num, col_num, True)
                        token_list.append(get_token)
                        col_num += 1
                        token_str = []
                        continue
                    if character == '.':
                        current_state = 3
                        token_str.append(character)
                        continue
                    matter = pattern_spec2.match(character)
                    if matter:
                        current_state = 4
                        token_str2 = ''
                        token_str2 = token_str2.join(token_str)
                        get_token = token(token_str2, line_num, col_num, True)
                        col_num += 1
                        token_list.append(get_token)
                        token_str = []
                        token_str.append(character)
                        continue
                    if character == ' ':
                        current_state = 0
                        token_str2 = ''
                        token_str2 = token_str2.join(token_str)
                        get_token = token(token_str2, line_num, col_num, True)
                        col_num += 1
                        token_list.append(get_token)
                        token_str = []
                        continue
                    print "Error: unexpected character %s found at %s" % (character, line_num)
                    sys.exit("unexpected character")
                elif current_state == 3:
                    matter = pattern_num.match(character)
                    if matter:
                        current_state = 3
                        token_str.append(character)
                        continue
                    matter = pattern_spec.match(character)
                    if matter:
                        current_state = 0
                        token_str2 = ''
                        token_str2 = token_str2.join(token_str)
                        get_token = token(token_str2, line_num, col_num, True)
                        token_list.append(get_token)
                        col_num += 1
                        get_token = token(character, line_num, col_num, True)
                        token_list.append(get_token)
                        col_num += 1
                        token_str = []
                        continue
                    matter = pattern_spec2.match(character)
                    if matter:
                        current_state = 4
                        token_str2 = ''
                        token_str2 = token_str2.join(token_str)
                        get_token = token(token_str2, line_num, col_num, True)
                        col_num += 1
                        token_list.append(get_token)
                        token_str = []
                        token_str.append(character)
                        continue
                    if character == ' ':
                        current_state = 0
                        token_str2 = ''
                        token_str2 = token_str2.join(token_str)
                        get_token = token(token_str2, line_num, col_num, True)
                        col_num += 1
                        token_list.append(get_token)
                        token_str = []
                        continue
                    print "Error: unexpected character %s found at %s" % (character, line_num)
                    sys.exit("unexpected character")
                elif current_state == 4:
                    if character == token_str[0]:
                        current_state = 0
                        token_str.append(character)
                        token_str2 = ''
                        token_str2 = token_str2.join(token_str)
                        get_token = token(token_str2, line_num, col_num, True)
                        col_num += 1
                        token_list.append(get_token)
                        token_str = []
                        if get_token.token_type == 'ANNOTATION':
                            break
                        continue
                    if character == ' ':
                        current_state = 0
                        token_str2 = ''
                        token_str2 = token_str2.join(token_str)
                        get_token = token(token_str2, line_num, col_num, True)
                        col_num += 1
                        token_list.append(get_token)
                        token_str = []
                        continue
                    matter = pattern_num.match(character)
                    if matter:
                        current_state = 2
                        token_str2 = ''
                        token_str2 = token_str2.join(token_str)
                        get_token = token(token_str2, line_num, col_num, True)
                        col_num += 1
                        token_list.append(get_token)
                        token_str = []
                        token_str.append(character)
                        continue
                    matter = pattern_word.match(character)
                    if matter:
                        current_state = 1
                        token_str2 = ''
                        token_str2 = token_str2.join(token_str)
                        get_token = token(token_str2, line_num, col_num, True)
                        col_num += 1
                        token_list.append(get_token)
                        token_str = []
                        token_str.append(character)
                        continue
                    if character == ' ':
                        current_state = 0
                        token_str2 = ''
                        token_str2 = token_str2.join(token_str)
                        get_token = token(token_str2, line_num, col_num, True)
                        col_num += 1
                        token_list.append(get_token)
                        token_str = []
                        continue
                    print "Error: unexpected character %s found at %s" % (character, line_num)
                    sys.exit("unexpected character")

    def TEST_CASE(self):
        for item in token_list:
            print item.token_type, item.token_value
            print item.line_num, item.col_num

if __name__ == "__main__":
    # parse = OptionParser()
    # parse.add_option('-f',
    #                  dest='source_file',
    #                  help='the file of source code',
    #                  default=None)
    #
    # (options, arges) = parse.parse_args()
    # source_file = None
    # if options.source_file is None:
    #     source_file = sys.stdin
    # elif options.source_file is not None:
    #     source_file = options.source_file
    # else:
    #     print 'No source filename specified, system with exit\n'
    #     sys.exit('System will exit')

    source_file = 'test1.txt'
    interpreter = Interpreter(source_file)
    interpreter.dfa()
    interpreter.TEST_CASE()