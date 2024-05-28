from enum import Enum


class MyConstant(Enum):
    NETZVERB = "Netzverb Wörterbuch"
    WERBUNG = "Werbung ausblenden"
    COLUMNS = ['Learned', 'Tags', 'Word', 'Transcription', 'Translation', 'Additional translation', 'Examples']
    HEADERS = {"Accept-Language": "uk-UA,uk;q=0.9,ru-UA;q=0.8,ru;q=0.7,en-US;q=0.6,en;q=0.5"}


class VerbFormenError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MultyRes(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
