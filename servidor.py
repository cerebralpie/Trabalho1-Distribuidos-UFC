import cliente_protobuf.sd_protocol_pb2 as sdpb
import interface as inter
import socket
import time, datetime
import json
import struct
import sys

def criar_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s

def enviar_tcp(socket, mensagem, protobuf_msg=False):
    inicio_tempo = time.perf_counter()

    msg = mensagem
    if not protobuf_msg:
        try:
            socket.sendall(bytes(msg, 'utf-8'))
            print('Enviado pacote de {} bytes'.format(sys.getsizeof(msg)))
            data = socket.recv(1024).decode('utf-8')
            print('Recebido pacote de {} bytes'.format(sys.getsizeof(data)))
            #s.close()
        except Exception as e:
            print(e)
            exit()
        # print ('REPOSTA SERVIDOR: {s}'.format(s=repr(data)))
    
    else:
        tamanho = len(msg)
        header = struct.pack('>I', tamanho)
        pacote = header + msg
        try:
            socket.sendall(pacote)
            print('Enviado pacote de {} bytes'.format(sys.getsizeof(pacote)))
            header_resp = socket.recv(4)
            tamanho_resp = struct.unpack('>I', header_resp)[0]
            data = socket.recv(1024)
            print('Recebido pacote de {} bytes'.format(sys.getsizeof(data)))
            #s.close()
        except Exception as e:
            print(e)
            exit()
        # print ('REPOSTA SERVIDOR: {s}'.format(s=repr(data)))

    fim_tempo = time.perf_counter()
    total_tempo = fim_tempo - inicio_tempo
    total_tempo = total_tempo*1000 # Para ficar em ms
    print(f'Tempo da comunicação: {total_tempo:.6f} ms')

    return data

def autenticar(socket, protocolo, porta, matricula, host='3.88.99.255'):
    PORT = porta
    HOST = host
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S')
    protocolo = int(protocolo)

    try:
        socket.connect((HOST, PORT))

        if protocolo == 1: # String
            mensagem = 'AUTH|aluno_id={}|timestamp={}|FIM'.format(matricula, timestamp)
            print(mensagem)
            resposta = enviar_tcp(socket, mensagem)
            print(resposta)
            split1 = resposta.split('|')
            split2 = split1[1].split('=')
            token = split2[1]
            arquivo = open('cliente_strings/token.txt', 'w')

        elif protocolo == 2: # Json
            mensagem = {
                'tipo' : 'autenticar',
                'aluno_id' : matricula,
                'timestamp' : timestamp, 
            }
            mensagem = json.dumps(mensagem)
            print(mensagem)

            resposta = enviar_tcp(socket, mensagem)
            resposta = json.loads(resposta)
            print(resposta)
            token = resposta['token']

            arquivo = open('cliente_json/token.txt', 'w')

        elif protocolo == 3: # Protobuf
            mensagem = sdpb.Requisicao()
            mensagem.auth.aluno_id = matricula
            mensagem.auth.timestamp_cliente = timestamp
            mensagem = mensagem.SerializeToString()
            print(mensagem)

            resposta = enviar_tcp(socket, mensagem, protobuf_msg=True)
            resposta_pb = sdpb.Resposta()
            resposta_pb.ParseFromString(resposta)
            print(resposta_pb)
            token = resposta_pb.ok.dados.get('token')

            arquivo = open('cliente_protobuf/token.txt', 'w')

        else:
            raise Exception('Operacao Invalida!')
        
        arquivo.write(token)
        arquivo.close()

    except Exception as e:
        print(e)
        exit()

    print('Autenticado com sucesso!')


def recuperar_sessao(socket, protocolo, token):
    if protocolo == 1: # Strings
        # Verificar se token ainda eh valido
        mensagem = 'OP|token={}|operacao=status|FIM'.format(token)
        print(mensagem)
        resposta = enviar_tcp(socket, mensagem)
        print(resposta)
        resposta = resposta.split('|')
        print('Estado do servidor: {}'.format(resposta[0]))

        if resposta[0] == 'ERROR': # Autenticar e guardar novo token
            print('Sem sessoes para recuperar, realize novo login!')
            inter.pressione_enter()
            return False
        
    if protocolo == 2: # JSON
        mensagem = {
                'tipo' : 'operacao',
                'token' : token,
                'operacao' : 'status'
            }
            
        mensagem = json.dumps(mensagem)
        res_servidor = enviar_tcp(socket, mensagem)
        res_servidor = json.loads(res_servidor)

        if res_servidor['sucesso'] == False:
            print('Sem sessoes para recuperar, realize novo login!')
            inter.pressione_enter()
            return False
        
    if protocolo == 3: # Protobuf
        mensagem = sdpb.Requisicao()
        mensagem.operacao.token = token
        mensagem.operacao.operacao = 'status'
        mensagem = mensagem.SerializeToString()
        print(mensagem)

        resposta = enviar_tcp(socket, mensagem)
        resposta_pb = sdpb.Resposta()
        resposta_pb.ParseFromString(resposta)
        print(resposta_pb)
        return False
        
        #if resposta_pb. == False:
        #    print('Sem sessoes para recuperar, realize novo login!')
        #    inter.pressione_enter()
        #    return False

    return True
