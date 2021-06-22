from src.model.supply_chain_logic.forecast_items.forecast_item_basic import ForecastOptimalItemsUniqueShops
from src.model.supply_chain_logic.forecast_items.forecast_item_basic import ForecastOptimalItemsCrossShops


class DemandFirstEchelon(ForecastOptimalItemsCrossShops):
    def __init__(self, df_cleaned_sales, products, optimal_parameters):
        super().__init__(df_cleaned_sales, products, optimal_parameters)

class DemandSecondEchelon(ForecastOptimalItemsUniqueShops):
    def __init__(self, df_cleaned_sales, products, optimal_parameters, shops):
        super().__init__(df_cleaned_sales, products, optimal_parameters, shops)