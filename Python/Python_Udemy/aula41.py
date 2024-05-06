import numpy as np
import statistics

dados = {'nome':'',
         'sexo':'',
         'idade':'',
         'endereços':[
             {'rua': 'Aveinida Fagundes',
              'numero': '1356'}
         ]}

dados['nome'] = 'Gustavo'
dados['sexo'] = 'Masculino'
dados['idade'] = 23




b = [5,8,10,12,15]

print(statistics.stdev(b))
