#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################
# RAC Shared v0.1
# Written by Simon Pratt
# Components shared between basic and advanced tests
################################################################################

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

