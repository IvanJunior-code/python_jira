from jira import JIRA

# Autenticação e URL do Jira
jira_url = 'https://dominio.atlassian.net'
jira_username = 'email@dominio.com.br'
jira_api_token = ''

# Instância do cliente Jira com o token de API
jira_connection = JIRA(server=jira_url, basic_auth=(jira_username, jira_api_token))

# Usuário a ser consultado
usuario_jira = 'Ivan Edson'

# Função `search_users` para buscar o usuário pelo nome
usuarios_encontrados = JIRA.search_users(self=jira_connection, query=usuario_jira, maxResults=1)
print(f'USUÁRIO COMPLETO: {usuarios_encontrados}')

if usuarios_encontrados:
    primeiro_usuario = usuarios_encontrados[0]  # Primeiro usuário encontrado
    print(f'Nome do usuário: {primeiro_usuario.displayName}')
    print(f'Email do usuário: {primeiro_usuario.emailAddress}')
    print(f'Account ID do Jira: {primeiro_usuario.accountId}')
    print(f'Self do Jira: {primeiro_usuario.self}')
    print(f'Tipo de conta do Jira: {primeiro_usuario.accountType}')
else:
    print(f'Nenhum usuário encontrado com o nome {usuario_jira}')

# Número da issue/chamado
issue_id = 'XXXX-9999'

# Função `issue` para obter informações da issue
chamado = JIRA.issue(self=jira_connection, id=issue_id)

# Exibir informações da issue
print(f'\n\nINFORMAÇÕES DO CHAMADO')
print(f'ID da Issue: {chamado.id}')
print(f'Título da Issue: {chamado.fields.summary}')
print(f'Descrição da Issue: {chamado.fields.description}')
print(f'Tipo de Issue: {chamado.fields.issuetype.name}')
print(f'Prioridade da Issue: {chamado.fields.priority.name}')
print(f'Estado da Issue: {chamado.fields.status.name}')
print(f'Relator da Issue: {chamado.fields.reporter.displayName}')
print(f'Assignee da Issue: {chamado.fields.assignee.displayName}')


print('\n\n')

# Solicitação à API REST do Jira para obter o histórico de atividades da issue
histories = JIRA._get_json(jira_connection, 'issue/' + issue_id + '?expand=changelog', )['changelog']['histories']

# Mostrar as três últimas atividades
# ultimas_atividades = histories[-3:]
# for historico_item in ultimas_atividades:
#     print(f'Data da Atividade: {historico_item["created"]}')
#     print(f'Autor da Atividade: {historico_item["author"]["displayName"]}')
    
#     # Verifique se há comentários na atividade
#     for item in historico_item['items']:
#         if item['field'] == 'comment':
#             print(f'Comentário: {item["toString"]}')


# Lista para acumular os grupos em que o chamado já passou
lista_grupos = []

# Mostrando todas as atividades do chamado
for historico_item in histories:
    if historico_item["author"]["displayName"] != 'ScriptRunner for Jira' and \
        historico_item["author"]["displayName"] != 'JIRA_INT_ITSM' and \
        historico_item["author"]["displayName"] != 'Automation for Jira':
        print(f'Data da Atividade: {historico_item["created"]}')
        print(f'Autor da Atividade: {historico_item["author"]["displayName"]}')
        
        # Verificando se há comentários na atividade
        for item in historico_item['items']:
            if item['field'] == 'Motivo':
                print(f'Comentário: {item["toString"]}')
            if item['field'] == 'Grupo Solucionador (Portal/Agente)':
                print(f'Direcionado para o grupo: {item["toString"]}')
                lista_grupos.append(item['toString']) # adiciona os grupos em que o chamado passou
        
        print('\n\n')


# Mostra quais os grupos que o chamado já passou
print(f'Grupos em que o chamado {issue_id} passou: {lista_grupos}')
