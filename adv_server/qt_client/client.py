import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QToolTip, QDesktopWidget,
    QPushButton, QApplication, QMessageBox, QDesktopWidget, QGridLayout,
    QLabel, QTextEdit, QLineEdit, QTabWidget, QFormLayout, QListWidget, QListWidgetItem,
    QComboBox, QFileDialog, QCheckBox, QHBoxLayout)
from PyQt5.QtGui import QFont, QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp, QThread, pyqtSignal
from adv_server.qt_client.plot import *
from adv_server.solver import main_solver
from adv_server.beta_function import beta_functions_dict
import matplotlib
matplotlib.use("qt5agg")
import matplotlib.pyplot as plt
import pickle
import multiprocessing
from collections import defaultdict

unicode_to_latex = {
    '\u03B2(S - x)' : '$\\beta (S - x)$',
    '\u03B2(x - z)' : '$\\beta (x - z)$',
    '\u03B2' : '$\\beta$'
}

colors = ['red', 'green', 'blue', 'black', 'yellow', 'grey']

temp_file_name = "adv_server_temp_file.tmp"

class ComputationalThread(QThread):
    status_trigger = pyqtSignal('QString')

    def __init__(self, parameters, manual):
        QThread.__init__(self)
        self.parameters = parameters
        self.manual = manual

    def __del__(self):
        self.wait()

    def run(self):
        res = main_solver(self.parameters, self, self.manual)
        with open(temp_file_name, "wb") as ftw:
            pickle.dump(res, ftw)

    def update_status(self, string):
        self.status_trigger.emit(string)


def plot_builder():
    with open(temp_file_name, 'rb') as ftr:
        data = pickle.load(ftr)

    fig = plt.figure(figsize=(15, 12), facecolor='white')
    #plt.plot(range(10))
    if data[5] is not None:
        axes1 = fig.add_subplot(2, 3, 1)
        axes1.plot(data[0][1], data[0][0][:,0], label="x")
        axes1.plot(data[1].arguments, data[1].values, label="S")
        axes1.set_xlabel("t")
        axes1.legend()
        axes2 = fig.add_subplot(2, 3, 3)
        axes2.plot(data[0][1], data[0][0][:,1], label="y")
        axes2.set_xlabel("t")
        axes2.legend()
        axes3  = fig.add_subplot(2, 3, 4)
        axes3.plot(data[3].arguments, data[3].values, label="$\\rho$")
        axes3.set_xlabel("t")
        axes3.legend()
        axes4 = fig.add_subplot(2, 3, 2)
        axes4.plot(data[2].arguments, data[2].values, label="z")
        axes4.set_xlabel("t")
        axes4.legend()
        axes5 = fig.add_subplot(2, 3, 5)
        axes5.plot(data[0][0][:,0], data[1].values)
        axes5.set_xlabel('x')
        axes5.set_ylabel('S')
        axes5.set_title('S(x)')
        axes6 = fig.add_subplot(2, 3, 6)
        axes6.plot(data[1].arguments, data[1].values - data[0][0][:,0])
        axes6.set_title("S(t) - x(t)")
        axes6.set_xlabel("t")
    else:
        if data[0][0] == -1:
            return
        axes1 = fig.add_subplot(2, 4, 1)
        for x in data[0][1]:
            axes1.plot(x[2][1], x[2][0][:,0], color="black", alpha=0.5)
        axes1.plot(data[0][1][data[0][0]][2][1], data[0][1][data[0][0]][2][0][:,0], color="red", label="best x")
        axes1.plot(data[1].arguments, data[1].values, color="green", label="S")
        axes1.set_xlabel("t")
        axes1.legend()
        axes2 = fig.add_subplot(2, 4, 2)
        for x in data[0][1]:
            axes2.plot(x[2][1], x[2][0][:, 1], color="black", alpha=0.5)
        axes2.plot(data[0][1][data[0][0]][2][1], data[0][1][data[0][0]][2][0][:, 1], color="red", label="best y")
        axes2.set_xlabel("t")
        axes2.legend()
        axes3 = fig.add_subplot(2, 4, 4)
        axes3.plot(data[3].arguments, data[3].values, label="$\\rho$")
        axes3.set_xlabel("w")
        axes3.legend()
        axes4 = fig.add_subplot(2, 4, 3)
        axes4.plot(data[2].arguments, data[2].values, label="z")
        axes4.set_xlabel("t")
        axes4.legend()
        axes5 = fig.add_subplot(2, 4, 5)
        for x in data[0][1]:
            axes5.plot(x[2][0][:, 0], data[1].values, color="black", alpha=0.5)
        axes5.plot(data[0][1][data[0][0]][2][0][:, 0], data[1].values, color="red", label="best x")
        axes5.set_title("S(x)")
        axes5.set_xlabel("x")
        axes5.set_ylabel("y")
        axes6 = fig.add_subplot(2, 4, 6)
        for x in data[0][1]:
            axes6.plot(x[2][1], data[1].values - x[2][0][:, 0], color="black", alpha=0.5)
        axes6.plot(data[0][1][data[0][0]][2][1], data[1].values - data[0][1][data[0][0]][2][0][:, 0], color="red", label="best x")
        axes6.set_title("S(t) - x(t)")
        axes6.set_xlabel("t")
        fd = defaultdict(list)
        for i, x in enumerate(data[0][1]):
            print(x[0])
            fd[x[0]].append(i)
        axes7 = fig.add_subplot(2, 4, 7)
        axes8 = fig.add_subplot(2, 4, 8)
        axes7.set_title("C1")
        axes7.set_xlabel("$\\beta$")
        axes8.set_title("C2")
        axes8.set_xlabel("$\\beta$")
        for col, (b_name, indexs) in enumerate(fd.items()):
            b = [x[1] for i, x in enumerate(data[0][1]) if i in indexs]
            c1 = [x[2][2] for i, x in enumerate(data[0][1]) if i in indexs]
            c2 = [x[2][3] for i, x in enumerate(data[0][1]) if i in indexs]
            print(b, c1, c2)
            axes7.scatter(b, c1, label=unicode_to_latex[b_name], color=colors[col])
            axes8.scatter(b, c2, label=unicode_to_latex[b_name], color=colors[col])
        axes7.legend()
        axes8.legend()

    plt.tight_layout()
    plt.show()


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
        plots_side = QWidget()
        self.plots_grid = QGridLayout()

        tabs = QTabWidget()
        grid.addWidget(QLabel('Messages'))
        grid.addWidget(plots_side, 2, 0, 1, 15)
        grid.addWidget(tabs, 1, 15, 2, 6)

        self.status_field = QListWidget()
        self.plots_grid.addWidget(self.status_field)

        self.manual_tab = QWidget()
        tabs.addTab(self.manual_tab, 'Manual Mode')
        self.auto_tab = QWidget()
        tabs.addTab(self.auto_tab, 'Auto Mode')

        self.init_auto_tab()
        self.init_manual_tab()

        plots_side.setLayout(self.plots_grid)
        self.setLayout(grid)

        self.resize(1600, 1200)
        self.center()
        self.setWindowTitle('Advertising Server')
        self.show()

    def init_manual_tab(self):
        self.manual_rho_file = None
        self.manual_z_file = None
        self.manual_S_file = None

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

        form.addRow(QLabel('Files'))
        self.manual_rho_file_button = QPushButton('Choose file')
        self.manual_S_file_button = QPushButton('Choose file')
        self.manual_z_file_button = QPushButton('Choose file')
        form.addRow(QLabel('\u03C1 file'), self.manual_rho_file_button)
        form.addRow(QLabel('S file'), self.manual_S_file_button)
        form.addRow(QLabel('z file'), self.manual_z_file_button)
        self.manual_rho_file_button.clicked.connect(lambda : self.file_button('rho', 1))
        self.manual_S_file_button.clicked.connect(lambda: self.file_button('S', 1))
        self.manual_z_file_button.clicked.connect(lambda: self.file_button('z', 1))
        self.manual_rho_is_file_button = QCheckBox('use \u03C1 file')
        self.manual_S_is_file_button = QCheckBox('use S file')
        self.manual_z_is_file_button = QCheckBox('use z file')
        checkbox_grid = QHBoxLayout()
        form.addRow(checkbox_grid)
        checkbox_grid.addWidget(self.manual_rho_is_file_button)
        checkbox_grid.addWidget(self.manual_S_is_file_button)
        checkbox_grid.addWidget(self.manual_z_is_file_button)

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
            qline.setValidator(QRegExpValidator(QRegExp('[+-]?\\d+[\\.]?\\d+')))
        self.manual_submit = QPushButton('Submit')
        self.manual_submit.clicked.connect(self.manual_submit_clicked)

        form.addRow(self.manual_submit)
        self.manual_x0.setText('0')
        self.manual_y0.setText('0')
        self.manual_z_e.setText('4')
        self.manual_z_f.setText('1')
        self.manual_S_c.setText('3')
        self.manual_S_d.setText('1')
        self.manual_T.setText('1')
        self.manual_rho_a.setText('6')
        self.manual_rho_b.setText('1')
        self.manual_beta.setText('0.01')
        self.manual_tab.setLayout(form)

    def init_auto_tab(self):
        self.auto_rho_file = None
        self.auto_z_file = None
        self.auto_S_file = None

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

        form.addRow(QLabel('Files'))
        self.auto_rho_file_button = QPushButton('Choose file')
        self.auto_S_file_button = QPushButton('Choose file')
        self.auto_z_file_button = QPushButton('Choose file')
        form.addRow(QLabel('\u03C1 file'), self.auto_rho_file_button)
        form.addRow(QLabel('S file'), self.auto_S_file_button)
        form.addRow(QLabel('z file'), self.auto_z_file_button)
        self.auto_rho_file_button.clicked.connect(lambda: self.file_button('rho', 0))
        self.auto_S_file_button.clicked.connect(lambda: self.file_button('S', 0))
        self.auto_z_file_button.clicked.connect(lambda: self.file_button('z', 0))

        self.auto_rho_is_file_button = QCheckBox('use \u03C1 file')
        self.auto_S_is_file_button = QCheckBox('use S file')
        self.auto_z_is_file_button = QCheckBox('use z file')
        checkbox_grid = QHBoxLayout()
        form.addRow(checkbox_grid)
        checkbox_grid.addWidget(self.auto_rho_is_file_button)
        checkbox_grid.addWidget(self.auto_S_is_file_button)
        checkbox_grid.addWidget(self.auto_z_is_file_button)

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
            qline.setValidator(QRegExpValidator(QRegExp('[+-]?\\d+[\\.]?\\d+')))

        self.auto_submit = QPushButton('Submit')
        self.auto_submit.clicked.connect(self.auto_submit_clicked)
        form.addRow(self.auto_submit)
        self.auto_x0.setText('0')
        self.auto_y0.setText('0')
        self.auto_z_e.setText('4')
        self.auto_z_f.setText('1')
        self.auto_S_c.setText('3')
        self.auto_S_d.setText('1')
        self.auto_T.setText('1')
        self.auto_rho_a.setText('6')
        self.auto_rho_b.setText('1')
        self.auto_beta_lower_bound.setText('0')
        self.auto_beta_upper_bound.setText('0.1')
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
        if not self._check_non_empty([self.manual_T,
                      self.manual_beta,
                      self.manual_x0,
                      self.manual_y0]):
            QMessageBox.about(self, 'Message', 'Some fields are empty')
            return
        
        parameters = {'T' : float(self.manual_T.text()),
                      'beta': float(self.manual_beta.text()),
                      'beta_function' : self.manual_combobox.currentText(),
                      'x0' : float(self.manual_x0.text()),
                      'y0' : float(self.manual_y0.text())
                      }

        if self.manual_rho_is_file_button.isChecked():
            parameters['rho_file'] = self.manual_rho_file
            if self.manual_rho_file is None:
                QMessageBox.about(self, 'Message', 'Some files aren\'t choosen')
                return
        else:
            if self.manual_rho_a.text() == '' or self.manual_rho_b.text() == '':
                QMessageBox.about(self, 'Message', 'Some fields are empty')
                return
            parameters['rho_a'] = float(self.manual_rho_a.text())
            parameters['rho_b'] = float(self.manual_rho_b.text())

        if self.manual_S_is_file_button.isChecked():
            parameters['S_file'] = self.manual_S_file
            if self.manual_S_file is None:
                QMessageBox.about(self, 'Message', 'Some files aren\'t choosen')
                return
        else:
            if self.manual_S_c.text() == '' or self.manual_S_d.text() == '':
                QMessageBox.about(self, 'Message', 'Some fields are empty')
                return
            parameters['S_c'] = float(self.manual_S_c.text())
            parameters['S_d'] = float(self.manual_S_d.text())

        if self.manual_z_is_file_button.isChecked():
            parameters['z_file'] = self.manual_z_file
            if self.manual_z_file is None:
                QMessageBox.about(self, 'Message', 'Some files aren\'t choosen')
                return
        else:
            if self.manual_z_e.text() == '' or self.manual_z_f.text() == '':
                QMessageBox.about(self, 'Message', 'Some fields are empty')
                return
            parameters['z_e'] = float(self.manual_z_e.text())
            parameters['z_f'] = float(self.manual_z_f.text())

        self.solver_thread = ComputationalThread(parameters, manual=True)
        self.manual_submit.setEnabled(False)
        self.auto_submit.setEnabled(False)
        self.solver_thread.finished.connect(self.done)
        #self.connect(self.solver_thread, SIGNAL("finished()"), self.done)
        self.solver_thread.status_trigger.connect(self.update_status)
        self.solver_thread.start()
        #main_solver(parameters, self, manual=True)

    def auto_submit_clicked(self):
        if not self._check_non_empty([self.auto_T,
                                      self.auto_beta_lower_bound,
                                      self.auto_beta_upper_bound,
                                      self.auto_x0,
                                      self.auto_y0]):
            QMessageBox.about(self, 'Message', 'Some fields are empty')
            return
        parameters = {'T': float(self.auto_T.text()),
                      'lower_beta': float(self.auto_beta_lower_bound.text()),
                      'upper_beta': float(self.auto_beta_upper_bound.text()),
                      'beta_function': self.auto_combobox.currentText(),
                      'x0': float(self.auto_x0.text()),
                      'y0': float(self.auto_y0.text())
                      }

        if self.auto_rho_is_file_button.isChecked():
            parameters['rho_file'] = self.auto_rho_file
            if self.auto_rho_file is None:
                QMessageBox.about(self, 'Message', 'Some files aren\'t choosen')
                return
        else:
            if self.auto_rho_a.text() == '' or self.auto_rho_b.text() == '':
                QMessageBox.about(self, 'Message', 'Some fields are empty')
                return
            parameters['rho_a'] = float(self.auto_rho_a.text())
            parameters['rho_b'] = float(self.auto_rho_b.text())

        if self.auto_S_is_file_button.isChecked():
            parameters['S_file'] = self.auto_S_file
            if self.auto_S_file is None:
                QMessageBox.about(self, 'Message', 'Some files aren\'t choosen')
                return
        else:
            if self.auto_S_c.text() == '' or self.auto_S_d.text() == '':
                QMessageBox.about(self, 'Message', 'Some fields are empty')
                return
            parameters['S_c'] = float(self.auto_S_c.text())
            parameters['S_d'] = float(self.auto_S_d.text())

        if self.auto_z_is_file_button.isChecked():
            parameters['z_file'] = self.auto_z_file
            if self.auto_z_file is None:
                QMessageBox.about(self, 'Message', 'Some files aren\'t choosen')
                return
        else:
            if self.auto_z_e.text() == '' or self.auto_z_f.text() == '':
                QMessageBox.about(self, 'Message', 'Some fields are empty')
                return
            parameters['z_e'] = float(self.auto_z_e.text())
            parameters['z_f'] = float(self.auto_z_f.text())

        self.solver_thread = ComputationalThread(parameters, manual=False)
        self.manual_submit.setEnabled(False)
        self.auto_submit.setEnabled(False)
        self.solver_thread.finished.connect(self.done)
        #self.connect(self.solver_thread, SIGNAL("finished()"), self.done)
        self.solver_thread.status_trigger.connect(self.update_status)
        self.solver_thread.start()
        ## main_solver(parameters, self, manual=False)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to exit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def done(self):
        plot_builder()
        self.manual_submit.setEnabled(True)
        self.auto_submit.setEnabled(True)

    def update_status(self, string):
        self.status_field.addItem(string)

    def file_button(self, name, manual):
        file_buttons = [{'z' : self.manual_z_file_button,
                         'S' : self.manual_S_file_button,
                         'rho' : self.manual_rho_file_button},
                        {'z': self.auto_z_file_button,
                         'S': self.auto_S_file_button,
                         'rho': self.auto_rho_file_button}]

        new_file = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        if new_file == '':
            new_file = None
        if manual:
            if name == 'z':
                self.manual_z_file = new_file
            elif name == 'S':
                self.manual_S_file = new_file
            else:
                self.manual_rho_file = new_file
        else:
            if name == 'z':
                self.auto_z_file = new_file
            elif name == 'S':
                self.auto_S_file = new_file
            else:
                self.auto_rho_file = new_file
        if new_file is None:
            file_buttons[1 - manual][name].setText('Choose file')
            return
        if len(new_file) > 30:
            new_file = '...' + new_file[-30:]
        file_buttons[1 - manual][name].setText(new_file)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
