#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################
# RAC Quiz v0.2
# Written by Simon Pratt
# This program takes a question bank in the format used by exHAMiner and
# quizzes the user with questions and answers from the bank.
################################################################################

import io
from sys import argv
from random import randint

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

################################################################################
# Functions
################################################################################

def isQuestion(line):
    """takes a line of input and returns true if that line is a question"""
    return line != '' and (line[0] == 'A' or line[0] == 'B')

################################################################################
# Classes
################################################################################

class Question:
    """A class to hold a question, including answers, correct answer and hint"""
    
    def ask(self,lang):
        print self.section+'-'+self.subsection+'-'+self.number,self.text
        for answer in self.answers:
            print answer
        reply = raw_input(prompt[lang])
        if reply[0] == self.correct:
            print congrats[lang]
        else:
            print correction[lang],self.correct
            print self.hint
        print
        return reply[0] == self.correct

    @staticmethod
    def parse(filename):
        with open(filename) as file:
            line = file.readline()
            while line != '':
                # strip leading and trailing whitespace
                line = line.strip()
                
                # if not the beginning of a question, skip to next line
                if not isQuestion(line):
                    line = file.readline()
                    continue

                q = Question()
                q.text = line[line.find(')')+2:]
                q.section, q.subsection, q.number = line[2:line.find(' ')].split('-')
                if len(q.subsection) == 1:
                    q.subsection = "0" + q.subsection
                q.correct = line[line.find('(')+1:line.find(')')]
                q.answers = []
                q.answers.append(file.readline().strip())
                q.answers.append(file.readline().strip())
                q.answers.append(file.readline().strip())
                q.answers.append(file.readline().strip())
                q.hint = (file.readline().strip())[2:]

                # Save the question
                key = q.section + '-' + q.subsection
                if not key in questions:
                    questions[key] = []
                questions[key].append(q)

                # read in next line and begin again
                line = file.readline()
                
if __name__ == "__main__":
    if len(argv) < 2:
        print 'Usage: racquiz.py {quiz} [section]'
        print '{quiz}    := basic'
        print '           | basic_fr (français)'
        print '           | advanced'
        print '           | advanced_fr (français)'
        print '[section] :='
        print '           | (section)'
        print '           | ? - list sections'
        exit()

    lang = 'en'
    if argv[1][-3] == '_':
        lang = argv[1][-2:]

    Question.parse(argv[1] + '.txt')

    sections = questions.keys()
    sections.sort()

    if len(argv) > 2:
        wanted = argv[2]
        if wanted[0] == '?':
            for section in sections:
                print section
            exit()
        sections = wanted.split(',')
    asked = 0
    correct = 0
    for section in sections:
        asked += 1
        if questions[section][randint(0,len(questions[section])-1)].ask(lang):
            correct += 1
            print score[lang],"%1.0f%%" % (100 * float(correct) / float(asked))
            print
