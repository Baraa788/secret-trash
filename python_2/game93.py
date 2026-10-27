print("welcome to my computer quiz!")

playing = input("Do you want to play..? ")
if playing.lower() != "yes":
    quit()

print("okay.. let's play:")
score = 0


quiz_data = {
    "what does CPU stand for? ": "central processing unit",
    "what does GPU stand for? ": "graphics processing unit",
    "what does RAM stand for? ": "random access memory",
    "what does PSU stand for? ": "power supply"
}


for question, correct_answer in quiz_data.items():
    answer = input(question)
    
    if answer.lower() == correct_answer:
        print("Correct :)")
        score += 1
    else:
        print("Incorrect :(")


total_questions = len(quiz_data)

#you got 3 out of 4 questions correct!
print(f"you got {score} out of {total_questions} questions correct..!")
