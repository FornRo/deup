import logging

from bs4 import BeautifulSoup

from datetime import datetime

from requests import RequestException
from requests import get as requests_get_page

from .my_lib import MultyRes, MyConstant


class DeuParser:
    def __init__(self, url="https://www.verbformen.de"):
        self.url = url
        self.res_data = {}
        self.res_datas = []

    def __str__(self):
        return f"{self.__name__},  with data [url: {self.url}]"

    def __repr__(self):
        return f"{type(self).__name__} [url: {self.url} ]"

    def _data_collector(self, word: str = None):
        self.res_data['start_word'] = word
        url = f"{self.url}/?w={word}"

        try:
            # Send a GET request to the URL
            page = requests_get_page(url, headers=MyConstant.HEADERS.value)

            # Check if the request was successful (status code 200)
            page.raise_for_status()  # This will raise an exception for non-200 status codes

            # Access the HTML content of the page
            self.soup = BeautifulSoup(page.text, "html.parser")

            # if (self.soup.find('div', class_="rLinks rHell").text.strip() == MyConstant.NETZVERB.value
            #         or
            if self.soup.find('div', class_="rCntr").text.strip() == MyConstant.WERBUNG.value:
                raise MultyRes("U got MultyRes in qwr_set")

            # TODO need add for Nomen Pl form in end. example: (das Buch -"e)
            self.res_data['word_with_article'] = self.soup.find('div', class_="rCntr rClear").text.strip()
            self.set_example_uk()
            self.set_translate_uk()
            self.set_context_data()

        except RequestException as e:
            self.set_none_data()
            logging.error("Failed to retrieve HTML:### %s", e)
        except MultyRes as e:
            self.set_none_data()
            logging.error('Failed with that word [%s] more info: ### %s', url, e)
        except AttributeError as e:
            self.set_none_data()
            logging.error("Failed in result by caught empty res in [%s] :### %s", self.res_data['start_word'], e)

    def set_none_data(self):
        self.res_data['word_with_article'] = None
        self.res_data["main_translate_uk"] = None
        self.res_data["translate_uk"] = None
        self.res_data["example"] = None
        self.res_data["context"] = None

    def set_example_uk(self):  # todo there some time got strange result like "jedenSchrott" joined str.
        li_objects = self.soup.find('h2', class_="rNt").parent.parent.find_all('li')
        self.res_data["example"] = []
        for li in li_objects:
            li = li.text
            li = li.replace('\n', '')
            li = li.replace('\xa0', '')
            li = li.replace('?', '?.')
            self.res_data["example"].append(li.split('.', maxsplit=1)[0])

    def set_translate_uk(self):
        res = self.soup.find('p', class_="r1Zeile rU3px rO0px")
        res = res.text.replace('\n', '').replace('\xa0', '')
        main_translation, other = res.split(',')[0], res.split(',')[1:]
        other = other if len(other) >= 1 else None
        self.res_data["main_translate_uk"], self.res_data["translate_uk"] = main_translation, other

    def set_context_data(self):
        context = self.soup.find('p', class_="vStm rCntr").text
        self.res_data["context"] = list(map(lambda x: x.strip(), context.split('·')))

    def getter_word(self, word: str = None):
        self._data_collector(word=word)
        return self.res_data

    def getter_words_data_collector(self, words: list[str] = None):
        for word in words:
            self.res_datas.append(self.getter_word(word=word))
            self.res_data = {}
        return self.res_datas

    def packag_xsl_and_collector(self, words: list[str] = None):
        self.getter_words_data_collector(words)

        keys = self.res_datas[0].keys()
        data = [item.values() for item in self.res_datas]

        res = dict(zip(keys, zip(*data)))

        today = datetime.now().strftime("%Y_%m_%d")
        range_by_len_columns = range(len(res['start_word']))

        # adapting for xls
        res['Learned'] = ['0%' for _ in range_by_len_columns]
        # TODO need add tag for Nomen or Verb. example: (2024_09_15, Nomen), (2024_09_15, Verb)
        res['Tags'] = [today for _ in range_by_len_columns]
        res['Word'] = res['word_with_article']
        res['Transcription'] = [None for _ in range_by_len_columns]
        res['Translation'] = res['main_translate_uk']
        res['Additional translation'] = [None if val is None else "; ".join(val) for val in res['translate_uk']]
        res['Examples'] = [None if val is None else "\n".join(val) for val in res['example']]

        return res


if __name__ == '__main__':
    verb_test_word = DeuParser().getter_word(word="machen")
    test_word = DeuParser().getter_word(word="Fenster")
    for key, val in test_word.items():
        print(key, ' = ', val)

    logging.basicConfig(filename='deutsch_parser.log', level=logging.DEBUG)
    res = DeuParser().packag_xsl_and_collector(['machen', 'Fenster'])
    print(res)
