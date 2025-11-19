import cliente_protobuf.sd_protocol_pb2 as sdpb
import socket
import time, datetime
import json
import struct

# Conexao
CHAVE_ACESSO = '538045'

def criar_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s

def enviar_tcp(socket, mensagem, protobuf_msg=False):
    msg = mensagem
    if not protobuf_msg:
        try:
            socket.sendall(bytes(msg, 'utf-8'))
            data = socket.recv(1024).decode('utf-8')
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
            header_resp = socket.recv(4)
            tamanho_resp = struct.unpack('>I', header_resp)[0]
            data = socket.recv(1024)
            #s.close()
        except Exception as e:
            print(e)
            exit()
        # print ('REPOSTA SERVIDOR: {s}'.format(s=repr(data)))

    return data


def autenticar(socket, protocolo, porta, host='3.88.99.255', chave=CHAVE_ACESSO):
    PORT = porta
    HOST = host
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S')
    protocolo = int(protocolo)

    try:
        try: 
            socket.connect((HOST, PORT))
        except:
            socket.connect(('192.168.100.4', PORT))

        if protocolo == 1: # String
            mensagem = 'AUTH|aluno_id={}|timestamp={}|FIM'.format(chave, timestamp)
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
                'aluno_id' : chave,
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
            mensagem.auth.aluno_id = CHAVE_ACESSO
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

