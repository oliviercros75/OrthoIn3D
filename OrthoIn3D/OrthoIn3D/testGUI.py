from PyQt5 import QtWidgets

class Widget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.resize(500,500)
        self.items = []
        self.item_count = 0
        self.item_factory = QtWidgets.QLineEdit

        group_box = QtWidgets.QGroupBox()
        self.item_layout = QtWidgets.QVBoxLayout(group_box)
        self.item_layout.addStretch(2)

        self.spin_box = QtWidgets.QSpinBox(self)
        self.spin_box.valueChanged.connect(self.set_item_count)

        h_layout = QtWidgets.QHBoxLayout(self)
        h_layout.addWidget(group_box, 2)
        h_layout.addWidget(self.spin_box, 0)


    def set_item_count(self, new_count:int):
        n_items = len(self.items)
        for ii in range(n_items, new_count):
            item = self.item_factory(self)
            self.items.append(item)
            self.item_layout.insertWidget(n_items, item)
        for ii in range(self.item_count, new_count):
            self.item_layout.itemAt(ii).widget().show()
        for ii in range(new_count, self.item_count):
            self.item_layout.itemAt(ii).widget().hide()
        self.item_count = new_count

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Widget()
    window.show()
    app.exec()