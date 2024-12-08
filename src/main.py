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


        layout1 = QHBoxLayout()
        layout2 = QGridLayout()
        self.place = QListView()
        
        layout1.addLayout(layout2)
        layout1.addWidget(self.place)
        

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
        
        layout2.setAlignment(Qt.AlignTop)


        layout2.addWidget(self.ourlabel,1,1)
        layout2.addWidget(self.our_org,1,2)
        
        layout2.addWidget(self.clientlabel,2,1)
        layout2.addWidget(self.client,2,2)

        layout2.addWidget(self.doctypelabel,3,1)
        layout2.addWidget(self.doctype,3,2)

        layout2.addWidget(self.docnumlabel,4,1)
        layout2.addWidget(self.docnumber,4,2)
        
        layout2.addWidget(self.docdatelabel,5,1)
        layout2.addWidget(self.docdate,5,2)
        
        self.setLayout(layout1)

    
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

