"""Cálculos de energia, custo e impacto ambiental.

Conceitos aplicados:
  Energia (kWh) = Potência (kW) × Tempo (h)
  Calor para aquecer água: Q = m · c · ΔT   (m em kg; 1 L de água ≈ 1 kg)
  Potência média ponderada para uso misto inverno/verão
  Geração FV (kWh) = Potência instalada (kWp) × Irradiação (kWh/m²/dia) × PR × dias
  Payback simples = Investimento ÷ Economia anual líquida
  Emissões evitadas (kgCO2) = Energia evitada (kWh) × Fator de emissão (kgCO2/kWh)
"""
from dataclasses import dataclass, field, replace
import math

from .dados import v


@dataclass
class Perfil:
    """Situação da família. Começa com o cenário de referência e é ajustada pelo usuário."""
    pessoas: int = int(v("pessoas"))
    minutos_banho: float = v("minutos_banho")
    potencia_inverno_w: float = v("potencia_inverno_w")
    potencia_verao_w: float = v("potencia_verao_w")
    meses_verao_atual: int = 0          # cenário atual: chuveiro sempre no inverno
    consumo_total_kwh_mes: float = v("consumo_total_kwh_mes")
    tarifa_kwh: float = v("tarifa_kwh")
    tarifa_social: bool = False         # gratuidade de 80 kWh (Lei 15.235/2025)
    custo_disponibilidade_kwh: float = v("custo_disponibilidade_kwh")
    informados: set = field(default_factory=set)  # quais campos o usuário informou (o resto é estimado)

    def copia(self, **mudancas):
        return replace(self, informados=set(self.informados), **mudancas)


# ------------------------------------------------------------------ básicos

def energia_kwh(potencia_w, horas):
    """E = P × t. Potência em W, tempo em h, resultado em kWh."""
    return potencia_w / 1000 * horas


def potencia_media_w(p_inverno, p_verao, meses_verao):
    """Média ponderada pelo número de meses em cada posição."""
    return (p_inverno * (12 - meses_verao) + p_verao * meses_verao) / 12


def horas_banho_mes(pessoas, minutos, dias=None):
    dias = dias or v("dias_mes")
    return pessoas * minutos / 60 * dias


def chuveiro_kwh_mes(perfil, minutos=None, meses_verao=None):
    minutos = perfil.minutos_banho if minutos is None else minutos
    meses_verao = perfil.meses_verao_atual if meses_verao is None else meses_verao
    p = potencia_media_w(perfil.potencia_inverno_w, perfil.potencia_verao_w, meses_verao)
    return energia_kwh(p, horas_banho_mes(perfil.pessoas, minutos))


def aumento_temperatura_c(potencia_w, vazao_l_min=None):
    """ΔT que o chuveiro dá à água: P = (m/t)·c·ΔT  →  ΔT = P / (ṁ·c)."""
    vazao = vazao_l_min or v("vazao_l_min")
    m_por_s = vazao / 60  # kg/s
    return potencia_w / (m_por_s * v("calor_especifico_agua"))


def agua_litros_mes(pessoas, minutos, vazao_l_min=None):
    return pessoas * minutos * (vazao_l_min or v("vazao_l_min")) * v("dias_mes")


# ------------------------------------------------------------------ conta de luz

def conta_mensal(consumo_kwh, perfil):
    """Valor aproximado da conta (R$). Simplificado: tarifa única com tributos, sem bandeira.

    - Fatura-se no mínimo o custo de disponibilidade.
    - Tarifa Social (Lei 15.235/2025): os primeiros 80 kWh são gratuitos; o excedente paga tarifa cheia.
    """
    if perfil.tarifa_social:
        return max(0.0, consumo_kwh - v("gratuidade_tarifa_social_kwh")) * perfil.tarifa_kwh
    return max(consumo_kwh, perfil.custo_disponibilidade_kwh) * perfil.tarifa_kwh


# ------------------------------------------------------------------ fotovoltaico

def fv_geracao_kwh_mes(kwp):
    return kwp * v("irradiacao_kwh_m2_dia") * v("performance_ratio") * v("dias_mes")


def fv_dimensionar_kwp(kwh_alvo_mes):
    """kWp necessário, arredondado para cima em número inteiro de módulos."""
    bruto = kwh_alvo_mes / (v("irradiacao_kwh_m2_dia") * v("performance_ratio") * v("dias_mes"))
    modulos = max(1, math.ceil(bruto / v("potencia_modulo_kwp")))
    return modulos * v("potencia_modulo_kwp"), modulos


def conta_com_fv(perfil, geracao_kwh, limite_kwh=None):
    """Conta com microgeração (Lei 14.300/2022), simplificada.

    O banho acontece à noite, então quase toda a geração vai para a rede e volta como crédito.
    Cada kWh compensado paga 60% do Fio B em 2026. Não se compensa abaixo do custo de disponibilidade.
    """
    compensavel = max(0.0, perfil.consumo_total_kwh_mes - perfil.custo_disponibilidade_kwh)
    compensada = min(geracao_kwh, compensavel)
    if limite_kwh is not None:  # para comparar a MESMA necessidade (só o banho)
        compensada = min(compensada, limite_kwh)
    custo_fio_b = compensada * perfil.tarifa_kwh * v("fracao_fio_b_tarifa") * v("percentual_fio_b_2026")
    base = perfil.copia(tarifa_social=False)
    return conta_mensal(perfil.consumo_total_kwh_mes - compensada, base) + custo_fio_b, compensada


# ------------------------------------------------------------------ indicadores

def payback_anos(investimento, economia_anual_liquida):
    if economia_anual_liquida <= 0:
        return math.inf
    return investimento / economia_anual_liquida


def co2_kg(kwh):
    return kwh * v("fator_emissao_kg_kwh")
