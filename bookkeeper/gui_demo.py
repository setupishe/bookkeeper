
import sys

from PySide6 import QtWidgets
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository


exp_repo = SQLiteRepository[Expense]('demo_expenses.db', Expense)
data = exp_repo.get_all()

app = QtWidgets.QApplication(sys.argv)

expenses_table = QtWidgets.QTableWidget(5, 100)
expenses_table.setColumnCount(5)
expenses_table.setRowCount(10)
expenses_table.setHorizontalHeaderLabels(
"Сумма Категория Потрачено Добавлено Комментарий".split())
header = expenses_table.horizontalHeader()
header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

expenses_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
expenses_table.verticalHeader().hide()

def set_data(data: list[Expense]):
    for i, expense in enumerate(data):
        for j, x in enumerate(list(expense.__dict__.values())):
            expenses_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(x).capitalize()))


set_data(data)

expenses_table.show()

sys.exit(app.exec())