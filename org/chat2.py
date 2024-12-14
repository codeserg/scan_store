import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QStackedWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Основное окно
        self.setWindowTitle("Приложение с двумя таблицами")
        self.setGeometry(100, 100, 600, 400)

        # Создаем центральный виджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Создаем слой QStackedWidget для переключения между таблицами
        self.stacked_widget = QStackedWidget(self)

        # Создаем первую таблицу
        self.table1 = QTableWidget(3, 3)  # 3 строки, 3 столбца
        self.table1.setHorizontalHeaderLabels(['Колонка 1', 'Колонка 2', 'Колонка 3'])
        for i in range(3):
            for j in range(3):
                self.table1.setItem(i, j, QTableWidgetItem(f'Ячейка {i+1},{j+1}'))

        # Создаем вторую таблицу
        self.table2 = QTableWidget(4, 4)  # 4 строки, 4 столбца
        self.table2.setHorizontalHeaderLabels(['A', 'B', 'C', 'D'])
        for i in range(4):
            for j in range(4):
                self.table2.setItem(i, j, QTableWidgetItem(f'Ячейка {i+1},{j+1}'))

        # Добавляем таблицы в QStackedWidget
        self.stacked_widget.addWidget(self.table1)
        self.stacked_widget.addWidget(self.table2)

        # Создаем кнопки для переключения таблиц
        button1 = QPushButton("Показать таблицу 1")
        button2 = QPushButton("Показать таблицу 2")

        # Привязываем кнопки к методам переключения таблиц
        button1.clicked.connect(self.show_table1)
        button2.clicked.connect(self.show_table2)

        # Создаем layout и добавляем виджеты
        layout = QVBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(self.stacked_widget)

        central_widget.setLayout(layout)

    def show_table1(self):
        self.stacked_widget.setCurrentIndex(0)  # Показать первую таблицу

    def show_table2(self):
        self.stacked_widget.setCurrentIndex(1)  # Показать вторую таблицу

# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
