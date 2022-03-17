import requests
from bs4 import BeautifulSoup
import random


class ParseImdbSite:

    def __init__(self):
        self.name_of_film = []
        self.date_of_realise = []
        response = requests.get("https://www.imdb.com/chart/top/")
        soup = BeautifulSoup(response.text, 'lxml')
        self.list_with_films = soup.findAll('td', class_='titleColumn')

    def main(self):
        if not self.name_of_film:
            self.get_name_of_film()
            self.get_realised_date()
            self.get_random_number_film()
            return self.get_random_number_film()
        else:
            self.get_random_number_film()
            return self.get_random_number_film()

    def get_name_of_film(self):
        for film in self.list_with_films:
            find_name_of_films = film.find('a').text
            self.name_of_film.append(find_name_of_films)

    def get_realised_date(self):
        for film in self.list_with_films:
            find_film_realise_year = film.find('span', class_='secondaryInfo').text
            to_str_film_realise_year = str(find_film_realise_year)
            film_realise_date = to_str_film_realise_year.replace('(', '').replace(')', '')
            self.date_of_realise.append(film_realise_date)

    def get_random_number_film(self):
        random_number = random.randrange(1, len(self.name_of_film))
        return self.name_of_film[random_number] + ' ' + self.date_of_realise[random_number] + ' - року'


class ParsingAnimego:

    def __init__(self):
        self.names_of_title = []
        self.status_info = []
        self.rating = []
        response = requests.get('https://animego.online/top100/')
        soup = BeautifulSoup(response.text, 'lxml')
        self.list_with_titles = soup.find_all('a', class_='poster-item grid-item')

    def main(self):
        self.get_name_of_title()
        self.get_status()
        self.get_random_title()
        return self.get_random_title()

    def get_name_of_title(self):
        for titles in self.list_with_titles:
            find_name_of_titles = titles.find('div', class_='poster-item__title').text
            self.names_of_title.append(find_name_of_titles)

    def get_status(self):
        for titles in self.list_with_titles:
            find_status_info = titles.find('span').text
            if find_status_info == '':
                find_status_info = 'Вийшло повінстю'
            self.status_info.append(find_status_info)

    def get_random_title(self):
        random_number = random.randrange(1, len(self.names_of_title))
        return self.names_of_title[random_number] + ' ' + self.status_info[random_number]


class ParsingTopReyting:
    def __init__(self):
        self.names_of_serial = []
        self.date_of_realise = []
        response = requests.get("https://top-reyting.ru/kino/reyting-luchshich-serialov-mira.html")
        soup = BeautifulSoup(response.text, 'lxml')
        self.list_with_serials = soup.findAll('div', class_='spisok')

    def main(self):
        self.get_serials_name()
        self.get_serials_realise_date()
        self.get_random_serial()
        return self.get_random_serial()

    def get_serials_name(self):
        for serial in self.list_with_serials:
            find_name_of_serial = serial.find('li', class_='name')
            unwanted = find_name_of_serial.find('span')
            unwanted.extract()
            self.names_of_serial.append(find_name_of_serial.text)

    def get_serials_realise_date(self):
        for serial in self.list_with_serials:
            find_date_of_realise = serial.find('li', class_='infofilm-data').text
            self.date_of_realise.append(find_date_of_realise)

    def get_random_serial(self):
        random_number = random.randrange(1, len(self.names_of_serial))
        return self.names_of_serial[random_number] + ' ' + self.date_of_realise[random_number]
