"""Chat do módulo de energia no terminal.

Uso:  python app_cli.py
"""
import re

from energia.assistente import AssistenteEnergia


def limpar_markdown(t):
    return re.sub(r"\*\*(.+?)\*\*", r"\1", t)


def main():
    bot = AssistenteEnergia()
    print(limpar_markdown(bot.responder("ajuda")))
    print("\n(Digite 'sair' para encerrar.)\n")
    while True:
        try:
            msg = input("Você: ")
        except (EOFError, KeyboardInterrupt):
            break
        if msg.strip().lower() in {"sair", "exit", "quit"}:
            break
        print("\nAssistente:\n" + limpar_markdown(bot.responder(msg)) + "\n")
    print("Até logo! 💡")


if __name__ == "__main__":
    main()
