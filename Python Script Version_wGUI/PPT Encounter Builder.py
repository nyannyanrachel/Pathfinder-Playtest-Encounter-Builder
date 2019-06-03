from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys

from PPTEB_UI import Ui_MainWindow

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(640, 480)
        self.setWindowIcon(QtGui.QIcon('data/village icon.png'))

    # ______________________________________________________________________________________________________
    # This Section Contains the signal (event) handling and it's slots (function calls)

        # Party Level Slider
        self.ui.pl_slider.valueChanged[int].connect(self.setPartyLevel)

        # Party Size Slider
        self.ui.ps_slider.valueChanged[int].connect(self.setPartySize)

        # Severity Check Box
        # No Signal Handling Needed

        # Custom XP Budget Text Box
        # No Signal Handling Needed

        # Min/Max Sliders
        self.ui.min_slider.valueChanged[int].connect(self.setMin)
        self.ui.max_slider.valueChanged[int].connect(self.setMax)

        # Create/Close Buttons
        self.ui.create_btn.clicked.connect(self.okayClicked)
        self.ui.close_btn.clicked.connect(self.quitClicked)

    def setPartyLevel(self):
        self.ui.pl_slider_counter.setText(str(self.getPartyLevel()))

    def getPartyLevel(self):
        return self.ui.pl_slider.value()

    def setPartySize(self):
        self.ui.ps_slider_counter.setText(str(self.getPartySize()))

    def getPartySize(self):
        return self.ui.ps_slider.value()

    def getSeverity(self):
        return self.ui.severity_cb.currentText()

    def getCustomBudget(self):
        return self.ui.cb_line.text()

    def setMin(self):
        if self.getMin() > self.getMax():
            self.ui.max_slider_counter.setText(str(self.getMin()))
            self.ui.max_slider.setValue(self.getMin())
        self.ui.min_slider_counter.setText(str(self.getMin()))

    def getMin(self):
        return self.ui.min_slider.value()

    def setMax(self):
        if self.getMax() < self.getMin():
            self.ui.min_slider_counter.setText(str(self.getMax()))
            self.ui.min_slider.setValue(self.getMax())
        self.ui.max_slider_counter.setText(str(self.getMax()))

    def getMax(self):
        return self.ui.max_slider.value()

    def okayClicked(self):
        print("I clicked the okay button.")
        print("The Value of the PL Slider is: ", self.getPartyLevel())
        print("The Value of the PS Slider is: ", self.getPartySize())
        print("The Value of the Severity Combo Box is: ", self.getSeverity())
        print("The Value of the Line Text Box is: ", self.getCustomBudget())
        print("The Value of the Min Slider is: ", self.getMin())
        print("The Value of the Max Slider is: ", self.getMax())

    def quitClicked(self):
        print("Exiting Application")
        sys.exit(0)


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())
