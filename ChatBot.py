import re
import unidecode


menu = [
    ["Margarita", "Sos pomidorowy łagodny, Ser mozzarella, Oregano", 25.5],
    ["Funghi", "Sos pomidorowy łagodny, Ser mozzarella, Pieczarki, Oregano", 26.5],
    ["Vege", "Sos pomidorowy łagodny, Ser mozzarella, Pieczarki, Oregano, Papryka, Kukurydza", 26.5],
    ["Rustica", "Sos pomidorowy łagodny, Ser mozzarella, Oregano, Boczek", 27.5],
    ["Salami", "Sos pomidorowy łagodny, Ser mozzarella, Oregano, Salami", 28.0],
    ["Capricciosa", "Sos pomidorowy łagodny, Ser mozzarella, Pieczarki, Oregano, Papryka, Szynka", 28.5],
    ["Meksykańska", "Sos pomidorowy pikantny, Ser mozzarella, Oregano, Cebula, Kiełbasa, Papryka, Kukurydza, Fasola czerwona, Wołowina, Papryczki Jalapeno, Zielony pieprz", 30.0],
    ["Kebab", "Sos pomidorowy pikantny, Ser mozzarella, Oregano, Pomidor, Ogórek świeży, Sos gyros, Kurczak gyros, Kapusta Pekińska, Czerwona Cebula", 30.0],
    ["Chorizo", "Sos pomidorowy łagodny, Ser mozzarella, Oregano, Pomidor koktajlowy, Czerwona Cebula, Kiełbasa Chorizo, Zielony pieprz", 32],
]

pizzas = ""

for i in range(0,len(menu)):
    pizzas += str(i+1) + '.' + menu[i][0] + '\n'


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


    answer('Dzień dobry.', ['czesc', 'halo', 'witam', 'dzien', 'dobry', 'hej','dzien', 'dobry'])

    answer('Do widzenia.', ['pa', 'do', 'widzenia', 'na', 'razie'])

    answer('Restauracja jest otwarta w godzinach 8:00 - 20:00.',
           ['w', 'jakich', 'godzinach', 'restauracja', 'otwarta', 'o ktorej'])

    answer('Restauracja jest otwarta od Poniedziałku do Piątku.',
           ['kiedy', 'otwarta', 'restauracja', 'w', 'jakich', 'dniach', 'tygodnia'])

    answer('Restauracja znajduje się przy ul. NieMaTakiejUlicy 42B, obok pomostu z krasnalem.',
           ['gdzie', 'znajduje', 'restauracja', 'ulicy', 'miejscu', 'w', 'jakim'])

    answer('Serwujemy najlepszą pizzę na naszej ulicy!',
           ['pizza', 'macie', 'serwujecie', 'posiadacie'], required=['pizza'])

    answer('Jest możliwość dowozu w obrębie Poznania, a dla Winogradów i Starego Miasta dostawa jest darmowa dla zamówień za min 50zł!',
           ['czy', 'macie', 'mozliwosc', 'dowozu', 'dowoz', 'dostawa', 'dostawy', 'opcja'])

    answer('Wszystkie nasze pizze mają około 30cm średnicy',
           ['pizza', 'wielkosc', 'duza', 'posiadacie', 'macie', 'rozmiar', 'średnica'])

    answer('Nasze sosy do pizzy: Pomodorowy łagodny i pikantny, BBQ, Czosnkowy, Bazyliowy, Ziołowy',
           ['pizzy', 'sosy', 'sos', 'macie', 'wybrac'])

    answer('Przy składaniu zamówienia jest opcja wyboru rodzaju ciasta (mamy i cienkie i grube)',
           ['pizza', 'pizzy', 'grubosc', 'ciasto', 'ciescie', 'ma', 'jakim'])

    answer('Aktualne promocje: \nStudenci 10% zniżki na zamówienie!\nTrzecia pizza gratis!\nDo każdej pizzy sos gratis!',
           ['promocje', 'rabaty', 'znizki', 'posiadacie', 'macie', 'jakies'])

    answer('Każdy student ma u nas 10% zniżki na całe zamówienie!',
        ['promocja', 'rabat', 'znizka', 'student', 'studencka', 'jakies'])

    answer('Wszystkie nasze pizza posiadają gluten :)',
        ['pizza', 'gluten', 'bez', 'glutenu', 'ma', 'posiada', 'bezglutenowe'])

    answer('Ananas na pizzy to zbrodnia przeciw ludzkości!',
           ['pizza', 'ananas', 'ananasem', 'dodac'])

    answer('Szanujmy sie, hawajska to nie pizza :)',
           ['pizza', 'hawajska', 'macie', 'gdzie', 'jest'], required=['hawajska'])

    answer('Nasza pizzeria oferuje następnujące menu: \n'+pizzas,
           ['pizze', 'jakie', 'macie', 'menu'])

    answer('Składniki:' +menu[0][1],
           ['pizza', 'margarita', 'skladniki', '1', 'jakie', 'ma'], required=['skladniki'])
    answer('Składniki:' +menu[1][1],
           ['pizza', 'funghi', 'fungi', '2', 'skladniki', 'jakie', 'ma'], required=['skladniki'])
    answer('Składniki:' +menu[2][1],
           ['pizza', 'vege', 'wegeterianska', '3', 'skladniki', 'jakie', 'ma'], required=['skladniki'])
    answer('Składniki:' +menu[3][1],
           ['pizza', 'rustica', '4', 'skladniki', 'jakie', 'ma'], required=['skladniki'])
    answer('Składniki:' +menu[4][1],
           ['pizza', 'salami', '5', 'skladniki', 'jakie', 'ma'], required=['skladniki'])
    answer('Składniki:' +menu[5][1],
           ['pizza', 'Capricciosa', 'Capriczioza', 'Capriciosa', '6', 'skladniki', 'jakie', 'ma'], required=['skladniki'])
    answer('Składniki:' +menu[6][1],
           ['pizza', 'meksykanska', '7', 'skladniki', 'jakie', 'ma'], required=['skladniki'])
    answer('Składniki:' +menu[7][1],
           ['pizza', 'kebab', '8', 'skladniki', 'jakie', 'ma'], required=['skladniki'])
    answer('Składniki:' + menu[8][1],
           ['pizza', 'chorizo', '9', 'skladniki', 'jakie', 'ma'], required=['skladniki'])

    answer('Pizza Margarita kosztuje ' + str(menu[0][2]) + 'zł',
           ['pizza', 'margarita', '1', 'cena', 'jaka', 'ile', 'kosztuje'])
    answer('Pizza Funghi kosztuje ' + str(menu[1][2]) + 'zł',
           ['pizza', 'funghi', 'fungi', '2', 'cena', 'jaka', 'ile', 'kosztuje'])
    answer('Pizza Vege kosztuje ' + str(menu[2][2]) + 'zł',
           ['pizza', 'vege', 'wegeterianska', '3', 'cena', 'jaka', 'ile', 'kosztuje'])
    answer('Pizza Rustica kosztuje ' + str(menu[3][2]) + 'zł',
           ['pizza', 'rustica', '4', 'skladniki', 'cena', 'jaka', 'ile', 'kosztuje'])
    answer('Pizza Salami kosztuje ' + str(menu[4][2]) + 'zł',
           ['pizza', 'salami', '5', 'skladniki', 'cena', 'jaka', 'ile', 'kosztuje'])
    answer('Pizza Capricciosa kosztuje ' + str(menu[5][2]) + 'zł',
           ['pizza', 'Capricciosa', 'Capriczioza', 'Capriciosa', '6', 'cena', 'jaka', 'ile', 'kosztuje'])
    answer('Pizza Meksykańska kosztuje ' + str(menu[6][2]) + 'zł',
           ['pizza', 'meksykanska', '7', 'cena', 'jaka', 'ile', 'kosztuje'])
    answer('Pizza Kebab kosztuje ' + str(menu[7][2]) + 'zł',
           ['pizza', 'kebab', '8', 'skladniki', 'cena', 'jaka', 'ile', 'kosztuje'])
    answer('Pizza Chorizo kosztuje ' + str(menu[8][2]) + 'zł',
           ['pizza', 'chorizo', '9', 'skladniki', 'cena', 'jaka', 'ile', 'kosztuje'])



    # Koniec odpowiedzi ------------------------------------------------------------------------------------------------




    matched = max(highest_probability_list, key=highest_probability_list.get)

    greeting = ""
    if matched != "Dzień dobry.":
        for word in message:
            if word in ['czesc', 'halo', 'witam','dzien', 'dobry', 'hej']:
                greeting = "Dzień dobry. "
                break

    return 'Przepraszam, ale nie rozumiem co masz na myśli...' if highest_probability_list[matched] < 10 else greeting+matched


def get_answer(message):
    split_message = re.split(r'\s+|[.,?!;-]\s*', unidecode.unidecode(message.lower()))
    answer = check_all(split_message)
    return answer


if __name__ == "__main__":
    while True:
        print('Adam: ' + get_answer(input('Ty: ')))
