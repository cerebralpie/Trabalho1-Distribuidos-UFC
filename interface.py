def menu_login():
    print('\n')
    print('Bem vindo! O que deseja fazer?')
    print('\n')
    print('1 - Novo Login')
    print('2 - Restaurar Sessão')
    print('9 - sair')

def menu_principal():
    print('\n')
    print('Olá, usuário! Escolha um protocolo:')
    print('\n')
    print('1 - Mensagem String')
    print('2 - Mensagem JSON')
    print('3 - Mensagem Protobuf')
    print('9 - Sair')

def menu_operacoes():
    print('\n')
    print('Escolha uma operacao:')
    print('1 - Status do servidor')
    print('2 - Timestamp do servidor')
    print('3 - Histórico de uso')
    print('4 - Echo')
    print('5 - Soma')
    print('9 - Logout')

def pressione_enter():
    print('Pressione ENTER para continuar...')
    input()

def entrada_invalida():
    print('\n')
    print('Entrada invalida!')
    pressione_enter()