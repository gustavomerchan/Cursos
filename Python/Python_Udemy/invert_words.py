def reverse_word(string):
    is_string(string)
    return(string[::-1])




def is_string(param):
  if not isinstance(param,str):
     raise TypeError('It s not a text bitch')
  else:
     return param



name = 'Gustavo'
print(reverse_word(name))