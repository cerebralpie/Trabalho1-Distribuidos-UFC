import socket
import time, datetime
import json

# Conexao
CHAVE_ACESSO = '538045'

def enviar_tcp(protocolo, mensagem, porta, host='3.88.99.255'):
    PORT = porta
    HOST = host
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    msg = mensagem
    if protocolo == 1: # String
        try:
            s.sendall(bytes(msg, 'utf-8'))
            data = s.recv(1024).decode('utf-8')
            s.close()
        except Exception as e:
            print(e)
            exit()
        # print ('REPOSTA SERVIDOR: {s}'.format(s=repr(data)))
        return data

    elif protocolo == 2: # Json
        try:
            s.sendall(bytes(msg, 'utf-8'))
            data = s.recv(1024).decode('utf-8')
            s.close()
        except Exception as e:
            print(e)
            exit()
        # print ('REPOSTA SERVIDOR: {s}'.format(s=repr(data)))
        return data


def autenticar(protocolo, porta, chave=CHAVE_ACESSO):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S')
    protocolo = int(protocolo)

    try:
        if protocolo == 1: # String
            mensagem = 'AUTH|aluno_id={}|timestamp={}|FIM'.format(chave, timestamp)
            print(mensagem)
            resposta = enviar_tcp(1, mensagem, porta)
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

            resposta = enviar_tcp(2, mensagem, porta)
            resposta = json.loads(resposta)
            print(resposta)
            token = resposta['token']

            arquivo = open('cliente_json/token.txt', 'w')

        elif protocolo == 3: # Protobuf
            arquivo = open('cliente_protobuf/token.txt', 'w')

        else:
            raise Exception('Operacao Invalida!')
        
        arquivo.write(token)
        arquivo.close()

    except Exception as e:
        print(e)
        exit()

    print('Autenticado com sucesso!')

