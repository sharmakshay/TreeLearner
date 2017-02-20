import numpy as np
import random


class RTLeaner(object):
    leafsize = 1
    log = False
    btree = None
    global node
    node = []


    def __init__(self, leaf_size, verbose):
        global leafsize
        global log

        leafsize = leaf_size
        log = verbose

    def author(self):
        return 'asharma313'

    def addEvidence(self, dataX, dataY):
        global btree
        global node
        data = np.column_stack((dataX, dataY))
        #dimen = data.shape
        #print data
        #arr = np.array([[1,2,3,2,9], [3,91,4,2,9], [4,2,5,2,9]])
        #check = np.all(arr[:, -1] == arr[0, -1], axis=0)
        #d = arr[arr[:, 2] < 4]
        #e = d[0, -1]
        #print d.shape[0] == 1

        btree = self.build_tree(data)
        print "---- PRINT BTREE ------"
        print btree
        return "done"

    def build_tree(self, d):
        global leafsize
        global node

        if d.shape[0] == 1:
            return ['leaf', d[0, -1], 'NA', 'NA']
        if np.all(d[:, -1] == d[0, -1], axis=0):
            return ['leaf', d[0, -1], 'NA', 'NA']
        else:
            # shaping the tree
            # randomly select feature i
            datacol = d.shape[1]
            randcol = random.randint(0, datacol - 2)

            # randomly select rows to split on
            # randrows = d[np.random.randint(d.shape[0], size=2), :]

            datarow = d.shape[0]
            randrow1 = random.randint(0, datarow - 1)
            randrow2 = random.randint(0, datarow - 1)
            print("ensure not same value")

            # ensure random rows generated are not of the same value
            while np.all(d[randrow1, randcol] == d[randrow2, randcol], axis=0):
                randrow1 = random.randint(0, datarow - 1)
                randrow2 = random.randint(0, datarow - 1)

            print(randrow1)
            print(randrow2)
            print(np.all(d[randrow1, randcol] == d[randrow2, randcol], axis=0))
            print("ensured")
            # converting splitval from ndarray to integer
            splitval = (d[randrow1, randcol] + d[randrow2, randcol]) / 2
            # print ("splitval: ", splitval[0])
            print splitval

            # if there is a case where data cannot split due to ties, then find two other random values
            # try this up to 10 times
            i = 0
            while (len(d) == len(d[d[:, randcol] <= splitval])) and i < 10:
                i += 1
                randrow1 = random.randint(0, datarow - 1)
                randrow2 = random.randint(0, datarow - 1)

            # if still unsplittable then try a different factor
            if len(d) == len(d[d[:, randcol] <= splitval]):
                randcol = random.randint(0, datacol - 2)

            # ensure leaf size check and tree is built according to given leaf size
            if d[d[:, randcol] <= splitval].shape[0] <= leafsize or d[d[:, randcol] > splitval].shape[0] <= leafsize:
                return ['leaf', d[0, -1], 'NA', 'NA']

            leftTree = self.build_tree(d[d[:, randcol] <= splitval])
            rightTree = self.build_tree(d[d[:, randcol] > splitval])
            rightTreeIndex = len(leftTree) + 1
            root = [randcol, splitval, 1, rightTreeIndex]
            print root
            print leftTree
            print rightTree
            branch = root + leftTree + rightTree
            n = node.append(branch)
            return n

    def query(self, dataX):
        ypred = []
        for row in dataX:
            y = self.traverse_tree(row, 0)
            ypred.append(y)

        return ypred

    def traverse_tree(self, d, r):
        global btree
        currNode = btree[r]
        print currNode
        return 1
        '''
        if currNode[0][0] == 'leaf':
            return currNode[1]
        compFactor = currNode[0][0]
        if d[compFactor] <= currNode[0][1]:
            print(currNode[2])
            r += int(currNode[2])

            self.traverse_tree(d, r)

        if d[compFactor] > currNode[1]:
            r += int(currNode[3])
            self.traverse_tree(d, r)
        '''