#exercicio
nome = 'Maria Helena'
tamanho_nome = len(nome)
letra = 0
novo_nome = ''

while True:
    print(f'*{nome[letra]}*',end = '')
    letra += 1
    if letra == tamanho_nome:
        break
