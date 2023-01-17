
import numpy as np
import pandas as pd
import sys

def cal_error(data, b):
    R=0
    for i in range(len(data)):
        R  += (data[i][3] - b[0]*data[i][0]-b[1]*data[i][1]-b[2]*data[i][2])**2
    R = R/(2*len(data))

    return R

def update_b(data, b, a):
    db = np.array([float(0), float(0), float(0)])
    for i in range(len(data)):
        xi = np.array([data[i][0], data[i][1], data[i][2]])
        db +=  (data[i][3] - b[0]*data[i][0] - b[1]*data[i][1] - b[2]*data[i][2])* xi
    n_b =  b+ a*db/len(data)
    # print(n_b)
    return n_b

def main():
    """
    YOUR CODE GOES HERE
    Implement Linear Regression using Gradient Descent, with varying alpha values and numbers of iterations.
    Write to an output csv file the outcome betas for each (alpha, iteration #) setting.
    Please run the file as follows: python3 lr.py data2.csv, results2.csv
    """
    #sys.argv[1]
    df = pd.read_csv(sys.argv[1], index_col=None, header=None)
    data = np.array(df)
    mean1 = np.mean(data[:, 0])
    mean2 = np.mean(data[:, 1])
    var1 = df.std()[0:1].values
    var2 = df.std()[1:2].values
    print(mean1)
    print(mean2)
    print(var1)
    print(var2)
    data[:, 0] = (data[:, 0] - mean1) / var1
    data[:, 1] = (data[:, 1] - mean2) / var2

    weight = pd.DataFrame(np.array(data))
    weight.to_csv('data_n.csv', header=False, index=False)

    data = np.insert(data, 0, 1, axis=1)
    # print(data)
    a_list = np.array([0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 0.8])


    out = []
    for a in a_list:
        Row = []
        Row.append(a)
        Row.append(100)
        b = np.array([0, 0, 0])
        k = 0
        while k <100:
            k += 1
            R = cal_error(data, b)
            b = update_b(data, b, a)
        print('weight', b, 'Risk', R)
        Row.append(b[0])
        Row.append(b[1])
        Row.append(b[2])
        out.append(Row)
    # print(out)
    outfile = pd.DataFrame(np.array(out))
    # print(weight)
    outfile.to_csv(sys.argv[2], header=False, index=False)



if __name__ == "__main__":
    main()