print("welcome to my computer quiz!")

playing = input("Do you want to play ?")

if playing.lower() != "yes":
    quit()
print("okay.. let's play:")
score = 0

answer = input("what does CPU stand for ?")
if answer.lower() == "central processing unit":
    print("Correct  (:")
    score += 1
else:
    print("Incorrect ):")


answer = input("what does GPU stand for ?")
if answer.lower() == "graphics processing unit":
    print("Correct  (:")
    score += 1
else:
    print("Incorrect ):")

answer = input("what does RAM stand for ?")
if answer.lower() == "random access memory":
    print("Correct  (:")
    score += 1
else:
    print("Incorrect ):")

answer = input("what does PSU stand for ?")
if answer.lower() == "power supply ":
    print("Correct  (:")
    score += 1
else:
    print("Incorrect ):")

print(f"you got {(score/4)*100} %")
