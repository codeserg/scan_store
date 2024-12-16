import os 
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError


# Создаем базовый класс
Base = declarative_base()

class SessionManager:
    def __init__(self, timeout=5):
    
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, 'example.db')
        self.engine = create_engine(f'sqlite:///{db_path}')

        self.Session = sessionmaker(bind=self.engine)
        self.session = None

    def __enter__(self):
        try:
            self.session = self.Session()
            return self.session  
        except SQLAlchemyError as e:
            print(f"Ошибка при подключении к базе данных: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        
        try:
            if exc_type is not None:
                self.session.rollback()  # Откатываем транзакцию при ошибке
            self.session.close()  
        except SQLAlchemyError as e:
            print(f"Ошибка при закрытии сессии: {e}")
            raise

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)

    # Связь с договорами
    contracts = relationship("Contract", back_populates="client")


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    contract_number = Column(String, nullable=False)
    date_signed = Column(Date)

    # Связь с клиентами
    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship("Client", back_populates="contracts")

    # Связь с документами
    documents = relationship("Document", back_populates="contract")

# Определяем таблицу "Документы"
class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    document_type = Column(String(255), nullable=False)
    content = Column(String)

    # Связь с договорами
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    contract = relationship("Contract", back_populates="documents")

class Our_orgs(Base):
    __tablename__ = 'our_orgs'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    storage_path=Column(String(255), nullable=False)

class Widget(QWidget):

    def __init__(self, *args, **kwargs):
          
        QWidget.__init__(self, *args, **kwargs)
        self.setWindowTitle("Хранилище документов")
        self.setAutoFillBackground(True)
        self.resize(1000,800); 

        self.setStyleSheet("""
            QWidget {
                font-size: 14px;           /* Общий размер шрифта для всех элементов */
            }
            QLabel {
                font-weight: bold;         /* Жирный шрифт для меток */
            }
        """)


        self.panel_tables = QTabWidget()
        self.layout_stack = QStackedLayout()
        self.layout_stack.addWidget(self.panel_tables)
        panel1 = QWidget(self.panel_tables)
        panel2 = QWidget(self.panel_tables)
        panel3 = QWidget(self.panel_tables)
        panel4 = QWidget(self.panel_tables)
        
        layout1= QGridLayout()
        layout2= QVBoxLayout()
        layout3= QVBoxLayout()
        layout4= QVBoxLayout()
        self.buttons1_layout = QHBoxLayout()

        panel1.setLayout(layout1)
        panel2.setLayout(layout2)
        panel3.setLayout(layout3)
        panel4.setLayout(layout4)
        
        self.panel_tables.addTab(panel1,'Документы')
        self.panel_tables.addTab(panel2,'Клиенты')
        self.panel_tables.addTab(panel3,'Договора')
        self.panel_tables.addTab(panel4,'Наши организации')
        
        self.buttons1_place = QWidget(panel1)
        self.buttons1_place.setLayout(self.buttons1_layout)

        button1 = QPushButton("Показать")
        button2 = QPushButton("Добавить")
        button3 = QPushButton("Редактировать")
        button4 = QPushButton("Удалить")

        self.buttons1_layout.addWidget(button1)
        self.buttons1_layout.addWidget(button2)
        self.buttons1_layout.addWidget(button3)
        self.buttons1_layout.addWidget(button4)
                
        self.our_org = QComboBox()
        self.ourlabel = QLabel("Наша организация")
        self.load_our_orgs()
        self.our_org.currentIndexChanged.connect(self.on_selection_change)
        self.client = QComboBox()
        self.clientlabel = QLabel("Клиент")
        self.doctype = QComboBox()
        self.doctypelabel = QLabel("Тип документа")
        self.docnumber = QLineEdit()
        self.docnumlabel = QLabel("№ документа")
        self.docdate = QDateEdit()
        self.docdatelabel = QLabel("Дата документа")
        
        self.data_grid = QTableWidget()
        #layout1.setAlignment(Qt.AlignTop)
        layout1.setSpacing(10)

        layout1.addWidget(self.ourlabel,0,0)
        layout1.addWidget(self.our_org,0,1)
        
        layout1.addWidget(self.clientlabel,1,0)
        layout1.addWidget(self.client,1,1)

        layout1.addWidget(self.doctypelabel,2,0)
        layout1.addWidget(self.doctype,2,1)

        layout1.addWidget(self.docnumlabel,3,0)
        layout1.addWidget(self.docnumber,3,1)
        
        layout1.addWidget(self.docdatelabel,4,0)
        layout1.addWidget(self.docdate,4,1)
        
        layout1.addWidget(self.buttons1_place,5,0,2,1)
        
        layout1.addWidget(self.data_grid,9,0,2,1)

        self.setLayout(self.layout_stack)

    def show_panel(self, panel_index):
        self.layout_stack.setCurrentIndex(panel_index)
        print(panel_index)
    
    def load_our_orgs(self):
        with SessionManager() as s:
            items = s.query(Our_orgs).all()
            for item in items:
                self.our_org.addItem(item.name, item.id)  # item.id сохраняется как пользовательские данные
    
    def on_selection_change(self):
    
        index = self.our_org.currentIndex()
        item_id = self.our_org.itemData(index)
        item_name = self.our_org.currentText()

        print(f"Selected: {item_name}, ID: {item_id}")

    def pickfile(self):
        pickedfile, pickettype = QFileDialog.getOpenFileName(self, 'Укажите файл для загрузки', '')
        if pickedfile:
            self.edit1.setText(pickedfile)
            self.logwindow.addItem("Обработка файла {}".format(pickedfile))

def create_db():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, 'example.db')

    engine = create_engine(f'sqlite:///{db_path}')

    Base.metadata.create_all(engine)

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
