from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, os, subprocess

from core import Search

class index(QDialog):
	def __init__(self, parent=None):
		super(index, self).__init__(parent)

		self.setWindowTitle("Translator")

		hbox = QHBoxLayout()

		languages = ["Português Brasileiro", "Inglês", "Espanhol"]
		informedic = QLabel("Dicionario contido neste servico:")
		self.label_from = QLabel("From:")
		self.text_from = QTextEdit()
		self.choices_from = QLabel("Auto-detectable language.")
		button_change = QPushButton("Change fields [Ctrl+Tab]")

		layout_change_languages = QHBoxLayout()
		layout_change_languages.addWidget(self.choices_from)
		layout_change_languages.addWidget(button_change)

		self.label_to = QLabel("To:")
		self.text_to = QTextEdit()
		self.choices_to = QComboBox()
		self.choices_to.addItems(languages)

		from_layout = QVBoxLayout()
		from_layout.addWidget(self.label_from)
		from_layout.addWidget(self.text_from)
		from_layout.addLayout(layout_change_languages)

		to_layout = QVBoxLayout()
		to_layout.addWidget(self.label_to)
		to_layout.addWidget(self.text_to)
		to_layout.addWidget(self.choices_to)

		all_layouts = QHBoxLayout()
		all_layouts.addLayout(from_layout)
		all_layouts.addLayout(to_layout)

		vbox = QVBoxLayout()
		vbox.addLayout(all_layouts)

		button_search = QPushButton("Translate! [Ctrl+Enter]")


		self.progress = QProgressBar(self)

		vbox1 = QVBoxLayout()
		vbox1.addLayout(hbox)
		vbox1.addLayout(vbox)
		vbox1.addWidget(self.progress)
		vbox1.addWidget(button_search)

		self.setLayout(vbox1)


		# Signals
		self.connect(button_search, SIGNAL("clicked()"), self.search)
		self.connect(button_change, SIGNAL("clicked()"), self.change_fields)
		shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
		shortcut2 = QShortcut(QKeySequence("Ctrl+Tab"), self)
		shortcut.activated.connect(self.search) 
		shortcut2.activated.connect(self.change_fields)

		self.setWindowFlags(Qt.Window) 
		self.setGeometry(300,100,700,430)

	def search(self):
		'''
		Search to translate.
		'''
		self.text_to.setDisabled(True)

		self.completed = 0

		while self.completed < 80:
			self.completed += 0.001
			self.progress.setValue(self.completed)

		instance_translate = Search(self.text_from.toPlainText(), self.choices_to.currentText())
		result = instance_translate.translate_txt()
		self.choices_from.setText("Language detected: {}".format(result.src))
		self.text_to.setText(result.text)
		self.text_from.setText(instance_translate.fix_text_from_paper())
		self.progress.setValue(100)
		self.text_to.setDisabled(False)

	def change_fields(self):
		temporary_text = self.text_to.toPlainText()
		self.text_to.setText(self.text_from.toPlainText())
		self.text_from.setText(temporary_text)


app = QApplication(sys.argv)
dlg = index()
dlg.show()
sys.exit(dlg.exec_())