def lowercaseWords(words):
    return [word.lower() for word in words]

def removeSymbolsAndNumbers(words):
    return [word for word in words if word.isalpha()]
    
def generateWordCountDictionary(words):
    dictionary = {}
    for word in words:
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
    return dictionary

def generateGlobalWordsList(globalList, text):
    for word in text:
        if word in globalList:
            continue
        else:
            globalList.append(word)