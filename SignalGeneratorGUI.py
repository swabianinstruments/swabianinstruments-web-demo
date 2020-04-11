import sys
import glob
from pathlib import Path
from importlib import util
from multiprocessing import Process
from threading import Thread
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTextEdit, QVBoxLayout
from pulsestreamer import findPulseStreamers

try:
    from pygments import highlight
    from pygments.lexers import Python3Lexer
    from pygments.formatters import HtmlFormatter
except Exception:
    pass

from SignalGenerator_ui import Ui_MainWindow


def load_file(name, path):
    """ Load python file as a module into a separate namespace """
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def start_example(py_file, ip):
    module = load_file('example', py_file)
    module.main(ip)



class SignalGeneratorGUI(QMainWindow):

    def __init__(self, scripts_dir='.'):
        super(SignalGeneratorGUI, self).__init__()
        self.scripts_dir = scripts_dir

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnStart.clicked.connect(self.btnStart_clicked)
        self.ui.btnStop.clicked.connect(self.btnStop_clicked)
        self.ui.btnSearchPS.clicked.connect(self.btnSearchPS_clicked)
        self.ui.btnShowCode.clicked.connect(self.btnShowCode_clicked)
        self.ui.lstConfiguration.itemClicked.connect(self.lstConfiguration_select)
        self.populateConfList()
        self.populatePulseStreamerList()

        self.example_process = None
        self.ui.btnStop.setEnabled(False)

    def populateConfList(self):
        """ Scan directory for script files and populate the list """
        self.ui.lstConfiguration.clear()
        for file_path in Path(self.scripts_dir).glob('*_PS*.py'):
            self.ui.lstConfiguration.addItem(file_path.name)
        self.ui.lstConfiguration.setCurrentRow(0)
        self.lstConfiguration_select(self.ui.lstConfiguration.currentItem())
        
    def populatePulseStreamerList(self):
        """ Search for Pulse Streamer devices and populate combobox """
        self.ui.cbxPSAddress.clear()
        ps_info = findPulseStreamers()
        addr_list = [ps[0] for ps in ps_info] 
        if len(addr_list) < 1:
            addr_list.append('169.254.8.2')
        self.ui.cbxPSAddress.addItems(addr_list)

    def active_example_path(self):
        fname = self.ui.lstConfiguration.currentItem().text()
        fpath = Path(self.scripts_dir, fname)
        return fpath

    def start_active_example(self):
        ip = self.ui.cbxPSAddress.currentText()

        def example_runner(obj, fpath, ip):
            obj.ui.btnStart.setEnabled(False)
            obj.ui.lstConfiguration.setEnabled(False)
            obj.ui.cbxPSAddress.setEnabled(False)
            obj.ui.btnSearchPS.setEnabled(False)
            obj.ui.btnStop.setEnabled(True)
            try:
                obj.example_process = Process(
                    target=start_example,
                    args=(fpath, ip))
                obj.example_process.start()
                obj.example_process.join()
            finally:
                obj.ui.btnStart.setEnabled(True)
                obj.ui.lstConfiguration.setEnabled(True)
                obj.ui.cbxPSAddress.setEnabled(True)
                obj.ui.btnSearchPS.setEnabled(True)
                obj.ui.btnStop.setEnabled(False)

        thr = Thread(
            target=example_runner, 
            args=(self, self.active_example_path(), ip),
            daemon=True
        )
        thr.start()

    def btnStart_clicked(self):
        self.start_active_example()

    def btnStop_clicked(self):
        if self.example_process.is_alive():
            self.example_process.terminate()

    def btnSearchPS_clicked(self):
        self.populatePulseStreamerList()

    def btnShowCode_clicked(self):
        self.codevw = CodeViewer(self.active_example_path())
        self.codevw.show()

    def lstConfiguration_select(self, item):
        fname = item.text()
        fpath = Path(self.scripts_dir, fname)
        example_module = load_file('example', fpath)
        self.ui.textDescription.setText(example_module.__doc__)



class CodeViewer(QDialog):

    def __init__(self, file_path):
        super(CodeViewer, self).__init__()

        self.setWindowTitle(f'Code: [{file_path}]')
        self.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.resize(800, 600)

        self.ui_text = QTextEdit(self)
        self.ui_text.setReadOnly(True)
        self.ui_text.setAcceptRichText(True)

        self.ui_layout = QVBoxLayout(self)
        self.ui_layout.addWidget(self.ui_text)
        self.setLayout(self.ui_layout)
        
        code_lexer = Python3Lexer()
        formatter = HtmlFormatter(style='colorful')
        self.ui_text.document().setDefaultStyleSheet(formatter.get_style_defs())

        code = Path(file_path).read_text()
        html = highlight(code, code_lexer, formatter)
        self.ui_text.setText(html)


def main():
    app = QApplication(sys.argv)
    window = SignalGeneratorGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()