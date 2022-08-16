import webbrowser
from Question_2a import MostLikelyTagEstimator
import re

class MostLikelyTagAnnotator(MostLikelyTagEstimator):
	def __init__(self, trainingFileName = 'pos_tagged.txt', testFileName = 'pos_test.txt'):
		super().__init__(trainingFileName)

		self._testSet = []

		self._annotatedWords = []

		self.AnnotateTestSet(testFileName)

	def AnnotateTestSet(self, testFileName):
		try:
			with open(testFileName) as testFile:
				testString = testFile.read()
		except IOError:
			print(f'Error: Could not open {testFileName}')
			print('Call \'LearnTestSet(FileName)\' to read the correct file.')
		else:
			testString = re.sub(r'(\w+)([.,\'"`!?])', r'\1 \2', testString)

			testString = re.sub(r'([.,\'"`!?])(\w+)', r'\1 \2', testString)

			testString = re.sub(r'([\t\n\r])([\w.,\'"!?])', r'\1 \2', testString)

			testString = re.sub(r'([\w.,\'"!?])([\t\n\r])', r'\1 \2', testString)

			self._testSet = testString.split(" ")

			for word in self._testSet:
				if not re.search(r'[\t\n\r]', word[0]):
					self._annotatedWords.append(word + "/" + self._mostLikelyTags.get(word, "NN"))
				else:
					self._annotatedWords.append(word)

			newFileName = f"annotated_{testFileName}"
			with open(newFileName, "w") as annotatedFile:
				annotatedFile.write(self.AnnotatedFileContents())

			print(f"File '{newFileName}' created")

			webbrowser.open(newFileName)

	def AnnotatedFileContents(self):
		return str.join(" ", self._annotatedWords)

def main():
	print("This program accepts a file as an input parameter and produces an annotated file containing POS tags for each word in the input file\n")
	
	mla = MostLikelyTagAnnotator()

	print("Contents of annotated file:\n")
	print(mla.AnnotatedFileContents())

	input("\nPress <RETURN> to continue")

if __name__ == "__main__":
	main()
