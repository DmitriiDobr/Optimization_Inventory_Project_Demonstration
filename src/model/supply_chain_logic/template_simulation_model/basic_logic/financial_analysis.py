from src.libraries.lib import pandas as pd
from src.libraries.lib import deepcopy


class FinancialAnalysis:
    """Класс предназначен для финансового анализа истории продаж

    Attributes
    _ _ _ _ _ _


    df_cleaned - очищенный датафреим, класса pandas.core.frame.DataFrame, является атрибутом класса SalesCleaning.

    df_aggregated_demand - является копией  df_cleaned, датафреим нужен для агрегации спроса, себестоимости,

    цены реализации

    df_abc_analysis  - атрибут с помощью, которого проводится abc анализ

    abc_categories - словарь, ключами, которого является категория товара (a, b, c), значениями же кортеж с товарами,

    этой категории


    Methods
    _ _ _ _ _ _

    __aggregate_demand

    __calculate_profit

    _abc_categories

    __calculate_profit_cumulata

    __abc_analysis

    __calculate_statistics

    __ADI_CV2_classifier

    calculate_abc_categories

    demand_classification

    mean_cost

    mean_price

    """

    def __init__(self, df_cleaned, marka):
        self.df_cleaned = df_cleaned
        self.marka = marka
        self.__df_aggregated_demand = deepcopy(df_cleaned)
        self.__df_abc_analysis = pd.DataFrame()
        self.__abc_categories = {}
        self.__status = "cleaned_data"

    def __repr__(self):
        return f"{self.__class__.__name__}(" f"{self.marka!r}, {self.status!r})"

    @property
    def df_cleaned(self):
        return self._df_cleaned

    @df_cleaned.setter
    def df_cleaned(self, df_cleaned):
        if isinstance(df_cleaned, pd.DataFrame):
            self._df_cleaned = df_cleaned
        else:
            raise TypeError("Type of file must be pd.DataFrame")

    @property
    def df_aggregated_demand(self):
        return self.__df_aggregated_demand

    @df_aggregated_demand.setter
    def df_aggregated_demand(self, df_aggregated_demand):
        self.__df_aggregated_demand = df_aggregated_demand

    @property
    def df_abc_analysis(self):
        return self.__df_abc_analysis

    @df_abc_analysis.setter
    def df_abc_analysis(self, df_abc_analysis):
        self.__df_abc_analysis = df_abc_analysis

    @property
    def abc_categories(self):
        return self.__abc_categories

    @abc_categories.setter
    def abc_categories(self, abc_categories):
        self.__abc_categories = abc_categories

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

    def __aggregate_demand(self):
        """Метод агрегируют спрос, себестоимость, цену реализации конкретного товара на конкретную дату,

        присваивает первоначальное значение атрибуту df_abc_analysis

        """
        self.df_aggregated_demand = self.df_aggregated_demand.groupby(
            ["Data", "Tovar_id"]
        ).agg(
            {
                "Tovarov_shtuk": "sum",
                "Sebestoimost_": "mean",
                "Tsena_realizatsii": "mean",
            }
        )
        self.df_aggregated_demand.reset_index(inplace=True)
        self.df_abc_analysis = deepcopy(self.df_aggregated_demand)

    def __calculate_profit(self):
        """Метод производит расчет прибыли и создает новую колонку - profit у атрибута - df_abc_analysis """
        self.df_abc_analysis = deepcopy(self.df_aggregated_demand)
        self.df_abc_analysis["profit"] = (
                                                 self.df_aggregated_demand.loc[:, "Tsena_realizatsii"]
                                                 - self.df_aggregated_demand.loc[:, "Sebestoimost_"]
                                         ) * self.df_aggregated_demand.loc[:, "Tovarov_shtuk"]

    def _abc_categories(self, perc):
        """Функция позволяет произвести товары на три категории - a,b,c

        Принимает на вход:

        perc - (кумулятивный процент)

        Возвращает:

        Категорию - A, B или C

        """
        if 0 < perc < 0.8:
            return "A"
        elif 0.8 <= perc < 0.95:
            return "B"
        elif perc >= 0.85:
            return "C"

    def __calculate_profit_cumulata(self):
        """Метод позволяет найти кумулятивный процент прибыли, предварительно сгрупировав, товары по уникальному id
        и, найдя процент каждого товара в общей прибыли.
        """
        self.__calculate_profit()
        self.df_abc_analysis = deepcopy(
            self.df_abc_analysis.groupby("Tovar_id").sum()[["profit", "Tovarov_shtuk"]]
        )
        self.df_abc_analysis["profit_percent"] = (
                self.df_abc_analysis["profit"] / self.df_abc_analysis["profit"].sum()
        )
        self.df_abc_analysis.sort_values(
            by="profit_percent", ascending=False, inplace=True
        )
        self.df_abc_analysis["cumulata_profit_percent"] = self.df_abc_analysis.loc[
                                                          :, "profit_percent"
                                                          ].cumsum()

    def __abc_analysis(self):
        """Имплементация ABC анализа прибыли. Метод позволяет найти категорию A, B, C каждого товара.

        Устанавливается атрибут abc_categories.

        Включает в себя следующие методы:

        __aggregate_demand

        __calculate_profit

        __calculate_profit_cumulata

        """

        self.__aggregate_demand()
        # self.__calculate_profit()
        self.__calculate_profit_cumulata()

        self.df_abc_analysis["abc_categories"] = self.df_abc_analysis[
            "cumulata_profit_percent"
        ].apply(self._abc_categories)

        self.df_abc_analysis.reset_index(inplace=True)
        abc_categories = dict(
            [
                (i, a)
                for i, a in zip(self.df_abc_analysis.Tovar_id, self.df_abc_analysis.abc_categories)
            ]
        )
        self.abc_categories = abc_categories

    def __calculate_statistics(self, product):
        """Метод позволяет произвести расчет статистических данных для дальнейшей типизации спроса,

        Возвращает:

        Словарь stats, с ключами ADI, CV2 и такими же ключами

        ADI - Average Demand Interval (средний интервал между двумя покупками)

        CV2 - Квадратичный кэффициент вариации.

        Подробнее о методике расчета - https://frepple.com/blog/demand-classification/

        """
        condition = self.df_aggregated_demand.loc[:, "Tovar_id"] == product

        amount = self.df_aggregated_demand.loc[condition].loc[:, "Tovar_id"].count()
        mean = self.df_aggregated_demand.loc[condition].loc[:, "Tovarov_shtuk"].mean()
        std = self.df_aggregated_demand.loc[condition].loc[:, "Tovarov_shtuk"].std()
        ADI = len(self.df_aggregated_demand) / amount
        CV2 = (std / mean) ** 2
        if amount == 1:
            ADI = "None"
            CV2 = "None"
        stats = {"ADI": ADI, "CV2": CV2}
        return stats

    def __ADI_CV2_classification(self, ADI, CV2):
        """Метод производит классификацию видов спроса

        Принимает на вход два параметра:

        ADI - Average Demand Interval (средний интервал между двумя покупками)

        CV2 - Квадратичный кэффициент вариации

        Возвращает:

        Тип спроса - "Smooth", "Intermittent", "Erratic", "Lumpy"

        """

        if (ADI < 1.32) & (CV2 < 0.49):
            return "Smooth"

        elif (ADI >= 1.32) & (CV2 < 0.49):
            return "Intermittent"

        elif (ADI < 1.32) & (CV2 >= 0.49):

            return "Erratic"

        elif (ADI >= 1.32) & (CV2 >= 0.49):
            return "Lumpy"

    def calculate_abc_categories(self):
        """Метод  устанвливает новое значения атрибута - abc_categories, ключи - категории товара (a,b,c),

        значения - кортежи с уникальными id товараов данной категории.


        Подробнее о ABC анализе - https://en.wikipedia.org/wiki/ABC_analysis
        """

        a = []
        b = []
        c = []
        self.__abc_analysis()

        unique_items = list(self.df_abc_analysis.loc[:, "Tovar_id"].unique())

        for i in unique_items:

            if self.abc_categories[i] == "A":
                a.append(i)

            if self.abc_categories[i] == "B":
                b.append(i)

            if self.abc_categories[i] == "C":
                c.append(i)

        self.abc_categories = {
            "a": tuple(a),
            "b": tuple(b),
            "c": tuple(c),
        }
        return self.abc_categories

    def demand_classification(self):
        """Классификация  спроса: ADI/CV2.

        Принимает на вход:
        -

        Возвращает:

        demand_type - словарь с ключами в виде уникальных id товаров и значениями - категориями спроса

        Включает в себя методы:

        __aggregate_demand

        __ADI_CV2_classification

        Подробнее о классификациях спроса: https://frepple.com/blog/demand-classification/

        """
        self.__aggregate_demand()
        demand_type = {}
        unique_products = list(self.df_aggregated_demand.loc[:, "Tovar_id"].unique())
        for i in unique_products:
            product = i
            stats = self.__calculate_statistics(product)
            demand_type[i] = self.__ADI_CV2_classification(
                stats["ADI"],
                stats["CV2"],
            )

        return demand_type

    def demand_classification_product(self, product_id):
        """Классификация  спроса: ADI/CV2.

        Принимает на вход:
        -

        Возвращает:

        demand_type - словарь с ключами в виде уникальных id товаров и значениями - категориями спроса

        Включает в себя методы:

        __aggregate_demand

        __ADI_CV2_classification

        Подробнее о классификациях спроса: https://frepple.com/blog/demand-classification/

        """
        self.__aggregate_demand()

        stats = self.__calculate_statistics(product_id)
        if stats["ADI"] == "None":
            demand_type_product = "None"
            return demand_type_product

        else:
            demand_type_product = self.__ADI_CV2_classification(
                stats["ADI"],
                stats["CV2"],
            )

            return demand_type_product

    def mean_cost(self):
        """Метод среднюю себестоимость для каждого товара
        Включает в себя методы:

        __aggregate_demand

        Возвращает:

        Словарь с уникальными id товара в качестве ключей и средней себестоимостью в виде значения.

        """
        mean_cost = {}
        self.__aggregate_demand()

        unique_products = list(self.df_aggregated_demand.loc[:, "Tovar_id"].unique())
        for i in unique_products:
            df_mean_cost = deepcopy(
                self.df_aggregated_demand.loc[
                    self.df_aggregated_demand.loc[:, "Tovar_id"] == i
                    ]
            )
            mean_cost[i] = (sum(df_mean_cost["Sebestoimost_"])) / len(df_mean_cost)
        return mean_cost

    def mean_cost_product(self, product_id):
        """Метод среднюю себестоимость для УНИКАЛЬНОГО товара
        Включает в себя методы:

        __aggregate_demand

        Возвращает:

        mean_cost_product - среднюю себестоимость.

        """

        self.__aggregate_demand()
        condition = self.df_aggregated_demand.loc[:, "Tovar_id"] == product_id
        df_mean_cost_product = deepcopy(self.df_aggregated_demand.loc[condition])
        mean_cost_product = (sum(df_mean_cost_product["Sebestoimost_"])) / len(
            df_mean_cost_product
        )
        return mean_cost_product

    def mean_price(self):
        """Метод среднюю цену реализации для каждого товара

        Включает в себя методы:

        __aggregate_demand

        Возвращает:

        Словарь с уникальными id товара в качестве ключей и средней ценой реализации в виде значения.

        """
        mean_price = {}
        self.__aggregate_demand()

        unique_products = list(self.df_aggregated_demand.loc[:, "Tovar_id"].unique())
        for i in unique_products:
            df_mean_price = deepcopy(
                self.df_aggregated_demand.loc[
                    self.df_aggregated_demand.loc[:, "Tovar_id"] == i
                    ]
            )
            mean_price[i] = (sum(df_mean_price["Tsena_realizatsii"])) / len(
                df_mean_price
            )
        return mean_price

    def mean_price_product(self, product_id):
        """Метод среднюю цену реализации для УНИКАЛЬНОГО товара

        Включает в себя методы:

        __aggregate_demand

        Возвращает:

        Средняя цена реализации в виде значения.

        """

        self.__aggregate_demand()
        condition = self.df_aggregated_demand.loc[:, "Tovar_id"] == product_id
        df_mean_price_product = deepcopy(self.df_aggregated_demand.loc[condition])
        mean_price_product = (sum(df_mean_price_product["Tsena_realizatsii"])) / len(
            df_mean_price_product
        )
        return mean_price_product
