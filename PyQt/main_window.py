import sys
import os
from PyQt5.QtWidgets import QTableView, QApplication, QWidget, QPushButton, QMainWindow, QAction, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlTableModel, QSqlQuery, QSqlRelationalTableModel, QSqlRelation, \
    QSqlRelationalDelegate
import py_form

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Создаем экземпляр класса формы (экземпляр интерфейса)
        # из файла py_form
        self.ui = py_form.Ui_MainWindow()
        # Связываем экземпляр интерфейса с данным окном
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.db_path = 'Databases/database.sqlite3'
        self.ui.path_db.setText(self.db_path)
        self.save_db = QAction(QIcon('icon/save.png'), 'Save', self)
        self.open_db_file = QAction(QIcon('icon/open-db.png'), 'Open', self)
        self.add_row = QAction(QIcon('icon/add.png'), 'Add row', self)
        self.del_row = QAction(QIcon('icon/del.png'), ' Del row', self)
        self.ui.toolBar.addAction(self.save_db)
        self.ui.toolBar.addAction(self.open_db_file)
        self.ui.toolBar.addAction(self.add_row)
        self.ui.toolBar.addAction(self.del_row)
        self.db = None
        self.table_model = None
        self.open_db()

        self.add_row.triggered.connect(self.add_row_action)
        self.del_row.triggered.connect(self.del_row_action)
        self.save_db.triggered.connect(self.save_change_db)
        self.open_db_file.triggered.connect(self.open_db_file_action)
        self.ui.comboBox.currentIndexChanged.connect(self.show_table)

    def open_db(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.db_path)
        self.db.open()
        self.get_tables_name()
        self.show_table()

    def get_tables_name(self):
        self.ui.comboBox.clear()
        for table_name in self.db.tables():
            self.ui.comboBox.addItem(table_name)

    def show_table(self):
        self.table_model = QSqlRelationalTableModel()
        table = self.ui.comboBox.currentText()
        if table == 'goods':
            self.create_goods_table_model()
        elif table == 'employees':
            self.create_employees_table_model()
        else:
            self.table_model.setTable(table)
            self.table_model.select()
        self.table_model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        view = self.ui.tableView
        view.setModel(self.table_model)
        view.setItemDelegate(QSqlRelationalDelegate(view))

    def create_goods_table_model(self):
        self.table_model.setTable('goods')
        self.table_model.setRelation(2, QSqlRelation('units', 'unit_id', 'unit'))
        self.table_model.setRelation(3, QSqlRelation('categories', 'category_id', 'category_name'))
        self.table_model.select()

    def create_employees_table_model(self):
        self.table_model.setTable('employees')
        self.table_model.setRelation(2, QSqlRelation('positions', 'position_id', 'position'))
        self.table_model.select()

    def add_row_action(self):
        self.table_model.insertRows(self.table_model.rowCount(), 1)

    def del_row_action(self):
        rs = list(map(lambda x: x.row(), self.ui.tableView.selectedIndexes()))
        print(rs)
        for i in rs:
            self.table_model.removeRows(i, 1)

    def open_db_file_action(self):
        self.db_path = QFileDialog.getOpenFileName(self, "Open file")[0]
        self.ui.path_db.setText(self.db_path)
        self.db.close()
        self.open_db()

    def save_change_db(self):
        if self.table_model.submitAll():
            self.ui.statusbar.showMessage('Изменения сохранены')
        else:
            self.ui.statusbar.showMessage(f'{self.table_model.lastError().text()}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec())