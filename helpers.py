import re
import nltk
import string
import contractions

from nltk.corpus import stopwords
stop_words = stopwords.words('english')


# def removePunctuation(s):
#     return re.sub(r'[^\w\s]','',s.lower())

def generateWordList(s):
    # clean_string = removePunctuation(s)
    tokens = nltk.word_tokenize(s)
    tokens = [word.lower() for word in tokens]
    tokens = [contractions.fix(word) for word in tokens]
    words = [word for word in tokens if word.isalpha()]
    words = [word for word in words if not word in stop_words]
    # clean_string = removePunctuationUnicode(s)
    # words = clean_string.split(' ')
    return words
