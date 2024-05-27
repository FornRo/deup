import logging

from pathlib import Path

from core.deutsch_parser import DeuParser
from core.reader_from_file import reader
from core.xls_creator import PdExel


def main():
    logging.basicConfig(filename='core/main.log', level=logging.DEBUG)

    cwd = Path.cwd()
    data_from_file = reader(cwd/'filename.txt')

    data = DeuParser().packag_xsl_and_collector(data_from_file)

    PdExel().create_w_xls(data)


if __name__ == '__main__':
    main()
