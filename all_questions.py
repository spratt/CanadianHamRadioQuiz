#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
# Canadian Ham Radio Quiz v1.0
# This program takes a question bank in the form of a text file, generates a
# quiz from the questions, then quizzes the user, keeping track of score
################################################################################
# Copyright (c) 2010, Simon David Pratt <me@simondavidpratt.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
################################################################################

import io
from sys import argv
from random import randint
import StringIO

################################################################################
# Internationalization
# For now, English and French.
################################################################################

prompt = {'en':'Your answer: ','fr':'Ta réponse: '}
congrats = {'en':'Correct.','fr':'Correcte.'}
correction = {'en':'The correct answer was:','fr':'La réponse correcte était:'}
score = {'en':'Your score:','fr':'Ta score:'}

################################################################################
# Data Structures
################################################################################

questions = dict()
wrong_questions = StringIO.StringIO()

################################################################################
# Functions
################################################################################

def isQuestion(line):
    """takes a line of input and returns true if that line is a question"""
    return line != '' and (line[0] == 'A' or line[0] == 'B')
                
def examine(stream):
    raw_line = stream.readline()
    while raw_line != '':
        line = raw_line.strip()
        # if not the beginning of a question, skip to next line
        if not isQuestion(line):
            raw_line = stream.readline()
            line = raw_line.strip()
            continue

        question = raw_line
            
        print line[2:line.find(' ')]
        print line[line.find(')')+2:]
        correct = line[line.find('(')+1:line.find(')')]

        # 4 choices
        raw_line = stream.readline()
        question = question + raw_line
        print raw_line.strip()
        raw_line = stream.readline()
        question = question + raw_line
        print raw_line.strip()
        raw_line = stream.readline()
        question = question + raw_line
        print raw_line.strip()
        raw_line = stream.readline()
        question = question + raw_line
        print raw_line.strip()
            
        # 1 hint
        raw_line = stream.readline()
        question = question + raw_line
        hint = (raw_line.strip())[2:]

        # get user answer
        reply = raw_input(prompt[lang])
        if reply[0] == correct:
            print congrats[lang]
        else:
            print correction[lang],correct
            print hint
            wrong_questions.write(question)
            
        # read in next line and begin again
        raw_line = stream.readline()
        line = raw_line.strip()

################################################################################
# Finally, quiz the user
################################################################################

if __name__ == "__main__":
    if len(argv) < 1:
        print 'Usage: chrq.py {quiz}'
        print '{quiz}    := basic'
        print '           | basic_fr (français)'
        print '           | advanced'
        print '           | advanced_fr (français)'
        exit()

    lang = 'en'
    if argv[1][-3] == '_':
        lang = argv[1][-2:]

    with open(argv[1] + '.txt') as file:
        examine(file)

    while 0 < len(wrong_questions.getvalue()):
        wrong_questions.seek(0)
        wq_temp = wrong_questions
        wrong_questions = StringIO.StringIO()
        examine(wq_temp)
        wq_temp.close()
        
    
