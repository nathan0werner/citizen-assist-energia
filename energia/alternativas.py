"""Comparação das alternativas para a MESMA necessidade (banho quente da família)
e o MESMO período de referência (mês e ano; horizonte de 10 anos para investimento).

A0 – Situação atual (chuveiro elétrico sempre no inverno)
A1 – Mudança de hábitos (banho mais curto + posição verão nos meses quentes)   [economia, custo zero]
A2 – Aquecedor solar térmico 300 L com apoio elétrico                                 [fonte renovável]
A3 – Sistema fotovoltaico conectado à rede (geração distribuída)                [fonte renovável]
A4 – Combinação A1 + A2
"""
from dataclasses import dataclass, field
import math

from . import calculos as c
from .dados import v

HORIZONTE_ANOS = 10


@dataclass
class Resultado:
    codigo: str
    nome: str
    renovavel: bool
    kwh_chuveiro_mes: float
    kwh_total_mes: float
    conta_mes: float
    investimento: float = 0.0
    manutencao_ano: float = 0.0
    demanda_pico_kw: float = 0.0
    agua_l_mes: float = 0.0
    economia_kwh_mes: float = 0.0
    economia_r_mes: float = 0.0
    economia_anual_liquida: float = 0.0
    payback_anos: float = 0.0
    saldo_horizonte: float = 0.0
    co2_evitado_kg_ano: float = 0.0
    viabilidade: str = ""
    limitacoes: list = field(default_factory=list)
    fontes: tuple = ()
    detalhes: dict = field(default_factory=dict)


def _finalizar(r, base):
    r.economia_kwh_mes = base.kwh_total_mes - r.kwh_total_mes
    r.economia_r_mes = base.conta_mes - r.conta_mes
    r.economia_anual_liquida = r.economia_r_mes * 12 - r.manutencao_ano
    r.payback_anos = 0.0 if r.investimento == 0 else c.payback_anos(r.investimento, r.economia_anual_liquida)
    r.saldo_horizonte = r.economia_anual_liquida * HORIZONTE_ANOS - r.investimento
    r.co2_evitado_kg_ano = c.co2_kg(r.economia_kwh_mes * 12)
    return r


def comparar(perfil):
    """Retorna dict codigo -> Resultado para o perfil informado."""
    pm_atual = c.potencia_media_w(perfil.potencia_inverno_w, perfil.potencia_verao_w, perfil.meses_verao_atual)
    kwh_ch = c.chuveiro_kwh_mes(perfil)
    outros = max(0.0, perfil.consumo_total_kwh_mes - kwh_ch)  # demais aparelhos (não mudam)
    agua_atual = c.agua_litros_mes(perfil.pessoas, perfil.minutos_banho)

    def total(kwh_chuveiro):
        return outros + kwh_chuveiro

    res = {}

    # A0 ----------------------------------------------------------------
    a0 = Resultado("A0", "Situação atual (chuveiro elétrico)", False, kwh_ch, perfil.consumo_total_kwh_mes,
                   c.conta_mensal(perfil.consumo_total_kwh_mes, perfil),
                   demanda_pico_kw=pm_atual / 1000, agua_l_mes=agua_atual,
                   viabilidade="Referência para comparação.",
                   fontes=("INMETRO_PBE_CHUVEIRO", "ANEEL_TARIFAS"))
    res["A0"] = _finalizar(a0, a0)

    # A1 – hábitos -------------------------------------------------------
    min_meta = min(perfil.minutos_banho, v("minutos_banho_meta"))
    meses_v = max(perfil.meses_verao_atual, int(v("meses_verao")))
    kwh_a1 = c.chuveiro_kwh_mes(perfil, minutos=min_meta, meses_verao=meses_v)
    a1 = Resultado("A1", "Hábitos: banho de %g min + posição verão %d meses/ano" % (min_meta, meses_v), False,
                   kwh_a1, total(kwh_a1), c.conta_mensal(total(kwh_a1), perfil),
                   demanda_pico_kw=c.potencia_media_w(perfil.potencia_inverno_w, perfil.potencia_verao_w, meses_v) / 1000,
                   agua_l_mes=c.agua_litros_mes(perfil.pessoas, min_meta),
                   viabilidade="Alta: custo zero e efeito imediato. Depende da adesão de todos os moradores.",
                   limitacoes=["A economia só acontece se o hábito for mantido.",
                               "Em dias frios a posição verão pode não ser confortável."],
                   fontes=("SABESP_USO_RACIONAL", "INMETRO_PBE_CHUVEIRO", "INMET_CLIMA_SP"))
    res["A1"] = _finalizar(a1, a0)

    # A2 – aquecedor solar ------------------------------------------------
    fs = v("fracao_solar")
    kwh_a2 = kwh_ch * (1 - fs)
    a2 = Resultado("A2", "Aquecedor solar térmico (300 L) com apoio elétrico", True,
                   kwh_a2, total(kwh_a2), c.conta_mensal(total(kwh_a2), perfil),
                   investimento=v("custo_aquecedor_solar"), manutencao_ano=v("manutencao_aquecedor_ano"),
                   demanda_pico_kw=pm_atual / 1000 * (1 - fs), agua_l_mes=agua_atual,
                   viabilidade="Média: exige telhado com sol (face norte), estrutura para o reservatório e "
                               "instalação hidráulica de água quente. Muitas vezes possível via programas habitacionais "
                               "ou da distribuidora (Programa de Eficiência Energética da ANEEL).",
                   limitacoes=["Fração solar de 70% é estimativa; em dias nublados seguidos o apoio elétrico trabalha mais.",
                               "O preço usado é só do kit (anúncio): a instalação não está incluída, então o payback real é maior.",
                               "Não serve para quem mora de aluguel sem autorização do proprietário."],
                   fontes=("ABNT_NBR_15569", "INMETRO_PBE_SOLAR", "CRESESB_SUNDATA", "PESQUISA_PRECOS_EQUIPE"),
                   detalhes={"fracao_solar": fs, "reservatorio_l": 300,
                             "agua_quente_dia_l": round(agua_atual / v("dias_mes"))})
    res["A2"] = _finalizar(a2, a0)

    # A3 – fotovoltaico ---------------------------------------------------
    # Usa o kit REAL pesquisado (não dá para comprar "meio kit" instalado pelo preço proporcional).
    kwp_min, modulos_min = c.fv_dimensionar_kwp(kwh_ch)   # quanto bastaria só para o banho (informativo)
    kwp = max(v("kit_fv_kwp"), kwp_min)
    investimento_fv = v("kit_fv_preco") * kwp / v("kit_fv_kwp")
    ger = c.fv_geracao_kwh_mes(kwp)
    conta_fv, compensada = c.conta_com_fv(perfil, ger, limite_kwh=kwh_ch)
    lim_fv = ["Na comparação só entra a energia do banho; o excedente de geração (%.0f kWh/mês) vira crédito "
              "para outros aparelhos e não foi contado na comparação." % max(0.0, ger - compensada),
              "Preço só dos equipamentos (anúncio): instalação e homologação por integrador são cobradas à parte, então o payback real é maior.",
              "O kit exige rede 220 V e área de telhado para 4 módulos.",
              "Geração varia com a estação (menor no inverno) e com sombreamento.",
              "Regras de compensação (Lei 14.300/2022) mudam ano a ano: o Fio B cobrado sobe até 2029.",
              "O inversor costuma precisar de troca uma vez na vida útil (não incluído no saldo de 10 anos).",
              "Não reduz o pico das 18h–21h: gera de dia, enquanto o banho é à noite."]
    viab = ("Média: exige telhado próprio, sem sombra, e homologação na distribuidora. "
            "O kit gera mais do que o banho precisa, então compensa mais quando o consumo total da casa é alto.")
    if perfil.tarifa_social:
        lim_fv.insert(0, "Para famílias com gratuidade da Tarifa Social, a interação com a compensação de créditos "
                         "não foi modelada; o cálculo usa a tarifa cheia e superestima a economia.")
        viab = "Baixa para quem já tem gratuidade da Tarifa Social: boa parte do consumo já é isenta."
        conta_base_cheia = c.conta_mensal(perfil.consumo_total_kwh_mes, perfil.copia(tarifa_social=False))
        conta_fv = max(0.0, conta_fv - conta_base_cheia + a0.conta_mes)  # economia calculada sobre a tarifa cheia
    a3 = Resultado("A3", "Kit fotovoltaico on-grid %s kWp" % f"{kwp:.2f}".replace(".", ","), True,
                   kwh_ch, perfil.consumo_total_kwh_mes, conta_fv,
                   investimento=investimento_fv, manutencao_ano=v("manutencao_fv_ano"),
                   demanda_pico_kw=pm_atual / 1000, agua_l_mes=agua_atual,
                   viabilidade=viab, limitacoes=lim_fv,
                   fontes=("CRESESB_SUNDATA", "CRESESB_MANUAL_FV", "LEI_14300_2022", "ANUNCIO_FV_NEOSOLAR", "ANEEL_REN_1000"),
                   detalhes={"kwp": kwp, "kwp_so_banho": kwp_min, "modulos_so_banho": modulos_min,
                             "geracao_kwh_mes": ger, "compensada_kwh_mes": compensada})
    r3 = _finalizar(a3, a0)
    r3.economia_kwh_mes = compensada  # energia da rede evitada (compensada pela geração)
    r3.co2_evitado_kg_ano = c.co2_kg(compensada * 12)
    res["A3"] = r3

    # A4 – hábitos + solar -----------------------------------------------
    kwh_a4 = kwh_a1 * (1 - fs)
    a4 = Resultado("A4", "Combinação: hábitos (A1) + aquecedor solar (A2)", True,
                   kwh_a4, total(kwh_a4), c.conta_mensal(total(kwh_a4), perfil),
                   investimento=a2.investimento, manutencao_ano=a2.manutencao_ano,
                   demanda_pico_kw=a1.demanda_pico_kw * (1 - fs), agua_l_mes=a1.agua_l_mes,
                   viabilidade="Média: soma as condições de A1 e A2.",
                   limitacoes=a1.limitacoes + a2.limitacoes[:1],
                   fontes=a1.fontes + a2.fontes)
    res["A4"] = _finalizar(a4, a0)
    return res


def recomendar(res, perfil):
    """Regra de recomendação coerente com a análise (usada pelo assistente).

    1º sempre os hábitos (custo zero).
    2º entre as renováveis, a de menor payback dentro da vida útil.
    """
    ordem = ["A1"]
    renov = [r for r in (res["A2"], res["A3"]) if r.payback_anos < (
        v("vida_util_aquecedor_anos") if r.codigo == "A2" else v("vida_util_fv_anos"))]
    renov.sort(key=lambda r: r.payback_anos)
    if perfil.tarifa_social:
        renov = [r for r in renov if r.codigo != "A3"] + [r for r in renov if r.codigo == "A3"]
    ordem += [r.codigo for r in renov]
    return ordem


def fmt_anos(x):
    if x == 0:
        return "imediato"
    if math.isinf(x):
        return "não se paga"
    return f"{x:.1f} anos".replace(".", ",")
