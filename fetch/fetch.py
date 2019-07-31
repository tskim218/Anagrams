import uuid

from nameko.rpc import rpc
from flask import Flask, request, jsonify
from collections import defaultdict
import statistics
import functools

class FetchService:
    name = "fetch_service"

    @rpc
    def fetchAnagramLimit(self, count, word, dictWords):
        anagramList = []
        try:
            word = word.split('.')[0].lower()
            sortedReqWord = "".join("".join(sorted(word)).split())
            for w in dictWords:
                sortedDictWord = "".join(sorted(w))
                if sortedDictWord == sortedReqWord:
                    anagramList.append(w)

            anagramList = sorted(anagramList)

            if word in anagramList:
                anagramList.remove(word)

            if count is not None:
                return {'anagrams': anagramList[:int(count)]}
            else:
                return {'anagrams': anagramList}
        except:
            return ""
 
    @rpc
    def fetchWord(self, word, dictWords):
        try:
            word = "".join(word.split('.')[0].lower().split())
            if word in dictWords:
                return {'word': word}
            else:
                return '{} no exist'.format(word)
        except:
            return "wrong format"

    @rpc
    def fetchStatics(self, dictWords):
        try:
            countValue  = len(dictWords)
            minValue    = min(map(len, dictWords.keys()))
            maxValue    = max(map(len, dictWords.keys()))
            medianValue = statistics.median(map(len, dictWords.keys()))
            meanValue   = statistics.mean(map(len, dictWords.keys()))

            response = { 'countOfValue': countValue, 'min': minValue, \
                        'max': maxValue, 'median': medianValue, 'average': meanValue }

            return response
        except:
            return ""

    @rpc
    def fetchIsAllAnagrms(self, wordList):
        groupAnagram = defaultdict(list)

        try:
            for word in wordList['words']:
                word = ("".join(word.split())).lower()
                sortedWord = "".join(sorted(word))
                if word:
                    groupAnagram[sortedWord].append(word)

            if len(groupAnagram) == 1:
                response = { 'anagrams': \
                        functools.reduce(lambda x, y: x + y,\
                            [group for group in groupAnagram.values()])
                            }

                return response
            return ""
        except:
            return ""

    @rpc
    def fetchMostAnagrmas(self, dictWords):
        groupAnagram = defaultdict(list)
        maxCount = 0

        try:
            for w in dictWords:
                sortedDictWord = "".join(sorted(w))
                if sortedDictWord not in groupAnagram:
                    groupAnagram[sortedDictWord] = [[w], [1]]
                else:
                    groupAnagram[sortedDictWord][0].append(w)
                    groupAnagram[sortedDictWord][1][0] += 1

                maxCount = max(maxCount, groupAnagram[sortedDictWord][1][0])

            maxAnagram = list()
            for anagrams in groupAnagram.values():
                if len(anagrams[0]) == maxCount:
                    maxAnagram.append(anagrams[0])

            return { 'Most Anagrams':  maxAnagram }
        except:
            return ""

    @rpc
    def fetchAnagramSize(self, size, dictWords):
        groupAnagram = defaultdict(list)

        try:
            for w in dictWords:
                sortedDictWord = "".join(sorted(w))
                groupAnagram[sortedDictWord].append(w)

            result = (list(filter(lambda x: len(x) >= int(size),\
                        [g for g in groupAnagram.values()])))
            return {'Anagrams': result}

        except:
            return ""
