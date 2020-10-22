import nltk
import contractions

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from helpers import lowercaseWords, removeSymbolsAndNumbers, generateWordCountDictionary

def generateTopicsDictionary(root):
    file_data = {}
    file_data['FILE_ID'] = root.attrib['itemid']
    file_topics = []
    for codes in root.iter('codes'):
        if codes.attrib['class'] == "bip:topics:1.0":
            for child in codes:
                file_topics.append(child.attrib['code'])
    file_data['FILE_TOPICS'] = file_topics
    return file_data

def getFileWords(root):
    file_words = []
    title_content = getElementContentFromFile(root, 'title')
    text_content = getElementContentFromFile(root, 'p')
    file_content = title_content + text_content
    file_words += generateWordList(file_content)
    return file_words

def getElementContentFromFile(root, elementName):
    content = ""
    for element in root.iter(elementName):
       content += element.text
    return content

def generateWordList(text):
    clean_text = removeContractions(text)
    tokens = tokenizeText(clean_text)
    lower_words = lowercaseWords(tokens)
    clean_words = removeSymbolsAndNumbers(lower_words)
    clean_words = removeStopWords(clean_words)
    return clean_words

def removeContractions(s):
    return contractions.fix(s)

def tokenizeText(s):
    return nltk.word_tokenize(s)

def removeStopWords(words):
    stop_words = stopwords.words('english')
    stop_words.append('reuters')
    stop_words.append('Reuters')
    return [word for word in words if not word in stop_words]

def lemmatizeWords(words):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in words]


