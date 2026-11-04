from maya import cmds
import sys

# Make wizard tower class with 5 parameters.


class WizardTower():

    # default height = 4, default radius = 1, windows are set to false
    # not editable but tower roof needs default radius of cylinder times
    # 2, and height should be cylinder height divided by 2. Height and
    # radius need to be floats.
    # I will need to make a gui element that can slide rgb values, but
    # that can be done later
    def __init__(self, height=6, radius=1, windows=False,
                 roofcolor="", subspires=False):
        # Mesh parameter variables
        self.cylinder_height = height
        self.cylinder_radius = radius
        # Non parameter variables
        self.roof_height = self.cylinder_height / 2
        self.roof_radius = self.cylinder_radius * 2

    def create_base(self):

        # This is what makes the basics of the tower. It will make a
        # cylinder and cone based on the default or given parameters.
        # It will then moe the cone on top of the spire and group themS
        # together.

        # Create Geometry
        cmds.polyCylinder(h=self.cylinder_height, r=self.cylinder_radius,
                          n="TowerBase")
        cmds.polyCone(h=self.roof_height, r=self.roof_radius, n="TowerRoof")
        # Move and group
        cmds.select("TowerBase")
        cmds.move(self.cylinder_height / 2, y=True)
        cmds.select("TowerRoof")
        cmds.move(self.cylinder_height + (self.roof_height / 2), y=True)
        cmds.group(['TowerBase', 'TowerRoof'], name="TowerGeometry")

    def create_roof_mat(self):

        # This will create a lambert shader for the roof. It takes input
        # from the roofcolor parameter
        pass

    def create_tower_mat(self):

        # This will make the lambert for the tower walls. It is not
        # editable
        pass

    def create_window_mat(self):

        # This will make the lambert for the windows. It is not editable
        pass
