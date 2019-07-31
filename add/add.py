import uuid

from nameko.rpc import rpc
from flask import Flask, request, jsonify

class AddService:
    name = "add_service"
 
    @rpc
    def wordAddition(self, wordList, dictWords):
        try:
            for word in wordList['words']:
                word = "".join(word.split())
                if word and word not in dictWords:
                    dictWords[word.lower()] = ''
            return dictWords
        except:
            return ""