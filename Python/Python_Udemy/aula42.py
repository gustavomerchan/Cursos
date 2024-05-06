import emoji
from time import sleep
perguntas = [
    {
        'Pergunta': 'Quanto é 2 + 2 ?',
        'Opções': ['1','2','3','4','5'],
        'Resposta': '4'
    },

      {
        'Pergunta': 'Quanto é 5 * 5 ?',
        'Opções': ['15','20','30','40','25'],
        'Resposta': '25'
    },

      {
        'Pergunta': 'Qual é capital do Brasil?',
        'Opções': ['São Paulo','Minas Gerais','Bahia','Rio de Janeiro','Brasília'],
        'Resposta': 'Brasília'
    },
    {
        'Pergunta': 'Qual é o nome de Deus?',
        'Opções': ['Jesus','Baal','Senhor','Jeová','Mumm-Ra'],
        'Resposta': 'Jeová'

    }

]

cont = 0
acertos = 0
erros = 0
while cont < len(perguntas):
    print('Pergunta:' ,perguntas[cont].get('Pergunta'))
    for indice,opcao in enumerate(perguntas[cont].get('Opções')):
        print(f'{indice}) {opcao}')
    opcao_pergunta = perguntas[cont].get('Opções')
    resposta_certa = perguntas[cont].get('Resposta')
    try:
        resposta_usuario = int(input('Escolha uma opção:'))
        if resposta_usuario == opcao_pergunta.index(resposta_certa):
            print(emoji.emojize('Você acertou fdp!✅'))
            print()
            acertos += 1
            
        else:
            print(emoji.emojize('Você errou fdp!❌'))
            erros += 1
    except:
        print(emoji.emojize('Você errou fdp!❌'))
        print()
        erros += 1
    sleep(1)
    cont += 1
print(f'Você acertou {acertos} de {len(perguntas)} perguntas')

