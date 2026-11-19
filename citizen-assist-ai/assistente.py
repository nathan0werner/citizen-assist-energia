import csv
import json
import time
from datetime import datetime

from base_conhecimento import MINIMO_ENCONTRADO, nivel_confianca

CAMINHO_HISTORICO = "data/historico.json"
CAMINHO_AVALIACOES = "data/avaliacoes.json"
CAMINHO_CSV = "data/atendimentos.csv"

CAMPOS_CSV = ["data", "origem", "pergunta", "id_orientacao",
              "encontrou", "ajudou", "tentativas", "tempo_segundos"]


# ---------- funções auxiliares de entrada (nunca encerram o programa) ----------

def ler_opcao(mensagem, maximo):
    """Lê um número entre 0 e maximo. Repete até a entrada ser válida."""
    while True:
        texto = input(mensagem).strip()
        if texto == "":
            print("Resposta vazia. Digite um número.")
            continue
        if not texto.isdigit():
            print("Digite apenas números.")
            continue
        numero = int(texto)
        if numero < 0 or numero > maximo:
            print(f"Opção fora da faixa. Escolha entre 0 e {maximo}.")
            continue
        return numero


def ler_sim_nao(mensagem):
    """Lê 's' ou 'n'. Devolve True para sim e False para não."""
    while True:
        texto = input(mensagem).strip().lower()
        if texto in ("s", "sim"):
            return True
        if texto in ("n", "nao", "não"):
            return False
        print("Resposta inválida. Digite s ou n.")


def contem_dado_pessoal(texto):
    """True se o texto tiver 8 ou mais dígitos (CPF, telefone...) ou @ (e-mail)."""
    digitos = sum(1 for c in texto if c.isdigit())
    return digitos >= 8 or "@" in texto


def ler_json_lista(caminho):
    """Lê um arquivo JSON que contém uma lista. Se faltar ou estiver corrompido, devolve []."""
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return dados if isinstance(dados, list) else []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Aviso: '{caminho}' estava corrompido. Começando uma lista nova.")
        return []


def salvar_json(caminho, dados):
    try:
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
    except OSError as erro:
        print(f"Erro ao salvar '{caminho}': {erro}")


class Assistente:
    """Conversa com o cidadão, guarda o histórico e calcula indicadores."""

    def __init__(self, nome, base):
        self.nome = nome
        self.base = base                                  # composição: objeto BaseConhecimento
        self.historico = ler_json_lista(CAMINHO_HISTORICO)
        self.avaliacoes = ler_json_lista(CAMINHO_AVALIACOES)

    # ------------------------------ atendimento ------------------------------

    def base_disponivel(self):
        if not self.base.orientacoes:
            print("A base de conhecimento não está disponível no momento.")
            return False
        return True

    def mostrar_resultado(self, resultados):
        """Exibe a melhor orientação e até duas alternativas. Devolve as alternativas."""
        pontos, melhor = resultados[0]
        print(f"\nConfiança da resposta: {nivel_confianca(pontos)} ({pontos} pontos)")
        melhor.exibir()

        alternativas = [(p, o) for p, o in resultados[1:3] if p >= MINIMO_ENCONTRADO]
        if alternativas:
            print("Outras orientações que podem ajudar:")
            for i, (p, o) in enumerate(alternativas, start=1):
                print(f"  {i} - {o.titulo} ({p} pontos)")
            print()
        return alternativas

    def perguntar(self):
        """Atendimento por pergunta em texto livre."""
        if not self.base_disponivel():
            return

        inicio = time.time()
        tentativas = 0
        ultima_pergunta = ""
        orientacao_mostrada = None
        encontrou = False

        while True:
            pergunta = input("Digite sua dúvida (0 para voltar): ").strip()

            if pergunta == "0":
                if tentativas > 0:   # desistiu sem resolver
                    self.registrar("pergunta", ultima_pergunta, orientacao_mostrada,
                                   encontrou, False, tentativas, inicio)
                return
            if pergunta == "":
                print("Resposta vazia. Escreva sua dúvida.")
                continue
            if contem_dado_pessoal(pergunta):
                # não conta tentativa e não é registrada
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            ultima_pergunta = pergunta
            resultados = self.base.buscar(pergunta)

            if not resultados or resultados[0][0] < MINIMO_ENCONTRADO:
                print("\nNão encontrei uma orientação para essa dúvida.")
                print("Tente outras palavras ou navegue por uma destas categorias:")
                for categoria in self.base.categorias():
                    print(f"  - {categoria}")
                print()
                continue

            encontrou = True
            alternativas = self.mostrar_resultado(resultados)
            orientacao_mostrada = resultados[0][1]

            if ler_sim_nao("Essa orientação respondeu sua dúvida? (s/n): "):
                self.registrar("pergunta", pergunta, orientacao_mostrada,
                               True, True, tentativas, inicio)
                return

            # não ajudou: oferece as alternativas
            while alternativas:
                escolha = ler_opcao(f"Ver alternativa (1-{len(alternativas)}) ou 0 para escrever outra dúvida: ",
                                    len(alternativas))
                if escolha == 0:
                    break
                tentativas += 1
                orientacao_mostrada = alternativas[escolha - 1][1]
                orientacao_mostrada.exibir()
                if ler_sim_nao("Essa orientação respondeu sua dúvida? (s/n): "):
                    self.registrar("pergunta", pergunta, orientacao_mostrada,
                                   True, True, tentativas, inicio)
                    return

            print("Tudo bem, tente escrever a dúvida de outro jeito.")

    def navegar(self):
        """Atendimento pela navegação por categorias."""
        if not self.base_disponivel():
            return

        while True:
            categorias = self.base.categorias()
            print("\n=== Categorias ===")
            for i, categoria in enumerate(categorias, start=1):
                print(f"{i} - {categoria}")
            print("0 - Voltar")
            escolha = ler_opcao("Escolha uma categoria: ", len(categorias))
            if escolha == 0:
                return
            categoria = categorias[escolha - 1]

            while True:
                inicio = time.time()
                orientacoes = self.base.por_categoria(categoria)
                print(f"\n=== {categoria} ===")
                for i, o in enumerate(orientacoes, start=1):
                    print(f"{i} - {o.titulo}")
                print("0 - Voltar")
                escolha = ler_opcao("Escolha uma orientação: ", len(orientacoes))
                if escolha == 0:
                    break
                orientacao = orientacoes[escolha - 1]
                orientacao.exibir()
                ajudou = ler_sim_nao("Essa orientação respondeu sua dúvida? (s/n): ")
                self.registrar("categoria", f"[{categoria}] {orientacao.titulo}",
                               orientacao, True, ajudou, 1, inicio)

    # ------------------------- histórico e indicadores -------------------------

    def registrar(self, origem, pergunta, orientacao, encontrou, ajudou, tentativas, inicio):
        """Salva um atendimento no histórico (data/historico.json)."""
        atendimento = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": orientacao.id if orientacao else None,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": round(time.time() - inicio, 1),
        }
        self.historico.append(atendimento)
        salvar_json(CAMINHO_HISTORICO, self.historico)

    def avaliar(self):
        """Pede a nota de facilidade de uso (1 a 5) ao sair."""
        while True:
            nota = ler_opcao("De 1 a 5, quão fácil foi usar o assistente? (0 para pular): ", 5)
            if nota == 0:
                return
            if nota >= 1:
                self.avaliacoes.append({"data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "nota": nota})
                salvar_json(CAMINHO_AVALIACOES, self.avaliacoes)
                print("Obrigado pela avaliação!")
                return

    def indicadores(self):
        """Calcula e exibe os indicadores. Também devolve um dicionário com eles."""
        total = len(self.historico)
        print("\n=== Indicadores ===")
        if total == 0:
            print("Ainda não há atendimentos registrados.")
            return {}

        encontrados = [a for a in self.historico if a["encontrou"]]
        ajudaram = [a for a in self.historico if a["ajudou"]]
        tempo_medio = (sum(a["tempo_segundos"] for a in ajudaram) / len(ajudaram)) if ajudaram else 0
        tentativas_media = sum(a["tentativas"] for a in self.historico) / total
        notas = [av["nota"] for av in self.avaliacoes]
        facilidade = sum(notas) / len(notas) if notas else 0

        sem_solucao = []
        for a in self.historico:
            if not a["ajudou"] and a["pergunta"] not in sem_solucao:
                sem_solucao.append(a["pergunta"])

        dados = {
            "total": total,
            "encontrada_pct": len(encontrados) / total * 100,
            "acerto_pct": len(ajudaram) / total * 100,
            "tempo_medio": tempo_medio,
            "tentativas_media": tentativas_media,
            "facilidade": facilidade,
            "sem_solucao": sem_solucao,
        }

        print(f"Atendimentos registrados:      {total}")
        print(f"Resposta encontrada:           {dados['encontrada_pct']:.1f}%")
        print(f"Taxa de acerto (ajudou):       {dados['acerto_pct']:.1f}%")
        print(f"Tempo médio para encontrar:    {tempo_medio:.1f} s")
        print(f"Tentativas por atendimento:    {tentativas_media:.1f}")
        if notas:
            print(f"Facilidade de uso (1 a 5):     {facilidade:.1f} ({len(notas)} avaliações)")
        else:
            print("Facilidade de uso (1 a 5):     sem avaliações")
        print("Dúvidas sem solução:")
        if sem_solucao:
            for pergunta in sem_solucao:
                print(f"  - {pergunta}")
        else:
            print("  - nenhuma")
        return dados

    def exportar_csv(self):
        """Exporta o histórico para data/atendimentos.csv usando csv.DictWriter."""
        try:
            with open(CAMINHO_CSV, "w", newline="", encoding="utf-8") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_CSV, delimiter=";")
                escritor.writeheader()
                for atendimento in self.historico:
                    escritor.writerow({campo: atendimento.get(campo, "") for campo in CAMPOS_CSV})
            print(f"{len(self.historico)} atendimento(s) exportado(s) para {CAMINHO_CSV}")
        except OSError as erro:
            print(f"Erro ao exportar CSV: {erro}")
