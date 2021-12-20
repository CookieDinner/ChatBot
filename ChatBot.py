import re
import unidecode


def message_probability(message, words, required=None):
    if required is None:
        required = []

    certainty = 0
    has_required = True

    for word in message:
        if word in words:
            certainty += 1

    total_probability = float(certainty) / float(len(words))

    if required:
        for word in required:
            if word not in message:
                has_required = False
                break

    if not required or has_required:
        return int(total_probability * 100)
    else:
        return 0


def check_all(message):
    highest_probability_list = {}

    def answer(bot_response, words_list, required=None):
        if required is None:
            required = []

        nonlocal highest_probability_list
        highest_probability_list[bot_response] = message_probability(message, words_list, required)

    # Tutaj wrzucamy odpowiedzi ----------------------------------------------------------------------------------------

    answer('Cześć.', ['czesc', 'halo', 'witam'])

    answer('Dzień dobry.', ['dzien', 'dobry'], required=['dzien', 'dobry'])

    answer('Do widzenia.', ['pa', 'do', 'widzenia', 'na', 'razie'])

    answer('Restauracja jest otwarta w godzinach 8:00 - 20:00.',
           ['w', 'jakich', 'godzinach', 'restauracja', 'otwarta'], required=['godzinach'])

    answer('Restauracja jest otwarta od Poniedziałku do Piątku.',
           ['kiedy', 'otwarta', 'restauracja', 'w', 'jakich', 'dniach', 'tygodnia'])

    answer('Restauracja znajduje się przy ul. NieMaTakiejUlicy 42B, obok pomostu z krasnalem.',
           ['gdzie', 'znajduje', 'restauracja', 'ulicy', 'miejscu', 'w', 'jakim'])

    answer('Serwujemy najlepszą pizzę na naszej ulicy!',
           ['pizza', 'macie', 'serwujecie', 'posiadacie'], required=['pizza'])

    # Koniec odpowiedzi ------------------------------------------------------------------------------------------------

    matched = max(highest_probability_list, key=highest_probability_list.get)

    return 'Przepraszam, ale nie rozumiem co masz na myśli...' if highest_probability_list[matched] < 10 else matched


def get_answer(message):
    split_message = re.split(r'\s+|[.,?!;-]\s*', unidecode.unidecode(message.lower()))
    answer = check_all(split_message)
    return answer


if __name__ == "__main__":
    while True:
        print('Adam: ' + get_answer(input('Ty: ')))
