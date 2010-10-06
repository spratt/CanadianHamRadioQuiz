#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################
# RAC Quiz v0.1
# Written by Simon Pratt
# This program takes a question bank in the format used by exHAMiner and
# quizzes the user with questions and answers from the bank.
################################################################################

import io
from sys import argv

if len(argv) < 2:
    print 'Usage: racquiz.py {quiz} [section]'
    print '{quiz} := basic'
    print '        | basic_fr'
    print '        | advanced'
    print '        | advanced_fr'
    print '[section] :='
    print '           | (section number)'
    print '           | ? - lists section numbers'
    exit()

# Internationalization
# For now, English and French.
prompt = {'en':'Your answer: ','fr':'Ta réponse: '}
congrats = {'en':'Correct.','fr':'Correcte.'}
correction = {'en':'The correct answer was:','fr':'La réponse correcte était:'}
score = {'en':'Your score:','fr':'Ta score:'}

def isAnswer(line):
    # takes a line of input, and returns:
    # true  - if the line is an answer (i.e. begins with 1,2,3 or 4)
    # false - otherwise
    c = line[0]
    return c == '1' or c == '2' or c == '3' or c == '4'

with open(argv[1] + '.txt') as file:
    # determine the language
    lang = 'en'
    if argv[1][-3] == '_':
        lang = argv[1][-2:]
    # set up some variables
    single_section = False
    correct = None
    answer = None
    questions = 0
    wrong = 0
    # if the user specified a section
    if len(argv) > 2:
        # if the user wants a list of sections
        if argv[2] == '?':
            for line in file:
                if line[0] == '{':
                    print line,
            exit()
        # otherwise, skip to the section
        single_section = True
        for line in file:
            if line[0] == '{' and line[:5].strip('{L}') == argv[2]:
                print line[line.find('}')+2:]
                break
    for line in file:
        if line[0] == 'B' or line[0] == 'A':
            # Question, in the format:
            # V-www-x-y (z) Question String
            # Where:
            #  V   - either B (basic) or A (advanced)
            #  www - indicates the section
            #  x   - indicates the part
            #  y   - indicates the question number
            #  z   - indicates the number of the correct answer
            print line[line.find(')')+2:],
            correct = line[line.find('(')+1]
        elif line[0] == '{':
            # Module heading, in the format:
            # {Lxyz} Module Title
            # Where:
            #  xy - indicates the number of the section
            #  z  - is an optional letter indicating a subsection
            if single_section:
                exit()
            print line[line.find('}')+2:]
        elif isAnswer(line):
            print line,
        elif line[0] == '>':
            # Hint
            # Since this always follows a question and its possible answers,
            # I can now ask the user for their answer
            questions = questions + 1
            answer = raw_input(prompt[lang])
            if correct == answer[0]:
                print
                print congrats[lang],
            else:
                wrong = wrong + 1
                print
                print line[2:]
                print correction[lang],correct,'. ',
            print score[lang],
            print '%.2f%%' % ((float(questions)-float(wrong))*100/float(questions))
            print
        elif line[0] == '^':
            # File header, in the format:
            # ^ Qualification ^ Number of Questions ^ Pass Mark ^
            parts = line.split('^ ')
            print parts[1]
