import re

def removePunctuation(s):
    return re.sub(r'[^\w\s]','',s.lower())

def generateWordList(s):
    clean_string = removePunctuation(s)
    words = clean_string.split(' ')
    return words

def generateWordCountDictionary(words):
    dictionary = {}
    for word in words:
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
    return dictionary