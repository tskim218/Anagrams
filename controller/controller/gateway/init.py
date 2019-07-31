from collections import defaultdict

import threading, gzip

class Semaphore:
	sem = None

	@staticmethod
	def getSemaphore():
		Semaphore.sem = threading.Semaphore()

		return Semaphore.sem

def getSemaphore():

	return Semaphore.getSemaphore()

def loadDict():
	with gzip.open('/controller/gateway/dictionary.txt.gz', 'rb') as filePtr:
	    fileBuffer = filePtr.read()

	dictWords = defaultdict(lambda: None)

	for word in fileBuffer.decode().split('\n'):
	    word = "".join(word.split())
	    if word:
	        dictWords[word.lower()] = ''

	return dictWords