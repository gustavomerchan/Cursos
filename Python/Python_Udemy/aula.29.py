#Introducao try except
numero_str = input('Vou dobrar o numero que voce digitar:')
try:
    numero_float = float(numero_str)
    print(f'O dobro de {numero_str} e {numero_float * 2}')
except:
   print('Isto nao e um numero sir')

'''verificador = numero_str.isdigit()
if verificador:
    print('Eh numero')
else :
    print('nao eh')'''

