import logging
from datetime import datetime

from pathlib import Path

from core.deutsch_parser import DeuParser
from core.reader_from_file import reader
from core.xls_creator import PdExel


def main():
    logging.basicConfig(filename='core/main.log', level=logging.INFO)
    cwd = Path.cwd()
    data_from_file = reader(cwd/'filename.txt')

    data = DeuParser().packag_xsl_and_collector(data_from_file)

    PdExel().create_w_xls(data)
    today = datetime.now().strftime("%Y_%m_%d")
    logging.info('This is end result ___ %s ___', today)

if __name__ == '__main__':
    main()
