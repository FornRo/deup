import logging
from pathlib import Path
import inspect


def reader(file_path='filename.txt') -> list[str]:
    """
    :return list(str)
    :example  ['ganzen', 'fließend']
    """
    try:
        if not (Path(file_path).exists()):
            raise FileNotFoundError

        with open(file_path, 'r') as file:
            file_line_data = [line.strip() for line in file]
        return file_line_data
    except FileNotFoundError as e:
        # todo add exit point for that exception
        logging.error('This is an error message: %s # in: %s', e, inspect.currentframe().f_code.co_name)


if __name__ == '__main__':
    logging.basicConfig(filename='reader_from_file.log', level=logging.DEBUG)

    file_data = reader()
    print("Data from the file:")
    print(file_data)
