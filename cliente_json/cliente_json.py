import servidor as srv
import interface as inter

import json
import time, datetime

PORTA = 8081
PROTOCOLO = 'TCP'


def autenticar():
    srv.autenticar(2, PORTA) # Autentica servidor json
    
def enviar_mensagem(mensagem):
    resposta = srv.enviar_tcp(2, mensagem, PORTA)
    return resposta

def menu_json():
    # Verificar se token ainda eh valido
    arquivo = open('cliente_json/token.txt', 'r')
    token = arquivo.read()
    arquivo.close()
    mensagem = {
        'tipo' : 'operacao',
        'token' : token,
        'operacao' : 'status'
    }
    mensagem = json.dumps(mensagem)

    res_servidor = enviar_mensagem(mensagem)
    res_servidor = json.loads(res_servidor)

    if res_servidor['sucesso'] == False:
        autenticar()
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
            res_servidor = enviar_mensagem(mensagem)
            res_servidor = json.loads(res_servidor)
            print('Resposta do servidor:')
            print(res_servidor)
            inter.pressione_enter()
            continue

        elif resposta == 9:
            mensagem = 'OP|token={}|operacao=logout|FIM'.format(token)
            enviar_mensagem(mensagem)
            inter.pressione_enter()
            break
