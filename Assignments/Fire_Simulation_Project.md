#  Cellular Automaton Fire Simulation Assignment
Create a cellular automaton (CA) simulation of fire spreading similar to the simulation 
developed in Module 10.3 of the text.  With this simulation, investigate the effect of forest
density and fire immunity.  Create a plot for the percentage of trees which do not burn as
as a function initial forest density for different values of immune probability.  For this:
-  Create a CA grid at least 100 x 200 with:
    - Periodic boundary conditions on the top and bottom of the grid.
    - Impenetrable boundary conditions on the grid right and left.  (In other words the grid
      just ends.)
    - All cells in the left column set on fire simulating a burning fire front.
-  Run the simulation for multiple values of initial forest density and immune probability.
Each time, run the simulation until no burning cells are left.
-  Create the required plot.  Note: you are not required to create
   an animation, but it might help in solving the problem.

NOTES/Hints:
+ For the plotting to work using the CAGrid class, there is a change to the CAGrid test code you need to make.  A good way of getting matplotlib to plot good colors for tree, empty and burning is to give a tuple of RGB values at each grid location.  This has several required changes.
    + To do this, you can set the 'value' field to a touple.  This requires specifing the numpydtype to contain 3 floats rather than one.  My code for the dtype is `MyDtype = numpy.dtype([('Tree', bool), ('Burning', bool), ('ProbImmune', 'f'), ('Value', 'f', (3,))]).`  The relevent part is `('Value', 'f', (3,))` in which the "(3,)" indicates there are thee floats rather than just one.
    + My code for setting the values is below.  I put this as a method of my FireGrid class.  The method below is overloading the underlying CAGrid method.
    
      ```python
      def SetValue(self):
          for y in range(self.shape[0]):
              for x in range(self.shape[1]):
                  if self['Burning'][y][x]:
                      self['Value'][y][x]=(1,0,0)
                  elif self['Tree'][y][x]:
                      self['Value'][y][x]=(0,.75,0)
                  else:
                      self['Value'][y][x]=(.34,.231,.05)
        ```
    + The tuples cause matplotlib.matshow to fail.  The code ```MyAxes.matshow(MyGrid['Value'])``` returns an error.  Instead, use ```MyAxes.imshow(MyGrid['Value'],interpolation='nearest')```
