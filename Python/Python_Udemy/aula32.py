"""
Faça um programa que peça ao usuário para digitar um número inteiro,
informe se este número é par ou ímpar. Caso o usuário não digite um número
inteiro, informe que não é um número inteiro.
"""
#numero_str = input('Digite um numero inteiro:')
#try:
#    numero_int = int(numero_str)
#    verifca_se_e_par = numero_int %2 == 0
#    if verifca_se_e_par:
#        print(f'O numero {numero_int} é Par')
#    else:
#       print(f'O numero {numero_int} é Ímpar')
#except:
#    print('Isto nao e um numero inteiro')

"""
Faça um programa que pergunte a hora ao usuário e, baseando-se no horário 
descrito, exiba a saudação apropriada. Ex. 
Bom dia 0-11, Boa tarde 12-17 e Boa noite 18-23.
"""
# Hora inserida pelo usuario
#ora_str = input('Digite a hora no Formato HH:MM:')
#ry:
#   # Separa as horas dos minutos
#   horas,minutos = map(int,hora_str.split(':'))
#   #verifica se a hora e valida
#   hora_valida = 0 <= horas <= 23 and 0 <= minutos <= 59
#   # Logica para saudacoes de acordo com horario
#   if hora_valida:
#       if horas >= 0 and horas <= 11:
#           print('Bom dia!')
#       elif horas >=12 and horas <= 17:
#           print('Boa Tarde!')
#       else:
#           print('Boa Noite!')
#   else:
#       print('Hora Invalida')
#xcept:
#   print('Isso nao e hora cussaum')

"""
Faça um programa que peça o primeiro nome do usuário. Se o nome tiver 4 letras ou 
menos escreva "Seu nome é curto"; se tiver entre 5 e 6 letras, escreva 
"Seu nome é normal"; maior que 6 escreva "Seu nome é muito grande". 
"""

nome_input = input('Digite seu nome:')
verifica_se_e_letra = nome_input.isalpha()
if verifica_se_e_letra:
    tamanho_nome = len(nome_input)
    if tamanho_nome <= 4:
        print('Seu nome e curto')
    elif 5 <= tamanho_nome <= 6:
        print('Seu nome e normal')
    else:
        print('Seu nome e muito grande')
else:
    print('Nome invalido')