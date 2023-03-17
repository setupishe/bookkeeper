import sys
from PySide6 import QtWidgets
from typing import Any


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


class AutoComboBox(QtWidgets.QComboBox):
    def __init__(self, data: list[Any], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_data(data)

    def _set_data(self, data: list[Any]):
        for i in range(len(data)):
            self.insertItem(i, data[i])


app = QtWidgets.QApplication(sys.argv)

categories_list = LabeledWidget("Категории", AutoComboBox(['11', '22', '2412424']))

add_summ = LabeledWidget("Сумма", QtWidgets.QLineEdit("0"))

layout = QtWidgets.QVBoxLayout()
layout.addWidget(categories_list)
layout.addWidget(add_summ)


window = QtWidgets.QWidget()
window.setLayout(layout)
window.show()

sys.exit(app.exec())

