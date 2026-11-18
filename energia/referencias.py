"""Referências verificáveis citadas pelo assistente e pela análise.

ATENÇÃO EQUIPE: confira cada link antes da entrega (ver VERIFICAR.md).
"""

REFERENCIAS = {
    "ANEEL_TARIFAS": ("ANEEL – Tarifas residenciais vigentes por distribuidora",
                      "https://portalrelatorios.aneel.gov.br/luznatarifa/basestarifas"),
    "EXAME_ENEL_2025": ("Exame – Conta de luz em SP: ANEEL aprova reajuste da Enel (jul/2025), tarifa B1 R$ 725,18/MWh",
                        "https://exame.com/economia/conta-de-luz-sp-aumento-enel-reajuste-tarifa-aneel-julho"),
    "ENEL_REAJUSTE_2026": ("Cenário Energia – ANEEL aprova reajuste da Enel SP com efeito médio de 10,18% (jun/2026)",
                           "https://cenarioenergia.com.br/2026/06/30/aneel-aprova-reajuste-da-enel-sao-paulo-com-efeito-medio-de-1018/"),
    "LEI_15235_2025": ("Lei nº 15.235/2025 – amplia a Tarifa Social de Energia Elétrica (gratuidade até 80 kWh)",
                       "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15235.htm"),
    "ANEEL_TSEE_2025": ("Cenário Energia – Gratuidade de 80 kWh na Tarifa Social é regulamentada pela ANEEL",
                        "https://cenarioenergia.com.br/2025/06/10/gratuidade-de-80-kwh-mensais-na-tarifa-social-e-regulamentada-pela-aneel-e-beneficia-mais-de-17-milhoes-de-familias/"),
    "ANEEL_REN_1000": ("ANEEL – Resolução Normativa nº 1.000/2021 (custo de disponibilidade: 30/50/100 kWh)",
                       "https://www2.aneel.gov.br/cedoc/ren20211000.html"),
    "LEI_14300_2022": ("Lei nº 14.300/2022 – Marco legal da micro e minigeração distribuída (cobrança gradual do Fio B)",
                       "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14300.htm"),
    "INMETRO_PBE_CHUVEIRO": ("INMETRO – Programa Brasileiro de Etiquetagem: tabelas de chuveiros elétricos",
                             "https://www.gov.br/inmetro/pt-br/assuntos/avaliacao-da-conformidade/programa-brasileiro-de-etiquetagem/tabelas-de-eficiencia-energetica"),
    "INMETRO_PBE_SOLAR": ("INMETRO – PBE: tabelas de coletores solares e reservatórios térmicos",
                          "https://www.gov.br/inmetro/pt-br/assuntos/avaliacao-da-conformidade/programa-brasileiro-de-etiquetagem/tabelas-de-eficiencia-energetica"),
    "ABNT_NBR_15569": ("ABNT NBR 15569 – Sistema de aquecimento solar de água em circuito direto: projeto e instalação",
                       "https://www.abntcatalogo.com.br/"),
    "CRESESB_SUNDATA": ("CRESESB/CEPEL – SunData v3: irradiação solar por localidade",
                        "https://cresesb.cepel.br/index.php?section=sundata"),
    "ATLAS_SOLAR_2017": ("INPE – Atlas Brasileiro de Energia Solar, 2ª edição (2017)",
                         "https://labren.ccst.inpe.br/atlas_2017.html"),
    "CRESESB_MANUAL_FV": ("CRESESB/CEPEL – Manual de Engenharia para Sistemas Fotovoltaicos (2014)",
                          "https://cresesb.cepel.br/publicacoes/download/Manual_de_Engenharia_FV_2014.pdf"),
    "GREENER_ESTUDO_GD": ("Greener – Estudo Estratégico de Geração Distribuída (preços de sistemas FV)",
                          "https://www.greener.com.br/estudos/"),
    "MCTI_FATOR_EMISSAO": ("MCTI/SIRENE – Fatores de emissão de CO2 do Sistema Interligado Nacional",
                           "https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao"),
    "EPE_ANUARIO": ("EPE – Anuário Estatístico de Energia Elétrica (consumo médio residencial)",
                    "https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/anuario-estatistico-de-energia-eletrica"),
    "PROCEL_PPH": ("PROCEL/Eletrobras – Pesquisa de Posse de Equipamentos e Hábitos de Uso (PPH 2019, classe residencial)",
                   "https://www.procelinfo.com.br/"),
    "IBGE_CENSO": ("IBGE – Censo Demográfico 2022: moradores por domicílio",
                   "https://censo2022.ibge.gov.br/"),
    "INMET_CLIMA_SP": ("INMET – Normais climatológicas (São Paulo)",
                       "https://portal.inmet.gov.br/normais"),
    "SABESP_USO_RACIONAL": ("SABESP – Dicas de uso racional da água (banho de até 5 minutos)",
                            "https://site.sabesp.com.br/"),
    "REFERENCIA_EQUIPE": ("Valor de referência informado pela equipe: R$ 90,62 para 83,1 kWh/mês (≈ R$ 1,09/kWh)", ""),
    "PESQUISA_PRECOS_EQUIPE": ("Pesquisa de preços da equipe em lojas de materiais e instaladores (ver data/pesquisa_precos.csv)",
                               "data/pesquisa_precos.csv"),
    "FISICA_BASICA": ("Halliday, Resnick & Walker – Fundamentos de Física, vol. 2 (calor específico, Q = m·c·ΔT)", ""),
}


def formatar(ids):
    """Lista curta de fontes para o rodapé das respostas do assistente."""
    linhas = []
    for i in dict.fromkeys(ids):  # remove repetidos mantendo a ordem
        if i in REFERENCIAS:
            titulo, url = REFERENCIAS[i]
            linhas.append(f"- {titulo}" + (f" — {url}" if url else ""))
    return "\n".join(linhas)
