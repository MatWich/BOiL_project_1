import numpy as np

class Grid:
    def __init__(self, dataFromForm=None):           # data user provides
        self.providers = np.zeros(2)            # Provider stuff
        self.suppliers = np.zeros(2)            # Supplier stuff
        self.grid = np.zeros((2, 2))            # later filled up with Nodes
        self.alfa = [0, 0, 0, 0]
        self.beta = [0, 0, 0, 0]
        self.optCheckGrid = np.zeros((2, 2))
        self.data = dataFromForm

        self.earn = 0                           # zysk

        self.set_up()

    def set_up(self):
        self.optCheckGrid[0] = -1

    def calc_primary_delivery_plan(self):
        pass

    # next iterations
    def optimize(self):
        if self.is_optimized():
            return self.grid, self.earn            # I guess this is what we have to show
        else:
            pass
        """If not start optimize"""

    # loops the optCheckGrid if it finds positive number returns true
    def is_optimized(self):
        return True if self.optCheckGrid.min() < 0 else False

