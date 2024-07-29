from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QComboBox,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QSpinBox,
    QHBoxLayout,
)

import sys

ENTER_PLAIN_TEXT = "Enter plain text"
ENTER_ENCRYPTED_TEXT = "Enter encrypted text"


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Caesar cipher")
        layout = QVBoxLayout()

        list_box = QComboBox()
        list_box.addItems(["Encryption", "Decryption"])
        list_box.currentIndexChanged.connect(self.list_box_index_changed)
        layout.addWidget(list_box)

        self.type = 0
        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(0)
        self.spin_box.setMaximum(26)
        self.spin_box.setValue(3)
        layout.addWidget(self.spin_box)

        self.edit_box = QLineEdit()
        self.edit_box.setPlaceholderText(ENTER_PLAIN_TEXT)
        self.edit_box.returnPressed.connect(self.process)
        layout.addWidget(self.edit_box)

        lyt_result = QHBoxLayout()
        lyt_result.setContentsMargins(10, 10, 10, 10)
        lyt_result.addWidget(QLabel("Result = "))
        self.lbl_result = QLabel("")
        self.lbl_result.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        lyt_result.addWidget(self.lbl_result)
        layout.addLayout(lyt_result)

        push_button = QPushButton("Enter")
        push_button.clicked.connect(self.process)
        layout.addWidget(push_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def process(self):
        text = self.edit_box.text().lower()
        shift = self.spin_box.value()
        base = ord("a")
        result = []
        for ch in text:
            if ch == " ":
                result.append(" ")
                continue
            if self.type == 0:
                res = (ord(ch) - base + shift) % 26
            else:
                res = (ord(ch) - base - shift) % 26
            result.append(chr(res + base))
        self.lbl_result.setText("".join(result))

    def list_box_index_changed(self, i):
        self.type = i
        if i == 0:
            self.edit_box.setPlaceholderText(ENTER_PLAIN_TEXT)
        else:
            self.edit_box.setPlaceholderText(ENTER_ENCRYPTED_TEXT)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
