from CellularAutomaton import CAGrid
import numpy
import math

import matplotlib


class HTGrid(CAGrid):
    """Class for 2D heat transfer simulations using cellular automaton"""

    IncludeDiagonalNeighbors = False

    def __new__(cls,shape, *args, tau=0.2, **kwargs):

        ni=CAGrid.__new__(cls,shape, *args, **kwargs)
        ni.tau=tau
        return ni

    def Update(self):
        #Calculate T_left + T_top + T_right + T_bottom - 4 T_node
        numpy.place(self.count,self.TrueArray,0)
        self.count = self.count - 4 * self['T']
        for n in self.Neighbors:
            self.count = self.count + n['T']

        #Multiply by tau
        self.count = self.tau * self.count

        #Add value of deltaT (count) to current value
        self['T'] += self.count
        self.SetBoundary()

    def SetBoundary(self):

        # copy the rows and columns.  These are views into the base created in __new__
        #  This simulation assumes adiabatic (or reflective) walls.
        numpy.copyto(self.BBottomRow, self.BottomRow)
        numpy.copyto(self.BLeftColumn, self.LeftColumn)
        numpy.copyto(self.BTopRow, self.TopRow)
        numpy.copyto(self.BRightColumn, self.RightColumn)

        # copy the corners
        # We don't need to do this for a HT simulation since the corners are not a neighbor
        #  to any real cell.
        #self.Base[0][0] = self[self.shape[0] - 1][self.shape[1] - 1]  # Set Top Left Corner
        #self.Base[0][self.Base.shape[1] - 1] = self[self.shape[0] - 1][0]  # Set Top    Right Corner
        #self.Base[self.Base.shape[0] - 1][self.Base.shape[1] - 1] = self[0][0]  # Set Bottom Right Corner
        #self.Base[self.Base.shape[0] - 1][0] = self[0][self.shape[1] - 1]  # Set Bottom Left Corner

def setrandomT(grid):
    a=100*numpy.random.random(grid.shape)
    numpy.copyto(grid["T"],a)
    grid.SetBoundary()

def HT_Test():


    print(matplotlib.__version__)
    MyDtype = numpy.dtype([('T','f')])
    rows = 3
    columns = 3
    MyGrid=HTGrid((rows,columns), MyDtype, tau=0.1)
    setrandomT(MyGrid)
    for n in range(60):
        print(n)
        print(MyGrid)
        MyGrid.Update()


#HT_Test()

def format_plot(a,ts):
    """Format a plot for presenation.  Function takes one parameter, a matplotlib.axes object."""

    goldenratio = 1 / 2 * (1 + math.sqrt(5))  # The next few lines are used for the size of plots
    fsx = 7  # Width (in inches) for the figures.
    fsy = fsx / goldenratio  # Height (in inches) for the figures.

    a.tick_params(labelsize=ts)
    a.xaxis.label.set_size(ts+2)
    a.yaxis.label.set_size(ts+2)
    a.title.set_size(ts+4)
    a.legend(fontsize=ts)
    a.get_figure().set_size_inches(fsx, fsy)
    a.grid(1)