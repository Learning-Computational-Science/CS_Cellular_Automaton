import numpy


class Cell:
    """Cell is an object for cellular automaton simulations (especially game of life simulations).

    The cell object will keep track of its state, neighbors and update itself when update is called.
    This object is for the cell only.  It does not create an entire grid, nor can it determine what
    its neighbors are.

    Class variables:
        These are the same for all instances of the class.

        ProbInitialTrue = 0.5   ->  Used in __init__ to determine if the cell is initialized to
                                    True or False.

    Instance Variables (or Data Attributes):
        These are unique for each instance of the class.

        .state          ->  In the game of life, this tracks if the cell is 'alive' or 'dead.'
        .value          ->  Python expects this attribute to be returned in various cases.
        .Neighbors[]    ->  List of cell neighbors.  This list is used by update to know where to
                            check values.  This list must be set before calls to update.
                            This class provides no functionality for calculating the neighbors.
        .OldState       ->  Used in update to store the cell value from the previous time step.
                            This enables all cells to calculate their new state based on values
                            from the previous time step.
        .UpdateCount    ->  Number of times .update has completed.

    Methods:
        These are the functions of the class.
        update          ->  Calculates and sets cell value for the single timestep.
                            It calculates .state and updates .value.
                            This method does not modify .OldState
    Helper Functions:
        While it is not a member of this class, in this file there are two helper functions:

        SetNeighbors sets the neighbor values for all cells in a grid.
        SetOldStates sets .OldState = .State for  all cells in a grid.
        """

    ProbInitialTrue = 0.6

    def __init__(self, state=None, neighbors=None):
        if state is None:
            if numpy.random.rand() <= Cell.ProbInitialTrue:
                self.state = True
            else:
                self.state = False
        else:
            self.state = state
        if neighbors is None:
            self.Neighbors = []
        else:
            self.Neighbors = neighbors
        self.__set_value()
        self.OldState = self.state
        self.UpdateCount = 0

    def __str__(self):    # instead, we should really define __getitem__(self,i) which is called for x[i]
        return self.value.__str__()

    def __getitem__(self,i):
        return self[i].value

    def __repr__(self):
        return self.value.__str__()

    def update(self):
        c = 0
        for n in self.Neighbors:
            if n.OldState:                # This needs changed to old state
                c += 1
        if c > 3:
            self.state = False
        elif c == 3:
            self.state = True
        # if c = 2, don't change state.
        elif c == 1:
            self.state = False
        elif c == 0:
            self.state = False
        self.UpdateCount += 1
        self.__set_value()

    def __set_value(self):
        # self.value=self.state
        if self.state:
            self.value = 1
        else:
            self.value = 0

    def set_value(self):
        self.__set_value()

def SetOldStates(grid):
    """Function sets .OldState = .State for each cell in grid

        grid    ->  2D list of cells"""


    for row in grid:
        for c in row:
            c.OldState = c.state


def SetNeighbors(grid, columns, rows, IncludeDiagonalNeighbors=True):
    """Sets the neighbors for Cells in a 2D list.

    grid    ->  2D list of cells with dimensions columns x rows
    columns ->  Number of  columns in the simulation grid
    rows    ->  Number of rows in the simulation grid
    IncludeDiagonalNeighbors = (True by default)
                States if the neighbor lists should include:
                    just the 4 nearest neighbors (IncludeDiagonalNeighbors=False)
                    the 4 nearest neighbors and the 4 catty-corner cells (IncludeDiagonalNeighbors=True)
    """
    LastColumn = columns - 1
    LastRow = rows - 1

    for y in range(rows):
        for x in range(columns):
            grid[y][x].Neighbors[:]=[] #Clear the neighbor list

            # Find the indexes for right, left, top, bottom
            # to the right
            if x == LastColumn:
                r = 0
            else:
                r = x + 1
            # to the left
            if x == 0:
                l=LastColumn
            else:
                l = x-1
            # to the top
            if y == 0:
                t=LastRow
            else:
                t=y-1
            # to the bottom
            if y == LastRow:
                b=0
            else:
                b=y + 1

            grid[y][x].Neighbors.append(grid[y][r])  #right
            grid[y][x].Neighbors.append(grid[y][l])  #left
            grid[y][x].Neighbors.append(grid[t][x])  #top
            grid[y][x].Neighbors.append(grid[b][x])  #bottom
            if IncludeDiagonalNeighbors:
                grid[y][x].Neighbors.append(grid[t][r])  # top right
                grid[y][x].Neighbors.append(grid[t][l])  # top left
                grid[y][x].Neighbors.append(grid[b][r])  # bottom right
                grid[y][x].Neighbors.append(grid[b][l])  # bottom left


class CAGrid(numpy.ndarray):
    """Class for implementing cellular automaton grid simulations.

    Provides a framework for implementing 2D cellular automaton (CA) simulations using NumPy arrays.
    Each instance of the class has a NumPy array for the cell data.  The class automatically creates
    boundary cells surrounding the simulation grid.  It also creates views into the simulation grid,
    boundary cells, and neighbor cells for use with NumPy array calculation calls.

    Since this class inherits numpy.ndarray, several unique approaches must be used (especially for
    class instance creation.)  The document at
    https://docs.scipy.org/doc/numpy/user/basics.subclassing.html explains using ndarray as a
    subclass and these special approaches.

    Also important is the concept of an array view.  A view to an array does not use new data in
    memory, but simply 'views' the data which already exists.  This is explained some at
    https://docs.scipy.org/doc/numpy-dev/user/quickstart.html#copies-and-views
    Because of this efficiency, this class creates many views into the grid.  These views can be
    used later for efficient calculation through NumPy calls rather than iterating over items
    through interpreted python code.

    Class methods and attributes Inherited:
    All the instance variables associated with Numpy ndarray such as .shape, .dtype
    A complete list of ndarray methods and attributes is available at
    https://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.ndarray.html#numpy.ndarray


    The new class methods are:
    __new__ -> class initialization method.
                The array (or grid) shape must be provided.  The constructor will not take data.
                It creates an array 2 cells (or nodes) larger (in each direction) than the shape
                argument passed.  This allows for boundary cells in each direction.  The
                constructor returns a NumPy array for the main simulation data. This is actually
                a view into the data of the bigger array which also contains boundary cells.
                The bigger array is available through .Base or .base. The constructor also
                creates view arrays for the neighbors to the top, top right, left, bottom left ...

    __array_finalize_ ->  Always called after initialization.  It does not currently do anything.

    __init__ -> Not used since it is not always called for subclasses of ndarray.

    Update ->   Implements the rules of the cellular automaton
                Currently implements a simulation using 'game of life rules.'
                To implement other cellular automaton simulations, either:
                    1.) Change the code in this file (especially Update)
                    2.) Create a new class which inherits this class with
                        class NewClass(CAGrid):
                        and include in that class an update function which will replace the
                        one here.

    FinishUpdate -> Completes tasks after update
                    After cell values are updated, there are several tasks which must be completed
                    to prepare the CAGrid object for display and/or the next call to update.
                    Currently, this includes calling SetValue and SetBoundary.

    SetValue -> Sets the 'Value' field for the structured array.
                This function is somewhat tied to the Game of Life Simulation.
                The purpose of this function is do a fast conversion to float values as
                expected by matplotlib.matshow.

    SetBoundary ->  Sets the boundary conditions by copying cells from main simulation grid
                    to the boundary cells.

    New Data Attributes or Instance Variables are:
    .Base or .base ->   The large array which includes the boundary cells.
                        .base is the normal attribute for a NumPy array.
                            The array returned by the constructor is actually a view into the larger
                            array.  So NumPy automatically creates this reference.
                        .Base is created in the constructor.  It is probably not needed.  It might be
                            needed to keep the larger array in memory.

    .Neighbors[]  ->    List of arrays which are views which give the cell's neighbor in a direction.
                        In other words, one of the neighbors is TopLeft.  Accessing TopLeft[3][4]
                        returns the grid node at [2][3].
                        Diagonal neighbor arrays are included in the list depending on the value of
                        the class variable CAGrid.IncludeDiagonalNeighbors.  The default for this
                        variable is True.

    .Old    ->          Attribute which has the same attributes as the CAGrid object.  .Old is for
                        storing the old state of the object before update if necessary.
    .TrueArray  ->      Array of True values for use in mask/array operations.  It is the same size
                        as the simulation grid, not the base grid.  Used for update calculations.
                        Declaring .TrueArray makes the code run faster because memory is not created
                        with each update.  Since it is an instance variable, it is created and
                        initialized only once per simulation.
    .count      ->      Used by the game of life update to count number of alive neighbors.
    .UpdateCount    ->  Tracks the number of times Update is called.
    """

    IncludeDiagonalNeighbors = True

    def __new__(cls,shape, *args, **kwargs):
        """Creator of new CGAGrid array.

        shape:
                Size of the simulation grid.  The base grid will be two larger than this in
                each direction.
        buffer:
                buffer values are not allowed as they are with an ndarray.
                Including the buffer keyword raises an error.
                Taking a buffer would require COPYING the data instead of using the already
                existing memory location because the needed buffer is larger than the simulation
                grid.  Copying the data could cause memory usage problems.
        all other arguments and keywords are passed to the NumPy array creator.

        This function:
            Creates array with shape = passedshape + (2,2)
            Creates view into array for simulation grid  (This is the array object returned.)
            Adds to simulation grid array instance variables as described in class docstring.


        """

        if 'buffer' in kwargs:
            raise TypeError("buffer not allowed in constructor.  Initialize grid after constructor.")
            # If we did want to try and take a buffer, the code below would probably be needed as well as a
            # copying the data to the new array after it has been created, copyto(ni, buffer).
            # databuffer= kwargs['buffer']
            # del kwargs['buffer']
            # print('Buffer values will be used, but not the memory locations')
        BaseShape = tuple([d+2 for d in shape])

        Base = numpy.ndarray.__new__(cls, BaseShape,*args, **kwargs)

        # ni stands for new instance.  It is the object this __new__ will return
        ni = Base[1:BaseShape[0]-1,1:BaseShape[1]-1]                 # ni.Base might not be needed since this
        ni.Base        = Base                                        # is already defined as base by NumPy
        # Create views for the neighbors in each direction.
        ni.NTopLeft     = Base[0:BaseShape[0]-2, 0:BaseShape[1]-2]
        ni.NTop         = Base[0:BaseShape[0]-2, 1:BaseShape[1]-1]
        ni.NTopRight    = Base[0:BaseShape[0]-2, 2:BaseShape[1]]
        ni.NLeft        = Base[1:BaseShape[0]-1, 0:BaseShape[1]-2]
        ni.NRight       = Base[1:BaseShape[0]-1, 2:BaseShape[1]]
        ni.NBottomLeft  = Base[2:BaseShape[0],   0:BaseShape[1]-2]
        ni.NBottom      = Base[2:BaseShape[0],   1:BaseShape[1]-1]
        ni.NBottomRight = Base[2:BaseShape[0],   2:BaseShape[1]]
        if cls.IncludeDiagonalNeighbors:
            ni.Neighbors    = [ni.NTop,    ni.NTopRight,   ni.NRight, ni.NBottomRight,
                               ni.NBottom, ni.NBottomLeft, ni.NLeft,  ni.NTopLeft]
        else:
            ni.Neighbors = [ni.NTop, ni.NRight, ni.NBottom, ni.NLeft]
        # Create views for the grid boundaries.
        ni.TopRow       = Base[1:2,                           1:BaseShape[1]-1]
        ni.BottomRow    = Base[BaseShape[0]-2:BaseShape[0]-1, 1:BaseShape[1]-1]
        ni.LeftColumn   = Base[1:BaseShape[0]-1,              1:2]
        ni.RightColumn  = Base[1:BaseShape[0]-1,              BaseShape[1]-2:BaseShape[1]-1]
        # These are the views into the boundary cells
        ni.BTopRow      = Base[0:1,                           1:BaseShape[1]-1]
        ni.BBottomRow   = Base[BaseShape[0]-1:BaseShape[0],   1:BaseShape[1]-1]
        ni.BLeftColumn  = Base[1:BaseShape[0]-1,              0:1]
        ni.BRightColumn = Base[1:BaseShape[0]-1,              BaseShape[1]-1:BaseShape[1]]

        # Create a copy of the array in case it is need to keep the old data during an update.
        OldBase = Base.copy()
        Old     = OldBase[1:BaseShape[0]-1,1:BaseShape[1]-1]
        Old.Base        = OldBase
        Old.NTopLeft     = Old.Base[0:BaseShape[0]-2, 0:BaseShape[1]-2]
        Old.NTop         = Old.Base[0:BaseShape[0]-2, 1:BaseShape[1]-1]
        Old.NTopRight    = Old.Base[0:BaseShape[0]-2, 2:BaseShape[1]]
        Old.NLeft        = Old.Base[1:BaseShape[0]-1, 0:BaseShape[1]-2]
        Old.NRight       = Old.Base[1:BaseShape[0]-1, 2:BaseShape[1]]
        Old.NBottomLeft  = Old.Base[2:BaseShape[0],   0:BaseShape[1]-2]
        Old.NBottom      = Old.Base[2:BaseShape[0],   1:BaseShape[1]-1]
        Old.NBottomRight = Old.Base[2:BaseShape[0],   2:BaseShape[1]]
        if cls.IncludeDiagonalNeighbors:
            Old.Neighbors   = [Old.NTop, Old.NTopRight, Old.NRight, Old.NBottomRight,
                               Old.NBottom, Old.NBottomLeft, Old.NLeft, Old.NTopLeft]
        else:
            Old.Neighbors = [Old.NTop, Old.NRight, Old.NBottom, Old.NLeft]
        ni.Old       = Old
        ni.TrueArray = numpy.full(ni.shape,True,dtype=numpy.dtype('b'))
        ni.count     = numpy.zeros(ni.shape)
        if CAGrid.IncludeDiagonalNeighbors:
            ni.ran = numpy.random.rand(ni.shape[0], ni.shape[1]) * 8
        else:
            ni.ran = numpy.random.rand(ni.shape[0], ni.shape[1]) * 4
        ni.UpdateCount = 0

        return ni


    def __array_finalize__(self, obj):
        """Initialization code may be place here.

        Currently this function does nothing."""
        pass

    def Update(self):
        """Implements a single time step using Game of Life Rules

        Method currently takes no arguments.

        Method sums the 'Value' of the neighbor cells and then applies the game of life rules.
        Method uses array operations for calculations rather than iterators so that we take
            full advantage of underlying C and BLAS routines rather than slower Python code.

        Some of these routines are listed at:
        https://docs.scipy.org/doc/numpy/reference/routines.indexing.html#inserting-data-into-arrays
        In this method, numpy.place is used.  It is documented at:
        https://docs.scipy.org/doc/numpy/reference/generated/numpy.place.html#numpy.place

        Method also calls self.FinishUpdate
        """

        # Determine number of neighbors
        numpy.place(self.count,self.TrueArray,0)
        for n in self.Neighbors:
            self.count = self.count + n['Value']

        # Implement Game of Life Rules
        # Note:  Self.Old is actually not needed for Game of Life.
        #       It might not be needed for other Update methods either.
        # numpy.copyto(self.Old,self)                       # Default is no change for count = 2
        numpy.place(self['State'], self.count >3, False)   # If count > 3: new value = False
        numpy.place(self['State'], self.count ==3, True)   # If count = 3: new value = True
        numpy.place(self['State'], self.count <2, False)   # If count < 2: new value = False
        self.FinishUpdate()
        self.UpdateCount += 1

    def FinishUpdate(self):
        """Method cleans up the grid in preparation of the next call to Update.

        This function should be called:
            1. After grid initialization but before the first call to Update
            2. Between every call to Update.
            """

        self.SetValue()
        self.SetBoundary()



    def SetBoundary(self):
        """Method copies array items from the data grid cells to the surrounding boundary condition cells."""

        # copy the rows and columns.  These are views into the base created in __new__
        numpy.copyto(self.BBottomRow, self.TopRow)
        numpy.copyto(self.BLeftColumn, self.RightColumn)
        numpy.copyto(self.BTopRow, self.BottomRow)
        numpy.copyto(self.BRightColumn, self.LeftColumn)

        # copy the corners
        self.Base[0][0] = self[self.shape[0] - 1][self.shape[1] - 1]  # Set Top Left Corner
        self.Base[0][self.Base.shape[1] - 1] = self[self.shape[0] - 1][0]  # Set Top    Right Corner
        self.Base[self.Base.shape[0] - 1][self.Base.shape[1] - 1] = self[0][0]  # Set Bottom Right Corner
        self.Base[self.Base.shape[0] - 1][0] = self[0][self.shape[1] - 1]  # Set Bottom Left Corner

    def SetValue(self):
        """Sets the 'Value' field of the structured array equal to the 'State' Field."""
        numpy.copyto(self['Value'], self['State'])
