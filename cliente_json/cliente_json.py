import servidor as srv
import interface as inter

import json
import time, datetime

PORTA = 8081
PROTOCOLO = 'TCP'


def autenticar(socket):
    srv.autenticar(socket, 2, PORTA) # Autentica servidor json
    
def enviar_mensagem(socket, mensagem):
    resposta = srv.enviar_tcp(socket, mensagem)
    return resposta

def menu_json():
    # Verificar se token ainda eh valido
    #arquivo = open('cliente_json/token.txt', 'r')
    #token = arquivo.read()
    #arquivo.close()
    #mensagem = {
    #    'tipo' : 'operacao',
    #    'token' : token,
    #    'operacao' : 'status'
    #}
    #mensagem = json.dumps(mensagem)

    #res_servidor = enviar_mensagem(mensagem)
    #res_servidor = json.loads(res_servidor)

    #if res_servidor['sucesso'] == False:
    #    autenticar()
    #    arquivo = open('cliente_json/token.txt', 'r')
    #    token = arquivo.read()
    #    arquivo.close()
    
    sessao = srv.criar_socket()
    autenticar(sessao)
    arquivo = open('cliente_json/token.txt', 'r')
    token = arquivo.read()
    arquivo.close()

    while True:
        inter.menu_operacoes()
        resposta = int(input())

        if resposta not in (1,2,3,4,5,9):
            inter.entrada_invalida()
            continue

        if resposta == 1: # Status servidor
            mensagem = {
                'tipo' : 'operacao',
                'token' : token,
                'operacao' : 'status'
            }
            
            #'OP|token={}|operacao=status|FIM'.format(token)
            mensagem = json.dumps(mensagem)
            res_servidor = enviar_mensagem(sessao, mensagem)
            res_servidor = json.loads(res_servidor)
            print('Resposta do servidor:')
            print(res_servidor)
            inter.pressione_enter()
            continue

        elif resposta == 2: # Timestamp do servidor
            mensagem = {
                'tipo' : 'operacao',
                'token' : token,
                'operacao' : 'timestamp'
            }
            #mensagem = 'OP|token={}|operacao=timestamp|FIM'.format(token)
            mensagem = json.dumps(mensagem)
            res_servidor = enviar_mensagem(sessao, mensagem)
            res_servidor = json.loads(res_servidor)
            print('Resposta do servidor:')
            print(res_servidor)
            inter.pressione_enter()
            continue

        elif resposta == 3: # Historico de uso
            mensagem = {
                'tipo' : 'operacao',
                'token' : token,
                'operacao' : 'historico'
            }
            #mensagem = 'OP|token={}|operacao=historico|FIM'.format(token)
            mensagem = json.dumps(mensagem)
            res_servidor = enviar_mensagem(sessao, mensagem)
            res_servidor = json.loads(res_servidor)
            print('Resposta do servidor:')
            print(res_servidor)
            inter.pressione_enter()
            continue

        elif resposta == 4: # Echo
            print('\n')
            print('Digite a mensagem a ser enviada:')
            mensagem_echo = input()
            mensagem = {
                'tipo' : 'operacao',
                'token' : token,
                'operacao' : 'echo',
                'parametros' : {
                    'mensagem' : mensagem_echo
                }
            }
            #mensagem = 'OP|token={}|operacao=echo|mensagem={}|FIM'.format(token, mensagem_echo)
            mensagem = json.dumps(mensagem)
            res_servidor = enviar_mensagem(sessao, mensagem)
            res_servidor = json.loads(res_servidor)
            print('Resposta do servidor:')
            print(res_servidor)
            inter.pressione_enter()
            continue

        elif resposta == 5: # Soma
            print('\n')
            print('Digite os numeros a serem enviados (separados por espaço):')
            lista_num = input()
            lista_num = lista_num.split(' ')
            mensagem = {
                'tipo' : 'operacao',
                'token' : token,
                'operacao' : 'soma',
                'parametros' : {
                    'numeros' : lista_num
                }
            }
            #mensagem = 'OP|token={}|operacao=soma|numeros=(1 2 3)|FIM'.format(token)
            mensagem = json.dumps(mensagem)
            res_servidor = enviar_mensagem(sessao, mensagem)
            res_servidor = json.loads(res_servidor)
            print('Resposta do servidor:')
            print(res_servidor)
            inter.pressione_enter()
            continue

        elif resposta == 9:
            mensagem = {
                'tipo' : 'operacao',
                'token' : token,
                'operacao' : 'logout'
            }
            #mensagem = 'OP|token={}|operacao=logout|FIM'.format(token)
            mensagem = json.dumps(mensagem)
            res_servidor = enviar_mensagem(sessao, mensagem)
            res_servidor = json.loads(res_servidor)
            print('Resposta do servidor:')
            print(res_servidor)
            inter.pressione_enter()
            break
