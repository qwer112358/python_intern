import requests
from bs4 import BeautifulSoup


class Scraper:
    currencies = {
        'USD': '52148',
        'EUR': '52170',
        'GBP': '52146',
        'JPY': '52246',
        'TRY': '52158',
        'INR': '52238',
        'CNY': '52207'
    }

    def __init__(self, url, class_table):
        self.url = url
        self.class_table = class_table

    def __get_html(self):
        return requests.get(self.url).text

    def get_data(self):
        html = self.__get_html()
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table', class_=self.class_table)
        rows = table.find_all('tr')[1:]
        return [[col.text.strip() for col in row.find_all('td')] for row in rows]

    @staticmethod
    def parse_country_currencies():
        url = 'https://www.iban.ru/currency-codes'
        scraper = Scraper(url, 'table table-bordered downloads tablesorter')
        data = list(map(lambda col: [col[0], col[2]], scraper.get_data()))

        out = list(filter(lambda el: el[1] in Scraper.currencies.keys(), data))
        return out

    @staticmethod
    def parse_currency_rates(begin_date, end_date, currency_codes):

        data = sum(
            (
                [[cur_code, col[0], col[2]] for col in Scraper(
                    (f'https://www.finmarket.ru/currency/rates/?id=10148&pv=1&cur={Scraper.currencies[cur_code]}&bd={begin_date.day}&bm={begin_date.month}&by={begin_date.year}&ed={end_date.day}&em={end_date.month}&ey={end_date.year}&x=44&y=8#archive'),
                    'karramba').get_data()] for cur_code in currency_codes
            ),
            []
        )

        return data
