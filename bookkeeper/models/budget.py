
from dataclasses import dataclass


@dataclass(slots=True)
class Budget:
    """
    Бюджет на расходы.
    period = срок
    category - id категории расходов
    summ - сумма денег
    pk - id записи в базе данных
    """
    category: int
    summ: int = 0
    period: str = ''
    pk: int = 0
