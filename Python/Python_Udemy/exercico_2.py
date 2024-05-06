def multiply(x):
    def calculate(y):
        return x * y
    return calculate


double = multiply(2)
triple = multiply(3)

print(double(3))

print(triple(3))