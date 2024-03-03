alphabet = 'abcdefghijklmnopqrstuvwxyz '

def shifer(word):
    shifted_word = ""
    for i in range(0, len(word)):
        letter = word[i]
        if letter in alphabet:
            index = alphabet.index(letter)
            shifted_index = (index + 1) % len(alphabet)  # Зсув вправо на 1 позицію
            shifted_letter = alphabet[shifted_index]
            shifted_word += shifted_letter
        else:
            shifted_word += letter
    print(shifted_word)
    unshifer(shifted_word)

def unshifer(word):
    original_word = ""
    for i in range(0, len(word)):
        letter = word[i]
        if letter in alphabet:
            index = alphabet.index(letter)
            shifted_index = (index - 1) % len(alphabet)  # Зсув вліво на 1 позицію
            shifted_letter = alphabet[shifted_index]
            original_word += shifted_letter
        else:
            original_word += letter
    print(original_word)

shifer(input("Enter a word: "))



