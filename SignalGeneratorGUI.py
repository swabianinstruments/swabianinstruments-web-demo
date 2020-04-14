import sys
import glob
from pathlib import Path
from importlib import util
from multiprocessing import Process
from threading import Thread
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTextEdit, QVBoxLayout
from pulsestreamer import findPulseStreamers


def load_file(name, path):
    """ Load python file as a module into a separate namespace """
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def start_example(py_file, ip):
    module = load_file('example', py_file)
    module.main(ip)

def list_script_files(root_dir='.'):
    """Returns list of the script file paths"""
    return [fp.absolute() for fp in Path(root_dir).glob('*.py')]


class SignalGeneratorGUI(QMainWindow):

    def __init__(self, scripts_dir='emulated_signals'):
        super(SignalGeneratorGUI, self).__init__()
        self.scripts_dir = scripts_dir
        self.scripts = {}

        try:
            from SignalGenerator_ui import Ui_MainWindow        
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
        except ModuleNotFoundError:
            self.ui = uic.loadUi('SignalGenerator.ui', self)            

        self.ui.btnStart.clicked.connect(self.btnStart_clicked)
        self.ui.btnStop.clicked.connect(self.btnStop_clicked)
        self.ui.btnSearchPS.clicked.connect(self.btnSearchPS_clicked)
        self.ui.btnShowCode.clicked.connect(self.btnShowCode_clicked)
        self.ui.lstConfiguration.itemSelectionChanged.connect(self.lstConfiguration_select)
        self.refreshPulseStreamerList()
        self.refreshScriptsList()

        self.example_process = None
        self.ui.btnStop.setEnabled(False)
    
    def _read_LABEL(self, module):
        try:
            label = getattr(module, 'NAME')
        except AttributeError:
            print(f'Example file "{module.__file__}"')
            print('  Has no "NAME" variable at the module level.')
            print('  Define the "NAME" variable to provide custom list entry label.')
            label = Path(module.__file__).name
        return label
    
    def _read_DESCR(self, module):
        try:
            descr = getattr(module, 'DESCR')
        except AttributeError:
            descr = 'This example provides no description.'
            print(f'Example file "{module.__file__}"')
            print('  Has no "DESCR" variable at the module level.')
            print('  Define "DESCR" variable to provide example description.')
        return descr
    
    def refreshScriptsList(self):
        """ Scan directory for script files and populate the list """
        self.ui.lstConfiguration.clear()
        self.scripts = {}
        for file_path in list_script_files(self.scripts_dir):
            module = load_file('example', file_path)
            label = self._read_LABEL(module)
            self.scripts[label] = file_path
            self.ui.lstConfiguration.addItem(label)
            del module
        self.ui.lstConfiguration.setCurrentRow(0)
        self.lstConfiguration_select(self.ui.lstConfiguration.currentItem())
        
    def refreshPulseStreamerList(self):
        """ Search for Pulse Streamer devices and populate combobox """
        self.ui.cbxPSAddress.clear()
        ps_info = findPulseStreamers()
        addr_list = [ps[0] for ps in ps_info] 
        if len(addr_list) < 1:
            addr_list.append('169.254.8.2')
        self.ui.cbxPSAddress.addItems(addr_list)

    @property
    def selectedExample(self):
        return self.ui.lstConfiguration.currentItem().text()

    def start_example(self, example_label):
        """ Start example idensitified by the 'example_label' """
        
        def example_runner(obj, fpath, ip):
            """ This function is running in a separate thread"""
            try:
                # Set enable state of the widgets
                obj.ui.btnStart.setEnabled(False)
                obj.ui.lstConfiguration.setEnabled(False)
                obj.ui.cbxPSAddress.setEnabled(False)
                obj.ui.btnSearchPS.setEnabled(False)
                obj.ui.btnStop.setEnabled(True)
                
                # The example is started is aseparate subprocess
                obj.example_process = Process(
                    target=start_example,
                    args=(fpath, ip))
                obj.example_process.start()
                obj.example_process.join()  # Here we block until process is alive
            finally:
                # Restore enable state of the widgets
                obj.ui.btnStart.setEnabled(True)
                obj.ui.lstConfiguration.setEnabled(True)
                obj.ui.cbxPSAddress.setEnabled(True)
                obj.ui.btnSearchPS.setEnabled(True)
                obj.ui.btnStop.setEnabled(False)

        ip = self.ui.cbxPSAddress.currentText()
        example_path = self.scripts[example_label]
        thr = Thread(
            target=example_runner, 
            args=(self, example_path, ip),
            daemon=True
        )
        thr.start()

    def btnStart_clicked(self):
        self.start_example(self.selectedExample)

    def btnStop_clicked(self):
        # Terminate subprocess. This will also exit the example thread
        if self.example_process.is_alive():
            self.example_process.terminate()

    def btnSearchPS_clicked(self):
        self.refreshPulseStreamerList()

    def btnShowCode_clicked(self):
        example_path = self.scripts[self.selectedExample]
        self.codevw = CodeViewer(example_path)
        self.codevw.show()

    def lstConfiguration_select(self, *args):
        items = self.ui.lstConfiguration.selectedItems()
        if len(items) == 0:
            return
        label = items[0].text()
        fpath = self.scripts[label]
        module = load_file('example', fpath)
        descr = self._read_DESCR(module)
        del module
        try:
            from markdown import markdown
            self.ui.textDescription.setHtml(markdown(descr))
        except ModuleNotFoundError:
            print('Install markdown module to render the description as Markdown')
            print('  pip install markdown')
            self.ui.textDescription.setText(descr)


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
                
        code = Path(file_path).read_text()

        try:
            from pygments import highlight
            from pygments.lexers import Python3Lexer
            from pygments.formatters import HtmlFormatter
            code_lexer = Python3Lexer()
            formatter = HtmlFormatter(style='colorful')
            self.ui_text.document().setDefaultStyleSheet(formatter.get_style_defs())
            html = highlight(code, code_lexer, formatter)
            self.ui_text.setText(html)
            
        except ModuleNotFoundError:
            self.ui_text.setText(code)
            print('No "pygments" module found. Please install pygments to enable code highlighting.')
            print('   pip install pygments')
        

def main():
    app = QApplication(sys.argv)
    window = SignalGeneratorGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()