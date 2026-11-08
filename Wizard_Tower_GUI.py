from PySide6 import QtWidgets
from maya import OpenMayaUI as omui
from shiboken6 import wrapInstance
# from Wizard_Tower_Generator import WizardTower


def get_maya_main_win():
    """Return the Maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window), QtWidgets.QWidget)


class WizardWin(QtWidgets.QDialog):

    def __init__(self):
        """Construction"""
        super(WizardWin, self).__init__(parent=get_maya_main_win())
        self.setWindowTitle("Summon the spire!")
        self.resize(500, 500)
        self._define_widgets()
        self._set_input_guidelines()
        self._layout_ui()

    def _define_widgets(self):
        """Define all the UI elements and widgets"""
        # Create 4 widgets, height, radius, brickrows, brickcollumns
        # All are simple with a label and box to input a number. Use inputMask
        # on QLineEdit with mask character set to 9 to require character of
        # number category. Also add a create button that will create the tower
        # when finished.
        # Labels
        self.height_label = QtWidgets.QLabel("Height:")
        self.radius_label = QtWidgets.QLabel("Radius:")
        self.brickrow_label = QtWidgets.QLabel("Brick Rows:")
        self.brickcol_label = QtWidgets.QLabel("Brick Col:")
        # Editable values
        self.height_edit = QtWidgets.QLineEdit()
        self.radius_edit = QtWidgets.QLineEdit()
        self.brickrow_edit = QtWidgets.QLineEdit()
        self.brickcol_edit = QtWidgets.QLineEdit()
        # Create Button
        self.create_btn = QtWidgets.QPushButton("Create!")

    def _set_input_guidelines(self):
        """Ensure only compatible values are able to be entered"""
        # Input Masks
        self.height_edit.setInputMask("99.99")
        self.radius_edit.setInputMask("99.99")
        self.brickrow_edit.setInputMask("99.99")
        self.brickcol_edit.setInputMask("99.99")

    def _layout_ui(self):
        """Layout UI elements and widgets"""
        # Labels
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.height_label)
        self.main_layout.addWidget(self.radius_label)
        self.main_layout.addWidget(self.brickrow_label)
        self.main_layout.addWidget(self.brickcol_label)
        # Editable Values
        self.main_layout.addWidget(self.height_edit)
        self.main_layout.addWidget(self.radius_edit)
        self.main_layout.addWidget(self.brickrow_edit)
        self.main_layout.addWidget(self.brickcol_edit)
        # Create Button
        self.main_layout.addWidget(self.create_btn)
        self.setLayout(self.main_layout)
