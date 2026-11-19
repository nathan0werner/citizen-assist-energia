import json

from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}

CAMPOS_OBRIGATORIOS = ("id", "categoria", "titulo", "palavras_chave", "resposta",
                       "documentos", "onde", "fonte", "verificado_em")

PONTOS_PALAVRA_CHAVE = 3   # palavra-chave encontrada na pergunta
PONTOS_TITULO = 1          # palavra da pergunta (4+ letras) presente no título
MINIMO_ENCONTRADO = 3      # abaixo disso: "não encontrei"
MINIMO_ALTA = 6            # a partir disso: confiança ALTA


def normalizar(texto):
    """Deixa o texto em minúsculas, sem acentos e sem pontuação.
    Devolve com espaço no início e no fim para comparar palavras inteiras."""
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()-/\"'":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


def nivel_confianca(pontos):
    """Converte a pontuação em um nível de confiança."""
    if pontos >= MINIMO_ALTA:
        return "ALTA"
    if pontos >= MINIMO_ENCONTRADO:
        return "MÉDIA"
    return "BAIXA"


class BaseConhecimento:
    """Conjunto de todas as orientações, lidas do arquivo JSON."""

    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []   # lista de objetos Orientacao

    def carregar(self):
        """Lê o JSON e cria os objetos Orientacao.
        Devolve True se carregou pelo menos uma orientação."""
        self.orientacoes = []
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print(f"Erro: arquivo '{self.caminho}' não encontrado.")
            return False
        except json.JSONDecodeError:
            print(f"Erro: arquivo '{self.caminho}' está corrompido (JSON inválido).")
            return False

        if not isinstance(dados, list):
            print("Erro: a base de conhecimento deve ser uma lista de orientações.")
            return False

        for registro in dados:
            if not isinstance(registro, dict) or any(c not in registro for c in CAMPOS_OBRIGATORIOS):
                print(f"Aviso: registro ignorado por falta de campos: {registro}")
                continue
            # ** desempacota o dicionário nos parâmetros do construtor
            dados_orientacao = {campo: registro[campo] for campo in CAMPOS_OBRIGATORIOS}
            self.orientacoes.append(Orientacao(**dados_orientacao))

        return len(self.orientacoes) > 0

    def categorias(self):
        """Devolve a lista de categorias, sem repetição, em ordem alfabética."""
        return sorted({o.categoria for o in self.orientacoes})

    def por_categoria(self, categoria):
        """Devolve as orientações de uma categoria."""
        return [o for o in self.orientacoes if o.categoria == categoria]

    def buscar_por_id(self, id_orientacao):
        for o in self.orientacoes:
            if o.id == id_orientacao:
                return o
        return None

    def pontuar(self, pergunta, orientacao):
        """Calcula os pontos de uma orientação para a pergunta.
        +3 por palavra-chave presente na pergunta
        +1 por palavra da pergunta (4+ letras) presente no título"""
        pergunta_norm = normalizar(pergunta)
        pontos = 0

        for chave in orientacao.palavras_chave:
            if normalizar(chave) in pergunta_norm:
                pontos += PONTOS_PALAVRA_CHAVE

        palavras_titulo = set(normalizar(orientacao.titulo).split())
        palavras_pergunta = set(pergunta_norm.split())   # set evita contar repetidas
        for palavra in palavras_pergunta:
            if len(palavra) >= 4 and palavra in palavras_titulo:
                pontos += PONTOS_TITULO

        return pontos

    def buscar(self, pergunta):
        """Devolve uma lista de tuplas (pontos, orientacao) com pontos > 0,
        da maior para a menor pontuação."""
        resultados = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)
            if pontos > 0:
                resultados.append((pontos, orientacao))
        resultados.sort(key=lambda tupla: tupla[0], reverse=True)
        return resultados
