nome = str(input('Digite seu nome:'))
nome_sem_espacos = nome.replace(' ','')
idade = input('Digite sua idade:')
if idade:
    int(idade)
else:
    idade    
espacos = ''
if nome and idade:
    if ' ' in nome:
        espacos = 'contém'
    else:
        espacos = 'não contém'    
    

    print(f'Seu nome é {nome}')
    print(f'Seu nome invertido é {nome[::-1]}')
    print(f'Seu nome {espacos} espaços')
    print(f'Seu nome tem {len(nome_sem_espacos)} letras')
    print(f'A primeira letra do seu nome é {nome[0]}')
    print(f'A última letra do seu nome é {nome[-1]}')

else:
    print('Desculpe, você deixou campos vazios.')    
