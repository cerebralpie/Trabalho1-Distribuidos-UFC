import servidor as srv
import interface as inter

PORTA = 8080

def autenticar(socket):
    srv.autenticar(socket, 1, PORTA) # Autentica servidor strings
    
def enviar_mensagem(socket, mensagem):
    resposta = srv.enviar_tcp(socket, mensagem)
    return resposta

def menu_strings():
    # Verificar se token ainda eh valido
    #arquivo = open('cliente_strings/token.txt', 'r')
    #token = arquivo.read()
    #arquivo.close()
    #mensagem = 'OP|token={}|operacao=status|FIM'.format(token)
    #resposta = enviar_mensagem(mensagem)
    #resposta = resposta.split('|')
    #print('Estado do servidor: {}'.format(resposta[0]))

    #if resposta[0] == 'ERROR': # Autenticar e guardar novo token
    #    autenticar()
    #    arquivo = open('cliente_strings/token.txt', 'r')
    #    token = arquivo.read()
    #    arquivo.close()

    sessao = srv.criar_socket()
    autenticar(sessao)
    arquivo = open('cliente_strings/token.txt', 'r')
    token = arquivo.read()
    arquivo.close()

    while True:
        inter.menu_operacoes()
        resposta = int(input())

        if resposta not in (1,2,3,4,5,9):
            inter.entrada_invalida()
            continue

        if resposta == 1: # Status servidor
            mensagem = 'OP|token={}|operacao=status|FIM'.format(token)
            res_servidor = enviar_mensagem(sessao, mensagem)
            print('Resposta do servidor:')
            print(res_servidor)
            inter.pressione_enter()
            continue

        elif resposta == 2: # Timestamp do servidor
            mensagem = 'OP|token={}|operacao=timestamp|FIM'.format(token)
            res_servidor = enviar_mensagem(sessao, mensagem)
            print('Resposta do servidor:')
            print(res_servidor)
            inter.pressione_enter()
            continue

        elif resposta == 3: # Historico de uso
            mensagem = 'OP|token={}|operacao=historico|FIM'.format(token)
            res_servidor = enviar_mensagem(sessao, mensagem)
            print('Resposta do servidor:')
            print(res_servidor)
            inter.pressione_enter()
            continue

        elif resposta == 4: # Echo
            print('\n')
            print('Digite a mensagem a ser enviada:')
            mensagem_echo = input()
            mensagem = 'OP|token={}|operacao=echo|mensagem={}|FIM'.format(token, mensagem_echo)
            res_servidor = enviar_mensagem(sessao, mensagem)
            print('Resposta do servidor:')
            print(res_servidor)
            inter.pressione_enter()
            continue

        elif resposta == 5: # Soma
            print('\n')
            print('Digite os numeros a serem enviados (separados por espaço):')
            lista_num = input()
            #lista_num = lista_num.split(' ')
            print(lista_num)
            print(repr(lista_num))
            mensagem = 'OP|token={}|operacao=soma|numeros={}|FIM'.format(token, lista_num)
            print(mensagem)
            res_servidor = enviar_mensagem(sessao, mensagem)
            print('Resposta do servidor:')
            print(res_servidor)
            inter.pressione_enter()
            continue

        elif resposta == 9:
            mensagem = 'OP|token={}|operacao=logout|FIM'.format(token)
            res_servidor = enviar_mensagem(sessao, mensagem)
            print('Resposta do servidor:')
            print(res_servidor)
            inter.pressione_enter()
            break
