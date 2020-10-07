import xml.etree.ElementTree as ET
import os
import re
import pprint

path_mini = os.path.abspath("./Reuters_34/Training/")
path_full = os.path.abspath("./Reuters_7083/Training/")

def parseXMLFiles(path):
    trees = []
    for filename in os.listdir(path):
        if not filename.endswith('.XML'): continue
        fullname = os.path.join(path, filename)
        tree = ET.parse(fullname)
        trees.append(tree)
    return trees
    
def removePunctuation(s):
    return re.sub(r'[^\w\s]','',s.lower())

def generateWordList(s):
    clean_string = removePunctuation(s)
    words = clean_string.split(' ')
    return words

def generateWordCountDictionaries(words):
    dictionary = {}
    for word in words:
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
    return dictionary

def getTitleContent(root):
    title_tag = root.find('title')
    title_content = generateWordList(title_tag.text)
    return title_content

def getTextContent(root):
    text_content = []
    for text_tag in root.findall('text'):
        for p_tag in text_tag.findall('p'):
            text_content += generateWordList(p_tag.text)
    return text_content
    

if __name__ == "__main__":
    files = parseXMLFiles(path_mini)
    dictionaries_list = []

    for file in files:
        root = file.getroot()
        file_words = []
        file_words += getTitleContent(file)
        file_words += getTextContent(file)
        file_dict = generateWordCountDictionaries(file_words)
        dictionaries_list.append(file_dict)
        
    for d in range(len(dictionaries_list)):
        pprint.pprint(dictionaries_list[d])
    # pprint.pprint(dictionaries_list[0])
    # print(files.__len__())