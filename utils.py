def binaryArrayToInt(binaryArray, quantityOfBits):
    decimal = int(''.join(str(x) for x in binaryArray), 2)
    if (decimal & (1 << (quantityOfBits - 1))) != 0: 
        decimal = decimal - (1 << quantityOfBits)     
    return decimal