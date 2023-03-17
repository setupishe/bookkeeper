import sys
from PySide6 import QtWidgets, QtGui, QtCore
from typing import Any
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository


class LabeledWidget(QtWidgets.QWidget):
    """
    Creates vertical or horisontal layout with label and QtWidget
    """
    def __init__(self, text, widget: QtWidgets.QWidget, orientation: str = 'horisontal', *args, **kwargs):
        super().__init__(*args, **kwargs)

        if orientation == "vertical":
            self.layout = QtWidgets.QVBoxLayout()
        elif orientation == "horisontal":
            self.layout = QtWidgets.QHBoxLayout()
        else:
            raise ValueError("orientation must be either vertical or horisontal")
        self.label = QtWidgets.QLabel(text)
        self.widget = widget
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.widget)
        self.setLayout(self.layout)


class AutoTable(QtWidgets.QTableWidget):
    """
    Table for displaying recent expenses
    """
    def __init__(self, columns_names: list[str], data: list[Any], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setHorizontalHeaderLabels(columns_names)
        self.header = self.horizontalHeader()
        length = len(columns_names)
        for i in range(length - 1):
            self.header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(length - 1, QtWidgets.QHeaderView.Stretch)

        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.verticalHeader().hide()
        self._set_data(data)

    def _set_data(self, data: list[Any]):
        for i, expense in enumerate(data):
            for j, x in enumerate(expense):
                self.setItem(i, j, QtWidgets.QTableWidgetItem(str(x).capitalize()))


class AutoComboBox(QtWidgets.QComboBox):
    def __init__(self, data: list[Any], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_data(data)

    def _set_data(self, data: list[Any]):
        for i in range(len(data)):
            self.insertItem(i, data[i])


app = QtWidgets.QApplication(sys.argv)

categories_list = LabeledWidget("Категория", AutoComboBox(['11', '22', '2412424']))
item = QtGui.QStandardItem("test")
categories_list.widget.insertItem(0, "Изменить...")
newFont = QtGui.QFont("FontFamily", italic=True)
categories_list.widget.setItemData(0, newFont, QtCore.Qt.FontRole)

add_summ = LabeledWidget("Сумма", QtWidgets.QLineEdit("0"))



button = QtWidgets.QPushButton()
button.setText("Добавить")
button.setStyleSheet('QPushButton {background-color: #3b4dbf; color: white;}')

exp_repo = SQLiteRepository[Expense]('demo_expenses.db', Expense)
data = exp_repo.get_all()
data = [list(x.__dict__.values()) for x in data]


columns_names = "Сумма Категория Потрачено Добавлено Комментарий".split()
expenses_table = LabeledWidget("Последние расходы", AutoTable(columns_names, data, 10, 5), "vertical")
budget_columns = ["", "Сумма", "Бюджет", "Категория"]
budget_data = [["День", 200, 1000, 0], ["Неделя", 300, 1300, 0], ["Месяц", 400, 5000, 3]]
budget_table = LabeledWidget("Бюджет", AutoTable(budget_columns, budget_data, 3, 4), "vertical")

layout = QtWidgets.QVBoxLayout()
layout.addWidget(expenses_table)
layout.addWidget(budget_table)
layout.addWidget(add_summ)
layout.addWidget(categories_list)
layout.addWidget(button)

layout.addSpacing(1)

window = QtWidgets.QWidget()
window.setLayout(layout)
window.resize(max(expenses_table.width(), budget_table.width())+100, 700)
window.show()
sys.exit(app.exec())

