import pandas as pd
import os

from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys

from PPTEB_UI import Ui_MainWindow

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

# __________This section contains all of the background setup__________

# Load the bestiary database
bestiary = pd.read_csv('data/bestiary.csv')

# Set the baseline encounter xp values.
BUDGETS = {'Trivial': [40, 10], 'Low': [60, 15], 'High': [80, 20], 'Severe': [120, 30], 'Extreme': [160, 40]}


# __________This section contains the Algorithm that powers the encounter builder__________

# This global variable is the master list that contains all of the encounters.
encounter_list = []


# This function does most of the heavy lifting.
# Input:
#     catalogue: The bestiary an all of their associated xp values.
#            xp: The experience budget to dictate how many monsters can fit in a given encounter.
#   party_level: The party's level. Used in finding the xp value of a creature relative to the party's level.
#         max_c: The maxmimum amount of creatures allowed in an encounter.
#         min_c: The minimum amount of creatures allowed in an encounter.
#     encounter: (Optional) This contains the current encounter being worked on. Initially starts as empty but
#                           is filled during recursive calls.
# Returns:
#          None
# This function takes a series of parameters to build an encounter and append it to a global list of possible encounters
# Using recursion, it finds creatures in the bestiary that contain xp values less than the budget and adds it as a leaf
# node in the encounter tree. Then it attempts to recurse and add a new leaf node if there is more xp budget and there
# is enough space left in the encounter. If neither of those conditions are met, it publishes the current encounter to
# the global list an removes the leaf node to try a new one.
def find_creature(catalogue, xp, party_level, max_c, min_c, encounter=[]):
    # Base Case
    # The xp budget is 0 therefore no new leaf nodes can be added. Immediately publish the current encounter.
    if xp < 10:
        publish(encounter.copy())

    # Otherwise iterate through the whole list of monsters to find appropriate children
    else:
        # Loop through every monster
        for index, row in catalogue.iterrows():
            # Check to see if we can afford the xp cost of the current monster.
            if int(row[str(party_level)]) <= xp:
                encounter.append(
                    row['CREATURE NAME'])  # We can afford it so add it as a leaf node to the encounter tree.
                newBudget = xp - int(row[str(party_level)])  # Calcualte the remaining budget.
                if len(encounter) < max_c:  # If we still have space in the encounter, recursively call and
                    # attempt to find a new monster that we can afford.
                    find_creature(catalogue, newBudget, party_level, max_c, min_c, encounter)

                # Once we have used up the budget we can publish.
                # This works because if we haven't added anything to the encounter then we can publish what we have.
                # If it did add something to the encounter however, that level's recursive call will handle the
                # publishing.

                if len(encounter) >= min_c:  # If the encounter meets the minimum monster count we can publish.
                    publish(encounter.copy())
                del encounter[-1]  # After publishing the encounter we want to remove the leaf that was used and
                # so that we can try a new one.


# This is a helper function to publish an encounter to the encounter list.
# Input:
#   current_enc: Contains the encounter to be published in list form.
# Returns:
#          None
def publish(current_enc):
    global encounter_list
    if len(current_enc) > 0:  # Check to make sure we aren't publishing an empty list.
        if current_enc not in encounter_list:  # Also make sure that we don't publish something that's already there.
            encounter_list.append(current_enc)


# This is the driver function that's called from the main body.
# Input:
#   party_level: The party's level. Used in finding the xp value of a creature relative to the party's level.
#    party_size: The size of the party. Used in conjunction with the severity to calculate the XP budget.
#      severity: Used with the party size to calculate the XP budget in the event a budget is not provided.
#         max_c: The maxmimum amount of creatures allowed in an encounter.
#         min_c: The minimum amount of creatures allowed in an encounter.
#        budget: A manually input XP budget.
# Returns:
#          None
def build_encounters(party_level, party_size, severity, max_c, min_c, budget):
    print("Build Encounters")
    global encounter_list
    # First, calcualte total encounter budget.
    if budget > 0:
        XP_Budget = budget
    else:
        if party_size > 4:
            XP_Budget = BUDGETS[severity][0] + (BUDGETS[severity][1] * (party_size - 4))
        elif party_size < 4:
            XP_Budget = BUDGETS[severity][0] - (BUDGETS[severity][1] * (4 - party_size))
        else:
            XP_Budget = BUDGETS[severity][0]
    print("Budget Calculated")
    # Next, consult the database and get the XP values for each creature based on the specified level.
    xp_costs = bestiary[['CREATURE NAME', str(party_level)]]  # Get the cost for all creatures.
    nontrivial_xp_costs = xp_costs[xp_costs[str(party_level)] != '-']  # Remove all creatures of trivial difficulty.
    pruned_xp_costs = nontrivial_xp_costs[nontrivial_xp_costs[str(party_level)] != 'X']  # Remove all creatures of impossible difficulty.
    print("Built the pruned monster list")

    print("Finding All Encounters")
    # Now that we have the creatures and how much they cost, build all possible encounters.
    find_creature(pruned_xp_costs, XP_Budget, party_level, max_c, min_c)  # This function does most of the heavy lifting
    print("Found All Encounters")
    # and builds the encounter list into a global variable.
    temp_enc_list = encounter_list.copy()  # Copy the encounters list into a temporary value to return
    encounter_list = []  # Scrub the global encounters list clean so that it can be ready for another
    # query.
    return temp_enc_list  # Return the copy of the list.


# Testing Function
# Build an High threat encounter for a party of 4 level 1 adventurers with a max of five monsters and a minimum of one.
# XP Budget: 80
#test = build_encounters(1, 4, 'High', 5, 1, 0)

#print("Test Encounters: ", test)

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
        if self.ui.cb_line.text() == '':
            return 0
        else:
            try:
                return int(self.ui.cb_line.text())
            except:
                return 0

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
        # print("I clicked the okay button.")
        # print("The Value of the PL Slider is: ", self.getPartyLevel())
        # print("The Value of the PS Slider is: ", self.getPartySize())
        # print("The Value of the Severity Combo Box is: ", self.getSeverity())
        # print("The Value of the Line Text Box is: ", self.getCustomBudget())
        # print("The Value of the Min Slider is: ", self.getMin())
        # print("The Value of the Max Slider is: ", self.getMax())
        print('Working...')
        solution = build_encounters(self.getPartyLevel(),
                                      self.getPartySize(),
                                      self.getSeverity(),
                                      self.getMax(),
                                      self.getMin(),
                                      self.getCustomBudget())
        #print("Encounters: ")
        #print(solution)

        directory = './output'
        if not os.path.exists(directory):
            os.mkdir(directory)
        filename = 'PL-' + str(self.getPartyLevel()) + '_PS-' + str(self.getPartySize()) + '_SEV-'
        filename = filename + self.getSeverity() + '_MIN-' + str(self.getMin()) + '_Max-' + str(self.getMax())
        filename = filename + '_CB-' + str(self.getCustomBudget()) + '.csv'

        filename = os.path.join(directory, filename)
        print("Attempting to save file to: ", filename)
        df = pd.DataFrame(solution)
        # print("Number of Columns: ",len(df.columns))
        columnNames = []
        for col in df.columns:
            columnNames.append('Monster ' + str(col + 1))
        df.columns = columnNames
        df.to_csv(filename, index=False)
        print('Encounters saved to file: ', filename)

    def quitClicked(self):
        print("Exiting Application")
        sys.exit(0)


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())
