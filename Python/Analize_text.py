import string


def words(file):
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    for p in string.punctuation:
        text = text.replace(p, " ")
    words = text.split()
    with open("Analize_text.txt", "a") as f:
        f.write(f"\n{len(words)} words \n")


def analize_text(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            text = f.read().lower()
    except FileNotFoundError:
        print(f"Файл з назвою {file} не знайдено.")
        return
    for p in string.punctuation:
        text = text.replace(p, " ")

    words = text.split()
    word_count = {}

    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

    with open("Analize_text.txt", "a", encoding="utf-8") as f:
        f.write(f"\nRetreated words:\n")
        for word, count in sorted_words:
            f.write(f"\n{word}: {count} ")
    print("Аналіз тексту успішно завершено.")


def Average_length(file):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        line_count = len(lines)
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    letter_count = len(text.replace(" ", ""))
    average_length = letter_count / line_count
    with open(f"Analize_text.txt", "a", encoding="utf-8") as f:
        f.write(f"Average length: {round(average_length)}")


def punctuation(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            text = f.read().lower()
    except FileNotFoundError:
        print(f"Файл з назвою {file} не знайдено.")
        return
    text = text.replace(" ", "")
    letter_count = sum(1 for char in text if char.isalpha())
    punctuation_count = sum(1 for char in text if char in string.punctuation)
    with open(f"Analize_text.txt", "a", encoding="utf-8") as f:
        f.write(f"\nletter_count: {letter_count}\npunctuation_count: {punctuation_count}\n")

def main():
        file = input("File:")
        words(file)
        Average_length(file)
        punctuation(file)
        analize_text(file)



if __name__ == "__main__":
    main()
