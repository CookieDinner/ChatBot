import re
from Dictionary import Matcher

__optimize = True

#start
menu = [
    ["Margarita", "Sos pomidorowy łagodny, Ser mozzarella, Oregano", 25.5, ['margharita', 'margerita', 'margherita']],
    ["Funghi", "Sos pomidorowy łagodny, Ser mozzarella, Pieczarki, Oregano", 26.5, ['fungi', 'fundżi', 'fudżi', 'fugi']],
    ["Vege", "Sos pomidorowy łagodny, Ser mozzarella, Pieczarki, Oregano, Papryka, Kukurydza, wege, wegetariańska", 26.5, ['wege', 'wegetariańska']],
    ["Rustica", "Sos pomidorowy łagodny, Ser mozzarella, Oregano, Boczek", 27.5, ['rustika', 'wiejska']],
    ["Salami", "Sos pomidorowy łagodny, Ser mozzarella, Oregano, Salami", 28.0, []],
    ["Capricciosa", "Sos pomidorowy łagodny, Ser mozzarella, Pieczarki, Oregano, Papryka, Szynka", 28.5, ['capriciosa', 'kapriczioza']],
    ["Meksykańska", "Sos pomidorowy pikantny, Ser mozzarella, Oregano, Cebula, Kiełbasa, Papryka, Kukurydza, Fasola czerwona, Wołowina, Papryczki Jalapeno, Zielony pieprz",
     30.0, ['mexicana']],
    ["Kebab", "Sos pomidorowy pikantny, Ser mozzarella, Oregano, Pomidor, Ogórek świeży, Sos gyros, Kurczak gyros, Kapusta Pekińska, Czerwona Cebula", 30.0, ['kebap']],
    ["Chorizo", "Sos pomidorowy łagodny, Ser mozzarella, Oregano, Pomidor koktajlowy, Czerwona Cebula, Kiełbasa Chorizo, Zielony pieprz", 32, ['czorizo']],
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
        if word in words: #słowo dokładnie w takiej formie
            certainty += 1
        elif Matcher.wordInPerfectly(word, words): #słowo odmienione
            certainty += 0.8
        elif Matcher.wordInImperfectly(word, words, 0):
            certainty += 0.7
        elif not __optimize and Matcher.wordInImperfectly(word, words, 2): # 2 litery różnicy (bez polskich znaków)
            certainty += 0.4

    if required:
        for wordsGroup in required:
            has_required = True
            for word in wordsGroup:
                if word not in message and not Matcher.wordInImperfectlyReversed(word, message, 2 if not __optimize else 0):
                    has_required = False
                    break
            if has_required == True:
                certainty += 1
                break

    total_probability = float(certainty)

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

    answer('Dzień dobry', ['czesc', 'halo', 'witam', 'dzien', 'dobry', 'hej','dzien', 'dobry'])

    answer('Do zobaczenia!', ['pa', 'do', 'widzenia', 'na', 'razie'])

    answer('Restauracja jest czynna w godzinach 8:00 - 20:00.',
           ['w', 'jakich', 'godzinach', 'restauracja', 'otwarta', 'ktorej', 'czynna'])

    answer('Restauracja jest czynna od Poniedziałku do Piątku.',
           ['kiedy', 'otwarta', 'restauracja', 'w', 'jakich', 'dniach', 'tygodnia'])

    answer('Restauracja znajduje się przy ul. NieMaTakiejUlicy 42B, obok pomostu z krasnalem.',
           ['gdzie', 'znajduje', 'restauracja', 'ulicy', 'miejscu', 'w', 'jakim', 'adres', 'lokalizacja', 'podać'])

    answer('Serwujemy najlepszą pizzę na naszej ulicy!',
           ['co', 'państwo', 'pizza', 'macie', 'serwujecie', 'oferujecie', 'posiadacie', 'jakie', 'potrawy', 'dania'])

    answer('Jest możliwość dowozu w obrębie Poznania, a dla Winograd i Starego Miasta dostawa jest darmowa dla zamówień za min 50zł! Dzwoń: 333 333 333!',
           ['czy', 'macie', 'mozliwosc', 'dowóz', 'dostawa', 'dostawy', 'opcja', 'dostarczać'])

    answer('Dzwoń: 333 333 333!', ['tel', 'numer', 'telefon', 'kontakt', 'kontaktować', 'skontaktować', 'dzwonić'])

    answer('Wszystkie nasze pizze mają około 30cm średnicy',
           ['pizza', 'wielkosc', 'duza', 'posiadacie', 'macie', 'rozmiar', 'średnica'], required=[['średnica'],['rozmiar'],['duża'], ['mała'], ['średnia'], ['familijna']])

    answer('Nasze sosy do pizzy: Pomidorowy łagodny i pikantny, BBQ, Czosnkowy, Bazyliowy, Ziołowy',
           ['jakie', 'macie', 'pizzy', 'sosy', 'wybrac'])

    answer('Przy składaniu zamówienia jest opcja wyboru rodzaju ciasta (mamy i cienkie i grube)',
           ['pizza', 'pizzy', 'grubosc', 'ciasto', 'ciescie', 'ma', 'jakim'])

    answer('Aktualne promocje: \nStudenci 10% zniżki na zamówienie!\nTrzecia pizza gratis!\nDo każdej pizzy sos gratis!',
           ['promocje', 'rabaty', 'znizki', 'posiadacie', 'macie', 'jakies'])

    answer('Każdy student ma u nas 10% zniżki na całe zamówienie!',
        ['promocja', 'rabat', 'znizka', 'student', 'studencka', 'jakies'])

    answer('Wszystkie nasze pizza posiadają gluten :)',
        ['pizza', 'gluten', 'bez', 'glutenu', 'ma', 'posiada', 'bezglutenowe'])

    answer('Ananas na pizzy to zbrodnia przeciw ludzkości!',
           ['pizza', 'ananas', 'dodac'], required=[['ananas']])

    answer('Szanujmy sie, hawajska to nie pizza :)',
           ['pizza', 'hawajska', 'macie', 'gdzie', 'jest'], required=[['hawajska']])

    answer('Nasza pizzeria oferuje następnujące menu: \n'+pizzas,
           ['pizze', 'jakie', 'macie', 'menu', 'oferta', 'rodzaje', 'oferujecie', 'można', 'zjeść', 'wybór','jadłospis'],
                required=[['menu'],['jadłospis'], ['rodzaje', 'pizzy'], ['można', 'zjeść'], ['co', 'oferujecie']])

    for i, pizza in enumerate(menu):
        answer(pizza[0] + ' - Składniki:' + pizza[1], ['pizza', pizza[0], 'skladniki', 'sklad', str(i + 1), 'jakie', 'ma'] + pizza[3],
               required=[['skladniki'], ['sklad'], ['zawiera']])

        answer(f'Pizza {pizza[0]} kosztuje ' + str(menu[i][2]) + 'zł',
               ['pizza', pizza[0], str(i + 1), 'cena', 'jaka', 'ile', 'kosztuje'] + pizza[3])

        words = pizza[1].replace(',', '').split(' ')
        answer(f'Co powiesz na pizzę {pizza[0]}? Składniki: {pizza[1]}',
               words + ['jakie', 'czy', 'macie', 'są', 'szukam', 'z', 'czym', 'składniki', 'zawiera'],
               required=[['z']])


    # Koniec odpowiedzi ------------------------------------------------------------------------------------------------




    matched = max(highest_probability_list, key=highest_probability_list.get)

    greeting = ""
    if matched != "Dzień dobry.":
        for word in message:
            if word in ['czesc', 'halo', 'witam','dzien', 'dobry', 'hej']:
                greeting = "Dzień dobry. "
                break
    #end

    return 'Przepraszam, ale nie rozumiem, co masz na myśli...' if highest_probability_list[matched] < 0.4 else greeting+matched


def get_answer(message):
    split_message = re.split(r'\s+|[.,?!;-]\s*', message.lower())
    answer = check_all(split_message)
    return answer


if __name__ == "__main__":
    while True:
        print('Adam: ' + get_answer(input('Ty: ')))
