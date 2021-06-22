from src.libraries.lib import deepcopy
from src.libraries.lib import pandas as pd
from src.libraries.lib import translit


class SalesCleaning:
    """Класс реализует методы очистки и предобработки новых данных.


    Attributes
    _ _ _ _ _ _

    df_uncleaned - датафреим с неочищенной историей продаж и остатками на складах, является экземляром

    pd.core.frame.DataFrame

    df_cleaned - датафреим с очищенной историей продаж и остатками на складах, является экземляром

    pd.core.frame.DataFrame

    product - словарь, где каждому товару присвоен уникальный id

    shop - словарь, где каждому магазину присвоен уникальный id

    marka - марка продукта

    status - статус изначально полученного датафреима (высталяется по умолчанию)

    Methods
    _ _ _ _ _ _

    preparation_of_data - Основная функция, делающая поэтапную обработку данных.

    df_information

    df_shape

    __filter_negative_values

    __drop_duplicates

    __drop_columns

    __columns

    __translate_column_names_to_english

    __convert_string_to_float

    __convert_string_to_int

    __convert_date_to_datetime_format

    __partitate_date_to_columns

    __change_column_order

    __change_column_order

    __drop_OOO_cities

    __create_categories_tovar

    __create_categories_magazin

    __save_magazin_id_names

    __save_tovar_id_names

    """

    def __init__(self, df_uncleaned: pd.DataFrame(), marka: str):
        """Конструтору подается неочищенный файл с продажами и остатками на складах формата xlsx - df_uncleaned,

        создается копия файла df_uncleaned, с которой будут производится поэтапные манипуляции с целью очистки данных.

        Неообходимо указать марку продаваемого продукта (str).
        """
        self.df_uncleaned = df_uncleaned
        self.df_cleaned = deepcopy(df_uncleaned)
        self.marka = marka
        self.__status = "uncleaned_data"
        self.__product = {}
        self.__shop = {}

    def __repr__(self):
        return f"{self.__class__.__name__}(" f"{self.marka!r}, {self.status!r})"

    @property
    def df_uncleaned(self):
        return self._df_uncleaned

    @df_uncleaned.setter
    def df_uncleaned(self, df_uncleaned):
        if isinstance(df_uncleaned, pd.DataFrame):
            self._df_uncleaned = df_uncleaned
        else:
            raise TypeError("Type of file must be pd.core.frame.DataFrame")

    @property
    def df_cleaned(self):
        return self._df_cleaned

    @df_cleaned.setter
    def df_cleaned(self, df_cleaned):
        if isinstance(df_cleaned, pd.DataFrame):
            self._df_cleaned = df_cleaned
        else:
            raise TypeError("Type of file must be pd.core.frame.DataFrame")

    @property
    def product(self):
        return self.__product

    @product.setter
    def product(self, product):
        self.__product = product

    @property
    def shop(self):
        return self.__shop

    @shop.setter
    def shop(self, shop):
        self.__shop = shop

    @property
    def marka(self):
        return self._marka

    @marka.setter
    def marka(self, marka):
        if isinstance(marka, str):
            self._marka = marka
        else:
            raise TypeError("Type of marka must be a string")

    @property
    def status(self):
        return self.__status

    def df_shape(self, cleaned=False):
        """Публичный метод,возвращает информацию о датафреиме.

        Если cleaned ==True возвращается форма df_cleaned и форма df_uncleaned в противном случае"""
        if cleaned:
            return self._df_cleaned.shape
        else:
            return self._df_uncleaned.shape

    def df_information(self, cleaned=False):
        """Публичный метод,возвращает информацию о датафреиме.

        Если cleaned ==True возвращается информация о df_cleaned и информация df_uncleaned в противном случае"""
        if cleaned:
            return self._df_cleaned.info()
        else:
            return self._df_uncleaned.info()

    def __filter_negative_values(self):
        """Метод удаляет отрицательные значения"""
        check_zeros_columns = ["Sebestoimost_", "Tsena_realizatsii", "Tovarov_shtuk"]
        for i in check_zeros_columns:
            self.df_cleaned.query(f"{i} > 0", inplace=True)

        self.df_cleaned.query("Ostatok_tovara_shtuk => 0", inplace=True)

    def __drop_duplicates(self):
        """Метод удаляет дубликаты"""
        self.df_cleaned.drop_duplicates(keep="first", inplace=True)

    def __drop_columns(self, columns=["Magazin", "Tovar"]):
        """Метод удаляет колонки Magazin, Tovar """
        self.df_cleaned.drop(columns, axis=1, inplace=True)

    def __columns(self):
        """Метод возвращает список названия колонок"""
        df_cleaned_columns = list(self.df_cleaned.columns)
        return df_cleaned_columns

    def __translate_column_names_to_english(self):
        """Метод переводит русские названия с английского языка с помощью функции translit"""
        df_cleaned_columns = self.__columns()
        english_names = {}
        for i in df_cleaned_columns:
            translated_word = (
                translit(i, "ru", reversed=True).replace(" ", "_").replace(",", "").replace("'", "")
            )
            english_names[i] = translated_word

        self.df_cleaned.rename(english_names, axis=1, inplace=True)

    def __convert_string_to_float(self):
        """Метод проверяет данные колонок Tsena_realizatsii, Sebestoimost_ на возможный формат str и переводит в
        формат float. """

        def convert_to_float(
                x,
        ):
            if isinstance(x, str):
                x = x.replace(",", ".").split()
                x = float("".join(x))
                return x
            else:
                return float(x)

        self.df_cleaned["Tsena_realizatsii"] = self.df_cleaned[
            "Tsena_realizatsii"
        ].apply(lambda x: convert_to_float(x))
        self.df_cleaned["Sebestoimost_"] = self.df_cleaned["Sebestoimost_"].apply(
            lambda x: convert_to_float(x)
        )

    def __convert_string_to_int(self):
        """Метод проверяет данные колонок Tovarov_shtuk, Ostatok_tovara_shtuk на возможный формат str и переводит в
        формат int. """

        def convert_to_int(
                x,
        ):
            if isinstance(x, str):
                x = x.replace(",", ".").split()
                x = int("".join(x))
                return x
            else:
                return int(x)

        self.df_cleaned["Tovarov_shtuk"] = self.df_cleaned["Tovarov_shtuk"].apply(
            lambda x: convert_to_int(x)
        )
        self.df_cleaned["Ostatok_tovara_shtuk"] = self.df_cleaned[
            "Ostatok_tovara_shtuk"
        ].apply(lambda x: convert_to_int(x))

    def __convert_date_to_datetime_format(self):
        """ Метод переводит дату в формат  pd.to_datetime"""

        self.df_cleaned["Data"] = pd.to_datetime(self.df_cleaned["Data"], dayfirst=True)

    def __partitate_date_to_columns(self):
        self.df_cleaned["day"] = self.df_cleaned["Data"].dt.day
        self.df_cleaned["month"] = self.df_cleaned["Data"].dt.month
        self.df_cleaned["year"] = self.df_cleaned["Data"].dt.year

    def __change_column_order(self):
        date_columns = ["day", "month", "year"]

        new_columns = date_columns + self.__columns()

        self.__partitate_date_to_columns()

        self.df_cleaned = deepcopy(self.df_cleaned[new_columns])
        self.df_cleaned.set_index("Data", inplace=True)

    def __drop_OOO_cities(self):
        """Метод удаляет города, которые не входят в ООО"""
        list_to_drop = list(
            self.df_cleaned[
                (self.df_cleaned["Magazin"] == "Пермь")
                | (self.df_cleaned["Magazin"] == "Новосибирск")
                | (self.df_cleaned["Magazin"] == "Владивосток")
                | (self.df_cleaned["Magazin"] == "Екатеринбург")
                | (self.df_cleaned["Magazin"] == "Красноярск")
                | (self.df_cleaned["Magazin"] == "Екатеринбург")
                ].index
        )
        self.df_cleaned.drop(list_to_drop, inplace=True)

    def __create_categories_tovar(self):
        """Метод переводит Tovar в разряд категориальных переменных"""
        cat_feat_tovar = "Tovar"
        self.df_cleaned[cat_feat_tovar] = self.df_cleaned[cat_feat_tovar].astype(
            "category"
        )
        self.df_cleaned[cat_feat_tovar + "_id"] = self.df_cleaned[
            cat_feat_tovar
        ].cat.codes

    def __create_categories_magazin(self):
        """Метод переводит Magazin в разряд категориальных переменных"""
        cat_feat_tovar = "Magazin"
        self.df_cleaned[cat_feat_tovar] = self.df_cleaned[cat_feat_tovar].astype(
            "category"
        )
        self.df_cleaned[cat_feat_tovar + "_id"] = self.df_cleaned[
            cat_feat_tovar
        ].cat.codes

    def __save_magazin_id_names(self):
        """Метод возвращает словарь с ключами в виде категории Magazin и значениями в виде названий магазинов """
        shop = {}
        for i, j in enumerate(self.df_cleaned["Magazin"].cat.categories):
            new_key = j
            new_key = new_key.replace("\xa0", " ")
            shop[i] = new_key
        return shop

    def __save_tovar_id_names(self):
        """Метод возвращает словарь с ключами в виде категории Tovar и значениями в виде названий товаров """
        product = {}
        for i, j in enumerate(self.df_cleaned["Tovar"].cat.categories):
            new_key = j
            new_key = new_key.replace("\xa0", " ")
            product[i] = new_key
        return product

    def preparation_of_data(self):
        """Метод производит поэтапную очистку данных. Также устанавливает значения атрибутов shop, product на
        последнем этапе """
        self.__translate_column_names_to_english()
        self.__convert_string_to_float()
        self.__convert_string_to_int()
        self.__convert_date_to_datetime_format()
        self.__change_column_order()
        self.__drop_OOO_cities()
        self.__create_categories_magazin()
        self.__create_categories_tovar()
        self.__drop_columns()
        self.__drop_duplicates()
        return self.df_cleaned
