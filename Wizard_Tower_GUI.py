from PySide6 import QtWidgets
# from Wizard_Tower_Generator import WizardTower


class WizardWin(QtWidgets.QDialog):

    def __init__(self):
        """Construction"""
        super(WizardWin, self).__init__()
        self.setWindowTitle("Summon the spire!")
        self.resize(500, 500)

