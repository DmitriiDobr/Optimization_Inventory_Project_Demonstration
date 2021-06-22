from src.libraries.lib import pandas as pd


class Uploader:
    """Класс предназначен для загрузки таблицы эксель с историей продаж и остатками на складах.
    Таблица имеет следующие колонки:
    """

    @staticmethod
    def upload_xlsx(file_path):  # функция, чтобы подгрузить данные
        if isinstance(file_path, str):
            return pd.read_excel(file_path)
        else:
            raise TypeError("Type of file must be a string")
