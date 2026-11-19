import os

from assistente import Assistente, ler_opcao
from base_conhecimento import BaseConhecimento

# garante que os caminhos "data/..." funcionem de qualquer pasta
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("data", exist_ok=True)


def menu(assistente):
    print(f"\nOlá! Eu sou o {assistente.nome}.")
    print("Tiro dúvidas de pessoas idosas sobre saúde, transporte e direitos.")
    print("Nunca digite nome, CPF, telefone ou e-mail.")

    while True:
        print("\n===== MENU =====")
        print("1 - Fazer uma pergunta")
        print("2 - Navegar por categorias")
        print("3 - Ver indicadores")
        print("4 - Exportar atendimentos (CSV)")
        print("0 - Sair")
        opcao = ler_opcao("Escolha uma opção: ", 4)

        if opcao == 1:
            assistente.perguntar()
        elif opcao == 2:
            assistente.navegar()
        elif opcao == 3:
            assistente.indicadores()
        elif opcao == 4:
            assistente.exportar_csv()
        else:
            assistente.avaliar()
            print("Até logo!")
            break


def main():
    base = BaseConhecimento("data/base_conhecimento.json")
    if base.carregar():
        print(f"{len(base.orientacoes)} orientações carregadas.")
    else:
        print("O assistente vai abrir sem a base. Corrija o arquivo e reinicie.")

    assistente = Assistente("Citizen Assist AI", base)
    try:
        menu(assistente)
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")


if __name__ == "__main__":
    main()
