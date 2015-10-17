__author__ = 'liqihui'

import re, codecs
# --------------------------------GRADE COMPARATOR------------------------------
# --------------------------------WORD LEVEL------------------------------
class gradeComparator:
    # constructor, read in dictionary file
    # compile punctuation regex
    def __init__(self, dictionary_filename):
        punc_pattern = '[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]'
        self.pregex = re.compile(re.escape(punc_pattern), flags=re.UNICODE)
        self.setDictionary(dictionary_filename)

    def preprocessWord(self, word):
        processed = self.pregex.sub('',word)
        return processed.lower()

    def setDictionary(self, dictionary_filename):
        self.dic = set([])
        with codecs.open(dictionary_filename, encoding='utf-8', mode='r') as fdict:
            for line in fdict:
                self.dic.add(line.strip().lower())
# grade a student answer word given a correct word
# @params
#  - correct: a unicode string word, the correct answer word
#  - student: a unicode string word, the word the student typed
#
# @return
#  returns a string result in ("Correct","Typo","Wrong")
    def gradeWord(self, correct, student):
         #preprocess word
        sword = self.preprocessWord(student)
        cword = self.preprocessWord(correct)

        if sword == cword:
            return "Correct"
        elif self.isTypo(cword,sword):
            return "Typo"
        else:
            return "Wrong"

    def isTypo(self,cword,sword):
         #if in dictionary
        if sword in self.dic:
            return False

        c_word = list(cword)
        s_word = list(sword)

        clen = len(c_word)
        slen = len(s_word)
        distance = clen - slen

        # More than 2 inserts or deletes
        if distance > 1 or distance < -1:
            return False

        # set bummer trailing character
        if distance == -1:
            c_word.append('.')
        elif distance == 1:
            s_word.append('.')

        length = max(clen,slen)

        for i in range(length):
            if not s_word[i] == c_word[i]:
                if distance == 0:
                    if i < length - 1 and not s_word[i+1] == c_word[i+1]:
                        # SWAP
                        s = s_word[i]
                        s_word[i] = s_word[i+1]
                        s_word[i+1] = s
                    else:
                        # REPLACE
                        s_word[i] = c_word[i]
                elif distance == -1:
                    # DELETE
                    del s_word[i]
                elif distance == 1:
                    # INSERT
                    s_word.insert(i,c_word[i])
                break

        # get rid of bummer trailing character
        if distance == -1:
            c_word.pop()
        elif distance == 1:
            s_word.pop()

        if s_word == c_word:
            return True
        else:
            return False
