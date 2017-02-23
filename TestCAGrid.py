from CellularAutomaton import *
import numpy as np


def test_init(Rows, Columns, States):


    MyDtype = numpy.dtype([('Value', 'f'), ('State', bool)])
    MyGrid = CAGrid((Rows, Columns), MyDtype)

    i = 0
    for y in range(Rows):
        for x in range(Columns):
            MyGrid["State"][y][x] = States[i]
            i = i + 1
    MyGrid.SetValue()
    MyGrid.SetBoundary()
    print(MyGrid['State'])
    print(MyGrid['Value'])

test_init(3,3, (0,1,0,1,0,1,0,1,0))


def test_setboundary():
    Rows = 3
    Columns = 6
    mydtype = np.dtype([('Value','f'),('State', 'b')])
    MyGrid = CAGrid((Rows,Columns),mydtype)

    for yy in range(Rows):
         for xx in range(Columns):
             MyGrid['Value'][yy][xx] = 10*yy + xx + 100

    print('Before Set Boundary ************')
    print(MyGrid)
    print('The base is')
    print(MyGrid.Base)

    MyGrid.SetBoundary()
    print('After Set Boundary*******************')
    print(MyGrid)
    print('The base is')
    print(MyGrid.Base)

def test_update(rows, columns, interations, states):
    mydtype = np.dtype([('Value','f'),('State', 'bool')])
    MyGrid = CAGrid((rows,columns),mydtype)

    i=0
    for y in range(rows):
        for x in range(columns):
            MyGrid["State"][y][x]=states[i]
            i = i + 1
    MyGrid.SetValue()
    MyGrid.SetBoundary()
    print('After Initialization')
    print(MyGrid)

    for i in range(interations):
        MyGrid.Update()
        print('After Update i = {}'.format(i+1))
        print(MyGrid)




print('*** Running test_setboundar ****')
test_setboundary()
print('test_update(3, 3, 2, states = (0,1,0,1,0,1,0,1,0))')
test_update(3, 3, 2, states = (0,1,0,1,0,1,0,1,0))
print('next should give a stable block in upper right corner.')
test_update(3, 3, 2, states = (1,1,0,1,1,0,0,0,0))
print('next should go from vertical line to filled, to dead,')
test_update(3, 3, 2, states = (0,0,0,1,1,1,0,0,0))
print('next should go give a line blinker')
test_update(4, 5, 5, states = (0,0,0,0,0,
                               0,0,0,0,0,
                               0,1,1,1,0,
                               0,0,0,0,0))
print('Checkerboard')
test_update(3,3,3,states = (0,1,0,1,0,1,0,1,0))
