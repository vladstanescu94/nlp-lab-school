from xml_parser import getTitleTagContent, getTextTagContent

def generateWordCountDictionary(words):
    dictionary = {}
    for word in words:
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
    return dictionary

def generateGlobalWordsDictionary(dictionary, text):
    for word in text:
        if word in dictionary:
            continue
        else:
            dictionary.append(word)



def generateCountDictionaies(globalList, files):
    dictionaries_list = []

    for file in files:
        root = file.getroot()
        file_words = []
        file_words += getTitleTagContent(root)
        file_words += getTextTagContent(root)
        generateGlobalWordsDictionary(globalList, file_words)
        file_dict = generateWordCountDictionary(file_words)
        dictionaries_list.append(file_dict)

    return dictionaries_list