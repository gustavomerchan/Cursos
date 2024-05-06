def unpack_dict(dict):
    for chave, valor in dict.items():
        print(f'{chave}: {valor}')


pessoa = {'nome': 'Gustavo',
          'sobrenome': 'Merchan'}

dados_pesso = {'idade': 23,
               'altura':1.75
               }
pessoa_copleta = {**pessoa,**dados_pesso}


unpack_dict(pessoa_copleta)