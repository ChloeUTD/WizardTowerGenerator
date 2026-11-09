from maya import cmds
import random
from PySide6 import QtWidgets, QtGui, QtCore
from maya import OpenMayaUI as omui
from shiboken6 import wrapInstance


def get_maya_main_win():
    """Return the Maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window), QtWidgets.QWidget)


class WizardTower():

    def __init__(self, height=6, radius=1, brickrows=20,
                 brickcol=10, roofcolor=[0, 0, 0], roofheight=3,
                 roofradius=2):
        # Mesh parameter variables
        self.cylinder_height = height
        self.cylinder_radius = radius
        # Make sure rows and collumns are valid. If not, reset to default
        self.brick_rows = brickrows
        self.brick_col = brickcol
        # Color parameter variable
        self.roof_color = roofcolor
        # Non parameter variables
        self.roof_height = roofheight
        self.roof_radius = roofradius
        # Color non parameter variable
        self.wall_color = [0.463, 0.49, 0.522]

    def create(self):
        """This will run the other functions required to make the tower"""
        self.create_base()
        self.create_roof_mat()
        self.create_tower_mat()
        self.create_bricks()
        self.clean_and_merge()

    def create_base(self):
        """Create and move tower geometry"""
        # Create Geometry
        cmds.polyCylinder(h=self.cylinder_height, r=self.cylinder_radius,
                          n="TowerBase")
        cmds.polyCone(h=self.roof_height, r=self.roof_radius, n="TowerRoof")
        # Move and group
        cmds.select("TowerBase")
        cmds.move(self.cylinder_height / 2, y=True)
        cmds.select("TowerRoof")
        cmds.move(self.cylinder_height + (self.roof_height / 2), y=True)

    def clean_and_merge(self):
        """Remove history and transforms after base is created and materials
        are applied. This will allow scaling to be done uniformly to the
        model"""
        cmds.delete("TowerBase", "TowerRoof", ch=1)
        cmds.makeIdentity("TowerBase", apply=1, translate=1, rotate=1,
                          scale=1)
        cmds.makeIdentity("TowerRoof", apply=1, translate=1, rotate=1,
                          scale=1)
        cmds.polyUnite("TowerBase", "TowerRoof", n="WizardTower")
        cmds.delete("TowerBase", "TowerRoof")

    def create_roof_mat(self):

        """Create material for roof"""
        shader = cmds.shadingNode('aiStandardSurface', asShader=1,
                                  name='roofMat')
        # Color assign, rgb values are from 0-1
        rgb = []
        for value in self.roof_color:
            rgb.append(value)
        cmds.setAttr((shader + '.baseColor'), rgb[0], rgb[1], rgb[2],
                     type='double3')
        cmds.select('TowerRoof')
        cmds.hyperShade(a=shader)

    def create_tower_mat(self):
        """Create material for tower walls"""
        shader = cmds.shadingNode('aiStandardSurface', asShader=1,
                                  name='wallMat')
        cmds.setAttr((shader + '.baseColor'), self.wall_color[0],
                     self.wall_color[1], self.wall_color[2], type='double3')
        cmds.select('TowerBase')
        cmds.hyperShade(a=shader)

    def create_bricks(self):
        """Create wall bricks based on brick row and brick collumn
        parameters"""
        # Divide mesh.
        cmds.setAttr("polyCylinder1.subdivisionsAxis", self.brick_col)
        cmds.setAttr("polyCylinder1.subdivisionsHeight", self.brick_rows)
        cmds.setAttr("polyCylinder1.subdivisionsCaps", 0)
        # Count bricks
        count = 0
        faces_to_extrude = []
        for row in range(self.brick_rows):
            for col in range(self.brick_col):
                face_index = (row * self.brick_col) + col
                extrude_thickness = random.uniform(0.01, 0.05)
                mortar_gap = random.uniform(0.04, 0.07)
                # Adds each face to the list to be extruded
                faces_to_extrude.append(f"TowerBaseShape.f[{face_index}]")
                # Extrude Faces
                cmds.polyExtrudeFacet(faces_to_extrude[count], ch=1, kft=0,
                                      ls=(1.0 - mortar_gap, 1.0 - mortar_gap,
                                      1.0), ltz=extrude_thickness)
                count += 1

        cmds.select(clear=True)


class WizardWin(QtWidgets.QDialog):

    def __init__(self):
        """Construction"""
        super(WizardWin, self).__init__(parent=get_maya_main_win())
        self.setWindowTitle("Summon the spire!")
        self.resize(500, 500)
        self._define_widgets()
        self._define_color_elements()
        self._set_input_guidelines()
        self._layout_ui()
        self._apply_layout_param()
        self._apply_layout_color()
        self._connect_signals()

    def _connect_signals(self):
        """Link buttons to functions"""
        self.height_edit.editingFinished.connect(self._handle_input)
        self.radius_edit.editingFinished.connect(self._handle_input)
        self.brickrow_edit.editingFinished.connect(self._handle_input)
        self.brickcol_edit.editingFinished.connect(self._handle_input)
        self.roof_height_edit.editingFinished.connect(self._handle_input)
        self.roof_radius_edit.editingFinished.connect(self._handle_input)
        # Link create button to create tower function
        self.create_btn.clicked.connect(self._create_tower)

    def _define_widgets(self):
        """Define all the UI elements and widgets"""
        # Editable values
        self.height_edit = QtWidgets.QLineEdit("6")
        self.radius_edit = QtWidgets.QLineEdit("2")
        self.brickrow_edit = QtWidgets.QLineEdit("20")
        self.brickcol_edit = QtWidgets.QLineEdit("10")
        self.roof_height_edit = QtWidgets.QLineEdit("3")
        self.roof_radius_edit = QtWidgets.QLineEdit("4")
        # Create Button
        self.create_btn = QtWidgets.QPushButton("Create!")

    def _set_input_guidelines(self):
        """Ensure only compatible values are able to be entered"""
        # Input Masks
        self.height_edit.setInputMask("99")
        self.radius_edit.setInputMask("99")
        self.brickrow_edit.setInputMask("99")
        self.brickcol_edit.setInputMask("99")
        self.roof_height_edit.setInputMask("99")
        self.roof_radius_edit.setInputMask("99")

    def _handle_input(self):
        """Control input for the lineEdit variables"""
        # Convert user input to float
        self.height_input = float(self.height_edit.text())
        self.radius_input = float(self.radius_edit.text())
        self.brickrow_input = int(self.brickrow_edit.text())
        self.brickcol_input = int(self.brickcol_edit.text())
        self.roof_height_input = float(self.roof_height_edit.text())
        self.roof_radius_input = float(self.roof_radius_edit.text())

    def _layout_ui(self):
        """Layout UI elements and widgets"""
        # Layouts
        self.main_layout = QtWidgets.QVBoxLayout()
        self.controls_layout = QtWidgets.QVBoxLayout()
        self.form_layout_color = QtWidgets.QFormLayout()
        self.form_layout_param = QtWidgets.QFormLayout()
        self._handle_input()
        # Create Button
        self.main_layout.addWidget(self.create_btn)
        # Layout application
        self.setLayout(self.main_layout)

    def _apply_layout_param(self):
        """Apply and organize layout for parameters"""
        # Add rows to form layout param
        self.form_layout_param.addRow("Height:", self._create_row_layout_param(
                                      self.height_edit))
        self.form_layout_param.addRow("Radius:", self._create_row_layout_param(
                                      self.radius_edit))
        self.form_layout_param.addRow("Brick Rows:",
                                      self._create_row_layout_param(
                                       self.brickrow_edit))
        self.form_layout_param.addRow("Brick Collumns:",
                                      self._create_row_layout_param(
                                       self.brickcol_edit))
        self.form_layout_param.addRow("Roof Height:",
                                      self._create_row_layout_param(
                                       self.roof_height_edit))
        self.form_layout_param.addRow("Roof Radius:",
                                      self._create_row_layout_param(
                                       self.roof_radius_edit))
        # Make form_layout_param child of main_layout
        self.main_layout.addLayout(self.form_layout_param)

    def _apply_layout_color(self):
        """Apply and organize layout for colors"""
        # Add rows to form layout color
        self.form_layout_color.addRow("Red:", self._create_row_layout
                                      (self.r_slider, self.r_val_label))
        self.form_layout_color.addRow("Green:", self._create_row_layout(
                                self.g_slider, self.g_val_label))
        self.form_layout_color.addRow("Blue:", self._create_row_layout(
                                      self.b_slider, self.b_val_label))
        # Make form_layout_color child of controls_layout
        self.controls_layout.addLayout(self.form_layout_color)
        # Controls on left, preview on right
        self.main_layout.addLayout(self.controls_layout)
        self.main_layout.addWidget(self.preview_box,
        alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        # Connect signals so update triggers when sliders move
        self.r_slider.valueChanged.connect(self._update_color)
        self.g_slider.valueChanged.connect(self._update_color)
        self.b_slider.valueChanged.connect(self._update_color)
        self._update_color()

    def _define_color_elements(self):
        """Define components exclusive to color box"""
        # Box
        self.preview_box = QtWidgets.QLabel()
        self.preview_box.setFixedSize(100, 100)
        self.preview_box.setAutoFillBackground(True)
        # Sliders
        self.r_slider = self._create_color_slider()
        self.g_slider = self._create_color_slider()
        self.b_slider = self._create_color_slider()
        # Labels, shows current 0-1 values
        self.r_val_label = QtWidgets.QLabel("0.50")
        self.g_val_label = QtWidgets.QLabel("0.50")
        self.b_val_label = QtWidgets.QLabel("0.50")

    def _create_color_slider(self):
        """Create matching horizontal sliders"""
        slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(50)
        return slider

    def _create_row_layout(self, field, label):
        """Aligns slider next to its value text"""
        row = QtWidgets.QHBoxLayout()
        row.addWidget(field)
        row.addWidget(label)
        label.setFixedWidth(35)
        return row

    def _create_row_layout_param(self, field):
        """Create row layout for editable parameters"""
        row = QtWidgets.QHBoxLayout()
        row.addWidget(field)
        return row

    def _update_color(self):
        """Updates the color and text of label"""
        # Sliders
        self.r = self.r_slider.value() / 100.0
        self.g = self.g_slider.value() / 100.0
        self.b = self.b_slider.value() / 100.0
        # Text
        self.r_val_label.setText(f"{self.r:.2f}")
        self.g_val_label.setText(f"{self.g:.2f}")
        self.b_val_label.setText(f"{self.b:.2f}")
        # Apply color to preview window
        color = QtGui.QColor.fromRgbF(self.r, self.g, self.b)
        palette = self.preview_box.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, color)
        self.preview_box.setPalette(palette)

    def _create_tower(self):
        """Creates Wizard Tower when create button is pressed"""
        self._handle_input()
        new_tower = WizardTower(height=self.height_input,
                                radius=self.radius_input,
                                brickrows=self.brickrow_input,
                                brickcol=self.brickcol_input, roofcolor=[
                                self.r, self.g, self.b],
                                roofheight=self.roof_height_input,
                                roofradius=self.roof_radius_input)
        new_tower.create()
