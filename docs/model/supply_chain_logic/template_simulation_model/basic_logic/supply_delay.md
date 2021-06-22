from src.libraries.lib import numpy as np


class SupplyDelayShops:
    """
    Класс предназначен для имитации задержек поставок, как в конкретные магазины, так и на основной склад.

    Attributes:
    _ _ _ _ _ _

    main_center_expected_arrival(int) - ожидаемое количество дней для прибытия на основной склад

    shops_expected_arrival(dict) - ключи: конкретный магазин,

    значения - ожидаемое количество дней доставки для магазина.

    Methods:
    _ _ _ _ _ _

    generate_lead_main_center

    generate_lead_from_main_to_shops




    """

    def __init__(self, main_center_expected_arrival, shops_expected_arrival):
        self.main_center_expected_arrival = main_center_expected_arrival
        self.shops_expected_arrival = shops_expected_arrival

    def generate_lead_main_center(self, lower=3, upper=10):
        """Метод нужен для того, чтобы получить  отклонения от ожидаемого времени прибытия товара.

        Принимает на вход:

        lower(int) - максимальный срок прибытия товара за ранее

        upper(int) - маскимальный срок срыва поставки (дней)

        Возвращает:

        generated_arraivals(np.array) - сгенерированные отклонения от ожидаемого срока поставки


        """
        key = list(self.main_center_expected_arrival.keys())[0]
        expected = self.main_center_expected_arrival[key]
        lower_bound = expected - lower
        upper_bound = expected + upper
        arrivals_variants = [x for x in range(lower_bound, upper_bound)]

        generated_arrivals = np.random.choice(arrivals_variants, 20)

        generated_arrivals = generated_arrivals - expected

        return generated_arrivals

    def generate_lead_from_main_to_shops(
            self,
            shop_id,
            lower=1,
            upper=3,
    ):
        """
        Метод Метод нужен для того,

        чтобы получить  отклонения от ожидаемого времени прибытия товара для каждого магазина.

        Поставка из распределительного центра!

        Принимает на вход:

        shop_id(int) - уникальный id магазина, для которого генерируются отклонения

        lower(int) - максимальный срок прибытия товара заранее (дней)

        upper(int) - маскимальный срок срыва поставки (дней)

        Возвращет:

        generated_arraivals(np.array) - сгенерированные отклонения от ожидаемого срока поставки

        """

        key = shop_id
        center_key = list(self.main_center_expected_arrival.keys())[0]

        if shop_id == center_key:
            return np.zeros(20)

        expected = self.shops_expected_arrival[key]
        lower_bound = expected - lower
        upper_bound = expected + upper
        arrivals_variants = [x for x in range(lower_bound, upper_bound)]
        generated_arraivals = np.random.choice(arrivals_variants, 20)

        generated_arraivals = generated_arraivals - expected

        return generated_arraivals

    def generate_lead_all_route(self, shop_id):
        """Метод позволяет найти отклонения общего время доставки до каждого города с завода изготовителя.

        Включает в себя методы:

        generate_lead_main_center

        generate_lead_from_main_to_shops

        Принимает на вход:

        shop_id(int) - уникальный id магазина.

        Возвращает:

        generated_all_way(np.array) - сгенерированные отклонения от ожидаемого срока поставки

        """
        center_key = list(self.main_center_expected_arrival.keys())[0]

        if shop_id == center_key:
            return self.generate_lead_main_center(4, 10)

        generated_lead_main_center = self.generate_lead_main_center(4, 10)
        generated_lead_shops = self.generate_lead_from_main_to_shops(
            shop_id,
            1,
            3,
        )

        expected_shop = self.shops_expected_arrival.get(shop_id)
        expected_center = self.main_center_expected_arrival.get(center_key)

        generated_all_way = (
                np.array(generated_lead_shops)
                + np.array(generated_lead_main_center)
                - (expected_shop + expected_center)
        )

        return generated_all_way

    @classmethod
    def lead_time(cls):  # as a constructor
        """
        Метод позволяет инициализировать конструктор, для последующей генерации задержек и ранних сроков прибытия.

        """
        main_center_expected_arrival = {2: 30}
        shops_expected_arrival = {0: 10, 1: 4, 3: 5, 4: 3}
        return cls(main_center_expected_arrival, shops_expected_arrival)
