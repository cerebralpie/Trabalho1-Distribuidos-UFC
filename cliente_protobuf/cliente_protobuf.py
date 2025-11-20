import servidor as srv
import interface as inter
import cliente_protobuf.sd_protocol_pb2 as sdpb

PORTA = 8082

def autenticar(socket, matricula):
    srv.autenticar(socket, 3, PORTA, matricula) # Autentica servidor strings
    
def enviar_mensagem(socket, mensagem):
    resposta = srv.enviar_tcp(socket, mensagem, protobuf_msg=True)
    return resposta

def menu_protobuf():
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
            srv.autenticar(sessao, 3, PORTA, resposta2)
            arquivo = open('cliente_protobuf/token.txt', 'r')
            token = arquivo.read()
            arquivo.close()
            logado = True

        elif resposta1 == 2:
            arquivo = open('cliente_protobuf/token.txt', 'r')
            token = arquivo.read()
            arquivo.close()
            if srv.recuperar_sessao(sessao, 3, token):
                logado = True
            else:
                continue
        
        elif resposta1 == 9:
            break

        while logado and True:
            inter.menu_operacoes()
            resposta = int(input())

            if resposta not in (1,2,3,4,5,9):
                inter.entrada_invalida()
                continue

            if resposta == 1: # Status servidor
                mensagem = sdpb.Requisicao()
                mensagem.operacao.token = token
                mensagem.operacao.operacao = 'status'
                mensagem = mensagem.SerializeToString()
                print(mensagem)

                resposta = enviar_mensagem(sessao, mensagem)
                resposta_pb = sdpb.Resposta()
                resposta_pb.ParseFromString(resposta)
                #mensagem = 'OP|token={}|operacao=status|FIM'.format(token)
                #res_servidor = enviar_mensagem(sessao, mensagem)
                print('Resposta do servidor:')
                print(resposta_pb)
                inter.pressione_enter()
                continue

            elif resposta == 2: # Timestamp do servidor
                mensagem = sdpb.Requisicao()
                mensagem.operacao.token = token
                mensagem.operacao.operacao = 'timestamp'
                mensagem = mensagem.SerializeToString()
                print(mensagem)

                resposta = enviar_mensagem(sessao, mensagem)
                resposta_pb = sdpb.Resposta()
                resposta_pb.ParseFromString(resposta)
                #mensagem = 'OP|token={}|operacao=status|FIM'.format(token)
                #res_servidor = enviar_mensagem(sessao, mensagem)
                print('Resposta do servidor:')
                print(resposta_pb)
                inter.pressione_enter()
                continue

            elif resposta == 3: # Historico de uso
                mensagem = sdpb.Requisicao()
                mensagem.operacao.token = token
                mensagem.operacao.operacao = 'historico'
                mensagem = mensagem.SerializeToString()
                print(mensagem)

                resposta = enviar_mensagem(sessao, mensagem)
                resposta_pb = sdpb.Resposta()
                resposta_pb.ParseFromString(resposta)
                #mensagem = 'OP|token={}|operacao=status|FIM'.format(token)
                #res_servidor = enviar_mensagem(sessao, mensagem)
                print('Resposta do servidor:')
                print(resposta_pb)
                inter.pressione_enter()
                continue

            elif resposta == 4: # Echo
                print('\n')
                print('Digite a mensagem a ser enviada:')
                mensagem_echo = input()
                parametros = {
                    'mensagem' : mensagem_echo
                }
                mensagem = sdpb.Requisicao()
                mensagem.operacao.token = token
                mensagem.operacao.operacao = 'echo'
                mensagem.operacao.parametros.update(parametros)
                mensagem = mensagem.SerializeToString()
                print(mensagem)

                resposta = enviar_mensagem(sessao, mensagem)
                resposta_pb = sdpb.Resposta()
                resposta_pb.ParseFromString(resposta)
                #mensagem = 'OP|token={}|operacao=status|FIM'.format(token)
                #res_servidor = enviar_mensagem(sessao, mensagem)
                print('Resposta do servidor:')
                print(resposta_pb)
                inter.pressione_enter()
                continue

            elif resposta == 5: # Soma
                print('\n')
                print('Digite os numeros a serem enviados (separados por espaço):')
                lista_num = input()
                lista_num = lista_num.split(' ')
                lista_num_format = ""
                lista_tam = len(lista_num)
                for i, num in enumerate(lista_num):
                    if i < (lista_tam - 1):
                        lista_num_format = lista_num_format + str(num) + ','
                    else:
                        lista_num_format = lista_num_format + str(num)

                print(lista_num_format)
                parametros = {
                    'numeros' : lista_num_format
                }
                mensagem = sdpb.Requisicao()
                mensagem.operacao.token = token
                mensagem.operacao.operacao = 'soma'
                mensagem.operacao.parametros.update(parametros)
                mensagem = mensagem.SerializeToString()
                print(mensagem)

                resposta = enviar_mensagem(sessao, mensagem)
                resposta_pb = sdpb.Resposta()
                resposta_pb.ParseFromString(resposta)
                #mensagem = 'OP|token={}|operacao=status|FIM'.format(token)
                #res_servidor = enviar_mensagem(sessao, mensagem)
                print('Resposta do servidor:')
                print(resposta_pb)
                inter.pressione_enter()
                continue

            elif resposta == 9:
                mensagem = 'OP|token={}|operacao=logout|FIM'.format(token)
                res_servidor = enviar_mensagem(sessao, mensagem)
                print('Resposta do servidor:')
                print(res_servidor)
                inter.pressione_enter()
                break

