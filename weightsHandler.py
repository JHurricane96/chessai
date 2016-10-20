import weights

class WeightsHandler(object):
	def __init__(self, weightsFileName):
		self._weightsFileName = weightsFileName
		self._weightsFileHandler = open(self._weightsFileName, "w")
		weights.initPosPnts = [[0 for i in range (0, 64)] for j in range (0, 6)]
		weights.finalPosPnts = [[0 for i in range (0, 64)] for j in range (0, 6)]
		self.writeWeightsToFile()

	def writeWeightsToFile(self):
		self._weightsFileHandler.seek(0, 0)
		self._weightsFileHandler.write(
			"initPosPnts = {}\nfinalPosPnts = {}".format(
				str(weights.initPosPnts),
				str(weights.finalPosPnts)
			)
		)

	def closeWeightsFile(self):
		self._weightsFileHandler.close()

	def setWeights(self, initPosWeights, finalPosWeights):
		weights.initPosPnts = initPosWeights[:]
		weights.finalPosPnts = finalPosWeights[:]

	def getWeights(self):
		return (weights.initPosPnts[:], weights.finalPosPnts[:])