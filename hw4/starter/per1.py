import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
import sys


def main():
    '''YOUR CODE GOES HERE'''
    df = pd.read_csv('per_con_data.csv', index_col=None, header = None)
    # print(df)
    data = np.array(df)

    x1 =[]
    x2 =[]
    y1 =[]
    y2=[]
    z1 =[]
    z2=[]
    for i in range(len(data)):
        if data[i][3]>0:
            x1.append(data[i][0])
            y1.append(data[i][1])
            z1.append(data[i][2])
        else:
            x2.append(data[i][0])
            y2.append(data[i][1])
            z2.append(data[i][2])


    print(x1,y1,z1)
    print(x2,y2,z2)

    fig = plt.figure()
    ax = plt.figure().add_subplot(projection='3d')
    ax.scatter(x1, y1, z1, c='r', label='1')
    ax.scatter(x2, y2, z2, c='g', label='-1')
    plt.legend()


    xlim = (-5, 5)
    ylim = (-5, 5)
    zlim = (-1, 1)
    ax.set_xlim3d(xlim)
    ax.set_ylim3d(ylim)
    ax.set_zlim3d(zlim)

    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_zlabel('X3')

    plt.show()

    #
    # data = np.insert(data, 0, 1, axis=1)
    # # print(data[0][0])
    # w0 = np.array([1, 1, 1, 1])
    # w1 = np.array([0, 0, 0, 0])
    # a = 1
    # weight =[]
    # k = 0

    # while k < 100 :
    #     k += 1
    #     for i in range(len(data)):
    #         w0 = w1
    #         if data[i][4]* np.sign(data[i][0]*w0[0]+data[i][1]*w0[1]+data[i][2]*w0[2]+data[i][3]*w0[3]) <= 0:
    #
    #             w1 = w0 + [a*data[i][4]*data[i][0], a*data[i][4]*data[i][1], a*data[i][4]*data[i][2], a*data[i][4]*data[i][3]]
    #         weight.append(w1)
    # weight.append(w1)
    # weight = pd.DataFrame(np.array(weight))
    # print(weight)
    # weight.to_csv('con.csv', header=False, index=False)


if __name__ == "__main__":
    """DO NOT MODIFY"""
    main()