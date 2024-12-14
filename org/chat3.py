import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QStackedWidget
from sqlalchemy import create_engine, MetaData, Table, select

# Пример функции для загрузки данных из базы данных
def fetch_data_from_db(table_name):
    engine = create_engine('sqlite:///example.db')  # Пример для SQLite базы данных
    connection = engine.connect()
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)
    
    stmt = select([table])
    result = connection.execute(stmt).fetchall()
    
    connection.close()
    return result

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

        # Создаем пустые таблицы
        self.table1 = QTableWidget()  # таблица для данных из DB
        self.table2 = QTableWidget()  # другая таблица

        # Добавляем таблицы в QStackedWidget
        self.stacked_widget.addWidget(self.table1)
        self.stacked_widget.addWidget(self.table2)

        # Статус загрузки данных
        self.is_table1_loaded = False
        self.is_table2_loaded = False

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
        if not self.is_table1_loaded:
            # Загрузка данных из базы в таблицу 1
            data = fetch_data_from_db('table1')  # Пример функции для SQLAlchemy
            self.populate_table(self.table1, data)
            self.is_table1_loaded = True  # Данные загружены
        self.stacked_widget.setCurrentIndex(0)  # Показать первую таблицу

    def show_table2(self):
        if not self.is_table2_loaded:
            # Загрузка данных из базы в таблицу 2
            data = fetch_data_from_db('table2')  # Пример функции для SQLAlchemy
            self.populate_table(self.table2, data)
            self.is_table2_loaded = True  # Данные загружены
        self.stacked_widget.setCurrentIndex(1)  # Показать вторую таблицу

    def populate_table(self, table_widget, data):
        # Функция для заполнения QTableWidget данными
        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(data[0]))  # Предполагаем, что данные это список кортежей
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
