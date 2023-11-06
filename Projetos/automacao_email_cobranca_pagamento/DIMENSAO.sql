WITH
    QTD_DE_PARCELAS
    AS(
SELECT
A.DOCUMENTO 'HANDLE NF',
COUNT(A.HANDLE) 'QTD PARCELAS'

FROM FN_PARCELAS A
WHERE A.DOCUMENTO IS NOT NULL

GROUP BY A.DOCUMENTO
    ),

    CONTATOS_TRATADOS
    AS(
        SELECT DISTINCT
P.HANDLE AS HANDLE_CLIENTE,
REPLACE(REPLACE(REPLACE(CONCAT_WS(',', TRIM(p.EMAIL), TRIM(p.K_EMAIL2), TRIM(p.K_EMAIL3), TRIM(c.EMAIL)), CHAR(13), ''), CHAR(10), ''), CHAR(9), '') AS EMAILS,
REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(CONCAT_WS(',', COALESCE(p.TELEFONEEMPRESA,''), COALESCE(c.TELEFONE,'')), CHAR(13), ''), CHAR(10), ''), CHAR(9), '') , ' ','') ,'-',''), '(',''), ')',''), '+',''), '.','') AS TELEFONES

FROM GN_PESSOAS p
LEFT JOIN (
            SELECT 
            p1.PESSOA,
            (
                STUFF( (SELECT ',' + cast(EMAIL as varchar(255)) 
                       FROM GN_PESSOACONTATOS p2
                       WHERE p2.PESSOA = p1.PESSOA OR
                             (p2.PESSOA IS NULL AND p1.PESSOA IS NULL)
                       ORDER BY EMAIL
                       FOR XML PATH(''), TYPE).value('.', 'varchar(max)')
                     ,1,1,'')
                    ) AS EMAIL,
            (
                STUFF( (SELECT ',' + cast(TELEFONE as varchar(255)) 
                       FROM GN_PESSOACONTATOS p2
                       WHERE p2.PESSOA = p1.PESSOA OR
                             (p2.PESSOA IS NULL AND p1.PESSOA IS NULL)
                       ORDER BY TELEFONE
                       FOR XML PATH(''), TYPE).value('.', 'varchar(max)')
                     ,1,1,'')
                    ) AS TELEFONE

            FROM GN_PESSOACONTATOS p1
            GROUP BY PESSOA) C       ON P.HANDLE = C.PESSOA


    ),

    PARCELAS
    AS(
SELECT 
A.FILIAL 'HANDLE FILIAL',
A.DOCUMENTO 'HANDLE NF',
DOC.DOCUMENTODIGITADO 'DOCUMENTO', 
CONCAT('Doc: ', DOC.DOCUMENTODIGITADO) 'DOC COM LEGENDA',  
CONCAT('N° Parc: ', A.PARCELADIGITADA, ' | Total Parcelas: ', QTD_DE_PARCELAS.[QTD PARCELAS]) 'PARCELA COM LEGENDA',
DOC.AGENTEVENDAS 'HANDLE VENDEDOR',
CASE
    WHEN A.EMABERTO = 'S' THEN 'Em Aberto'
    ELSE 'Fechado'
    END AS 'Situaçâo Documento',
DOC.PESSOA 'HANDLE CLIENTE' ,
CAST(DOC.DATAEMISSAO AS DATE) 'DATA EMISSAO', 
CAST(A.DATAVENCIMENTO AS DATE) 'DATA VENCIMENTO', 
CAST(A.VCTOPRORROGADO AS DATE) 'VENCIMENTO PRORROGADO',
CAST(A.DATALIQUIDACAO AS DATE) 'DATA LIQUIDAÇÃO',
CONCAT('Data Emissão: ', FORMAT(DOC.DATAEMISSAO, 'dd/MM/yyyy'), ' | Data Prorrogado: ', FORMAT(A.VCTOPRORROGADO, 'dd/MM/yyyy') ) 'DATA COM LEGENDA',
CASE
    WHEN A.EMABERTO = 'S' AND CAST(A.VCTOPRORROGADO AS DATE) < CAST(GETDATE() AS DATE) THEN DATEDIFF(DAY, A.VCTOPRORROGADO, GETDATE())
    ELSE 0
    END AS 'DIAS DE ATRASO',
CASE
    WHEN A.EMABERTO = 'S' AND CAST(A.VCTOPRORROGADO AS DATE) < CAST(GETDATE() AS DATE) THEN 'Atrasado'
    WHEN A.EMABERTO = 'N' THEN 'Concluído'
    ELSE 'Em Dia'
    END AS 'Situação Pagamento',
CASE
    WHEN A.EMABERTO = 'S' AND CAST(A.VCTOPRORROGADO AS DATE) < CAST(GETDATE() AS DATE) THEN 2
    WHEN A.EMABERTO = 'N' THEN 0
    ELSE 1
    END AS 'Situação Pagamento - Código',
A.PARCELADIGITADA 'PARCELA', 
FORMAPGTO.NOME 'FORMA DE PAGAMENTO',
CONCAT('Forma de Pgto: ', FORMAPGTO.NOME) 'FORMA DE PAGAMENTO COM LEGENDA',
A.VALOR 'VALOR ORIGINAL',
A.ACRESCIMOS,
A.ABATIMENTOS,
A.VALORDESAGIO 'VALOR DESAGIO',
A.VALORESBAIXADOS 'VALOR ATUAL',
A.PERCENTUALMULTA 'PERCENTUAL MULTA',
A.MORADIARIA 'MORA DIARIA',
CASE
	WHEN ( A.EMABERTO = 'S' AND CAST(A.VCTOPRORROGADO AS DATE) < CAST(GETDATE() AS DATE)  ) THEN ( ((A.VALOR * (A.PERCENTUALMULTA / 100)) + A.VALOR) + ( (DATEDIFF(day, A.DATAVENCIMENTO, GETDATE())) * A.MORADIARIA)) - COALESCE(A.VALORESBAIXADOS,0)
	WHEN   A.EMABERTO = 'N' THEN ( ( COALESCE(A.VALORESBAIXADOS,0) + COALESCE(A.ACRESCIMOS,0) ) - (COALESCE(A.ABATIMENTOS,0) + COALESCE(A.VALORDESAGIO,0) ) )
	ELSE ( ( COALESCE(A.VALOR,0) + COALESCE(A.ACRESCIMOS,0) ) - (COALESCE(A.ABATIMENTOS,0) + COALESCE(A.VALORDESAGIO,0) ) ) - COALESCE(A.VALORESBAIXADOS,0)
	END AS 'VALOR TOTAL COM JUROS',
( ( COALESCE(A.VALOR,0) + COALESCE(A.ACRESCIMOS,0) ) - (COALESCE(A.ABATIMENTOS,0) + COALESCE(A.VALORDESAGIO,0) ) ) - COALESCE(A.VALORESBAIXADOS,0) 'VALOR TOTAL SEM JUROS',
QTD_DE_PARCELAS.[QTD PARCELAS] 'QTD DE PARCELAS'

FROM FN_PARCELAS A
LEFT JOIN FN_DOCUMENTOS DOC                 ON A.DOCUMENTO = DOC.HANDLE
LEFT JOIN QTD_DE_PARCELAS QTD_DE_PARCELAS   ON A.DOCUMENTO = QTD_DE_PARCELAS.[HANDLE NF] 
LEFT JOIN FN_FORMASPAGAMENTO FORMAPGTO      ON A.FORMALIQUIDACAO = FORMAPGTO.HANDLE

WHERE 
    A.VALOR > 0
AND 
    DOC.ENTRADASAIDA IN ('S') 
AND 
    DOC.TIPODEMOVIMENTO IN (1, 2)  
AND 
    DOC.DATACANCELAMENTO IS NULL
AND  
    A.DOCUMENTOSUSPENSO = 'N'
AND 
    A.PREVISAO = 'N'
AND
    DOC.PESSOA NOT IN (2237,6873,494,4210,3393,7586,4544,5812,3394,2326) -- Remove a venda entre filiais
AND
    DOC.OPERACAO != 177 --- Remove a operação "2003 - CRE - Adiantamento de Clientes"
AND FORMAPGTO.HANDLE = 3    


    UNION

SELECT 
'1'                                                         'HANDLE FILIAL',
'324001'                                                    'HANDLE NF',
'028216'                                                    'DOCUMENTO', 
'Doc: 028216'                                               'DOC COM LEGENDA',  
'N° Parc: 6 | Total Parcelas: 10'                           'PARCELA COM LEGENDA',
'4435'                                                      'HANDLE VENDEDOR',
'Em Aberto'                                                 'Situaçâo Documento',
'10247'                                                     'HANDLE CLIENTE' ,
'11/08/2022'                                                'DATA EMISSAO', 
'11/05/2022'                                                'DATA VENCIMENTO', 
'03/11/2023'                                                'VENCIMENTO PRORROGADO',
NULL                                                        'DATA LIQUIDAÇÃO',
'Data Emissão: 11/08/2022 | Data Prorrogado: 26/09/2022'    'DATA COM LEGENDA',
'345'                                                       'DIAS DE ATRASO',
'Em dia'                                                  'Situação Pagamento',
'2'                                                         'Situação Pagamento - Código',
'6'                                                         'PARCELA', 
'Boleto'                                                    'FORMA DE PAGAMENTO',
'Forma de Pgto: Boleto'                                     'FORMA DE PAGAMENTO COM LEGENDA',
'1521'                                                      'VALOR ORIGINAL',
'0'                                                         'ACRESCIMOS',
'0'                                                         'ABATIMENTOS',
'0'                                                         'VALOR DESAGIO',
'0'                                                         'VALOR ATUAL',
'2'                                                         'PERCENTUAL MULTA',
'3.8025'                                                    'MORA DIARIA',
'2863.2825'                                                 'VALOR TOTAL COM JUROS',
'1521'                                                      'VALOR TOTAL SEM JUROS',
'10'                                                        'QTD DE PARCELAS'

UNION

SELECT 
'1'                                                         'HANDLE FILIAL',
'324001'                                                    'HANDLE NF',
'028255'                                                    'DOCUMENTO', 
'Doc: 028255'                                               'DOC COM LEGENDA',  
'N° Parc: 3 | Total Parcelas: 4'                            'PARCELA COM LEGENDA',
'4435'                                                      'HANDLE VENDEDOR',
'Em Aberto'                                                 'Situaçâo Documento',
'10247'                                                     'HANDLE CLIENTE' ,
'25/01/2022'                                                'DATA EMISSAO', 
'26/03/2022'                                                'DATA VENCIMENTO', 
'07/11/2023'                                                'VENCIMENTO PRORROGADO',
NULL                                                        'DATA LIQUIDAÇÃO',
'Data Emissão: 25/01/2021 | Data Prorrogado: 26/03/2022'    'DATA COM LEGENDA',
'8'                                                       'DIAS DE ATRASO',
'Em dia'                                                  'Situação Pagamento',
'2'                                                         'Situação Pagamento - Código',
'4'                                                         'PARCELA', 
'Boleto'                                                    'FORMA DE PAGAMENTO',
'Forma de Pgto: Boleto'                                     'FORMA DE PAGAMENTO COM LEGENDA',
'958.63'                                                     'VALOR ORIGINAL',
'0'                                                         'ACRESCIMOS',
'0'                                                         'ABATIMENTOS',
'0'                                                         'VALOR DESAGIO',
'0'                                                         'VALOR ATUAL',
'2'                                                         'PERCENTUAL MULTA',
'3'                                                         'MORA DIARIA',
'1500.2825'                                                 'VALOR TOTAL COM JUROS',
'958.63'                                                    'VALOR TOTAL SEM JUROS',
'4'                                                         'QTD DE PARCELAS'


UNION

SELECT 
'1'                                                         'HANDLE FILIAL',
'324001'                                                    'HANDLE NF',
'028255'                                                    'DOCUMENTO', 
'Doc: 028255'                                               'DOC COM LEGENDA',  
'N° Parc: 2 | Total Parcelas: 4'                            'PARCELA COM LEGENDA',
'4435'                                                      'HANDLE VENDEDOR',
'Em Aberto'                                                 'Situaçâo Documento',
'10247'                                                     'HANDLE CLIENTE' ,
'25/01/2022'                                                'DATA EMISSAO', 
'26/03/2022'                                                'DATA VENCIMENTO', 
'27/10/2023'                                                'VENCIMENTO PRORROGADO',
NULL                                                        'DATA LIQUIDAÇÃO',
'Data Emissão: 25/01/2021 | Data Prorrogado: 26/03/2022'    'DATA COM LEGENDA',
'8'                                                       'DIAS DE ATRASO',
'Atrasado'                                                  'Situação Pagamento',
'2'                                                         'Situação Pagamento - Código',
'4'                                                         'PARCELA', 
'Boleto'                                                    'FORMA DE PAGAMENTO',
'Forma de Pgto: Boleto'                                     'FORMA DE PAGAMENTO COM LEGENDA',
'958.63'                                                     'VALOR ORIGINAL',
'0'                                                         'ACRESCIMOS',
'0'                                                         'ABATIMENTOS',
'0'                                                         'VALOR DESAGIO',
'0'                                                         'VALOR ATUAL',
'2'                                                         'PERCENTUAL MULTA',
'3'                                                         'MORA DIARIA',
'1500.2825'                                                 'VALOR TOTAL COM JUROS',
'958.63'                                                    'VALOR TOTAL SEM JUROS',
'4'                                                         'QTD DE PARCELAS'


FROM FN_PARCELAS A
LEFT JOIN FN_DOCUMENTOS DOC                 ON A.DOCUMENTO = DOC.HANDLE
LEFT JOIN QTD_DE_PARCELAS QTD_DE_PARCELAS   ON A.DOCUMENTO = QTD_DE_PARCELAS.[HANDLE NF] 
LEFT JOIN FN_FORMASPAGAMENTO FORMAPGTO      ON A.FORMALIQUIDACAO = FORMAPGTO.HANDLE




    )

SELECT   
CLIENTE.HANDLE,
CLIENTE.NOME CLIENTE,
A.[DOCUMENTO],
A.[PARCELA],
A.[QTD DE PARCELAS],
A.[VENCIMENTO PRORROGADO],
A.[VALOR ORIGINAL] AS 'VALOR DA PARCELA',
A.[Situaçâo Documento] AS 'SITUACAO DO DOCUMENTO',
A.[Situação Pagamento] AS 'SITUACAO DO PAGAMENTO',
CONTATOS.EMAILS

FROM PARCELAS A
LEFT JOIN GN_PESSOAS CLIENTE            ON A.[HANDLE CLIENTE] = CLIENTE.HANDLE
LEFT JOIN GN_PESSOAS VENDEDOR           ON A.[HANDLE VENDEDOR] = VENDEDOR.HANDLE
LEFT JOIN CONTATOS_TRATADOS CONTATOS      ON A.[HANDLE CLIENTE] = CONTATOS.HANDLE_CLIENTE

WHERE 
    YEAR(A.[VENCIMENTO PRORROGADO]) >= 2022  
AND A.[HANDLE FILIAL] = 1
AND CLIENTE.HANDLE = 10247


