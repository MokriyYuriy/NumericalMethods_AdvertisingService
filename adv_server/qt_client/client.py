import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QToolTip, QDesktopWidget,
    QPushButton, QApplication, QMessageBox, QDesktopWidget, QGridLayout,
    QLabel, QTextEdit, QLineEdit, QTabWidget, QFormLayout, QListWidget, QListWidgetItem,
    QComboBox)
from PyQt5.QtGui import QFont, QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp
from adv_server.qt_client.plot import *
from adv_server.solver import solver
from adv_server.beta_function import beta_functions_dict

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 12))

        grid = QGridLayout()
        grid.setSpacing(0)

        #self.statusBar()

        plot_widget = QWidget()

        tabs = QTabWidget()
        grid.addWidget(QLabel('Plots'))
        grid.addWidget(plot_widget, 2, 0, 1, 15)
        grid.addWidget(tabs, 1, 15, 2, 6)

        self.manual_tab = QWidget()
        tabs.addTab(self.manual_tab, 'Manual Mode')
        self.auto_tab = QWidget()
        tabs.addTab(self.auto_tab, 'Auto Mode')

        self.init_auto_tab()
        self.init_manual_tab()

        self.setLayout(grid)

        self.resize(1200, 800)
        self.center()
        self.setWindowTitle('Advertising Server')
        self.show()

    def init_manual_tab(self):
        form = QFormLayout()
        form.setSpacing(10)

        self.manual_x0 = QLineEdit()
        self.manual_y0 = QLineEdit()
        form.addRow(QLabel('x0'), self.manual_x0)
        form.addRow(QLabel('y0'), self.manual_y0)

        self.manual_T = QLineEdit()
        form.addRow(QLabel('T'), self.manual_T)

        form.addRow(QLabel('\u03C1(t) = aw * (b - w)'))
        self.manual_rho_a = QLineEdit()
        self.manual_rho_b = QLineEdit()
        form.addRow(QLabel('a:'), self.manual_rho_a)
        form.addRow(QLabel('b:'), self.manual_rho_b)

        form.addRow(QLabel('S(t) = c * t + d * sin(t)'))
        self.manual_S_c = QLineEdit()
        self.manual_S_d = QLineEdit()
        form.addRow(QLabel('c:'), self.manual_S_c)
        form.addRow(QLabel('d:'), self.manual_S_d)

        form.addRow(QLabel('z(t) = e * t + f * cos(t)'))
        self.manual_z_e = QLineEdit()
        self.manual_z_f = QLineEdit()
        form.addRow(QLabel('e:'), self.manual_z_e)
        form.addRow(QLabel('f:'), self.manual_z_f)

        form.addRow(QLabel('Beta function type'))
        self.manual_combobox = QComboBox()
        self.manual_combobox.addItems(list(beta_functions_dict.keys()))
        form.addRow(self.manual_combobox)
        self.manual_beta = QLineEdit()
        form.addRow(QLabel('Beta:'), self.manual_beta)

        self.all_manual_edit_lines = [self.manual_z_e,
                      self.manual_z_f,
                      self.manual_S_c,
                      self.manual_S_d,
                      self.manual_T,
                      self.manual_rho_a,
                      self.manual_rho_b,
                      self.manual_beta,
                      self.manual_x0,
                      self.manual_y0]

        for qline in self.all_manual_edit_lines:
            qline.setValidator(QRegExpValidator(QRegExp('[+-]?\\d*[\\.,]?\\d+')))
        self.manual_submit = QPushButton('Submit')
        self.manual_submit.clicked.connect(self.manual_submit_clicked)

        form.addRow(self.manual_submit)
        self.manual_tab.setLayout(form)

    def init_auto_tab(self):
        form = QFormLayout()
        form.setSpacing(10)

        self.auto_x0 = QLineEdit()
        self.auto_y0 = QLineEdit()
        form.addRow(QLabel('x0'), self.auto_x0)
        form.addRow(QLabel('y0'), self.auto_y0)

        self.auto_T = QLineEdit()
        form.addRow(QLabel('T'), self.auto_T)

        form.addRow(QLabel('\u03C1(t) = aw * (b - w)'))
        self.auto_rho_a = QLineEdit()
        self.auto_rho_b = QLineEdit()
        form.addRow(QLabel('a:'), self.auto_rho_a)
        form.addRow(QLabel('b:'), self.auto_rho_b)

        form.addRow(QLabel('S(t) = c * t + d * sin(t)'))
        self.auto_S_c = QLineEdit()
        self.auto_S_d = QLineEdit()
        form.addRow(QLabel('c:'), self.auto_S_c)
        form.addRow(QLabel('d:'), self.auto_S_d)

        form.addRow(QLabel('z(t) = e * t + f * cos(t)'))
        self.auto_z_e = QLineEdit()
        self.auto_z_f = QLineEdit()
        form.addRow(QLabel('e:'), self.auto_z_e)
        form.addRow(QLabel('f:'), self.auto_z_f)

        form.addRow(QLabel('Beta function type'))
        self.auto_combobox = QComboBox()
        self.auto_combobox.addItems(list(beta_functions_dict.keys()))
        form.addRow(self.auto_combobox)
        self.auto_beta_lower_bound = QLineEdit()
        self.auto_beta_upper_bound = QLineEdit()
        form.addRow(QLabel('Beta:'))
        form.addRow(QLabel('From:'), self.auto_beta_lower_bound)
        form.addRow(QLabel('To:'), self.auto_beta_upper_bound)

        self.all_auto_edit_lines = [self.auto_z_e,
                      self.auto_z_f,
                      self.auto_S_c,
                      self.auto_S_d,
                      self.auto_rho_a,
                      self.auto_rho_b,
                      self.auto_T,
                      self.auto_beta_lower_bound,
                      self.auto_beta_upper_bound,
                      self.auto_x0,
                      self.auto_y0]

        for qline in self.all_auto_edit_lines:
            qline.setValidator(QRegExpValidator(QRegExp('[+-]?\\d*[\\.,]?\\d+')))

        self.auto_submit = QPushButton('Submit')
        self.auto_submit.clicked.connect(self.auto_submit_clicked)
        form.addRow(self.auto_submit)
        self.auto_tab.setLayout(form)

    def _check_non_empty(self, qlines):
        for qline in qlines:
            if qline.text() == '':
                return False
        return True

    def manual_plot_builder(self):
        pass

    def auto_plot_builder(self):
        pass

    def manual_submit_clicked(self):
        if not self._check_non_empty(self.all_manual_edit_lines):
            QMessageBox.about(self, 'Message', 'Some fields are empty')
            return
        parameters = {'rho_a': float(self.manual_rho_a.text()),
                      'rho_b': float(self.manual_rho_b.text()),
                      'S_c': float(self.manual_S_c.text()),
                      'S_d': float(self.manual_S_d.text()),
                      'z_e': float(self.manual_z_e.text()),
                      'z_f': float(self.manual_z_f.text()),
                      'T' : float(self.manual_T.text()),
                      'beta': float(self.manual_beta.text()),
                      'beta_function' : self.manual_combobox.currentText(),
                      'x0' : float(self.manual_x0.text()),
                      'y0' : float(self.manual_y0.text())
                      }
        solver(parameters, self, manual=True)

    def auto_submit_clicked(self):
        if not self._check_non_empty(self.all_auto_edit_lines):
            QMessageBox.about(self, 'Message', 'Some fields are empty')
            return
        parameters = {'rho_a': float(self.auto_rho_a.text()),
                      'rho_b': float(self.auto_rho_b.text()),
                      'S_c': float(self.auto_S_c.text()),
                      'S_d': float(self.auto_S_d.text()),
                      'z_e': float(self.auto_z_e.text()),
                      'z_f': float(self.auto_z_f.text()),
                      'T': float(self.auto_T.text()),
                      'lower_beta': float(self.auto_beta_lower_bound.text()),
                      'upper_beta': float(self.auto_beta_upper_bound.text()),
                      'beta_function': self.auto_combobox.currentText(),
                      'x0': float(self.auto_x0.text()),
                      'y0': float(self.auto_y0.text())
                      }
        solver(parameters, self, manual=False)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to exit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
