nome = input('Digite seu nome:')
try:
    tamannho_nome = len(nome)

    if tamannho_nome <= 4 :
        print('Seu nome é curto')
    elif tamannho_nome >= 5 and len(nome) <=6 :
        print('Seu nome é normal')
   
    else:
            print('Seu nome é muito grande')       

except:
    print('Digite um nome por favor')    