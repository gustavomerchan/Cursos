'''  
    Actors: Vinícius Fernandes
            Gustavo Merchan 
    Date: 11/08/2023
    Program Description: Busca os registros de faturas emitidas pela WTA (venda de produtos) na filial WTA - WATANABE TECNOLOGIA APLICADA EIRELI - EPP
        afim de filtrar pagamentos que ainda estão em aberto. A consulta retorna também os dados dos clientes para então realizar
        o envio de um e-mail realizando o lembrete do titulo em aberto. 
        A consulta limita-se à essa filial e exclui cobranças realizadas via cartão de crédito.
    Operation System: Windows 10 or higher.
    Versão: 1.0
'''

import pyodbc
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import time
import os
import json
import socket
import base64

##  Se o código foi iniciado, variável = 1
##  Se o código já estiver rodando, variável será alterada para 0
firstRun = 1

##  Pasta onde os arquivos de log estão salvos. Caso não exista, essa pasta é criada automaticamente.
path_logs = 'C:\\automacao_email\\logs\\'    

##  Pasta onde o arquivo Dimensão.sql deve estar salvo.
##  Este arquivo possui a consulta ao banco de dados.
path_dimensaoSql = 'C:\\Users\\gustavo.gomes\\Desktop\\Cursos\\Projetos\\automacao_email_cobranca_pagamento\\'

##  Senha do e-mail utilizado. 
##  Essa senha deverá estar salva na variável de sistema.
varEmail = os.environ.get('var73656e6861')

##  Seção que verifica se a pasta de logs e se todos os arquivos de logs já estão criados
##  Se algum arquivo não existir, ele será criado nessa seção.
lista_arquivos_logs = []    ##  Lista utilizada para salvar os nomes dos arquivos de logs

##  Verifica se a pasta de logs já existe, caso contrário ela será criada
if not os.path.isdir(path_logs):   
    os.mkdir(path_logs) 

##  Percorre a pasta de logs e salva os arquivos contidos nela dentro da lista 'lista_arquivos_logs'
for log in os.listdir(path_logs):
    lista_arquivos_logs.append(log)

##  Os arquivos de logs utilizados nesse programa são: log_email_enviado.json, logExecucoes.json, log_email_erro.json
##  Caso algum desses 3 nomes não estejam na lista eles serão criados. 
if 'log_email_enviado.json' not in lista_arquivos_logs or 'logExecucoes.json' not in lista_arquivos_logs or 'log_email_erro.json' not in lista_arquivos_logs:
    data = []
    json_string = json.dumps(data)
    if 'log_email_enviado.json' not in lista_arquivos_logs:
        with open(str(path_logs) + 'log_email_enviado.json', 'w') as outfile:
            outfile.write(json_string)
    if 'logExecucoes.json' not in lista_arquivos_logs:
        with open(str(path_logs) + 'logExecucoes.json', 'w') as outfile:
            outfile.write(json_string)
    if 'log_email_erro.json' not in lista_arquivos_logs:
        with open(str(path_logs) + 'log_email_erro.json', 'w') as outfile:
            outfile.write(json_string)
lista_arquivos_logs.clear()
##  Fim da seção.


##  Na função 'filtros' é realizada a consulta ao SQL Server. Essa consulta é realizada apenas para os clientes do Brasil da empresa WTA Watanabe. Após essa consulta é realizada a separação dos ->
##  registros encontrados em listas (são os filtros). As listas recebem os registros que faltam 7 dias para o vencimento, 3 dias para o vencimento e 7 dias depois do vencimento ->
##  Após as listas serem alimentadas, é realizado o envio do e-mail para cada registro de cada lista, sendo a mensagem enviada personalizada para cada envio.
def filtros():
    ##  Erro L73: Erro ao enviar e-mails:
    ##  Para economizar entradas extensas e repetitivas, a mensagem de erro ao enviar e-mails, em todos os casos observados até a implementação foi a mensagem abaixo:
    ##  'The mail server could not deliver mail. The account or domain may not exist, they may be blacklisted, or missing the proper dns entries.' 
    ##  É recomendável olhar primeiramente o que foi digitado no cadastro do cliente, no campo de e-mails e tentar um envio manual antes de qualquer alteração de código.
    
    ## Variável com a data de hoje no formato: 2020-01-31 00:00:00
    hoje = pd.Timestamp.now().normalize()

    ## Configurações de conexão com o banco de dados e consulta
    cnxn_str = "DRIVER={SQL Server Native Client 11.0};SERVER=db1;DATABASE=CORPORATIVO_PRODUCAO;UID=sa;PWD=wt@b3nNeR21;"
    cnxn = pyodbc.connect(cnxn_str)
    sql = open(path_dimensaoSql+'DIMENSAO.sql').read()
    df = pd.read_sql_query(sql, cnxn)

    ## Realiza a conversão da coluna de data que foi obtida na consulta ao SQL para o formato: 2020-01-31
    df['VENCIMENTO PRORROGADO'] = pd.to_datetime(df['VENCIMENTO PRORROGADO'])

    ##  Filtro que obtem apenas os registros que ainda faltam 7 dias para vencer.
    antecedencia_7dias = hoje + pd.DateOffset(days=7)
    filtro_vencimento_7dias_antes = (df['VENCIMENTO PRORROGADO'].dt.normalize() == antecedencia_7dias) & (df['SITUACAO DO DOCUMENTO'] == 'Em Aberto')
    linhas_para_enviar_email_7_dias_antes_vet = df[filtro_vencimento_7dias_antes]

    ##  Filtro que obtem apenas os registros que ainda faltam 3 dias para vencer.
    antecedencia_3dias = hoje + pd.DateOffset(days=3)
    filtro_vencimento_3dias_antes = (df['VENCIMENTO PRORROGADO'].dt.normalize() == antecedencia_3dias) & (df['SITUACAO DO DOCUMENTO'] == 'Em Aberto')
    linhas_para_enviar_email_3_dias_antes_vet = df[filtro_vencimento_3dias_antes]

    ## Filtro que obtem apenas os registros que já estão vencidos à 7 dias
    atraso_7dias = hoje - pd.DateOffset(days=7)
    filtro_atraso_7dias = (df['VENCIMENTO PRORROGADO'].dt.normalize() == atraso_7dias) & (df['SITUACAO DO PAGAMENTO'] == 'Atrasado')
    linhas_para_enviar_email_atraso_7dias_vet = df[filtro_atraso_7dias]

    ## Envio de e-mails 7 dias antes do vencimento
    for _, linha in linhas_para_enviar_email_7_dias_antes_vet.iterrows():
        personalizaMensagem(hoje, 'em dia', '7 dias antes', linha['CLIENTE'], linha['VENCIMENTO PRORROGADO'].strftime('%d/%m/%Y'), linha['PARCELA'], linha['QTD DE PARCELAS'], linha['DOCUMENTO'], linha['VALOR DA PARCELA'], linha['EMAILS'])

    ## Envio de e-mails 3 dias antes do vencimento
    for _, linha in linhas_para_enviar_email_3_dias_antes_vet.iterrows():
        personalizaMensagem(hoje, 'em dia', '3 dias antes', linha['CLIENTE'], linha['VENCIMENTO PRORROGADO'].strftime('%d/%m/%Y'), linha['PARCELA'], linha['QTD DE PARCELAS'], linha['DOCUMENTO'], linha['VALOR DA PARCELA'], linha['EMAILS'])

    ##  Envio de e-mails com 7 dias de atraso
    for _, linha in linhas_para_enviar_email_atraso_7dias_vet.iterrows():
        personalizaMensagem(hoje, 'atrasado', 'Atraso 7 dias', linha['CLIENTE'], linha['VENCIMENTO PRORROGADO'].strftime('%d/%m/%Y'), linha['PARCELA'], linha['QTD DE PARCELAS'], linha['DOCUMENTO'], linha['VALOR DA PARCELA'], linha['EMAILS'])

    ## Fecha a conexão com o SQL
    cnxn.close()    


##  Assim como na função 'filtros', a função 'filtro_reenvio' realiza a consulta ao SQL Server e essa consulta realiza a separação ->
##  apenas dos registros que estão com a situação do pagamento em atraso. Os registros encontrados serão carregados na lista 'busca_atrasados_sql' ->
##  Na sequencia, será aberto o arquivo de log de e-mail enviado para buscar os e-mails que já foram enviados para clientes com a situação ->
##  de pagamento atrasado, e então os registros serão carregados para a lista 'busca_atrasados_json'. ->
##  Depois é verificado se já faz exatamente 10 dias após o ultimo envio de e-mail para então verificar se o cliente ainda está com o pagamento ->
##  atrasado, e caso esteja é realizado um novo envio de e-mail.
def filtro_reenvio():
    busca_atrasados_json = []
    busca_atrasados_sql = []

    ##  Variável com a data de hoje no formato: 2020-01-31
    hoje = datetime.strptime(str(datetime.today())[:10], "%Y-%m-%d").date()
    
    ## Realiza a configuração da conexão com o banco de dados e realiza a consulta de registros com o status 'Atrasado'
    cnxn_str = "DRIVER={SQL Server Native Client 11.0};SERVER=db1;DATABASE=CORPORATIVO_PRODUCAO;UID=sa;PWD=wt@b3nNeR21;"
    cnxn = pyodbc.connect(cnxn_str)
    sql = open(path_dimensaoSql+'DIMENSAO.sql').read()
    df = pd.read_sql_query(sql, cnxn)
    filtro_atrasadas = (df['SITUACAO DO PAGAMENTO'] == 'Atrasado')
    df_consulta_sql = df[filtro_atrasadas]
    cnxn.close()

    ##  Será dispensado o valor do Handle, e então realiza a iteração dos resultados da busca do SQL.
    ##  As informações abaixo ficarão na lista busca_atrasados_sql
    for _, item in df_consulta_sql.iterrows():
        atrasados = {
            'Handle': item['HANDLE'],
            'Cliente': item['CLIENTE'],
            'Documento': item['DOCUMENTO'],
            'Situacao Pagamento': item['SITUACAO DO PAGAMENTO'],
            'E-mail': item['EMAILS'],
            'Vencimento': item['VENCIMENTO PRORROGADO'].isoformat(),
            'Parcela': item['PARCELA'],
            'Qtd_parcelas': item['QTD DE PARCELAS'],
            'Valor da parcela': item['VALOR DA PARCELA']
        }
        busca_atrasados_sql.append(atrasados)

    ##  Abre o json de logs
    with open(str(path_logs) + 'log_email_enviado.json') as json_file:
        jsonOpened = json.load(json_file)

    ##  Separa apenas os itens que possuem o tipo do envio = 'atrasado'
    for item in jsonOpened:
        if item['Situacao pagamento'] == 'atrasado':
            busca_atrasados_json.append(item)

    ##  Dentro desse for as duas listas são percorridas: a lista busca_atrasados_json e busca_atrasados_sql
    ##  Para cada resultado em busca_atrasados_json é verificado se fazem 10 dias que o e-mail foi enviado.
    ##  Caso faça 10 dias desde o envio, buscamos uma correspondencia na lista busca_atrasados_sql e se houver correspondencia de registro, o e-mail é enviado novamente.
    for itemJson in busca_atrasados_json:
        itemData = datetime.strptime(itemJson['DataHora'], "%Y-%m-%dT%H:%M:%S.%f")
        itemData = itemData.date()
        if (hoje - itemData).days == 10:
            for itemSql in busca_atrasados_sql:
                if itemJson['Documento'] == itemSql['Documento'] and itemJson['Cliente'] == itemSql['Cliente'] and itemJson['Parcela'] == itemSql['Parcela']:
                    vencimento = datetime.strptime(itemSql['Vencimento'], "%Y-%m-%d")
                    vencimento = vencimento.date()
                    if itemJson['Tipo filtro'] == 'Reenvio de atraso':
                        numTipoFiltro = itemJson['Num tipo filtro']
                        numTipoFiltro = numTipoFiltro + 1
                    else:
                        numTipoFiltro = 0
                    personalizaMensagem(hoje, 'atrasado', 'Reenvio de atraso', numTipoFiltro, itemSql['Cliente'], itemSql['Vencimento'].strftime('%d/%m/%Y'), itemSql['Parcela'],itemSql['Qtd_parcelas'], itemSql['Documento'], itemSql['Valor da parcela'], itemSql['E-mail'])
                    break


def personalizaMensagem(hoje, situacaoPagamento, tipoFiltro, numTipoFiltro, cliente, vencimento, parcela, qntParcelas, documento, valorParcela, destinatarios):
    if situacaoPagamento == 'atrasado':
        assuntoConteudo = 'Atraso'
        corpo = f"Prezado(a) {cliente}, \n\nEsperamos que esta mensagem o(a) encontre bem. Gostaríamos de informar que nosso sistema identificou que a parcela N° {parcela} de {qntParcelas}, referente ao Título: {documento}, no valor de R${valorParcela}, ainda não foi registrada como paga. A atualização necessária apresenta um atraso de {(hoje - vencimento).days} dias.\nPedimos gentilmente que, caso o pagamento já tenha sido efetuado, por favor, desconsidere este comunicado. Caso contrário, solicitamos que verifique e regularize o pagamento o quanto antes, a fim de evitar quaisquer inconvenientes futuros.\n\nEstamos à sua disposição para esclarecer qualquer dúvida ou fornecer o suporte necessário.\nAgradecemos a atenção e reiteramos o nosso compromisso em oferecer um serviço de qualidade.\n\nAtenciosamente,\nWTA - Watanabe Tecnologia Aplicada Epp.\nTelefone: +55 (16)3951-8161\nWhatsApp: +55 (16)98131-1725 - Najara\nEmail: financeiro@wtavet.com.br\n\nEnvio de NFe e XML para : administrativo@wtavet.com.br"
    else:
        assuntoConteudo = 'Vencimento'
        corpo = f"Prezado(a) {cliente}, \n\nEsperamos que esta mensagem o(a) encontre bem. Gostaríamos de lembrá-lo sobre a sua parcela N° {parcela} de {qntParcelas}, referente ao Título: {documento} com o vencimento em {vencimento}. O valor a ser pago é de R${valorParcela} \nPedimos gentilmente que, caso o pagamento já tenha sido efetuado, por favor, desconsidere este comunicado.ainda não foi registrada como paga. A atualização necessária apresenta um atraso de {(hoje - vencimento).days} dias.\nPedimos gentilmente que, caso o pagamento já tenha sido efetuado, por favor, desconsidere este comunicado. Estamos à sua disposição para esclarecer qualquer dúvida ou fornecer o suporte necessário.\nAgradecemos a atenção e reiteramos o nosso compromisso em oferecer um serviço de qualidade.\n\nAtenciosamente,\nWTA - Watanabe Tecnologia Aplicada Epp.\nTelefone: +55 (16)3951-8161\nWhatsApp: +55 (16)98131-1725 - Najara\nEmail: financeiro@wtavet.com.br\n\nEnvio de NFe e XML para : administrativo@wtavet.com.br"
    assunto = f"WTA - Lembrete de {assuntoConteudo} de fatura! Vencimento {vencimento} - {cliente}"
    try:
        enviar_email(destinatarios, assunto, corpo, cliente, documento, parcela, tipoFiltro, numTipoFiltro, situacaoPagamento, vencimento)
    except:
        geraLogsEmailErro('Erro L73', cliente, documento, situacaoPagamento, destinatarios, vencimento, parcela, tipoFiltro, numTipoFiltro)


# Função para enviar e-mails de aviso
def enviar_email(destinatarios, assunto, corpo, cliente, documento, parcela, tipoFiltro, numTipoFiltro, situacaoPagamento, vencimento):
    global path_logs
    global varEmail
    list_email_enviado = []
    
    msg = MIMEText(corpo)
    msg['From'] = 'pagamentos@wtavet.com.br'
    msg['To'] = destinatarios
    msg['Subject'] = assunto

    with smtplib.SMTP('mail.wtavet.com.br', 587) as smtp:
        smtp.starttls()
        smtp.login('pagamentos@wtavet.com.br', var(varEmail))
        smtp.send_message(msg)

    mensagem = {
        'Cliente': cliente, ##  Nome do Cliente
        'Documento': documento, ##  Número do documento (Nota Fiscal)
        'Situacao pagamento': situacaoPagamento,    ##  Se está "em dia" ou "atrasado"
        'E-mail': destinatarios,    ##  E-mail do cliente
        'Vencimento': vencimento,   ##  Data de vencimento da cobrança
        'Parcela': parcela, ##  Número da parcela.
        'Assunto': assunto, ##  Assunto do e-mail enviado
        'Corpo': corpo, ##  Corpo do e-mail enviado
        'DataHora envio': datetime.now().isoformat(),   ##  Data e hora que o e-mail foi enviado
        'Tipo filtro': tipoFiltro,   ##  Refere-se ao filtro "7 dias antes", "3 dias antes", "Atraso 7 dias" ou "Reenvio de atraso"
        'Num tipo filtro': numTipoFiltro    ## Refere-se ao número da tentativa de reenvio de e-mails com o status "Reenvio de atraso"
    }

    with open(str(path_logs) + 'log_email_enviado.json') as json_file:
        list_email_enviado = json.load(json_file)
    ##  Adiciona os dados da mensagem às informações que já existiam no log e salva novamente o arquivo.
    list_email_enviado.append(mensagem)
    json_string = json.dumps(list_email_enviado)
    with open(str(path_logs) + 'log_email_enviado.json', 'w') as outfile:
        outfile.write(json_string)
    time.sleep(10)


def verify_internet_connection():
    try:
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except OSError:
        pass
    return False

def var(varEmail):
    varEmail2 = base64.b64decode(varEmail)
    varEmail3 = varEmail2.decode('utf-8')
    return varEmail3

def geraLogsEmailErro(mensagem_erro, cliente, documento, situacaoPagamento, destinatarios, vencimento, parcela, tipoFiltro, numTipoFiltro):
    with open(str(path_logs) + 'log_email_erro.json') as json_file:
        logErros = json.load(json_file)
    erroDict = {
        'Mensagem de erro': mensagem_erro,
        'Cliente': cliente, ##  Nome do Cliente
        'Documento': documento, ##  Número do documento (Nota Fiscal)
        'Situacao pagamento': situacaoPagamento,    ##  Se está "em dia" ou "atrasado"
        'E-mail': destinatarios,    ##  E-mail do cliente
        'Vencimento': vencimento,   ##  Data de vencimento da cobrança
        'Parcela': parcela, ##  Número da parcela.
        'DataHora envio': datetime.now().isoformat(),   ##  Data e hora que o e-mail foi enviado
        'Tipo filtro': tipoFiltro,   ##  Refere-se ao filtro "7 dias antes", "3 dias antes", "Atraso 7 dias" ou "Reenvio de atraso"
        'Num tipo filtro': numTipoFiltro    ## Refere-se ao número da tentativa de reenvio de e-mails com o status "Reenvio de atraso"
    }
    logErros.append(erroDict)
    json_string = json.dumps(logErros)
    with open(str(path_logs) + 'log_email_erro.json', 'w') as outfile:
        outfile.write(json_string)


def geraLogsExecucoes(evento):
    with open(str(path_logs) + 'logExecucoes.json') as json_file:
        logExecucao = json.load(json_file)
    execDict = {
        'Execution date': datetime.strptime(str(datetime.today())[:10], "%Y-%m-%d").date(),   ##  Data e hora que o log foi registrado
        'Execution time': datetime.now().strftime("%H:%M:%S"),
        'Evento': evento
    }
    logExecucao.append(execDict)
    json_string = json.dumps(logExecucao)
    with open(str(path_logs) + 'logExecucoes.json', 'w') as outfile:
        outfile.write(json_string)


if __name__ == '__main__':
    try:
        while True:
            if firstRun == 1:
                with open(str(path_logs) + 'logExecucoes.json') as json_file:
                    logExecucoes = json.load(json_file)
                if len(logExecucoes) == 0:
                    firstRun = 0
                else:
                    for date in logExecucoes:
                        if 'Evento' in date and date['Evento'] == 'email enviado':
                            if date['Execution date'] == datetime.strptime(str(datetime.today())[:10], "%Y-%m-%d").date().isoformat():
                                time.sleep(86400)   ##  86400 segundos = 1 dia de espera
                            else: 
                                firstRun = 0
            else:
                if verify_internet_connection():    ##  escrever no log o evento "OK"
                    filtros()
                    filtro_reenvio()
                    geraLogsExecucoes('email enviado')
                    time.sleep(86400)   ##  86400 segundos = 1 dia de espera
                else:
                    geraLogsExecucoes('sem conexao')
                    time.sleep(3600)    ##  3600 segundos = 60 minutos = 1 hora de espera
    except KeyboardInterrupt():
        geraLogsExecucoes('execucao encerrada')
        time.sleep(1)
