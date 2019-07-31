from flask import request, jsonify, Blueprint

import threading
import gzip
import os

from controller.gateway.utils import rpcProxy
from controller.gateway.init import getSemaphore
from controller.gateway.init import loadDict


controllerBlueprint = Blueprint('controllerBlueprint', __name__)

## init ##
semaphore = getSemaphore()
dictWords = loadDict()


## returns a count of words in the corpus and min/max/median/average word length
@controllerBlueprint.route('/statics', methods=['GET'])
def generalOps():
    global dictWords

    if request.method == 'GET':
        with rpcProxy('fetch_service') as fetchRpc:
            semaphore.acquire()
            result = fetchRpc.fetchStatics(dictWords)
            semaphore.release()

        return jsonify(result), 200

    return jsonify(""), 200


@controllerBlueprint.route('/words.json', methods=['POST', 'DELETE'])
def corpusOPs():
    global dictWords

    if request.method == 'POST':
        with rpcProxy('add_service') as addRpc:
            semaphore.acquire()
            result = addRpc.wordAddition(request.get_json(force=True), dictWords)
            semaphore.release()

            if isinstance(result, dict):
                dictWords = result

            return '', 201

    else:  #### request.method == 'DELETE':   
        with rpcProxy('delete_service') as deleteRpc:
            semaphore.acquire()
            dictWords = deleteRpc.deleteAllWords(dictWords)
            semaphore.release()

        return '', 204


## returns whether or not they are all anagrams of each other
@controllerBlueprint.route('/anagrams', methods=['POST'])
def anagramsChkOps():
    global dictWords

    if request.method == 'POST':
        with rpcProxy('fetch_service') as fetchRpc:
            semaphore.acquire()
            result = fetchRpc.fetchIsAllAnagrms(request.get_json(force=True))
            semaphore.release()

        return jsonify(result), 201


@controllerBlueprint.route('/anagrams/<word>', methods=['GET', 'DELETE'])
def anagramsOps(word):
    global dictWords

    ## Endpoint to delete a word *and all of its anagrams*
    if request.method == 'DELETE':
        with rpcProxy('delete_service') as deleteRpc:
            semaphore.acquire()
            dictWords = deleteRpc.deleteAnagrms(word, dictWords)
            semaphore.release()

        return '', 204

    else:  ####  request.method == 'GET':
        with rpcProxy('fetch_service') as fetchRpc:
            result = ""

            if 'size' in request.args:
                semaphore.acquire()
                result = fetchRpc.fetchAnagramSize(request.args.get('size'), dictWords)
                semaphore.release()

            ## Endpoint that identifies words with the most anagrams
            elif word.lower() == 'most':
                semaphore.acquire()
                result = fetchRpc.fetchMostAnagrmas(dictWords)
                semaphore.release()

            else:  ##if 'limit' in request.args:
                semaphore.acquire()
                result = fetchRpc.fetchAnagramLimit(request.args.get('limit'), word, dictWords)
                semaphore.release()

            return jsonify(result), 200


@controllerBlueprint.route('/words/<word>', methods=['GET', 'DELETE'])
def wordsOps(word):
    global dictWords

    if request.method == 'DELETE':
        with rpcProxy('delete_service') as deleteRpc:
            semaphore.acquire()
            dictWords = deleteRpc.deleteSingle(word, dictWords)
            semaphore.release()

        return '', 204

    ## check if a word exists in corups
    else: ####  request.method == 'GET':
        with rpcProxy('fetch_service') as fetchRpc:
            semaphore.acquire()
            result = fetchRpc.fetchWord(word, dictWords)
            semaphore.release()

        return jsonify(result), 200
