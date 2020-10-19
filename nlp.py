import re
import nltk
import string
import contractions

from nltk.corpus import stopwords
from helpers import lowercaseWords, removeSymbolsAndNumbers, generateWordCountDictionary

def tokenizeSentence(s):
    return nltk.word_tokenize(s)

def removeContractions(words):
    return [contractions.fix(word) for word in words]

def removeStopWords(words):
    stop_words = stopwords.words('english')
    return [word for word in words if not word in stop_words]

def generateWordList(s):
    tokens = tokenizeSentence(s)
    words = lowercaseWords(tokens)
    words = removeContractions(words)
    words = removeSymbolsAndNumbers(words)
    words = removeStopWords(words)
    return words

def getTitleTagContent(root):
    title_tag = root.find('title')
    title_content = generateWordList(title_tag.text)
    return title_content

def getTextTagContent(root):
    text_content = []
    for text_tag in root.findall('text'):
        for p_tag in text_tag.findall('p'):
            text_content += generateWordList(p_tag.text)
    return text_content

def generateGlobalWordsList(wordList, text):
    for word in text:
        if word in wordList:
            continue
        else:
            wordList.append(word)

def generateCountDictionaies(globalList, files):
    dictionaries_list = []

    for file in files:
        root = file.getroot()
        file_words = []
        file_words += getTitleTagContent(root)
        file_words += getTextTagContent(root)
        generateGlobalWordsList(globalList, file_words)
        file_dict = generateWordCountDictionary(file_words)
        dictionaries_list.append(file_dict)

    return dictionaries_list

