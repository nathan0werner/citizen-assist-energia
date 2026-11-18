"""Parâmetros usados nos cálculos de energia do Citizen Assist AI.

Cada parâmetro guarda valor, unidade, origem (id em energia/referencias.py)
e se é um dado ESTIMADO (premissa da equipe) ou um dado PUBLICADO por fonte.
O arquivo data/parametros.csv é gerado a partir daqui (scripts/gerar_analise.py).
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Parametro:
    valor: float
    unidade: str
    descricao: str
    fontes: tuple
    estimado: bool
    nota: str = ""


P = {
    # ---------------- Chuveiro elétrico ----------------
    "potencia_inverno_w": Parametro(
        5500, "W", "Potência do chuveiro elétrico na posição inverno (quente)",
        ("INMETRO_PBE_CHUVEIRO",), True,
        "Valor comum de mercado (faixa típica 4.500–7.500 W). O usuário pode informar a potência da etiqueta."),
    "potencia_verao_w": Parametro(
        3200, "W", "Potência do mesmo chuveiro na posição verão (morno)",
        ("INMETRO_PBE_CHUVEIRO",), True,
        "Aproximação para chuveiros de 5.500 W; varia por modelo."),
    "vazao_l_min": Parametro(
        3.0, "L/min", "Vazão de água de um chuveiro elétrico em uso",
        ("INMETRO_PBE_CHUVEIRO",), True,
        "Chuveiros elétricos operam tipicamente entre 3 e 5 L/min."),
    # ---------------- Família de referência ----------------
    "pessoas": Parametro(4, "pessoas", "Moradores da residência de referência", ("IBGE_CENSO",), True,
                         "Arredondamento para cima do tamanho médio do domicílio (~2,8–3 pessoas) para representar famílias com filhos."),
    "minutos_banho": Parametro(8, "min/pessoa/dia", "Duração do banho no cenário atual", ("PROCEL_PPH",), True,
                               "Premissa da equipe; o usuário informa a sua."),
    "minutos_banho_meta": Parametro(5, "min/pessoa/dia", "Duração do banho proposta na alternativa de hábitos",
                                    ("SABESP_USO_RACIONAL",), True, "Meta de uso racional adotada pela equipe."),
    "meses_verao": Parametro(6, "meses/ano", "Meses em que é possível usar a posição verão", ("INMET_CLIMA_SP",), True,
                             "Out–mar em São Paulo; premissa da equipe."),
    "dias_mes": Parametro(30, "dias", "Dias por mês usados nos cálculos", (), True, "Convenção de cálculo."),
    "consumo_total_kwh_mes": Parametro(
        220, "kWh/mês", "Consumo total da residência de referência",
        ("EPE_ANUARIO", "PROCEL_PPH"), True,
        "Família com chuveiro elétrico consome mais que a média residencial nacional (~170 kWh/mês, EPE)."),
    # ---------------- Tarifa ----------------
    "tarifa_kwh": Parametro(
        1.09, "R$/kWh", "Tarifa final de referência (com tributos) – residencial, Grande São Paulo, 2026",
        ("REFERENCIA_EQUIPE", "ANEEL_TARIFAS", "EXAME_ENEL_2025", "ENEL_REAJUSTE_2026"), True,
        "Valor informado pela equipe: R$ 90,62 para 83,1 kWh no mês (R$ 90,62 ÷ 83,1 ≈ R$ 1,09/kWh). "
        "Checagem pela tarifa publicada: R$ 725,18/MWh (B1 Enel SP 2025) × 1,0902 (reajuste 2026) ≈ R$ 0,79/kWh "
        "sem tributos; com ICMS, PIS/COFINS, bandeira e iluminação pública chega à faixa de R$ 0,95–1,10/kWh. "
        "O usuário pode informar a própria conta: total ÷ kWh."),
    "gratuidade_tarifa_social_kwh": Parametro(
        80, "kWh/mês", "Consumo isento para famílias da Tarifa Social (CadÚnico, renda ≤ ½ salário mínimo per capita)",
        ("LEI_15235_2025", "ANEEL_TSEE_2025"), False,
        "Consumo acima de 80 kWh é cobrado sem desconto."),
    "custo_disponibilidade_kwh": Parametro(
        50, "kWh/mês", "Consumo mínimo faturado (ligação bifásica). Monofásica = 30; trifásica = 100.",
        ("ANEEL_REN_1000",), False),
    # ---------------- Aquecedor solar térmico ----------------
    "fracao_solar": Parametro(
        0.70, "fração", "Parcela da energia do banho fornecida pelo sol (aquecedor solar em São Paulo)",
        ("ABNT_NBR_15569", "INMETRO_PBE_SOLAR", "CRESESB_SUNDATA"), True,
        "Sistemas bem dimensionados ficam tipicamente entre 60% e 80%; o restante vem da resistência elétrica de apoio."),
    "custo_aquecedor_solar": Parametro(
        5624, "R$", "Kit aquecedor solar 300 L (nível) + 2 placas coletoras – preço do kit, sem instalação",
        ("ANUNCIO_AQUECEDOR_ML",), False,
        "Anúncio no Mercado Livre pesquisado pela equipe em 18/11/2026. Instalação não incluída: o custo real é maior."),
    "vida_util_aquecedor_anos": Parametro(15, "anos", "Vida útil do aquecedor solar", ("INMETRO_PBE_SOLAR",), True),
    "manutencao_aquecedor_ano": Parametro(100, "R$/ano", "Limpeza de coletores / revisão", ("PESQUISA_PRECOS_EQUIPE",), True),
    # ---------------- Fotovoltaico ----------------
    "irradiacao_kwh_m2_dia": Parametro(
        4.6, "kWh/m²/dia", "Irradiação média diária no plano inclinado – São Paulo",
        ("CRESESB_SUNDATA", "ATLAS_SOLAR_2017"), False, "Média anual; no inverno é menor."),
    "performance_ratio": Parametro(0.75, "fração", "Rendimento global do sistema FV (perdas, temperatura, inversor)",
                                   ("CRESESB_MANUAL_FV",), True, "Valores típicos 0,70–0,80."),
    "potencia_modulo_kwp": Parametro(0.55, "kWp", "Potência de um módulo comercial", ("PESQUISA_PRECOS_EQUIPE",), True),
    "kit_fv_kwp": Parametro(2.48, "kWp", "Potência do menor kit fotovoltaico on-grid pesquisado (microinversor)",
                            ("ANUNCIO_FV_NEOSOLAR",), False),
    "kit_fv_preco": Parametro(4159, "R$", "Preço do kit fotovoltaico 2,48 kWp com instalação, segundo a equipe",
                              ("ANUNCIO_FV_NEOSOLAR",), False,
                              "Anúncio Neosolar pesquisado pela equipe em 18/11/2026 (≈ R$ 1.677/kWp). "
                              "Valor abaixo do usual para sistema instalado: confirmar se a instalação está mesmo incluída."),
    "fracao_fio_b_tarifa": Parametro(0.25, "fração", "Participação aproximada do Fio B na tarifa final",
                                     ("ANEEL_TARIFAS",), True),
    "percentual_fio_b_2026": Parametro(0.60, "fração", "Parcela do Fio B cobrada sobre energia compensada em 2026 (sistemas novos)",
                                       ("LEI_14300_2022",), False),
    "vida_util_fv_anos": Parametro(25, "anos", "Vida útil dos módulos FV", ("CRESESB_MANUAL_FV",), True,
                                   "Inversor costuma ser trocado uma vez nesse período (~10–12 anos)."),
    "manutencao_fv_ano": Parametro(100, "R$/ano", "Limpeza / inspeção do sistema FV", ("PESQUISA_PRECOS_EQUIPE",), True),
    # ---------------- Ambiente ----------------
    "fator_emissao_kg_kwh": Parametro(
        0.0385, "kgCO2/kWh", "Fator médio de emissão do Sistema Interligado Nacional (2023)",
        ("MCTI_FATOR_EMISSAO",), False,
        "Valores mensais de 2025 (nova base de cálculo) são menores, ex.: 0,0289 em abr/2025."),
    "calor_especifico_agua": Parametro(4186, "J/(kg·°C)", "Calor específico da água", ("FISICA_BASICA",), False),
}


def v(nome):
    """Atalho: valor numérico do parâmetro."""
    return P[nome].valor
