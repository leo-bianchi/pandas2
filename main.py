import pandas as pd

participantes = pd.read_csv(
    '../csv/EXEC_FINANC_ED_BAS_2017.csv', encoding='iso-8859-1', sep=';')

censo_email = pd.read_csv('../csv/cadastro.csv', encoding='utf-8', sep=',')

cadastro_geral = pd.read_csv(
    '../csv/todas_cadastro.csv', encoding='utf-8', low_memory=False)

email_column = pd.merge(
    participantes, censo_email[['cod_inep', 'E-mail']], on='cod_inep', how='outer')

final = pd.merge(participantes, cadastro_geral[[
    'cod_inep', 'terra_indigena', 'endereco', 'num_endereco', 'complemento', 'bairro', 'cep', 'ddd', 'fone1', 'fone2', 'tipo_área']], on='cod_inep', how='left')

final[['fone1', 'ddd']] = final[['fone1', 'ddd']].fillna(
    '0').astype(float).astype(int).astype(str)

final['fone1'] = final['fone1'].replace({'0': None})

# Concatena colunas
final['fone1'] = final['ddd'] + '-' + final['fone1']
final['fone2'] = final['ddd'] + '-' + final['fone2']

# Deleta colunas
final.drop(['ddd'], axis=1, inplace=True)

final[['bairro', 'endereco']] = final[[
    'bairro', 'endereco']].apply(lambda x: x.str.strip())

final['endereco_escola'] = final['endereco'] + ' ' + \
    final['num_endereco'] + '. ' + final['bairro']

final.drop(['num_endereco', 'bairro',
            'DT_INI_VINC_DIR', 'endereco'], axis=1, inplace=True)

final['email'] = email_column['E-mail']

final.columns = ['uf', 'nome_municipio', 'cod_municipio', 'nome_escola', 'cod_inep', 'qtd_alunos', 'rede', 'cnpj_uex', 'nome_uex',
                 'dirigente', 'custeio', 'capital', 'complemento_area', 'complemento_zona', 'cep', 'fone1', 'fone2', 'tipo_zona', 'endereco_escola', 'email']

final = final[['uf', 'nome_municipio', 'cod_municipio', 'rede', 'nome_escola', 'tipo_zona', 'complemento_area', 'complemento_zona', 'cod_inep', 'qtd_alunos',
               'endereco_escola', 'cep', 'fone1', 'fone2', 'email', 'cnpj_uex', 'nome_uex', 'dirigente', 'custeio', 'capital']]

final['cep'] = final['cep'].fillna('00000000').astype(int).astype(str).apply(lambda x: '{0:0>8}'.format(x))
final['cep'] = final['cep'].replace({'00000000': None})

final.to_csv('../csv/cadastros_pdde.csv', encoding='iso-8859-1')
