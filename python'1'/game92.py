import random

words_pool = ["apple", "banana", "orange", "kiwi"]
secret_word = random.choice(words_pool)

display_word = ["_"] * len(secret_word)
attempts_left = 6
guessed_letters = set()

print("Hello in the word game ^_^")
print("".join(display_word))

while attempts_left > 0 and "_" in display_word:
    guess = input("\n5amen 7aref: ").lower()

    if len(guess) != 1 or not guess.isalpha():
        print("Da5el 7aref wa7ad ma 2aktar!")
        continue

    if guess in guessed_letters:
        print("Hayda el 7aref jarrabto abel!")
        continue

    guessed_letters.add(guess)

    if guess in secret_word:
        print(f"Bravo! '{guess}' mawjoudeh.")

        for index in range(len(secret_word)):
            if secret_word[index] == guess:
                display_word[index] = guess
    else:
        attempts_left -= 1
        print(
            f"Ghalat! El 7arf mesh mawjouud. " f"El mo7awalet el be2yi: {attempts_left}"
        )

    print("".join(display_word))

if "_" not in display_word:
    print("\nMabrouk! Rbe7et! :D")
else:
    print(f"\n5esret! El kelme kenet: {secret_word} d:")
