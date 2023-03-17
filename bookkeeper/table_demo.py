
import sys

from PySide6 import QtWidgets
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository


class ExpensesTable(QtWidgets.QTableWidget):
    """
    Table for displaying recent expenses
    """
    def __init__(self, columns_names: list[str], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setHorizontalHeaderLabels(columns_names)
        self.header = self.horizontalHeader()
        length = len(columns_names)
        for i in range(length-1):
            self.header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(length-1, QtWidgets.QHeaderView.Stretch)

        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.verticalHeader().hide()

    def set_data(self, data: list[Expense]):
        for i, expense in enumerate(data):
            for j, x in enumerate(list(expense.__dict__.values())):
                self.setItem(i, j, QtWidgets.QTableWidgetItem(str(x).capitalize()))


exp_repo = SQLiteRepository[Expense]('demo_expenses.db', Expense)
data = exp_repo.get_all()

app = QtWidgets.QApplication(sys.argv)

columns_names = "Сумма Категория Потрачено Добавлено Комментарий".split()
expenses_table = ExpensesTable(columns_names, 10, 5)
expenses_table.set_data(data)


expenses_table.show()

sys.exit(app.exec())

