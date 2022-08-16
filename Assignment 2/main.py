import Question_2a
import Question_2b
import Question_2c

options = ["Question 2a (Question_2a)", "Question 2b (Question_2b)", "Question 2c (Question_2c)", "Exit"]

while True:
	print("Please enter the question you wish to run: (e.g. Question_2a)")
	for option in options:
		print(">> " + option)
	questionNumber = input(":: ").upper()
	print()

	if questionNumber == "EXIT":
		break
	elif questionNumber == "Question_2a":
		Q3_1.main()
	elif questionNumber == "Question_2b":
		Q3_2.main()
	elif questionNumber == "Question_2c":
		Q3_3.main()
	else:
		print("Error: Invalid input")
