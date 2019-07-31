import uuid

from nameko.rpc import rpc
from flask import Flask, request, jsonify
import copy

class DeleteService:
    name = "delete_service"
 
    @rpc
    def deleteAllWords(self, dictWords):
        dictWords.clear()

        return dictWords

    @rpc
    def deleteAnagrms(self, word, dictWords):
        copyDict = copy.deepcopy(dictWords)

        try:
            sortedReqWord = "".join(sorted(word.split('.')[0].lower()))
            for w in copyDict:
                sortedDictWord = "".join(sorted(w))
                if sortedDictWord == sortedReqWord:
                    dictWords.pop(w)
            copyDict = {}
            
            return dictWords
        except:
            return copyDict

    @rpc
    def deleteSingle(self, word, dictWords):
        word = "".join(word.split('.')[0].lower().split())
        dictWords.pop(word, None)

        return dictWords