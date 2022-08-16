class MostLikelyTagEstimator:
	
	def __init__(self, trainingFileName = 'pos_tagged.txt'):
		self._tagSet = set()
		self._mostLikelyTags = dict()
		self._mostLikelyProbabilities = {}
		self._trainingCorpus = []
		self.Train(trainingFileName)

	def Train(self, trainingFileName = 'pos_tagged.txt'):
		try:
			
			with open(trainingFileName) as trainingFile:
				self._trainingCorpus = list(x.split('/') for x in trainingFile.read().split())
		except IOError:
			print(f'Error: Could not open {trainingFileName}')
			print('Call \'Train(FileName)\' to read the correct file.')
		else:
			for wordTagPair in self._trainingCorpus:
				self._mostLikelyProbabilities[wordTagPair[0]] = 0
				self._mostLikelyTags[wordTagPair[0]] = ""
				self._tagSet.add(wordTagPair[1])

			trainingCorpusLength = len(self._trainingCorpus)

			self._printProgressBar(0, trainingCorpusLength)
			for i in range(trainingCorpusLength):
				word = self._trainingCorpus[i][0]

				previousTag = self._trainingCorpus[i - 1][1] if i != 0 else ""
				currentTag = self._trainingCorpus[i][1]

				highestProbability = self._calculatePriorTimesLikelihood(currentTag, previousTag, word)
				if highestProbability > self._mostLikelyProbabilities[word]:
					self._mostLikelyProbabilities[word] = highestProbability
					self._mostLikelyTags[word] = currentTag

				self._printProgressBar(i + 1, trainingCorpusLength)

	def PrintProbabilities(self):
		print("-" * 100)
		print(f"{'Word':<40s}| {'p*(t|w)':<25s}| {'Most Likely Tag':<10s}")
		print("-" * 100)
		for word in self._mostLikelyProbabilities:
			print(f"{word:<40s}| {str(self._mostLikelyProbabilities[word]):<25s}| {str(self._mostLikelyTags[word]):<10s}")

	def _calculatePriorTimesLikelihood(self, currentTag, previousTag, word):
		numCombinedPrior = 0

		numCombinedLikelihood = 0

		numOccurrences = 0

		if previousTag == "":
			for wordTagPair in self._trainingCorpus:
				if wordTagPair[1] == currentTag:
					numOccurrences += 1
					if wordTagPair[0] == word:
						numCombinedLikelihood += 1
			
			return numCombinedLikelihood / numOccurrences
		else:
			if self._trainingCorpus[0][1] == currentTag:
				numOccurrences += 1

			for i in range(len(self._trainingCorpus) - 1):
				if self._trainingCorpus[i + 1][1] == currentTag:
					numOccurrences += 1
					if self._trainingCorpus[i][1] == previousTag:
						numCombinedPrior += 1
					if self._trainingCorpus[i + 1][0] == word:
						numCombinedLikelihood += 1
			
			return (numCombinedPrior / numOccurrences) * (numCombinedLikelihood / numOccurrences)

	def _printProgressBar(self, currentIteration, totalIterations, precision = 1, width = 60, fillChar = '='):
		percentageComplete = ("{0:." + str(precision) + "f}").format(100 * (currentIteration / float(totalIterations)))
		filledLength = int(width * currentIteration // totalIterations)
		toPrint = fillChar * filledLength + '.' * (width - filledLength)
		print(f'\r{"Training in progress:"} [{toPrint}] {percentageComplete}% {"Complete"}', end = "\r")
		if currentIteration == totalIterations: 
			print()
			print()

def main():
	print("This program computes p*(t|w) = argmax p(t|w) for each word in a provided corpus of tagged sentences\n")
	mle = MostLikelyTagEstimator()

	mle.PrintProbabilities()

	input("\nPress <RETURN> to continue")

if __name__ == "__main__":
	main()

