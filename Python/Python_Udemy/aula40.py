# Calculadora
while True:
    try:
        n1 = float(input('Digite um numero:' ))
        n2 = float(input('Digite um numero:' ))
    except:
        print('Numero Invalido')
        continue

    op = input('Escolha a operacao que deseja realizar:\n+ Adição\n- Subtração\n* Multiplicação\n/ Divisão\nDigite o simbolo da operação desejada:')
    resultado = 0

    op_permitidos = '+-*/'

    if op not in op_permitidos:
        print('Operador Invalido')
        continue
    if len(op) > 1:
        print('Operador Invalido')
        continue

    if op == '+':
        resultado = n1 + n2
        print(f'{n1}{op}{n2} = {resultado}')
    elif op == '-':
        resultado = n1 - n2
        print(f'{n1}{op}{n2} = {resultado}')
    elif op == '*':
        resultado = n1 * n2
        print(f'{n1}{op}{n2} = {resultado}')
    elif op == '/':
        resultado = n1/n2
        print(f'{n1} {op} {n2} = {resultado}')

    sair = input('Quer sair? [s]im:').lower().startswith('s')
    if sair:
        break
print('Encerrando o programa...')