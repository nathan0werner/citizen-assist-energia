"""Gera as tabelas da análise a partir do código (garante que análise e assistente usam os mesmos números).

Saídas:
  data/parametros.csv              – todos os parâmetros, unidade, origem e se é estimado
  data/resultados_cenario_base.csv – comparação das alternativas (família de referência)
  data/sensibilidade.csv           – como o resultado muda com tarifa, minutos de banho e fração solar
  docs/resultados_gerados.md       – tabelas em Markdown para o README / análise

Uso:  python scripts/gerar_analise.py
"""
import csv
from dataclasses import replace
import math
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from energia import dados  # noqa: E402
from energia.alternativas import comparar, fmt_anos, recomendar  # noqa: E402
from energia.calculos import Perfil  # noqa: E402


def br(x, casas=2):
    if isinstance(x, float) and math.isinf(x):
        return "não se paga"
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def salvar_parametros():
    caminho = os.path.join(RAIZ, "data", "parametros.csv")
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["parametro", "valor", "unidade", "descricao", "tipo", "fontes", "nota"])
        for nome, p in dados.P.items():
            w.writerow([nome, p.valor, p.unidade, p.descricao, "ESTIMADO" if p.estimado else "PUBLICADO",
                        ";".join(p.fontes), p.nota])
    return caminho


def linhas_resultado(res):
    for r in res.values():
        yield [r.codigo, r.nome, "sim" if r.renovavel else "não", round(r.kwh_chuveiro_mes, 1),
               round(r.kwh_total_mes, 1), round(r.conta_mes, 2), round(r.economia_kwh_mes, 1),
               round(r.economia_r_mes, 2), round(r.economia_r_mes * 12, 2), round(r.investimento, 2),
               round(r.manutencao_ano, 2), "" if math.isinf(r.payback_anos) else round(r.payback_anos, 2),
               round(r.saldo_horizonte, 2), round(r.co2_evitado_kg_ano, 1), round(r.demanda_pico_kw, 2),
               round(r.agua_l_mes)]


CAB = ["codigo", "alternativa", "renovavel", "kwh_chuveiro_mes", "kwh_total_mes", "conta_r_mes",
       "economia_kwh_mes", "economia_r_mes", "economia_r_ano", "investimento_r", "manutencao_r_ano",
       "payback_anos", "saldo_10_anos_r", "co2_evitado_kg_ano", "demanda_pico_kw", "agua_l_mes"]


def tabela_md(res):
    out = ["| Alt. | Descrição | Banho (kWh/mês) | Conta (R$/mês) | Economia (R$/mês) | Economia (R$/ano) | "
           "Investimento (R$) | Payback | Saldo 10 anos (R$) | CO₂ evitado (kg/ano) | Potência média no pico (kW) |",
           "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in res.values():
        out.append(f"| {r.codigo} | {r.nome}{' 🌱' if r.renovavel else ''} | {br(r.kwh_chuveiro_mes, 1)} | "
                   f"{br(r.conta_mes)} | {br(r.economia_r_mes)} | {br(r.economia_r_mes * 12)} | {br(r.investimento)} | "
                   f"{fmt_anos(r.payback_anos) if r.codigo != 'A0' else '—'} | {br(r.saldo_horizonte)} | "
                   f"{br(r.co2_evitado_kg_ano, 1)} | {br(r.demanda_pico_kw)} |")
    return "\n".join(out)


def sensibilidade():
    linhas = []
    for tarifa in (0.90, 1.09, 1.30):
        for minutos in (5, 8, 12):
            for fs in (0.6, 0.7, 0.8):
                original = dados.P["fracao_solar"]
                dados.P["fracao_solar"] = replace(original, valor=fs)
                try:
                    res = comparar(Perfil(tarifa_kwh=tarifa, minutos_banho=minutos))
                finally:
                    dados.P["fracao_solar"] = original
                linhas.append([tarifa, minutos, fs] + [
                    "" if math.isinf(res[k].payback_anos) else round(res[k].payback_anos, 1) for k in ("A2", "A3", "A4")]
                    + [round(res[k].economia_r_mes, 2) for k in ("A1", "A2", "A3")])
    return linhas


def main():
    salvar_parametros()
    base = comparar(Perfil())
    social = comparar(Perfil(tarifa_social=True))
    casa_equipe = Perfil(pessoas=2, minutos_banho=8, potencia_inverno_w=4500,
                         potencia_verao_w=round(4500 * 3200 / 5500), consumo_total_kwh_mes=83.1)
    pequena = comparar(casa_equipe)

    with open(os.path.join(RAIZ, "data", "resultados_cenario_base.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cenario"] + CAB)
        for nome, res in (("tarifa_cheia", base), ("tarifa_social", social), ("casa_pequena_equipe", pequena)):
            for linha in linhas_resultado(res):
                w.writerow([nome] + linha)

    sens = sensibilidade()
    with open(os.path.join(RAIZ, "data", "sensibilidade.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["tarifa_r_kwh", "minutos_banho", "fracao_solar", "payback_A2", "payback_A3", "payback_A4",
                    "economia_A1_r_mes", "economia_A2_r_mes", "economia_A3_r_mes"])
        w.writerows(sens)

    md = ["# Resultados gerados automaticamente",
          "",
          "> Arquivo gerado por `python scripts/gerar_analise.py`. Não edite à mão: mude os parâmetros em "
          "`energia/dados.py` e rode o script de novo.",
          "",
          "## Cenário 1 – Família de referência, tarifa cheia",
          "",
          "4 pessoas, banho de 8 min, chuveiro de 5.500 W sempre no inverno, consumo total de 220 kWh/mês, "
          "tarifa de referência de R$ 1,09/kWh. Período de referência: 1 mês (e 1 ano); horizonte de investimento: 10 anos.",
          "",
          tabela_md(base),
          "",
          "## Cenário 2 – Mesma família com a Tarifa Social (80 kWh/mês grátis)",
          "",
          tabela_md(social),
          "",
          "> No cenário 2, a economia do fotovoltaico (A3) foi calculada com a tarifa cheia, porque a combinação "
          "gratuidade + compensação de créditos não foi modelada; por isso o valor está **superestimado**.",
          "",
          "## Cenário 3 – Casa de um integrante da equipe (2 pessoas)",
          "",
          "2 pessoas, banho de 8 min, chuveiro de baixa potência (4.500 W, **estimado**: a equipe descreveu como "
          "\"fraquinho\"), consumo total de 83,1 kWh/mês (referência informada pela equipe).",
          "",
          tabela_md(pequena),
          "",
          "> Recomendação do código para este caso: " + " → ".join(recomendar(pequena, casa_equipe)) +
          ". Com pouco uso de água quente, o aquecedor solar de 300 L não se paga dentro da vida útil (15 anos) e "
          "sai da recomendação.",
          "",
          "## Sensibilidade (payback em anos)",
          "",
          "| Tarifa (R$/kWh) | Banho (min) | Fração solar | Payback A2 | Payback A3 | Payback A4 |",
          "|---:|---:|---:|---:|---:|---:|"]
    for l in sens:
        if l[2] == 0.7 or (l[0] == 1.09 and l[1] == 8):
            md.append(f"| {br(l[0])} | {l[1]} | {br(l[2], 1)} | {br(l[3], 1) if l[3] != '' else '—'} | "
                      f"{br(l[4], 1) if l[4] != '' else '—'} | {br(l[5], 1) if l[5] != '' else '—'} |")
    md.append("")
    md.append("Tabela completa (27 combinações) em `data/sensibilidade.csv`.")
    with open(os.path.join(RAIZ, "docs", "resultados_gerados.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
