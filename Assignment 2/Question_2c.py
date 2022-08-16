from Question_2a import MostLikelyTagEstimator
import webbrowser

class MostLikelyTagAnalyzer(MostLikelyTagEstimator):
	def __init__(self, trainingFileName = 'pos_tagged.txt', goldenFileName = 'pos_golden_standard.txt'):
		super().__init__(trainingFileName)
		self._confusionMatrix = dict()
		self._goldenCorpus = []
		self._goldenTagSet = set()
		self._totalErrors = 0
		self._totalUnknownErrors = 0
		self.LearnGoldenStandard(goldenFileName)

	def LearnGoldenStandard(self, goldenFileName):
		try:
			with open(goldenFileName) as goldenFile:
				self._goldenCorpus = list(x.split('/') for x in goldenFile.read().split())
		except IOError:
			print(f'Error: Could not open {goldenFileName}')
			print('Call \'LearnTestSet(FileName)\' to read the correct file.')
		else:
			for wordTagPair in self._goldenCorpus:
				self._goldenTagSet.add(wordTagPair[1])
				self._goldenTagSet.add(self._mostLikelyTags.get(wordTagPair[0], "NN"))

			self._goldenTagSet.add("NN")

			self._initializeConfusionMatrix()

			self._computeConfusionMatrix()

	def DisplayConfusionMatrix(self):
		print("The Confusion Matrix might be too large for console output.")
		print("So it will be displayed in your default text editor instead.")
		print("Be sure to disable Word Wrapping to allow horizontal scrolling.")
		print("In Notepad, untick: Format >> Word Wrap")

		with open("confusion_matrix.txt", "w") as f:
			print("-----------------", file=f)
			print("Confusion Matrix:", file=f)
			print("-----------------", file=f)

			header = f"{'':^8s}"
			for tag in self._confusionMatrix:
				header += f"{tag:^8s}"
			print(header, file=f)

			for outerTag in self._confusionMatrix:
				line = f"{outerTag:^8s}"
				innerDict = self._confusionMatrix[outerTag]
				for innerTag in innerDict:
					innerValue = round(innerDict[innerTag], 5)
					line += f"{str(innerValue) if innerValue != 0 else '-':^8s}"
				
				print(line, file=f)

			print("-------------------------------------------------------", file=f)
			print(f"Total Errors: {self._totalErrors} ({self._totalUnknownErrors} of which are due to unknown words)", file=f)
			print(f"Accuracy: {round(((len(self._goldenCorpus) - self._totalErrors) / len(self._goldenCorpus) * 100), 5)}%", file=f)
			print("-------------------------------------------------------\n", file=f)

		webbrowser.open("confusion_matrix.txt")

	def _initializeConfusionMatrix(self):
		for outerTag in self._goldenTagSet:
			innerDict = dict()
			for innerTag in self._goldenTagSet:
				innerDict[innerTag] = 0
			
			self._confusionMatrix[outerTag] = innerDict

	def _computeConfusionMatrix(self):
		self._totalErrors = 0
		self._totalUnknownErrors = 0
		for wordTagPair in self._goldenCorpus:
			word = wordTagPair[0]
			correctTag = wordTagPair[1]
			predictedTag = self._mostLikelyTags.get(word, "NN")

			if correctTag != predictedTag:
				self._totalErrors += 1

				self._confusionMatrix[correctTag][predictedTag] += 1

				if predictedTag == "NN":
					self._totalUnknownErrors += 1

		if self._totalErrors != 0:
			for outerTag in self._confusionMatrix:
				for innerTag in self._confusionMatrix[outerTag]:
					self._confusionMatrix[outerTag][innerTag] /= self._totalErrors



def main():
	print("This program accepts a 'golden standard' file and prints a Confusion Matrix for the trained corpus\n")
		
	mla = MostLikelyTagAnalyzer()

	mla.DisplayConfusionMatrix()

	input("\nPress <RETURN> to continue")

if __name__ == "__main__":
	main()
