
from dataclasses import dataclass


@dataclass()
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

    def __setattr__(self, name, value):
        if name == 'summ' and value < 0:
            raise ValueError("Budget's sum must be positive value")
        self.__dict__[name] = value

