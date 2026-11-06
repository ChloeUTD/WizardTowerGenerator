from maya import cmds
# import sys

# Make wizard tower class with 5 parameters.


class WizardTower():

    # Current order:
    # 1. Create base, 2. Apply materials, 3. clean up and merge
    def __init__(self, height=6, radius=1, windows=False,
                 roofcolor=[0, 0, 0], subspires=False):
        # Mesh parameter variables
        self.cylinder_height = height
        self.cylinder_radius = radius
        # Color parameter variable
        self.roof_color = roofcolor
        # Non parameter variables
        self.roof_height = self.cylinder_height / 2
        self.roof_radius = self.cylinder_radius * 2
        # Color non parameter variable
        self.wall_color = [0.463, 0.49, 0.522]

    def create(self):
        """This will run the other functions required to make the tower"""
        self.create_base()
        # Put roof color and wall color here
        self.create_roof_mat()
        self.create_tower_mat()
        self.clean_and_merge()

    def create_base(self):

        # This is what makes the basics of the tower. It will make a
        # cylinder and cone based on the default or given parameters.
        # It will then move the cone on top of the spire and group them
        # together.

        # Create Geometry
        # Since the geometry will be merged I don't think I need to worry
        # about conflicting part names
        cmds.polyCylinder(h=self.cylinder_height, r=self.cylinder_radius,
                          n="TowerBase")
        cmds.polyCone(h=self.roof_height, r=self.roof_radius, n="TowerRoof")
        # Move and group
        cmds.select("TowerBase")
        cmds.move(self.cylinder_height / 2, y=True)
        cmds.select("TowerRoof")
        cmds.move(self.cylinder_height + (self.roof_height / 2), y=True)
        # cmds.group(['TowerBase', 'TowerRoof'], name="TowerGeometry")

    def clean_and_merge(self):
        """Remove history and transforms after base is created and materials
        are applied. This will allow scaling to be done uniformly to the
        model"""
        # First use cmds.delete with ch=True to delete construction history.
        # Then use makeIdentity with apply, translate, rotate and scale all set
        # to true. Use polyUnite to combine the roof and base
        cmds.delete("TowerBase", "TowerRoof", ch=1)
        cmds.makeIdentity("TowerBase", apply=1, translate=1, rotate=1,
                          scale=1)
        cmds.makeIdentity("TowerRoof", apply=1, translate=1, rotate=1,
                          scale=1)
        # Run edit names to see if WizardTower is taken. If not, add
        # a variable that you get from what edit_names returns
        cmds.polyUnite("TowerBase", "TowerRoof", n="WizardTower")

    def edit_names(self):
        """This will run if an instance of WizardTower already exists so the
        code doesn't rely on one hard coded name"""
        # Plan: Check and see if there is an object named whatever the wizard
        # tower will be named after the objects are merged. Also maybe
        # create a self. variable so it can be referenced throughout the
        # class
        pass

    def create_roof_mat(self):

        # This will create a shader for the roof. It takes input
        # from the roofcolor parameter
        # cmds.color("pCube1", rgb=(1, 0, 0))
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

        # This will make the shader for the tower walls. It is not
        # editable
        shader = cmds.shadingNode('aiStandardSurface', asShader=1,
                                  name='wallMat')
        #
        cmds.setAttr((shader + '.baseColor'), self.wall_color[0],
                     self.wall_color[1], self.wall_color[2], type='double3')
        cmds.select('TowerBase')
        cmds.hyperShade(a=shader)

    def create_window_mat(self):

        # This will make the lambert for the windows. It is not editable
        pass

# newtest = WizardTower(roofcolor=[1, 0, 0])
# Example of how to set parameters in maya editor
