
import sys

from PySide6 import QtWidgets
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from typing import Any
from gui_demo import LabeledWidget



class AutoTable(QtWidgets.QTableWidget):
    """
    Table for displaying recent expenses
    """
    def __init__(self, columns_names: list[str], data: list[Any], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setHorizontalHeaderLabels(columns_names)
        self.header = self.horizontalHeader()
        length = len(columns_names)
        for i in range(length-1):
            self.header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(length-1, QtWidgets.QHeaderView.Stretch)

        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.verticalHeader().hide()
        self._set_data(data)

    def _set_data(self, data: list[Any]):
        for i, expense in enumerate(data):
            for j, x in enumerate(expense):
                self.setItem(i, j, QtWidgets.QTableWidgetItem(str(x).capitalize()))


exp_repo = SQLiteRepository[Expense]('demo_expenses.db', Expense)
data = exp_repo.get_all()
data = [list(x.__dict__.values()) for x in data]

app = QtWidgets.QApplication(sys.argv)

columns_names = "Сумма Категория Потрачено Добавлено Комментарий".split()
expenses_table = LabeledWidget("Последние расходы", AutoTable(columns_names, data, 10, 5), "vertical")
budget_columns = ["", "Сумма", "Бюджет", "Категория"]
budget_data = [["День", 200, 1000, 0], ["Неделя", 300, 1300, 0], ["Месяц", 400, 5000, 3]]
budget_table = LabeledWidget("Бюджет", AutoTable(budget_columns, budget_data, 3, 4), "vertical")

budget_table.show()

sys.exit(app.exec())

