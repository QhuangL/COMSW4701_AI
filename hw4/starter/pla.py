import pandas as pd
import numpy as np
import sys

def main():
    '''YOUR CODE GOES HERE'''
    df = pd.read_csv(sys.argv[1], index_col=None, header = None)
    # print(df)
    data = np.array(df)
    data = np.insert(data, 2, 1, axis=1)
    # print(data[0][0])
    w0 = np.array([1, 1, 1])
    w1 = np.array([0, 0, 0])
    a = 1
    weight =[]
    k = 0

    while k < 20 :
        k += 1
        for i in range(len(data)):
            w0 = w1
            if data[i][3]* np.sign(data[i][0]*w0[0]+data[i][1]*w0[1]+data[i][2]*w0[2]) <= 0:

                w1 = w0 + [a*data[i][3]*data[i][0], a*data[i][3]*data[i][1], a*data[i][3]*data[i][2]]
            weight.append(w1)
    weight.append(w1)
    weight = pd.DataFrame(np.array(weight))
    # print(weight)
    weight.to_csv(sys.argv[2], header=False, index=False)


if __name__ == "__main__":
    """DO NOT MODIFY"""
    main()