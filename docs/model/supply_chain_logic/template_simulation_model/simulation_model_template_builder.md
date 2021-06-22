from src.libraries.lib import choice
from src.libraries.lib import abstractmethod, abstractproperty
from src.libraries.lib import ABC


class Builder( ABC ):
    """Класс предназначен для создания атрибутов для модели. Имеет двух наследников: BuilderdAllShopsModel,

    BuilderOneShopModel. Часть атрибутов будут случайными, часть задается клиентом.

    Attributes:
    _ _ _ _ _ _

    Methods
    _ _ _ _ _

    produce_start_date

    produce_end_date

    produce_shop(@abstractmethod)

    produce_shop_id

    produce_product_id

    produce_marka

    produce_outlier_filtration

    produce_sigma_parameter

    produce_number_of_paths

    produce_days_of_simulation

    produce_disp

    produce_logistic

    produce_a_level

    produce_b_level

    produce_c_level

    produce_add_deficit

    produce_one_year

    produce_new_configuration

    """

    @abstractproperty
    def product(self):
        pass

    def produce_start_date(self, start_date):
        """Метод позволяет добавить start_date(str) в словарь data"""
        self._data.update( {"start_date": start_date} )

    def produce_end_date(self, end_date):
        """Метод позволяет добавить end_date(str) в словарь data"""
        self._data.update( {"end_date": end_date} )

    @abstractmethod
    def produce_shop(self):
        """Метод позволяет добавить feature flag shop(boolean) в словарь data"""
        raise NotImplementedError( "There should be feature flag -  shop" )

    @abstractmethod
    def produce_shop_id(self):
        """Метод позволяет добавить shop_id(int) в словарь data"""
        raise NotImplementedError( "There should be shop_id" )

    def produce_product_id(self, product_id):
        """Метод позволяет добавить product_id(int) в словарь data"""
        self._data.update( {"product_id": product_id} )

    def produce_marka(self, marka):
        """Метод позволяет добавить marka(str) в словарь data"""
        self._data.update( {"marka": marka} )

    def produce_outlier_filtration(self):
        """Метод позволяет добавить outlier_filtration(boolean) в словарь data (случайный параметр)"""
        filtration_param = [True, False]
        outlier_filtration = choice( filtration_param )
        self._data.update( {"outlier_filtration": outlier_filtration} )

    def produce_sigma_parameter(self):
        """Метод позволяет добавить sigma_parameter(float) в словарь data (случайный параметр)"""
        sigma = [2.8, 3]
        sigma_parameter = choice( sigma )
        self._data.update( {"sigma_parameter": sigma_parameter} )

    def produce_number_of_paths(self):
        """Метод позволяет добавить number_of_paths(int) в словарь data"""
        number_of_paths = 10000
        self._data.update( {"number_of_paths": number_of_paths} )

    def produce_days_of_simulation(self, days_of_simulation):
        """Метод позволяет добавить days_of_simulation(int) в словарь data"""
        self._data.update( {"days_of_simulation": days_of_simulation} )

    def produce_disp(self):
        """Метод позволяет добавить disp(float) в словарь data (случайный параметр)"""
        disp_parameter = [0.9, 0.95, 1, 1.05, 1.1]
        disp = choice( disp_parameter )
        self._data.update( {"disp": disp} )

    def produce_logistic(self):
        """Метод позволяет добавить logistic(boolean) в словарь data (случайный параметр)"""
        logistic_param = [True, False]
        logistic = choice( logistic_param )
        self._data.update( {"logistic": logistic} )

    def produce_a_level(self):
        """Метод позволяет добавить a_level(float) в словарь data (случайный параметр)"""
        service_level = [0.96, 0.97, 0.98]
        a_level = choice( service_level )
        self._data.update( {"a_level": a_level} )

    def produce_b_level(self):
        """Метод позволяет добавить b_level(float) в словарь data (случайный параметр)"""
        service_level = [0.94, 0.95, 0.96]
        b_level = choice( service_level )
        self._data.update( {"b_level": b_level} )

    def produce_c_level(self):
        """Метод позволяет добавить c_level(float) в словарь data (случайный параметр)"""
        service_level = [0.90, 0.88, 0.89]
        c_level = choice( service_level )
        self._data.update( {"c_level": c_level} )

    def produce_add_deficit(self):
        """Метод позволяет добавить add_deficit(boolean) в словарь data (случайный параметр)"""
        deficit = [True, False]
        add_deficit = choice( deficit )
        self._data.update( {"add_deficit": add_deficit} )

    def produce_one_year(self):
        """Метод позволяет добавить one_year(boolean) в словарь data (случайный параметр)"""
        year = [True, False]
        one_year = choice( year )
        self._data.update( {"one_year": one_year} )

    def produce_seasonality(self):
        seasonal = [True, False]
        seasonality = choice( seasonal )
        self._data.update( {"seasonality": seasonality} )

    def produce_new_configuration(self):
        """Метод позволяет создать конфигурацию для модели."""
        self.produce_start_date()
        self.produce_end_date()
        self.produce_disp()
        self.produce_logistic()
        self.produce_days_of_simulation()
        self.produce_sigma_parameter()
        self.produce_number_of_paths()
        self.produce_outlier_filtration()
        self.produce_product_id()
        self.produce_marka()
        self.produce_shop()
        self.produce_shop_id()
        self.produce_add_deficit()
        self.produce_a_level()
        self.produce_b_level()
        self.produce_c_level()
        self.produce_one_year()
        self.produce_seasonality()
        self._product.set_attributes( parameters=self._data )
        pass


class BuilderdAllShopsModel( Builder ):
    """
    Класс является наследником класса Builder, который позволяет сконфигурировать атрибуты

    для модели конкретного города (без учета конкретного магазина)
    """

    def __init__(self):
        """
        Конструктор включает в себя два метода: reset, create_param_data.
        """
        self.reset()
        self.create_param_data()

    def reset(self):
        """Метод устанавливает новый атрибут - product, класса AllShopsModel"""
        self._product = AllShopsModel()

    def create_param_data(self):
        """Метод устанавливает атрибут data (словарь)"""
        data = {}
        self._data = data

    @property
    def product(self):
        product = self._product

        self.reset()
        return product

    @property
    def data(self):
        data = self._data

        self.create_param_data()
        return data

    def produce_shop(self):
        """Метод устанавливает Feature flag shop(boolean) и устанавливает в False"""
        shop = False
        self._data.update( {'shop': shop} )

    def produce_shop_id(self):
        """Метод устанавливает shop_id(int) - None """
        shop_id = None
        self._data.update( {'shop_id': shop_id} )

    def produce_new_configuration(self, start_date, end_date, marka, product_id, \
                                  days_of_simulation):
        """Метод позволяет создать конфигурацию для модели, вызывая метод

        set_attributes класса AllShopsModel(подавая в качестве parameters - data):

        часть параметров задается извне:

        start_date

        end_date

        marka

        product_id

        days_of_simulation

        Принимает на вход:

        -

        Возвращает:

        _


        """
        self.produce_start_date( start_date )
        self.produce_end_date( end_date )
        self.produce_product_id( product_id )
        self.produce_marka( marka )
        self.produce_days_of_simulation( days_of_simulation )
        self.produce_number_of_paths()
        self.produce_disp()
        self.produce_logistic()
        self.produce_sigma_parameter()
        self.produce_outlier_filtration()
        self.produce_product_id( product_id )
        self.produce_shop()
        self.produce_add_deficit()
        self.produce_shop_id()
        self.produce_a_level()
        self.produce_b_level()
        self.produce_c_level()
        self.produce_one_year()
        self.produce_seasonality()
        self._product.set_attributes( parameters=self._data )

        return self._product


class BuilderOneShopModel( Builder ):
    """
    Класс является наследником класса Builder, который позволяет сконфигурировать атрибуты

    для модели конкретного города (без учета конкретного магазина)
    """

    def __init__(self):
        """
        Конструктор включает в себя два метода: reset, create_param_data.
        """
        self.reset()
        self.create_param_data()

    def reset(self):
        self._product = OneShopModel()

    def create_param_data(self):
        data = {}
        self._data = data

    @property
    def product(self):
        product = self._product

        self.reset()
        return product

    @property
    def data(self):
        data = self._data

        self.create_param_data()
        return data

    def produce_shop(self):
        """Метод позволяет установить shop(boolean) True """
        shop = True
        self._data.update( {"shop": shop} )

    def produce_shop_id(self, shop_id):
        """Метод добавляет в переменную data shop_id(int) """
        shop_id = shop_id
        self._data.update( {"shop_id": shop_id} )

    def produce_new_configuration(
            self, start_date, end_date, marka, product_id, shop_id, days_of_simulation
    ):
        """Метод позволяет создать конфигурацию для модели, вызывая метод

        set_attributes класса OneShopModel(подавая в качестве parameters - data):

        часть параметров задается извне:

        start_date

        end_date

        marka

        product_id

        shop_id

        days_of_simulation

        Принимает на вход:

        -

        Возвращает:

        _


        """
        self.produce_start_date( start_date )
        self.produce_end_date( end_date )
        self.produce_product_id( product_id )
        self.produce_marka( marka )
        self.produce_shop_id( shop_id )
        self.produce_disp()
        self.produce_logistic()
        self.produce_number_of_paths()
        self.produce_days_of_simulation( days_of_simulation )
        self.produce_sigma_parameter()
        self.produce_outlier_filtration()
        self.produce_product_id( product_id )
        self.produce_add_deficit()
        self.produce_shop()
        self.produce_a_level()
        self.produce_b_level()
        self.produce_c_level()
        self.produce_one_year()
        self.produce_seasonality()
        self._product.set_attributes( parameters=self._data )

        return self._product
