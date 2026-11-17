"""Interface web do módulo de energia (somente biblioteca padrão do Python).

Uso:  python app_web.py   e abra http://localhost:8000
Endpoints:
  POST /api/chat        {"sessao": "...", "mensagem": "..."} -> {"resposta": "...", "comparacao": [...]}
  GET  /api/comparacao  tabela do cenário de referência (usada nos gráficos)
"""
import json
import os
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from energia.assistente import AssistenteEnergia
from energia.alternativas import comparar
from energia.calculos import Perfil

PASTA_WEB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
SESSOES = {}  # só números de consumo, em memória; nenhum dado pessoal é salvo em disco


def tabela(res):
    return [{"codigo": r.codigo, "nome": r.nome, "renovavel": r.renovavel,
             "kwh_chuveiro_mes": round(r.kwh_chuveiro_mes, 1), "conta_mes": round(r.conta_mes, 2),
             "economia_r_mes": round(r.economia_r_mes, 2), "investimento": round(r.investimento, 2),
             "payback_anos": None if r.payback_anos == float("inf") else round(r.payback_anos, 1),
             "co2_evitado_kg_ano": round(r.co2_evitado_kg_ano, 1), "demanda_pico_kw": round(r.demanda_pico_kw, 2)}
            for r in res.values()]


class Handler(BaseHTTPRequestHandler):
    def _json(self, obj, status=200):
        corpo = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        if self.path.startswith("/api/comparacao"):
            return self._json(tabela(comparar(Perfil())))
        if self.path in ("/", "/index.html"):
            with open(os.path.join(PASTA_WEB, "index.html"), "rb") as f:
                corpo = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo)))
            self.end_headers()
            self.wfile.write(corpo)
            return
        self._json({"erro": "não encontrado"}, 404)

    def do_POST(self):
        if self.path != "/api/chat":
            return self._json({"erro": "não encontrado"}, 404)
        tamanho = int(self.headers.get("Content-Length", 0))
        try:
            dados = json.loads(self.rfile.read(min(tamanho, 10000)) or b"{}")
        except json.JSONDecodeError:
            return self._json({"erro": "JSON inválido"}, 400)
        sessao = str(dados.get("sessao") or uuid.uuid4())[:64]
        bot = SESSOES.setdefault(sessao, AssistenteEnergia())
        resposta = bot.responder(str(dados.get("mensagem", ""))[:500])
        self._json({"sessao": sessao, "resposta": resposta, "comparacao": tabela(comparar(bot.perfil))})

    def log_message(self, *args):  # não registra mensagens dos usuários
        pass


def main():
    porta = int(os.environ.get("PORT", 8000))
    print(f"Citizen Assist AI – Energia rodando em http://localhost:{porta}")
    ThreadingHTTPServer(("0.0.0.0", porta), Handler).serve_forever()


if __name__ == "__main__":
    main()
