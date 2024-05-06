def create_function(function):
    def internal(*args, **kwargs):
        for arg in args:
            is_string(arg)
        return result


def invert(string):
    return string[::-1]

def is_string(param):
    if not isinstance(param,str):
        raise TypeError('param deve ser uma string')

print(invert('Cusaum'))