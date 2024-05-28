import logging

import pandas as pd
from pathlib import Path, PurePath
from datetime import datetime

from .my_lib import MyConstant


class PdExel:
    def __init__(self, file_name: str = None, dir_path=None, columns: list = None):
        self._init_path(file_name, dir_path)

        self.columns: list = columns or MyConstant.COLUMNS.value
        self.data = {key: [] for key in self.columns}

    def _init_path(self, file_name: str = None, dir_path=None):
        dir_path: Path = Path.cwd() if dir_path is None else Path(dir_path).resolve()
        file_name: str = file_name or "my_dictitionaty.xls"

        check_exists: bool = Path(dir_path / file_name).exists()
        if check_exists:
            new_file_name:list[str] = [PurePath(file_name).stem, datetime.now().strftime('_%Y_%m_%d'), PurePath(file_name).suffix]
            file_name = ''.join(new_file_name)

        self.file_path = Path(dir_path / file_name).resolve()

    def get_reader_existing(self):
        xls = pd.ExcelFile(self.file_path)
        existing_data = pd.read_excel(xls, sheet_name='de')
        return existing_data

    def conversion_data(self, data: dict = None):
        if not data:
            logging.error("Data in \"%s\" method empty", self.conversion_data.__name__)

        for key in self.columns:
            adding_data = data[key]
            self.data[key] = adding_data
        logging.debug("%s completed", self.conversion_data.__name__)

    def create_w_xls(self, data: dict = None):
        # todo need add stile like in example.xls
        self.conversion_data(data)

        new_data = pd.DataFrame(data=self.data, columns=self.columns, index=None)
        with pd.ExcelWriter(self.file_path, mode='w', engine='openpyxl') as writer:
            new_data.to_excel(writer, sheet_name='de', index=False)


if __name__ == '__main__':
    logging.basicConfig(filename='xls_creator.log', level=logging.DEBUG)

    pd_exel = PdExel()

    data: dict = {
        'Learned': ['0%', '0%', '0%'],
        'Tags': ['my_tag#1', 'test', "my_tag#3"],
        'Word': ['test1', 'test2', 'test3'],
        'Transcription': [None, None, None],
        'Translation': ['test_translation_1', 'test_translation_2', 'test_translation_3'],
        'Additional translation': ['test_add_translation_1', 'test_add_translation_2',
                                   'test_add_translation_3'],
        'Examples': [None, None, None],
    }

    pd_exel.create_w_xls(data=data)
