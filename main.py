# Universidade Federal do Ceará
# Disciplina de Sistemas Distribuídos
# Semestre 2025.2
# Eduardo Monteiro de Sousa

import servidor as srv
import cliente_json.cliente_json as cjson
import cliente_protobuf.cliente_protobuf as cpb
import cliente_strings.cliente_strings as cstr
import interface as inter

import time

def main():
    while True:
        inter.menu_principal()
        resposta1 = int(input())

        if resposta1 not in {1,2,3,9}:
            inter.entrada_invalida()
            continue

        elif resposta1 == 1:
            cstr.menu_strings()

        elif resposta1 == 2:
            cjson.menu_json()

        elif resposta1 == 2:
            cjson.menu_json()

        elif resposta1 == 9:
            break

if __name__ == '__main__':
    main()
