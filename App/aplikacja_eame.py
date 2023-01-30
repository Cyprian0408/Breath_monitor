import sys, os
from datetime import datetime
from PyQt6.QtCore import QDate, QTime, QDateTime, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction
import Functions



#-----funkcja pomocnicza do kompilacji UI i import formatki graficznej mainwindow.ui-----#
def compileUi(src_file, dst_file):
	from PyQt6.uic import compileUi
	src_fileh = open(os.path.dirname(__file__)+'/'+src_file, 'r')
	dst_fileh = open(os.path.dirname(__file__)+'/'+dst_file, 'w')
	compileUi(src_fileh, dst_fileh)
	src_fileh.close()
	dst_fileh.close()

compileUi('mainwindow.ui', 'mainwindow_ui.py')
from mainwindow_ui import Ui_MainWindow
#-----funkcja pomocnicza do kompilacji UI i import formatki graficznej mainwindow.ui-----#

isEmpty = 0

#-----klasa GUI / glowne okno-----#
class MainWindow(QMainWindow, Ui_MainWindow):

	#---konstruktor---#
	def __init__(self, *args, obj=None, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setupUi(self)

		self.label_lbl.setText(datetime.now().strftime("%H:%M:%S"))
		self.statusBar().showMessage('Aktualny czas: %s' % datetime.now().strftime("%H:%M:%S"))

		self.menuOpenFile = QAction('Otwórz plik', self)
		self.menuOpenFile.triggered.connect(self.obslLoadFile)
		self.menuPlik.addAction(self.menuOpenFile)

		self.menuHelpAbout = QAction('Informacje o projekcie', self)
		self.menuHelpAbout.triggered.connect(self.obslMenuHelpAbout)
		self.menupomoc.addAction(self.menuHelpAbout)

		self.startButton.clicked.connect(self.obslLoadAnalysis)

	#---konstruktor---#


	#---obsluga LOAD ANALYSIS---#
	def obslLoadAnalysis(self):

		global isEmpty
		if isEmpty != 0:	
			isEmpty = 0
			time=Functions.calculate_time()
			#tworzenie wykresów 
			Functions.plot_graphs(Functions.X_axis,Functions.Y_axis,Functions.Z_axis)
			text="Badanie trwało "+str(time)+" sekund i pobrano w tym czasie "+str(len(Functions.X_axis))+" próbek"
			self.textBrowser_Analysis.setText(text)
			Functions.breaths_per_minute()
			self.textBrowser.setText(str(Functions.breaths_per_minute_x))
			self.textBrowser_2.setText(str)((Functions.breaths_per_minute_y))	
	#---obsluga LOAD ANALYSIS---#

	#---obsluga LOAD FILE---#
	def obslLoadFile(self):

		fname = QFileDialog.getOpenFileName(self, 'Open file', os.path.dirname(__file__), "Text files (*.txt)")

		if fname[0] != '' :
			global isEmpty
			isEmpty = 1
			self.statusBar().showMessage('Otwieram plik: %s' % fname[0])
			fhook = open(fname[0], 'r')
			fcont = fhook.read()
			Functions.read_file(fname[0])

	#---obsluga LOAD FILE---#

	#---obsluga menu plik / about---#
	def obslMenuHelpAbout(self):

		okienko = QMessageBox()
		okienko.setStyleSheet('QLabel{min-width: 500px;}');
		okienko.setWindowTitle('Informacje o projekcie')
		okienko.setText('Projekt realizowany w ramach przedmiotu Elektroniczna Aparatura Medyczna.\nUrządzenie do analizy oddechu akcelerometrem. \n'
										'Autorzy: Cyprian Galicki, Ewa Mergo, Karolina Olszewska, Mikołaj Prażmo\nProwadzący: mgr inż. Krzysztof Dygnarowicz')
		okienko.exec()
	#---obsluga menu plik / about---#
	
#-----klasa GUI / glowne okno-----#

#-----"main"-----#
if __name__ == '__main__':

	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()
#-----"main"-----#
