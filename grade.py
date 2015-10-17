#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liqihui'
import re, string
from gradeComparator import gradeComparator

# Grade a student answer against a given correct answer
#
# @params
#  - correct_answer: a unicode string, the correct answer
#  - student_answer: a unicode string, what the student typed
#
# @return
#  returns a tuple (correct, blame, highlights)
#      - correct:      a boolean, True if and only if the student_answer
#                      should be considered a correct answer
#      - blame:        one out of {None, "typo", "missing", "wrong_word"}
#                      depending on the cause of the mistake, if it can
#                      be detected
#      - highlights:   a list of tuples, where each tuple is of type
#                      ((c1, c2), ((s1, s2)) and c1/s1 is the index of the
#                      first character of a blamed word in
#                      the correct/student's answer and c2/s2 is the index
#                      of the last character of that same blamed word

# --------------------------------GRADE FUNCTION------------------------------
# --------------------------------SENTENCE LEVEL------------------------------
def grade(correct_answer,student_answer):

    # initialize dictionary
    if not ('dictionary_filename' in globals()):
        global dictionary_filename
        dictionary_filename = 'en.txt'
    if not ('gradecomp' in globals()):
        global gradecomp
        gradecomp = gradeComparator(dictionary_filename)

    # initialize word regex
    if not ('word_regex' in globals()):
        global  word_regex
        punc = re.escape(string.punctuation)
        word_regex = re.compile(r'([^\s{}]+[^\s]+[^\s{}]+)|([^\s{}]+)' \
                .format(punc, punc, punc), flags=re.UNICODE)

    correct_wlocs = getWordLocs(correct_answer)
    student_wlocs = getWordLocs(student_answer)
    correct_words = [correct_answer[loc[0]:loc[1]] for loc in correct_wlocs]
    student_words = [student_answer[loc[0]:loc[1]] for loc in student_wlocs]

    cnum = len(correct_words)
    snum = len(student_words)
    distance = cnum - snum

    #student answer has more words than correct answer
    #student answer has more than 1 word missing
    if distance < 0 or distance > 1:
        return (False, None, [])

    # set bummer trailing word
    if distance == 1:
        clastword = correct_words[cnum - 1]
        bummerword = clastword + 'ab'
        student_words.append(bummerword)

    error_num = 0
    mistake_type = ""
    highlights = []

    # index of current word in student answer
    i = 0

    for j in range(cnum):
        grade = gradecomp.gradeWord(correct_words[j], student_words[i])

        if grade == "Wrong":
            error_num += 1

            if error_num > 1:
                return (False, None, [])

            if distance == 1:
                # MISSING WORD
                if i != cnum - 1:
                    start = student_wlocs[i][0]
                else:
                    start = len(student_answer)
                i -= 1
                mistake_type = "missing"
                highlights = []
                highlights.append((correct_wlocs[j],(start,start)))
            else:
                # WRONG WORD
                mistake_type = "wrong_word"
                highlights = []
                highlights.append((correct_wlocs[j],student_wlocs[i]))

        elif grade == "Typo":
            # TYPO
            if mistake_type == "":
                mistake_type = "typo"

            if mistake_type == "typo":
                highlights.append((correct_wlocs[j],student_wlocs[i]))

        i += 1

    # report result
    if mistake_type == "":
        return (True, None, [])
    elif mistake_type == "typo":
        return (True, mistake_type, highlights)
    else:
        return (False, mistake_type, highlights)

def getWordLocs(sentence):

    words_locs = word_regex.finditer(sentence)
    words_locations = [(m.start(),m.end()) for m in words_locs]

    return words_locations

def changeDictionary(dictionary_filename):
    global gradecomp
    gradecomp = gradeComparator(dictionary_filename)
#print grade(u"abaissâme", u"abaissâmes")