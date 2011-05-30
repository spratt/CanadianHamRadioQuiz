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
from chrq import Question, questions

if __name__ == "__main__":
    if len(argv) < 2:
        print 'Usage: print_quiz.py {quiz}'
        print '{quiz}    := basic'
        print '           | basic_fr (français)'
        print '           | advanced'
        print '           | advanced_fr (français)'
        exit()

    lang = 'en'
    if argv[1][-3] == '_':
        lang = argv[1][-2:]

    Question.parse(argv[1] + '.txt')

    sections = questions.keys()
    sections.sort()

    question_numbers = []
    answers = []
    print '==================== QUESTIONS ===================='
    for section in sections:
        question = questions[section][randint(0,len(questions[section])-1)]
        question.print_question()
        answers.append(question.correct)
        question_numbers.append(question.get_question_number())
        print
    print '===================== ANSWERS ====================='
    for (counter, answer) in enumerate(answers):
        print question_numbers[counter] + ':', answer

    
