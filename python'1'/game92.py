
import random

words_pool = ["apple", "banana", "orange", "kiwi"]
secret_word = random.choice(words_pool)

display_word = ["_"] * len(secret_word)
attempts_left = 6
guessed_letters = set()

print("Hello in the word game ^_^")
print("For a hint, enter '?' to reveal a letter and lose 2 attempts.")
print(" ".join(display_word))

while attempts_left > 0 and "_" in display_word:

    guess = input("\nDa5el 7aref (or '?' for hint): ").lower()

    # Hint feature
    if guess == "?":

        if attempts_left <= 2:
            print("Ma feek ta5od hint! You need more than 2 attempts.")
            continue

        # Find hidden letters not guessed yet
        hidden_letters = [
            letter for letter in secret_word
            if letter not in guessed_letters
        ]

        if not hidden_letters:
            print("All letters have already been discovered!")
            continue

        hint_letter = random.choice(hidden_letters)

        guessed_letters.add(hint_letter)
        attempts_left -= 2

        print(f" Hint: The letter is '{hint_letter}'")
        print(f" 2 attempts deducted! Remaining: {attempts_left}")

        # Reveal every occurrence of the hinted letter
        for index in range(len(secret_word)):
            if secret_word[index] == hint_letter:
                display_word[index] = hint_letter

        print(" ".join(display_word))

        continue

    # Validate the input
    if len(guess) != 1 or not guess.isalpha():
        print("Da5el 7aref wa7ad ma 2aktar!")
        continue

    # Prevent repeated guesses
    if guess in guessed_letters:
        print("Hayda el 7aref jarrabto abel!")
        continue

    guessed_letters.add(guess)

    # Check the guessed letter
    if guess in secret_word:
        print(f"Bravo! '{guess}' mawjoudeh.")

        for index in range(len(secret_word)):
            if secret_word[index] == guess:
                display_word[index] = guess

    else:
        attempts_left -= 1
        print(
            f"Ghalat! El 7aref mesh mawjoud. "
            f"El mo7awalet el be2yi: {attempts_left}"
        )

    print(" ".join(display_word))

# End of the game
if "_" not in display_word:
    print("\nMabrouk! Rbe7et! :D")
else:
    print(f"\nL2asaf! El kelme kenet: {secret_word} :(")
