#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################
# RAC Basic v0.1
# Written by Simon Pratt
# This program simulates the Industry Canada Amateur Radio Basic Qualification
# exam.
################################################################################

import io
from sys import argv
from racshared import *
from random import sample

################################################################################
# Modules
################################################################################

module_names = []
modules = []
modules_choose = []

with open('basicmodules.txt') as file:
    current_module = -1
    for line in file:
        if line[0] != 'B':
            choose, name = line[:-1].split(';')
            module_names.append(name)
            modules_choose.append(choose)
            current_module += 1
            modules.append([])
        else:
            modules[current_module].append(line[:-1])

################################################################################
# Command line arguments
################################################################################

chosen_mod = None
lang = 'en'

if len(argv) > 1:
    if argv[1] == 'help':
        print 'Usage: racbasic.py [module] [language]'
        print '[module] :='
        print '          | (module number)'
        print '          | ?    - lists module numbers'
        print '          | help - displays this help message'
        print '[language] :='
        print '            | en (default)'
        print '            | fr'
        exit()
    elif argv[1] == '?':
        for module in module_names:
            print module
        exit()
    else:
        chosen_mod = int(argv[1])-1
if len(argv) > 2:
    lang = argv[2]

######################################################################
# Generate question set
######################################################################

questions = []

if chosen_mod:
    choices = sample(xrange(len(modules[chosen_mod])),
                     int(modules_choose[chosen_mod]))
    choices.sort()
    for n in choices:
        questions.append(modules[chosen_mod][n])
else:
    for module in range(8):
            choices = sample(xrange(len(modules[module])),
                             int(modules_choose[module]))
            choices.sort()
            for n in choices:
                questions.append(modules[module][n])

######################################################################
# Finally, quiz the user
######################################################################

with open('basic.txt') as file:
    # set up some variables
    correct = None
    answer = None
    answered = 0
    right = 0
    line = file.readline()
    for question in questions:
        # Find the next chosen question
        while line[:line.find(' ')] != question:
            line = file.readline()
        # Print the question
        print 'Q'+str(answered+1),line[line.find(')')+2:],
        # Save the correct answer
        correct = line[line.find('(')+1]
        # Print the answers
        line = file.readline()
        while isAnswer(line):
            print line,
            line = file.readline()
        answer = raw_input(prompt[lang])
        if correct == answer[0]:
            right += 1
            print
            print congrats[lang],
        else:
            print
            print line[2:] # hint
            print correction[lang],correct,'. ',
        answered += 1
        print score[lang],
        print '%.2f%%' % (float(right)*100/float(answered))
        print
        while line[0] != 'B' and line[0] != 'A':
            line = file.readline()
            if line == '':
                exit()
