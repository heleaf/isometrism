#ndarray.ndim - # of axes (dimensions)
#ndarray.shape - dimensions (rows, cols)
#ndarray.size - total # of elements, rows*cols

def testArr(a):
    print(f'{a.ndim} dimensional array:\n {a}')
    print(f'shape: {a.shape}')
    #print(f'number of dimensions: {a.ndim}')
    #print(f'number of elements: {a.size}')
    print(f'array type: {type(a)}')
    print(f'element type: {a.dtype}')

def test1DAliases(a):
    aliases = 0
    for i in range(len(a)):
        for j in range(len(a)):
            if i!=j and (a[i] is a[j]):
                aliases += 1
    print(f'aliases: {aliases}')

def printArrays():
    a1 = np.zeros(5) # 1d array 
    a2 = np.array([1,2,2])
    a3 = np.array([1.5, 6, 0])
    a4 = np.array([[2,3,4],[4,5,6]])
    a5 = np.array([[3,4,5],[6,7,8],[9,7,8],[1,0,0]], dtype=complex)
    a6 = np.ones((2,3,4))
    testArr(a1)
    test1DAliases(a1)
    print()
    testArr(a2)
    test1DAliases(a2)
    print()
    testArr(a3)
    print()
    testArr(a4)
    print()
    testArr(a5)
    print()
    testArr(a6)

    #basic operations are element-wise
    print(a2-a3)
    print(2*a2) #scalar mult
    print(a2==1)

    #dot product
    print(a2.dot(a3))

    #indexing 
    print(a2[1:])
    print(a2[:2])
    print(a2[::-1])

    #looping
    for row in a4:
        print(row)