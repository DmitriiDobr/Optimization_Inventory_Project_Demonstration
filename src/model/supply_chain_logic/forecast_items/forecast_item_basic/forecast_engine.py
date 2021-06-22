from src.libraries.lib import ABC, abstractmethod

class ForecastOptimalItems(ABC):
    def __init__(self, df_cleaned_sales, products, optimal_parameters):
        self.df_cleaned_sales = df_cleaned_sales
        self.products = products
        self.optimal_parameters = optimal_parameters

    @abstractmethod
    def forecast_optimal_items(self):
        pass


class ForecastOptimalItemsUniqueShops(ForecastOptimalItems):
    def __init__(self, df_cleaned_sales, products, optimal_parameters, shops):
        super().__init__(df_cleaned_sales, products, optimal_parameters)
        self.shops = shops

    def forecast_optimal_items(self):

        forecast_unique_shops_products = {}

        for shop in self.shops:
            forecast_unique_shops = {}
            for product in self.products:

                optimal_parameters = self.optimal_parameters.get(shop).get(product)
                model_optimal_parameters = OneShopModel()

                model_optimal_parameters.set_attributes(optimal_parameters)
                solution = model_optimal_parameters.template_model(
                    self.df_cleaned_sales
                )

                forecast_unique_shops[product] = solution
            forecast_unique_shops_products[shop] = forecast_unique_shops
        return forecast_unique_shops_products


class ForecastOptimalItemsCrossShops(ForecastOptimalItems):
    def __init__(self, df_cleaned_sales, products, optimal_parameters):
        super().__init__(df_cleaned_sales, products, optimal_parameters)

    def forecast_optimal_items(self):

        forecast_unique_product = {}
        for product in self.products:

            optimal_parameters = self.optimal_parameter.get(product)
            model_optimal_parameters = AllShopsModel()

            model_optimal_parameters.set_attributes(optimal_parameters)

            solution = model_optimal_parameters.template_model(self.df_cleaned_sales)
            forecast_unique_product[product] = solution
        return forecast_unique_product