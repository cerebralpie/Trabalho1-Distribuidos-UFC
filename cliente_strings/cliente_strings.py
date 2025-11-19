import servidor as srv
import interface as inter

PORTA = 8080

def autenticar(socket):
    srv.autenticar(socket, 1, PORTA) # Autentica servidor strings
    
def enviar_mensagem(socket, mensagem):
    resposta = srv.enviar_tcp(socket, mensagem)
    return resposta

def menu_strings():
    while True:
        logado = False
        sessao = srv.criar_socket()
        inter.menu_login()
        resposta1 = int(input())
        
        if resposta1 not in {1,2,3,9}:
            inter.entrada_invalida()
            continue

        elif resposta1 == 1:
            print("Digite sua matricula:")
            resposta2 = str(input())
            srv.autenticar(sessao, 1, PORTA, resposta2)
            arquivo = open('cliente_strings/token.txt', 'r')
            token = arquivo.read()
            arquivo.close()
            logado = True

        elif resposta1 == 2:
            arquivo = open('cliente_strings/token.txt', 'r')
            token = arquivo.read()
            arquivo.close()
            if srv.recuperar_sessao(sessao, 1, token):
                logado = True
            else:
                continue

        while logado and True:
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
                lista_num = lista_num.split(' ')
                lista_num_tam = len(lista_num)
                lista_num_format = ''
                for i, num in enumerate(lista_num):
                    if i < (lista_num_tam - 1):
                        lista_num_format = lista_num_format + num + ','
                    else:
                        lista_num_format = lista_num_format + num

                mensagem = 'OP|token={}|operacao=soma|nums={}|FIM'.format(token, lista_num_format)
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
