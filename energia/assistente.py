"""Módulo de energia do Citizen Assist AI.

Assistente baseado em regras (sem chave de API), para que TODA resposta numérica
saia dos mesmos cálculos da análise (energia/alternativas.py). Assim as orientações
são coerentes com a análise e podem ser verificadas.

Fluxo: mensagem -> extrai dados (pessoas, minutos, potência, conta) -> identifica intenção
-> monta resposta com números, recomendação, fontes e limitações.
"""
import re
import unicodedata

from . import calculos as c
from .alternativas import comparar, recomendar, fmt_anos
from .dados import v
from .referencias import formatar

AVISO = ("⚠️ ATENÇÃO: é uma ESTIMATIVA, a economia NÃO é garantida. O valor real muda com a sua conta, "
         "o seu chuveiro, os preços e o clima. Digite \"limitações\" para saber mais.")


def _norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    return "".join(ch for ch in t if unicodedata.category(ch) != "Mn")


def brl(x):
    s = f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"


def num(x, casas=1):
    return f"{x:.{casas}f}".replace(".", ",")


def _f(txt):
    return float(txt.replace(".", "").replace(",", ".")) if re.fullmatch(r"\d{1,3}(\.\d{3})+", txt) else float(txt.replace(",", "."))


# ------------------------------------------------------------------ extração de dados

def extrair_dados(msg, perfil):
    """Atualiza o perfil com números citados pelo usuário. Retorna lista do que mudou."""
    t = _norm(msg)
    mud = []

    m = re.search(r"(\d+)\s*(pessoas|moradores|pessoa|morador)", t) or re.search(r"somos\s+(\d+)", t) \
        or re.search(r"moro\s+com\s+(\d+)", t)
    if m:
        n = int(m.group(1)) + (1 if t[m.start():m.start() + 8].startswith("moro com") else 0)
        if 1 <= n <= 15:
            perfil.pessoas = n
            perfil.informados.add("pessoas")
            mud.append(f"{n} pessoa(s) na casa")

    m = re.search(r"(\d+[\.,]?\d*)\s*(min|minutos)\b", t)
    if m:
        x = _f(m.group(1))
        if 1 <= x <= 60:
            perfil.minutos_banho = x
            perfil.informados.add("minutos_banho")
            mud.append(f"banho de {num(x, 0) if x == int(x) else num(x)} min")

    m = re.search(r"(\d+[\.,]?\d*)\s*(kw|w|watts?)\b(?!h)", t)
    if m:
        x = _f(m.group(1))
        if m.group(2) == "kw":
            x *= 1000
        if 2000 <= x <= 9000:
            perfil.potencia_inverno_w = x
            perfil.potencia_verao_w = round(x * v("potencia_verao_w") / v("potencia_inverno_w"))
            perfil.informados.add("potencia")
            mud.append(f"chuveiro de {num(x, 0)} W")

    kwh = re.search(r"(\d+[\.,]?\d*)\s*kwh", t)
    reais = re.search(r"r\$\s*(\d+[\.,]?\d*)", t)
    if kwh:
        x = _f(kwh.group(1))
        if 30 <= x <= 2000:
            perfil.consumo_total_kwh_mes = x
            perfil.informados.add("consumo")
            mud.append(f"consumo de {num(x, 0)} kWh/mês")
    if kwh and reais and not perfil.tarifa_social:
        tar = _f(reais.group(1)) / max(perfil.consumo_total_kwh_mes, 1)
        if 0.3 <= tar <= 2.0:
            perfil.tarifa_kwh = tar
            perfil.informados.add("tarifa")
            mud.append(f"tarifa calculada da sua conta: {brl(tar)}/kWh")

    if re.search(r"tarifa social|cadunico|cad unico|bolsa familia|baixa renda", t) and not re.search(r"\bnao (tenho|recebo)", t):
        if re.search(r"tenho|recebo|sou|estou|tem|faco parte|cadastrad", t):
            perfil.tarifa_social = True
            perfil.informados.add("tarifa_social")
            mud.append("você tem a Tarifa Social (80 kWh grátis)")
    if re.search(r"nao (tenho|recebo).{0,20}(tarifa social|cadunico)", t):
        perfil.tarifa_social = False
        perfil.informados.add("tarifa_social")
        mud.append("sem Tarifa Social")

    for fase, kwh_min in (("monofasic", 30), ("bifasic", 50), ("trifasic", 100)):
        if fase in t:
            perfil.custo_disponibilidade_kwh = kwh_min
            mud.append(f"ligação {fase}a (mínimo {kwh_min} kWh)")
    return mud


# ------------------------------------------------------------------ intenções

INTENCOES = [
    ("reiniciar", r"\b(reiniciar|recomecar|zerar|limpar)\b"),
    ("ajuda", r"\b(ajuda|menu|o que voce faz|comandos)\b|^oi\b|^ola\b|bom dia|boa tarde|boa noite"),
    ("limitacoes", r"limitac|limite|garant|confiavel|precis"),
    ("fontes", r"\b(fonte|fontes|referencia|referencias|de onde)\b"),
    ("perfil", r"\b(meus dados|perfil|o que voce sabe)\b"),
    ("tarifa_social", r"tarifa social|cadunico|cad unico|gratuidade|luz do povo|80 kwh"),
    ("fotovoltaico", r"fotovolt|placa solar|placas solares|painel|paineis|energia solar|gerar (minha )?energia|\bfv\b"),
    ("aquecedor_solar", r"aquecedor solar|aquecimento solar|coletor|boiler|solar termic|agua quente solar"),
    ("ambiente", r"co2|carbono|ambient|polui|sustentav|planeta|emiss"),
    ("habitos", r"\bdicas?\b|habito|banho (mais )?curto|posicao verao|verao|inverno"),
    ("comparar", r"compar|melhor opcao|qual (e )?(a )?melhor|vale (mais )?a pena|alternativ|recomend|o que fazer|economizar|economia|reduzir"),
    ("chuveiro", r"chuveiro|banho|quanto gasta|consumo|gasto|conta|kwh|watt|\bw\b"),
]


def detectar_intencao(msg):
    t = _norm(msg)
    for nome, padrao in INTENCOES:
        if re.search(padrao, t):
            return nome
    return None


# ------------------------------------------------------------------ respostas

def _rodape(fontes, aviso=True):
    partes = []
    if aviso:
        partes.append(AVISO)
    partes.append("📚 Fontes:\n" + formatar(fontes))
    return "\n\n".join(partes)


def _premissas(perfil):
    est = []
    if "pessoas" not in perfil.informados:
        est.append(f"{perfil.pessoas} pessoas")
    if "minutos_banho" not in perfil.informados:
        est.append(f"banho de {num(perfil.minutos_banho, 0)} min")
    if "potencia" not in perfil.informados:
        est.append(f"chuveiro de {num(perfil.potencia_inverno_w, 0)} W")
    if "tarifa" not in perfil.informados:
        est.append(f"tarifa estimada de {brl(perfil.tarifa_kwh)}/kWh")
    if "consumo" not in perfil.informados:
        est.append(f"consumo total de {num(perfil.consumo_total_kwh_mes, 0)} kWh/mês")
    if not est:
        return ""
    return ("ℹ️ Usei valores de referência (estimados) para: " + ", ".join(est) +
            ". Me conte os seus para um cálculo mais certo, ex.: \"somos 3 pessoas, banho de 10 minutos, chuveiro 6800 W, "
            "conta de R$ 150 com 160 kWh\".")


def r_ajuda(perfil, res):
    return ("Olá! Sou o módulo de energia do Citizen Assist AI 💡\n"
            "Ajudo famílias a gastar menos com o banho quente, que costuma ser o maior consumo da casa.\n\n"
            "Você pode perguntar, por exemplo:\n"
            "• \"Quanto gasta meu chuveiro?\" (diga quantas pessoas, minutos de banho e a potência)\n"
            "• \"Dicas para economizar no banho\"\n"
            "• \"Vale a pena aquecedor solar?\"\n"
            "• \"E placa solar (fotovoltaica)?\"\n"
            "• \"Compare as opções\"\n"
            "• \"Tenho tarifa social\" / \"Como funciona a tarifa social?\"\n"
            "• \"Impacto ambiental\", \"fontes\", \"limitações\", \"meus dados\", \"reiniciar\"")


def r_chuveiro(perfil, res):
    a0 = res["A0"]
    horas = c.horas_banho_mes(perfil.pessoas, perfil.minutos_banho)
    dt = c.aumento_temperatura_c(perfil.potencia_inverno_w)
    custo_banho = c.energia_kwh(perfil.potencia_inverno_w, perfil.minutos_banho / 60) * perfil.tarifa_kwh
    pct = a0.kwh_chuveiro_mes / perfil.consumo_total_kwh_mes * 100 if perfil.consumo_total_kwh_mes else 0
    txt = (f"🚿 Seu chuveiro de {num(perfil.potencia_inverno_w, 0)} W usado {num(perfil.minutos_banho, 0)} min por pessoa, "
           f"por {perfil.pessoas} pessoa(s), funciona cerca de {num(horas)} horas por mês.\n\n"
           f"• Energia: {num(perfil.potencia_inverno_w / 1000, 2)} kW × {num(horas)} h ≈ **{num(a0.kwh_chuveiro_mes)} kWh/mês**"
           f" (≈ {num(pct, 0)}% do consumo da casa).\n"
           f"• Cada banho de {num(perfil.minutos_banho, 0)} min custa ≈ {brl(custo_banho)}.\n"
           f"• Na conta: ≈ {brl(a0.kwh_chuveiro_mes * perfil.tarifa_kwh)}/mês só com banho"
           + (" (parte pode estar dentro dos 80 kWh grátis da Tarifa Social)" if perfil.tarifa_social else "") + ".\n"
           f"• Curiosidade: essa potência esquenta a água em ≈ {num(dt, 0)} °C com vazão de {num(v('vazao_l_min'), 0)} L/min.\n\n"
           f"Quer ver como reduzir? Pergunte \"dicas\" ou \"compare as opções\".")
    p = _premissas(perfil)
    return txt + ("\n\n" + p if p else "") + "\n\n" + _rodape(("INMETRO_PBE_CHUVEIRO", "ANEEL_TARIFAS", "FISICA_BASICA"))


def r_habitos(perfil, res):
    a0, a1 = res["A0"], res["A1"]
    agua = a0.agua_l_mes - a1.agua_l_mes
    txt = ("✅ Dicas de custo zero para o banho:\n"
           f"1. Banho de até {num(v('minutos_banho_meta'), 0)} minutos por pessoa (desligue ao se ensaboar).\n"
           f"2. Use a posição **verão** nos meses quentes (out–mar): a potência cai de ≈{num(perfil.potencia_inverno_w, 0)} W "
           f"para ≈{num(perfil.potencia_verao_w, 0)} W.\n"
           "3. Evite banhos entre 18h e 21h quando possível: é o horário de pico da rede.\n"
           "4. Não 'gambiarre' a resistência e troque-a só pela original: emendas aumentam perdas e risco de choque.\n"
           "5. Fora do banho: ao sair de casa, tire da tomada aparelhos em stand-by (TV, micro-ondas, carregadores).\n\n"
           f"📉 Para sua casa, isso reduz o banho de {num(a0.kwh_chuveiro_mes)} para {num(a1.kwh_chuveiro_mes)} kWh/mês: "
           f"economia de ≈ **{num(a1.economia_kwh_mes)} kWh** e ≈ **{brl(a1.economia_r_mes)} por mês** "
           f"({brl(a1.economia_r_mes * 12)} por ano), sem gastar nada.")
    if agua > 0:
        txt += f"\n💧 Bônus: ≈ {num(agua / 1000)} mil litros de água a menos por mês."
    if perfil.tarifa_social and a1.kwh_total_mes < v("gratuidade_tarifa_social_kwh"):
        txt += ("\n\nℹ️ Como seu consumo ficaria abaixo dos 80 kWh grátis da Tarifa Social, a economia em reais "
                "é pequena — mas ainda ajuda a rede e economiza água.")
    return txt + "\n\n" + _rodape(a1.fontes)


def r_aquecedor(perfil, res):
    a0, a2, a4 = res["A0"], res["A2"], res["A4"]
    txt = ("☀️ Aquecedor solar térmico (fonte renovável): placas no telhado esquentam a água com o sol e guardam num "
           f"reservatório de {a2.detalhes['reservatorio_l']} L. Sua casa usa ≈ {a2.detalhes['agua_quente_dia_l']} L de água "
           "quente por dia, então esse tamanho atende.\n\n"
           f"• O sol fornece ≈ {num(v('fracao_solar') * 100, 0)}% da energia do banho (estimativa para São Paulo).\n"
           f"• Banho cai de {num(a0.kwh_chuveiro_mes)} para {num(a2.kwh_chuveiro_mes)} kWh/mês → economia ≈ "
           f"**{brl(a2.economia_r_mes)}/mês**.\n"
           f"• Investimento ≈ {brl(a2.investimento)} pelo kit (sem instalação) + {brl(a2.manutencao_ano)}/ano de manutenção.\n"
           f"• Retorno do investimento (payback simples): **{fmt_anos(a2.payback_anos)}** (vida útil ≈ "
           f"{num(v('vida_util_aquecedor_anos'), 0)} anos).\n"
           f"• Saldo em 10 anos: {brl(a2.saldo_horizonte)}.\n"
           f"• Com hábitos + aquecedor: economia ≈ {brl(a4.economia_r_mes)}/mês, payback {fmt_anos(a4.payback_anos)}.\n"
           f"• Pico das 18h–21h: a potência média do chuveiro cai de {num(a0.demanda_pico_kw, 2)} para "
           f"{num(a2.demanda_pico_kw, 2)} kW — alivia a rede justamente no horário mais crítico.\n\n"
           f"🏠 Viabilidade: {a2.viabilidade}\n"
           "⚠️ Limitações: " + " ".join(a2.limitacoes))
    return txt + "\n\n" + _rodape(a2.fontes)


def r_fv(perfil, res):
    a0, a2, a3 = res["A0"], res["A2"], res["A3"]
    d = a3.detalhes
    txt = ("🔆 Placas fotovoltaicas (fonte renovável) geram eletricidade de dia; o que não é usado vai para a rede "
           "e volta como crédito na conta (Lei 14.300/2022).\n\n"
           "✋ Antes de decidir, só vale se você tiver:\n"
           "  ✔ telhado próprio, com sol e sem sombra;\n"
           "  ✔ dinheiro para a instalação, que é cobrada à parte e aumenta o tempo de retorno;\n"
           "  ✔ rede 220 V em casa e autorização da companhia de energia.\n\n"
           f"• Só para o banho ({num(a0.kwh_chuveiro_mes)} kWh/mês) bastariam {d['modulos_so_banho']} placa(s) "
           f"({num(d['kwp_so_banho'], 2)} kWp), mas o menor kit pesquisado tem {num(d['kwp'], 2)} kWp e gera "
           f"≈ {num(d['geracao_kwh_mes'], 0)} kWh/mês. Na conta abaixo só entra a parte do banho.\n"
           f"• Investimento ≈ {brl(a3.investimento)} pelo kit (sem instalação); economia ≈ **{brl(a3.economia_r_mes)}/mês** "
           "(já descontando o Fio B que passa a ser cobrado).\n"
           f"• Tempo para o dinheiro voltar (payback): **{fmt_anos(a3.payback_anos)}**, sem contar a instalação; saldo em 10 anos: {brl(a3.saldo_horizonte)}.\n"
           f"• Comparando: aquecedor solar custa {brl(a2.investimento)} e tem payback de {fmt_anos(a2.payback_anos)}.\n\n"
           f"🏠 Viabilidade: {a3.viabilidade}\n"
           "⚠️ Limitações: " + " ".join(a3.limitacoes))
    return txt + "\n\n" + _rodape(a3.fontes)


def r_comparar(perfil, res):
    ordem = recomendar(res, perfil)
    linhas = ["📊 Comparação para a mesma necessidade (banho quente da sua casa), período de 1 mês / 1 ano:\n"]
    for k in ("A0", "A1", "A2", "A3", "A4"):
        r = res[k]
        selo = " 🌱" if r.renovavel else ""
        if k == "A0":
            linhas.append(f"• {r.nome}: banho {num(r.kwh_chuveiro_mes)} kWh/mês, conta ≈ {brl(r.conta_mes)}/mês")
            continue
        linhas.append(f"• {r.nome}{selo}: economia ≈ {brl(r.economia_r_mes)}/mês ({brl(r.economia_r_mes * 12)}/ano), "
                      f"investimento {brl(r.investimento)}, retorno {fmt_anos(r.payback_anos)}, "
                      f"CO₂ evitado ≈ {num(r.co2_evitado_kg_ano, 0)} kg/ano")
    nomes = {"A1": "mudar hábitos (custo zero)", "A2": "aquecedor solar térmico", "A3": "placas fotovoltaicas"}
    rec = "\n\n🏆 Recomendação, nesta ordem:\n" + "\n".join(f"{i}. {nomes[k]}" for i, k in enumerate(ordem, 1))
    just = ["\n\nPor quê?",
            "• Hábitos vêm primeiro: não custam nada e já cortam ≈ "
            f"{num(res['A1'].economia_kwh_mes / max(res['A0'].kwh_chuveiro_mes, 1) * 100, 0)}% da energia do banho."]
    if "A2" in ordem and "A3" in ordem:
        if ordem.index("A2") < ordem.index("A3"):
            just.append("• O aquecedor solar vem antes"
                        + (" porque, com a Tarifa Social, os primeiros 80 kWh já são grátis e a placa FV tem pouco ganho real"
                           if perfil.tarifa_social else " porque se paga dentro da vida útil")
                        + "; além disso reduz o consumo no horário de pico (18h–21h), o que a placa FV sem bateria não faz.")
        else:
            just.append(f"• Comparando só o preço dos kits (sem instalação nos dois), o fotovoltaico ({brl(res['A3'].investimento)}) "
                        f"custa menos e se paga mais rápido que o aquecedor solar ({brl(res['A2'].investimento)}). Mas exige telhado "
                        "próprio sem sombra e, sem bateria, não reduz o pico das 18h–21h, o que o aquecedor solar faz.")
    if "A2" not in ordem:
        just.append(f"• O aquecedor solar ficou de fora: com o seu consumo de água quente, ele levaria "
                    f"{fmt_anos(res['A2'].payback_anos)} para se pagar, mais do que a vida útil "
                    f"(≈ {num(v('vida_util_aquecedor_anos'), 0)} anos).")
    if "A3" not in ordem:
        just.append(f"• A placa FV ficou de fora: levaria {fmt_anos(res['A3'].payback_anos)} para se pagar.")
    just.append("• A rede elétrica brasileira já é bem renovável (≈ 38 g de CO₂ por kWh), por isso o ganho de CO₂ é "
                "modesto; o maior benefício ambiental é aliviar o pico, quando usinas térmicas são acionadas.")
    txt = "\n".join(linhas) + rec + "\n".join(just)
    p = _premissas(perfil)
    fontes = tuple(f for k in ("A1", "A2", "A3") for f in res[k].fontes) + ("MCTI_FATOR_EMISSAO",)
    return txt + ("\n\n" + p if p else "") + "\n\n" + _rodape(fontes)


def r_tarifa_social(perfil, res):
    txt = ("🧾 Tarifa Social de Energia Elétrica (Lei 15.235/2025, em vigor desde 5/7/2025):\n"
           "• Quem tem direito: família inscrita no CadÚnico com renda de até ½ salário mínimo por pessoa "
           "(também há regras para BPC e outros casos — confira com a distribuidora ou o CRAS).\n"
           "• Benefício: os primeiros **80 kWh do mês são grátis**; o que passar disso é cobrado normalmente.\n"
           "• Para se inscrever: CRAS da sua cidade (CadÚnico) e depois a distribuidora (Enel, no caso de SP).\n\n")
    if perfil.tarifa_social:
        a0, a1 = res["A0"], res["A1"]
        txt += (f"Com {num(perfil.consumo_total_kwh_mes, 0)} kWh/mês, você paga só os "
                f"{num(max(0, perfil.consumo_total_kwh_mes - 80), 0)} kWh acima de 80 ≈ {brl(a0.conta_mes)}. "
                f"Mudando hábitos, a conta iria para ≈ {brl(a1.conta_mes)}.")
    else:
        txt += "Se você tem esse benefício, me diga \"tenho tarifa social\" que eu refaço os cálculos."
    return txt + "\n\n" + _rodape(("LEI_15235_2025", "ANEEL_TSEE_2025"), aviso=False)


def r_ambiente(perfil, res):
    linhas = ["🌎 Impacto ambiental de cada alternativa (por ano):"]
    for k in ("A1", "A2", "A3", "A4"):
        r = res[k]
        linhas.append(f"• {r.nome}: ≈ {num(r.co2_evitado_kg_ano, 0)} kg de CO₂ evitados; "
                      f"potência média no pico {num(r.demanda_pico_kw, 2)} kW (atual {num(res['A0'].demanda_pico_kw, 2)} kW)")
    linhas.append("\nPontos importantes:")
    linhas.append(f"• Fator médio da rede: {num(v('fator_emissao_kg_kwh') * 1000, 1)} g CO₂/kWh (MCTI, 2023). Como a rede é "
                  "majoritariamente hidrelétrica/eólica/solar, cada kWh economizado evita pouco CO₂.")
    linhas.append("• O chuveiro é um dos maiores responsáveis pelo pico de consumo no fim da tarde. Reduzir esse pico "
                  "(hábitos e aquecedor solar) diminui o uso de termelétricas, que emitem mais nesse horário.")
    linhas.append("• Banhos mais curtos economizam água, que também gasta energia para ser tratada e bombeada.")
    linhas.append("• Placas e coletores têm impacto na fabricação e precisam de descarte correto ao fim da vida útil.")
    return "\n".join(linhas) + "\n\n" + _rodape(("MCTI_FATOR_EMISSAO", "SABESP_USO_RACIONAL"))


def r_fontes(perfil, res):
    from .referencias import REFERENCIAS
    return "📚 Todas as referências usadas na análise:\n" + formatar(tuple(REFERENCIAS))


def r_limitacoes(perfil, res):
    return ("⚠️ Limitações das estimativas:\n"
            "• Tarifa: uso um valor de referência com tributos (R$ 1,09/kWh, Grande SP 2026). Bandeiras tarifárias, "
            "faixas de ICMS e taxa de iluminação pública não entram. Informe sua conta para melhorar o cálculo.\n"
            "• Chuveiro: potência e vazão variam por modelo; a posição verão foi estimada em ≈58% da potência de inverno.\n"
            "• Aquecedor solar: fração solar de 70% é média anual; inverno e dias nublados reduzem.\n"
            "• Fotovoltaico: geração média de São Paulo (CRESESB) e regras de 2026 da Lei 14.300; sombra, orientação "
            "do telhado e mudanças de regra alteram o resultado. Troca de inversor não foi incluída.\n"
            "• Preços: 1 anúncio de cada kit (nov/2026), só equipamentos; a instalação é cobrada à parte e aumenta o payback.\n"
            "• Aquecedor solar modelado com o kit de 300 L pesquisado, sem instalação; para 1–2 pessoas um kit menor pode compensar mais.\n"
            "• Payback é simples (sem juros, inflação ou reajustes de tarifa).\n"
            "• Tarifa Social combinada com placa FV não foi modelada, nem placa FV com bateria.\n"
            "• Antes de comprar, peça orçamento a instaladores e confira com a distribuidora. "
            "Instalações elétricas devem ser feitas por profissional (NBR 5410).")


def r_perfil(perfil, res):
    est = lambda campo: "" if campo in perfil.informados else " (estimado)"
    return ("📋 Dados que estou usando:\n"
            f"• Pessoas: {perfil.pessoas}{est('pessoas')}\n"
            f"• Banho: {num(perfil.minutos_banho, 0)} min/pessoa/dia{est('minutos_banho')}\n"
            f"• Chuveiro: {num(perfil.potencia_inverno_w, 0)} W inverno / {num(perfil.potencia_verao_w, 0)} W verão{est('potencia')}\n"
            f"• Consumo total: {num(perfil.consumo_total_kwh_mes, 0)} kWh/mês{est('consumo')}\n"
            f"• Tarifa: {brl(perfil.tarifa_kwh)}/kWh{est('tarifa')}\n"
            f"• Tarifa Social: {'sim' if perfil.tarifa_social else 'não'}{est('tarifa_social')}\n"
            "Não guardo nome, endereço ou documentos — só esses números, e só durante a conversa.")


RESPOSTAS = {
    "ajuda": r_ajuda, "chuveiro": r_chuveiro, "habitos": r_habitos, "aquecedor_solar": r_aquecedor,
    "fotovoltaico": r_fv, "comparar": r_comparar, "tarifa_social": r_tarifa_social, "ambiente": r_ambiente,
    "fontes": r_fontes, "limitacoes": r_limitacoes, "perfil": r_perfil,
}


class AssistenteEnergia:
    def __init__(self):
        self.perfil = c.Perfil()

    def responder(self, msg):
        msg = (msg or "").strip()
        if not msg:
            return "Pode escrever sua pergunta 🙂 (digite \"ajuda\" para ver exemplos)."
        intencao = detectar_intencao(msg)
        if intencao == "reiniciar":
            self.perfil = c.Perfil()
            return "Pronto, apaguei os dados da conversa e voltei aos valores de referência."
        mudancas = extrair_dados(msg, self.perfil)
        res = comparar(self.perfil)
        prefixo = ("✔️ Anotei: " + "; ".join(mudancas) + ".\n\n") if mudancas else ""
        if intencao is None or (intencao == "tarifa_social" and mudancas and "Tarifa Social" in " ".join(mudancas)
                                and not re.search(r"como|o que|quem|funciona|\?", _norm(msg))):
            if mudancas:
                return prefixo + r_comparar(self.perfil, res)
            return ("Não entendi bem 🤔. Posso falar sobre consumo do chuveiro, dicas de economia, aquecedor solar, "
                    "placa solar, tarifa social e impacto ambiental. Digite \"ajuda\" para exemplos.")
        if intencao in ("ajuda",) and mudancas:
            intencao = "comparar"
        return prefixo + RESPOSTAS[intencao](self.perfil, res)
