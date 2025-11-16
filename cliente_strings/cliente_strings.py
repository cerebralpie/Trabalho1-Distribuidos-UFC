import servidor as srv
import interface as inter

PORTA = 8080
PROTOCOLO = 'TCP'

def autenticar():
    srv.autenticar(1, PORTA) # Autentica servidor strings
    
def enviar_mensagem(mensagem):
    resposta = srv.enviar_tcp(mensagem, PORTA)
    return resposta

def menu_strings():
    # Verificar se token ainda eh valido
    arquivo = open('cliente_strings/token.txt', 'r')
    token = arquivo.read()
    mensagem = 'OP|token={}|operacao=status|FIM'.format(token)
    status, operacoes_processadas, tempo_ativo = enviar_mensagem(mensagem)
    print('Estado do servidor: {}'.format(status))

    if status == 'None': # Autenticar e guardar novo token
        autenticar()
        token = arquivo.read()

    while True:
        inter.menu_operacoes()
        resposta = int(input())

        if resposta not in (1,2,3,4,5,9):
            inter.entrada_invalida()
            continue

        if resposta == 1: # Status servidor
            mensagem = 'OP|token={}|operacao=status|FIM'.format(token)
            enviar_mensagem(mensagem)
            inter.pressione_enter()
            continue

        elif resposta == 9:
            mensagem = 'OP|token={}|operacao=logout|FIM'.format(token)
            enviar_mensagem(mensagem)
            inter.pressione_enter()
            break
