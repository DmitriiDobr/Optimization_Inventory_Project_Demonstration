from src.libraries.lib import numpy as np
from src.libraries.lib import pandas as pd
from src.libraries.lib import deepcopy


class BootstrapData:
    """Класс предназначен для создания массива для последующей процедуры бутстрапа.
    (Массив состоит из ненулевых продаж за период).

    Attributes
    _ _ _ _ _ _ _

    df_chosen_bootstrap_period - реиндексированный датафреим. Датафреим возвращает  метод \

    chosen_learning_period_seasonal, класса  DataPreproccessing.

    df_bootstrap - является копией df_chosen_bootstrap_period, нужен для последующих манипуляций

    marka - марка номенкулатурной группы

    product_id - уникальный Tovar_id

    Methods
    _ _ _ _ _ _ _

    __get_bootstrap_list

    __filter_outliers_z_score

    __substitute_non_zero_with_one

    __add_zero_to_empty_data_bootstrap

    __data_bootstrap_no_outliers

    claculate_bootstrap_data

    """

    def __init__(self, df_chosen_bootstrap_period, marka, product_id):
        self.df_chosen_bootstrap_period = df_chosen_bootstrap_period
        self.marka = marka
        self.product_id = product_id
        self.__df_bootstrap = deepcopy(df_chosen_bootstrap_period)
        self.__status = "df_chosen_bootstrap_period"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"{self.marka!r}, {self.product_id!r}, {self.status!r})"
        )

    @property
    def df_chosen_bootstrap_period(self):
        return self._df_chosen_bootstrap_period

    @df_chosen_bootstrap_period.setter
    def df_chosen_bootstrap_period(self, df_chosen_bootstrap_period):
        if isinstance(df_chosen_bootstrap_period, pd.DataFrame):
            self._df_chosen_bootstrap_period = df_chosen_bootstrap_period
        else:
            raise TypeError("Type of file must be pd.core.frame.DataFrame")

    @property
    def df_bootstrap(self):
        return self.__df_bootstrap

    @df_bootstrap.setter
    def df_bootstrap(self, df_bootstrap):
        self.__df_bootstrap = df_bootstrap

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
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        if isinstance(product_id, int):
            self._product_id = product_id
        else:
            raise TypeError("Type of product_id must be a string")

    @property
    def status(self):
        return self.__status

    def __get_bootstrap_list(self):
        """Метод позволяет создавать массив с ненулевыми значениями продаж

        Возвращает:

        Массив с ненулевыми значениями продаж
        """
        condition = self.df_bootstrap.loc[:, "Tovarov_shtuk"] > 0
        data_bootstrap = list(self.df_bootstrap.loc[condition].loc[:, "Tovarov_shtuk"])
        return data_bootstrap

    def __filter_outliers_z_score(self, data_bootstrap, sigma_parameter):
        """Метод позволяет отфильтровать выбросы (outliers) на основании z_score.

        Принимает:

        data_bootstrap - массив с ненулевыми значениями продаж

        sigma_parameter - параметр фильтрации выбросов, чем он больше, тем большие значения считаются выбросами

        Возвращает:

        Массив с выбросами в случае, если после фильтрации выбросов массив остается не пустой.

        Массив с выбросами в противном случае.

        Подробнее о z-score - https://www.geeksforgeeks.org/z-score-for-outlier-detection-python/

        """
        data_bootstrap_no_outliers = deepcopy(data_bootstrap)

        data_bootstrap = np.array(data_bootstrap)

        mean = np.mean(data_bootstrap)

        sigma = np.sqrt(np.sum(((data_bootstrap - mean) ** 2)) / len(data_bootstrap))

        z_score = mean + sigma_parameter * sigma

        data_bootstrap = list(data_bootstrap[data_bootstrap < z_score])

        if not data_bootstrap:
            return data_bootstrap_no_outliers
        else:
            return data_bootstrap

    def __add_zero_to_empty_data_bootstrap(self, data_bootstrap):
        """Метод добавляет 0 к массиву (list) , если он пустой"""
        data_bootstrap.append(0)
        return data_bootstrap

    def __data_bootstrap_outliers(self, data_bootstrap, sigma_parameter):
        """Метод позволяет получить массив очищенный от выбросов.

        Включает в себя следующие методы:

        __substitute_non_zero_with_one

        __add_zero_to_empty_data_bootstrap

        __filter_outliers_z_score

        Принимает на вход:

        data_bootstrap - массив (list) с ненулевыми продажами

        sigma parameter - параметр фильтрации выбросов, чем он больше, тем большие значения считаются выбросами

        Возвращает:

        в случае выполнения первого условия: Массив с одним значением -0

        в случае выполнения второго условия: Фильтрация выбросов не производится(массив слишком маленький)

        в третьем случае: Отфильтрованный от выбросов массив


        """

        if not data_bootstrap:
            return self.__add_zero_to_empty_data_bootstrap(data_bootstrap)

        elif len(data_bootstrap) <= 2:
            # self.__substitute_non_zero_with_one()
            return data_bootstrap

        else:
            # self.__substitute_non_zero_with_one()
            return self.__filter_outliers_z_score(
                data_bootstrap, sigma_parameter=sigma_parameter
            )

    def __data_bootstrap_no_outliers(self, data_bootstrap):
        """Метод проверяет то, что массив с продажами ненулевой, заменяет все ненулевые продажи на 1.

        Включает в себя методы:

        __add_zero_to_empty_data_bootstrap

        __substitute_non_zero_with_one

        Принимет на вход:

        data_bootstrap - массив ненулевых продаж

        Возвращает:

        data_bootstrap - массив ненулевых продаж

        """

        if not data_bootstrap:
            data_bootstrap = self.__add_zero_to_empty_data_bootstrap(data_bootstrap)
        # self.__substitute_non_zero_with_one()
        return data_bootstrap

    def calculate_bootstrap_data(self, outlier_filtration=False, sigma_parameter=None):
        """Основной метод класса, позволяет получить массив с ненулевыми продажами и заменить в датафреиме

        все ненулевые продажи на 1.

        Включает в себя методы:

        __get_bootstrap_list

        __data_bootstrap_outliers

        __data_bootstrap_no_outliers

        Принимает на вход:

        outlier_filtration - feature flag (boolean), регулирует тип возвращаемого массива для бутстрапа,

        если True - выбросы фильтруются

        sigma_parameter - параметр фильтрации выбросов, чем он больше, тем большие значения считаются выбросами
        """
        data_bootstrap = self.__get_bootstrap_list()
        if outlier_filtration:
            return self.__data_bootstrap_outliers(
                data_bootstrap, sigma_parameter=sigma_parameter
            )

        elif not outlier_filtration:
            return self.__data_bootstrap_no_outliers(data_bootstrap)
