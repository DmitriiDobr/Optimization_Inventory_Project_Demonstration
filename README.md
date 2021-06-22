## Название приложения:

Программа называется "Закупщик-Про".

***

## Цель создания:

Программа создана с целью минимизации товарных остатков на складах предприятия,
повышения прибыли, уменьшения времени для составления плана будущих закупок.


***
## Функционал программы :

- Создание оптимального заказа с учетом прогнозных значений остатков.
- Подбор оптимальных параметров для каждого товара при прогнозировании спроса . 
- Бэкстест на исторических данных, предварительно найденных параметров.
- Оценка экономического эффекта  найденного оптимального решения.
- Оценка предполагаемого дефицита за прошлые периоды.
- Визуализация движения товарных остатков на складах
- Визуализация основных экономических показателей деятельности компании.



***
## Основные используемые технологии :
- numpy
- numba
- pandas
- PyQt5
- matplotlib
- black

### Замечание:

Репозиторий служит для демонстрации части функциональности приложения. Следующие файлы служат для демонстрации:


- src.model.supply_chain_logic.template_simulation_model.basic_model.bootstrap_data.py
- src.model.supply_chain_logic.template_simulation_model.basic_model.financial_analysis.py
- src.model.supply_chain_logic.template_simulation_model.basic_model.sales_cleaning.py
- src.model.supply_chain_logic.template_simulation_model.basic_model.supply_delay.py
- src.model.supply_chain_logic.template_simulation_model.simulation_model_template_builder.py
- src.model.supply_chain_logic.forecast_items.forecast_items_basic.forecast_engine.py
- src.model.supply_chain_logic.forecast_items.demand.py
- src.model.supply_chain_logic.forecast_items.lead.py
- src.model.supply_chain_logic.forecast_items.recalculate_leftovers.py

