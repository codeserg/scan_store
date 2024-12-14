    def load_documents(self, documents=None):
        if documents is None:
            documents,status = get_documents()
            if not status:
                self.show_message ("Нет подключения к базе данных")
                self.close()
                sys.exit()

        self.table_widget.setRowCount(len(documents))
        self.table_widget.setColumnWidth(1, 300)
        self.table_widget.setColumnWidth(2, 300)
        self.table_widget.setColumnWidth(3, 300)

        for row, doc in enumerate(documents):
            
                      
            id_item = QTableWidgetItem(str(doc.id))
            #id_item.setFlags(id_item.flags() ^ QtWidgets.Qt.ItemIsEditable)
            self.table_widget.setItem(row, 0, id_item)

            seller_item = QTableWidgetItem(doc.seller)
            self.table_widget.setItem(row, 1, seller_item)

            buyer_item = QTableWidgetItem(doc.buyer)
            self.table_widget.setItem(row, 2, buyer_item)

            manager_item = QTableWidgetItem(doc.manager)
            self.table_widget.setItem(row, 3, manager_item)

            number_item = QTableWidgetItem(doc.number)
            self.table_widget.setItem(row, 4, number_item)

            date_item = QTableWidgetItem(doc.date.strftime("%d.%m.%Y"))
            self.table_widget.setItem(row, 5, date_item)
           
            
            checkbox = QCheckBox()
            self.table_widget.setCellWidget(row, 6, checkbox)
        
            if doc.uploaded:
                for cell in [id_item,seller_item,buyer_item,manager_item,number_item,date_item]:
                    cell.setBackground(QColor(255, 200, 200))        
            
        self.count_label.setText (f"Найдено документов: {len(documents)} ")
