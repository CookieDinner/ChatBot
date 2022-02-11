import csv
import unidecode
import textdistance
import dill as pickle
import pathlib
import re
import os
import functools

#strategia:
#słowa nie ma w słowniku?
#przeszukaj wszystkie słowa i znajdź najbliższe mu
#nie potrzeba tworzyc slownikow z literowkami

def haveCommonValues(list1, list2):
    return len(set(list1).intersection(set(list2))) > 0

class Dictionary:
    def __init__(self, file, wordsList = [], processWord = None):
        wordsList = [word.lower() for word in wordsList]
        wordsList = wordsList if processWord == None else [processWord(word) for word in wordsList]
        self.wordsList = wordsList
        self.processWord = processWord

        with open(file, newline='', encoding='utf-8') as csvfile:
            self.dictionary = {}
            reader = csv.reader(csvfile, delimiter=',')

            for forms in reader:
                forms = [form.lower() for form in forms]
                if processWord != None:
                    forms = [processWord(form) for form in forms]
                if self.shouldSkip(forms):
                    continue
                for form in forms:
                    if form not in self.dictionary:
                        self.dictionary[form] = []
                    if form[0] not in self.dictionary[form]:
                        self.dictionary[form].append(forms[0])
    def shouldSkip(self, forms):
        if self.wordsList == []:
            return False

        for form in forms:
            if form in self.wordsList:
                return False

        return True

    def findNearest(self, word, maxCharactersDifference):
        nearest = []
        minDistance = maxCharactersDifference + 1

        for potentialNearest in self.dictionary:
            if abs(len(word) - len(potentialNearest)) > maxCharactersDifference:
                continue
            distance = textdistance.levenshtein(word, potentialNearest)
            if distance > maxCharactersDifference:
                continue
            elif distance == minDistance:
                nearest.append(potentialNearest)
            elif distance < minDistance:
                minDistance = distance
                nearest = [potentialNearest]

        return nearest

    def match(self, word1, word2):
        if word1 == word2:
            return True

        word1 = (word1 if self.processWord == None else self.processWord(word1)).lower()
        word2 = (word2 if self.processWord == None else self.processWord(word2)).lower()

        if word1 == word2:
            return True

        if word1 in self.dictionary and word2 in self.dictionary and haveCommonValues(self.dictionary[word1], self.dictionary[word2]):
            return True

        return False

    def matchFirstImperfectSecondPerfect(self, word1, word2, maxCharactersDifference):
        if word1 == word2:
            return True

        word1 = (word1 if self.processWord == None else self.processWord(word1)).lower()
        word2 = (word2 if self.processWord == None else self.processWord(word2)).lower()

        if word1 == word2:
            return True

        if word1 in self.dictionary and word2 in self.dictionary and haveCommonValues(self.dictionary[word1], self.dictionary[word2]):
            return True

        if maxCharactersDifference > 0:
            word1Nearest = self.findNearest(word1, maxCharactersDifference)
            word1NearestMainForms = functools.reduce(lambda a,b: a + b, [self.dictionary[word] for word in word1Nearest])
            if word2 in self.dictionary and len(word1Nearest) > 0 and haveCommonValues(word1NearestMainForms, self.dictionary[word2]):
                return True

        return False

class Matcher:
    def init():
        path = str(pathlib.Path(__file__).parent.resolve()) + '\\' + "dictionary.txt"
        pathPicklePerfect = str(pathlib.Path(__file__).parent.resolve()) + '\\' + "perfect"
        pathPickleImperfect = str(pathlib.Path(__file__).parent.resolve()) + '\\' + "imperfect"
        supportedWords = Matcher.getSupportedWords()

        if os.path.exists(pathPicklePerfect):
            Matcher.perfect = pickle.load(open(pathPicklePerfect, 'rb'))
        else:
            print('Wczytywanie słownika dokładnego...')
            Matcher.perfect = Dictionary(path, wordsList=supportedWords)
            pickle.dump(Matcher.perfect, open(pathPicklePerfect, 'wb'))

        if os.path.exists(pathPickleImperfect):
            Matcher.imperfect = pickle.load(open(pathPickleImperfect, 'rb'))
        else:
            print('Wczytywanie słownika heurystycznego...')
            Matcher.imperfect = Dictionary(path, wordsList=supportedWords, processWord=lambda x: unidecode.unidecode(x))
            pickle.dump(Matcher.imperfect, open(pathPickleImperfect, 'wb'))
        pass
    def matchPerfectly(word1, word2):
        return Matcher.perfect.match(word1, word2)

    def matchFirstImperfectlySecondPerfectly(imperfect, perfect, maxCharactersDifference):
        return Matcher.imperfect.matchFirstImperfectSecondPerfect(imperfect, perfect, maxCharactersDifference)

    def getSupportedWords():
        path = str(pathlib.Path(__file__).parent.resolve()) + '\\' + "ChatBot.py"
        with open(path, 'r', encoding='utf-8') as file:
            fileText = file.read()
            fileText = (fileText.split('#start'))[1].split('#end')[0]
            fileText = re.sub("[^\wÀ-úÀ-ÿ]+", " ", fileText)
            words = fileText.split(' ')
            words = list(set(words))
            return words

    def wordInPerfectly(word, words):
        for matchWord in words:
            if Matcher.matchPerfectly(matchWord, word):
                return True

        return False

    def wordInImperfectly(word, words, maxCharactersDifference):
        for matchWord in words:
            if Matcher.matchFirstImperfectlySecondPerfectly(word, matchWord, maxCharactersDifference):
                return True
        return False

    def wordInImperfectlyReversed(word, words, maxCharactersDifference):
        for matchWord in words:
            if Matcher.matchFirstImperfectlySecondPerfectly(matchWord, word, maxCharactersDifference):
                return True
        return False


Matcher.init()

Matcher.matchFirstImperfectlySecondPerfectly('pieczarkii', 'pieczarki', 2)
print()
# assert(Matcher.wordInImperfectly(piz))