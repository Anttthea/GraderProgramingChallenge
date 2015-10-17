# Grader Programming Challenge

## Notes

* This code was developed with python version `2.7.6`
* Tested on English, French, German and Spanish
* To change the dictionary file, please use `changeDictionary('dictionary_file.txt')` in python. An example is given
  below. The dictionary files should be under the same folder as python files. The default dictionary of the program is en.txt(English) dictionary
* The dictionary files were taken from a scrabble game and they were found
  in https://github.com/atebits/Words and was more complete than the
  the /usr/share/dict/words and for not depending on a unix system


## Pre requisites

As pre requisites you need

* python `2.x`

## Word Recognition

* A word is defined as a non whitespaces string with no heading or trailing punctuations, but may contain punctuations in the middle. (e.g He's is considered as one word)
* All whitespaces are considered as delimiters. A delimiter contains at least one whitespace.
* The followings taken from string.punctuation in python are considered punctuations by the program and are ignored: `!"#$%&\'()*+,-./:;<=>?@[\\]^_``{|}~` (e.g grade("He is a student.", "He's a student.")) result: (False, None, []), since Hes is in english dictionary)


## Unicode Support

* The program supports unicode format string. For sentence containing non-ASCII characters, please specify the input string as u"string"
* The dictionary vocabulary file should be encoded in utf-8


## Usage

```
python

>>> from grade import *
>>> result = grade(correct_answer,student_answer)
>>> print result
[correct, blame, highlights]
```

Example:

```
>>> from grade import *
>>> result = grade("That is my house.", "This is your house!")
>>> print result
(False, None, [])
```

```
>>> from grade import *
>>> result = grade(u"abaissâme", u"abaissâmes")
>>> print result
# word "abaissâmes" is not in English dictionary "en.txt"
(True, 'typo', [((0, 9), (0, 10))])
>>> changeDictionary("fr.txt")
>>> result = grade(u"abaissâme", u"abaissâmes")
>>> print result
# word "abaissâmes" is in French dictionary "fr.txt"
(False, 'wrong_word', [((0, 9), (0, 10))])
```

```
>>> from grade import *
>>> result = grade("This is my house.", "This is mi hhouse")
>>> print result
# word "mi" is in the provided dictionary "en.txt"
(False, 'wrong_word', [((8, 10), (8, 10))])
```

```
>>> from grade import *
>>> result = grade(u"über is not an English word", u"über is not an English ")
>>> print result
# for missing word at the end of the string, the missing location displayed in result is the end of the sentence
(False, 'missing', [((23, 27), (23, 23))])
```

