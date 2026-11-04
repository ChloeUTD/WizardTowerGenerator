from maya import cmds

# Make wizard tower class with 5 parameters.


class WizardTower(height=6, radius=1, windows=False,
                  roofcolor="", subspires=False):

    # default height = 4, default radius = 1, windows are set to false
    # not editable but tower roof needs default radius of cylinder times
    # 2, and height should be cylinder height divided by 2. Height and
    # radius need to be floats.

    # I will need to make a gui element that can slide rgb values, but
    # that can be done later

    def create_base(self):

        # This is what makes the basics of the tower. It will make a
        # cylinder and cone based on the default or given parameters.
        # It will then moe the cone on top of the spire and group them
        # together.
        pass

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
