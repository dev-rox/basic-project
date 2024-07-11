# Raul Oliveira Xavier da Silva
# Análise e Desenvolvimento de Sistemas

import json


def exibir_menu_principal():  # lógica completa do menu principal que irá retornar a base de dados
    opcoes_principais = {
        1: "estudantes",
        2: "disciplinas",
        3: "professores",
        4: "turmas",
        5: "matriculas",
        0: "sair"
    }

    while True:
        print("\n--- Menu Principal ---")
        for chave, valor in opcoes_principais.items():
            print(f"{chave}: {valor.capitalize()}")

        try:
            opcao_desejada = int(input("Insira o número da opção desejada: "))
            if opcao_desejada == 0:
                print("\nO app será encerrado, volte sempre!")
                return "sair"
            elif opcao_desejada in opcoes_principais.keys():
                print(f"\nVocê escolheu a opção [{opcoes_principais.get(opcao_desejada)}]")
                return str(opcoes_principais.get(opcao_desejada) + ".json")
            else:
                print("\nOpção inválida. Por favor, insira um número de 0 até 5.")
        except ValueError:
            print("\nOpção inválida. Por favor, insira um número.")


def exibir_menu_operacoes():  # Lógica completa do menu de operaçoes que irá retornar a operação selecionada
    operacoes = {
        1: "incluir",
        2: "listar",
        3: "atualizar",
        4: "excluir",
        0: "voltar"
    }
    while True:
        print("\n--- Menu Operações ---")
        for chave, valor in operacoes.items():
            print(f"{chave}: {valor.capitalize()}")
        try:
            operacao_desejada = int(input("Insira o número da operação desejada: "))
            if operacao_desejada == 0:
                print("\nRetornando ao menu principal!")
                return "sair"
            elif operacao_desejada in operacoes.keys():
                print(f"\nVocê escolheu a opção [{operacoes.get(operacao_desejada).capitalize()}]")
                return str(operacoes.get(operacao_desejada))
            else:
                print("\nOpção inválida. Por favor, insira um número de 0 até 4.")
        except ValueError:
            print("\nOpção inválida. Por favor, insira um número.")


def carregar_arquivo(arquivo):  # Carregando os dados do arquivo json, caso ele exista
    try:
        with open(arquivo, "r") as f:
            loaded_file = json.load(f)
            return loaded_file
    except FileNotFoundError:
        print(f"O arquivo '{arquivo}' não foi encontrado.")
        return []


def salvar_arquivo(lista, arquivo):  # Salvando os dados no arquivo json selecionado, caso não exista um novo arquivo é criado
    with open(arquivo, "w", encoding='utf-8') as f:
        json.dump(lista, f, ensure_ascii=False)


def add_registro(database):  # Lógica completa para adicionar qualquer tipo de registo em diferentes bases
    base_atual = carregar_arquivo(database)

    if database == "estudantes.json" or database == "professores.json":
        item = {
            "codigo": None,
            "nome": None,
            "cpf": None
        }
    elif database == "disciplinas.json":
        item = {
            "codigo": None,
            "disciplina": None
        }
    elif database == "turmas.json":
        item = {
            "codigo": None,
            "professor": None,
            "disciplina": None
        }
    elif database == "matriculas.json":
        item = {
            "codigo": None,
            "estudante": None
        }

    for chave in item:
        if chave == 'codigo':
            while True:
                try:
                    codigo = int(input(f"Informe o {chave} (Apenas números): "))
                    # Verifica se ja existe um código igal nos registros
                    if any(d['codigo'] == codigo for d in base_atual):
                        print("Código já existente. Por favor, insira um novo código.")
                    else:
                        item[chave] = codigo
                        break
                except ValueError:
                    print("Entrada inválida. Por favor, insira um número inteiro.")
        else:
            item[chave] = input(f"Informe o {chave}: ")

    base_atual.append(item)

    salvar_arquivo(base_atual, database)
    print("\nRegistro incluído")

    input("\nPressione ENTER para continuar.")


def mostrar_registros(database):  # lógica para mostrar uma lista de qualquer tipo de registro
    loaded_list = carregar_arquivo(database)
    if len(loaded_list) == 0:
        print("--- Não há registros ---")
    else:
        print("\n--- Lista de Registros ---")
        for i in loaded_list:
            for chave, valor in i.items():
                print(f"- {chave.capitalize()}: {valor}", end=' ')
    print("\n")

    input("Pressione ENTER para continuar.")


def get_input(tipo):  # Função que irá nos ajudar a manter o mesmo tipo de dados quando estivermos atualizando os valores das chaves
    while True:
        valor = input()
        try:
            return tipo(valor)
        except ValueError:
            print("Valor inválido. Por favor, informe outro valor: ")


def atualizar_registro(database):  # lógica para atualizar os registros com base no código, enquanto mantemos a tipagem de cada valor no dicionário
    while True:
        try:
            cod = int(input("\nInforme o código: "))
        except ValueError:
            print("\nUtilize apenas números para informar o código.")
            continue
        break
    lista = carregar_arquivo(database)

    for item in lista:
        if item["codigo"] == cod:
            confirm = input("Registro encontrado, deseja atualizar? 'S/N': ")
            if confirm.lower() == "s":
                for campo in item:
                    # Solicitar ao usuário para atualizar o campo
                    print(f"Insira um novo valor para {campo} (atual: {item[campo]}): ", end="")
                    novo_valor = get_input(type(item[campo]))
                    # Atualizar o campo com o novo valor
                    item[campo] = novo_valor
                salvar_arquivo(lista, database)
                print("Registro atualizado!")
                input("\nPressione ENTER para continuar.")
                return
    # Se chegou até aqui, é porque não encontrou o registro ou houve desistência
    print("\nNenhuma alteração efetuada.")
    input("\nPressione ENTER para continuar.")


def excluir_registro(database):  # lógica para excluir um registo com base no código.
    while True:
        try:
            cod = int(input("\nInforme o código do registro que deseja excluir: "))
        except ValueError:
            print("\nUtilize apenas números para informar o código.")
            continue
        break

    remover = None

    lista = carregar_arquivo(database)

    for item in lista:
        if item["codigo"] == cod:
            confirm = input("Registro encontrado, deseja excluir? S/N: ")
            if confirm.lower() == "s":
                remover = item
    if remover:
        lista.remove(remover)
        salvar_arquivo(lista, database)
        print("Registro removido!")
    else:
        print("Registro não encontrado")
    input("Pressione ENTER para continuar.")


# inicio da execução do código
while True:
    database = exibir_menu_principal()

    if database == "sair":
        break

    while True:
        operacao = exibir_menu_operacoes()
        if operacao == "sair":
            break
        elif operacao == "incluir":
            add_registro(database)
        elif operacao == "listar":
            mostrar_registros(database)
        elif operacao == "atualizar":
            atualizar_registro(database)
        elif operacao == "excluir":
            excluir_registro(database)
# fim
