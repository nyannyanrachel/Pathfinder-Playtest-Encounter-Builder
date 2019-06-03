from PyQt5 import QtWidgets, uic
import sys

from PPTEB_UI import Ui_MainWindow


class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.okay_button.clicked.connect(self.okayClicked)
        self.ui.cancel_button.clicked.connect(self.quitClicked)

    def okayClicked(self):
        print("I clicked the okay button.")
        print("The Radio Button is Clicked: ", self.ui.radioButton.isChecked())
        print("Slider Value: ", self.ui.horizontalSlider.value())

    def quitClicked(self):
        print("Exiting Application")
        sys.exit(0)


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())
