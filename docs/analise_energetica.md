# Análise energética: banho quente em famílias de baixa renda

**Disciplina:** Soluções em Energias Renováveis e Sustentáveis · **Global Solution 2026.2 · Citizen Assist AI**

> Todos os números deste documento saem do código em `energia/` e são gerados por
> `python scripts/gerar_analise.py`, que grava as tabelas em [`resultados_gerados.md`](resultados_gerados.md).
> O assistente usa as mesmas funções, por isso as respostas do chat e esta análise sempre batem.

---

## 1. Contexto

### Público
Famílias de baixa renda da Região Metropolitana de São Paulo (área da Enel SP) que aquecem a água do banho com
**chuveiro elétrico**, incluindo famílias inscritas no CadÚnico que recebem a Tarifa Social de Energia Elétrica.

### Necessidade energética
**Gastar menos com o banho quente sem perder conforto.** O chuveiro elétrico é um dos aparelhos de maior potência
da casa (4.500 a 7.500 W) e, segundo a Pesquisa de Posse e Hábitos do PROCEL, está entre os maiores responsáveis
pelo consumo residencial. Ele também é usado em massa entre 18h e 21h, o **horário de pico** do sistema elétrico.

### Como as orientações ajudam
O Citizen Assist AI calcula, com os dados que a própria família informa (número de pessoas, tempo de banho,
potência do chuveiro e valor da conta):

1. quanto o banho consome e custa hoje;
2. quanto cada alternativa economiza, quanto custa e em quanto tempo se paga;
3. qual alternativa faz mais sentido para aquela casa, com fontes e limitações.

---

## 2. Dados e premissas

A lista completa está em [`../data/parametros.csv`](../data/parametros.csv): valor, unidade, origem e se o dado é
**PUBLICADO** (veio de uma fonte) ou **ESTIMADO** (premissa da equipe, justificada).

| Parâmetro | Valor | Tipo | Origem / justificativa |
|---|---|---|---|
| Potência do chuveiro (inverno / verão) | 5.500 W / 3.200 W | Estimado | Modelos comuns nas tabelas do PBE/INMETRO |
| Vazão do chuveiro | 3 L/min | Estimado | Faixa típica de chuveiros elétricos (3–5 L/min) |
| Família de referência | 4 pessoas, 8 min de banho/pessoa/dia | Estimado | Premissa da equipe; o usuário informa a sua situação |
| Consumo total da casa | 220 kWh/mês | Estimado | Acima da média residencial nacional (~170 kWh/mês, EPE), porque a casa tem chuveiro elétrico |
| Tarifa final | R$ 0,95/kWh | Estimado | R$ 725,18/MWh (B1 Enel SP, 2025) × 1,0902 (reajuste residencial de 2026) ≈ R$ 0,79/kWh sem tributos; ÷ (1 − 0,12 ICMS − 0,05 PIS/COFINS) ≈ R$ 0,95 |
| Gratuidade da Tarifa Social | 80 kWh/mês | Publicado | Lei 15.235/2025 |
| Custo de disponibilidade | 30 / 50 / 100 kWh | Publicado | ANEEL REN 1.000/2021 (mono/bi/trifásico) |
| Fração solar do aquecedor | 70% | Estimado | Faixa típica de 60–80% para São Paulo (NBR 15569, PBE) |
| Aquecedor solar 200 L instalado | R$ 3.500 | Estimado | Faixa de R$ 2.500 a R$ 5.000 (pesquisa da equipe, `data/pesquisa_precos.csv`) |
| Irradiação em São Paulo | 4,6 kWh/m²/dia | Publicado | CRESESB SunData / Atlas Solar INPE 2017 |
| Performance ratio do FV | 0,75 | Estimado | Faixa típica de 0,70–0,80 (Manual de Engenharia FV, CRESESB) |
| Custo do FV | R$ 4.000/kWp | Estimado | Sistemas pequenos (Greener, estudo de GD) |
| Fio B na tarifa / cobrado em 2026 | 25% / 60% | Estimado / Publicado | ANEEL; Lei 14.300/2022 |
| Fator de emissão da rede | 0,0385 kgCO₂/kWh | Publicado | MCTI, média de 2023 |

**Período de referência comum:** 1 mês (30 dias) e 1 ano. Para alternativas que exigem investimento, usamos
também um **horizonte de 10 anos**.

---

## 3. Conceitos e fórmulas

| Conceito | Fórmula | Exemplo com a família de referência |
|---|---|---|
| Energia | E = P × t | 5,5 kW × 16 h = **88 kWh/mês** |
| Tempo de banho no mês | t = pessoas × min ÷ 60 × 30 | 4 × 8 ÷ 60 × 30 = 16 h |
| Calor sensível | Q = m · c · ΔT  →  ΔT = P ÷ (ṁ · c) | 5.500 ÷ (0,05 kg/s × 4.186) ≈ **26 °C** de aquecimento |
| Potência média (inverno/verão) | P̄ = (P_inv·meses_inv + P_ver·meses_ver) ÷ 12 | (5.500·6 + 3.200·6) ÷ 12 = 4.350 W |
| Geração fotovoltaica | E = kWp × H × PR × 30 | 1,1 × 4,6 × 0,75 × 30 ≈ 114 kWh/mês |
| Payback simples | invest. ÷ (economia anual − manutenção) | 3.500 ÷ (58,52 × 12 − 100) ≈ 5,8 anos |
| Emissões evitadas | kWh evitados × fator de emissão | 44,5 × 12 × 0,0385 ≈ 20,6 kg/ano |

A **eficiência energética** aparece de duas formas:
- o chuveiro elétrico converte quase toda a eletricidade em calor, mas usa **eletricidade de alta qualidade** para
  um serviço de baixa temperatura (~40 °C), justamente no horário de pico;
- o aquecedor solar entrega o mesmo serviço (água quente) a partir de **energia térmica renovável**, deixando a
  eletricidade só como apoio.

---

## 4. Alternativas comparadas (mesma necessidade: banho quente da família)

| Código | Alternativa | Tipo |
|---|---|---|
| A0 | Situação atual: chuveiro elétrico sempre na posição inverno | Referência |
| A1 | Hábitos: banho de 5 min + posição verão de out. a mar. | Economia, custo zero |
| A2 | Aquecedor solar térmico 200 L com apoio elétrico | **Fonte renovável (solar térmica)** |
| A3 | Sistema fotovoltaico conectado à rede, dimensionado para a energia do banho | **Fonte renovável (solar FV)** |
| A4 | A1 + A2 | Combinação |

### Resultado: família de referência, tarifa cheia

| Alt. | Banho (kWh/mês) | Economia (R$/mês) | Economia (R$/ano) | Investimento | Payback | Saldo em 10 anos | CO₂ evitado (kg/ano) | Potência média no pico |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A0 | 88,0 | — | — | — | — | — | — | 5,50 kW |
| A1 | 43,5 | 42,28 | 507,30 | R$ 0 | imediato | R$ 5.073 | 20,6 | 4,35 kW |
| A2 🌱 | 26,4 | 58,52 | 702,24 | R$ 3.500 | 5,8 anos | R$ 2.522 | 28,5 | 1,65 kW |
| A3 🌱 | 88,0* | 71,06 | 852,72 | R$ 4.400 | 5,8 anos | R$ 3.127 | 40,7 | 5,50 kW |
| A4 🌱 | 13,1 | 71,20 | 854,43 | R$ 3.500 | 4,6 anos | R$ 4.044 | 34,6 | 1,31 kW |

\* O FV não muda o consumo do chuveiro: gera energia de dia, que volta como crédito. Para comparar a **mesma
necessidade**, só a energia do banho (88 kWh) entra como compensada; o excedente de ~26 kWh/mês não foi contado.

Tabela completa, cenário com Tarifa Social e sensibilidade: [`resultados_gerados.md`](resultados_gerados.md).

---

## 5. Custos, viabilidade e impactos ambientais

### A1: Hábitos
- **Custo:** zero. **Economia:** ~51% da energia do banho.
- **Viabilidade:** alta, mas depende de todos os moradores aderirem e manterem o hábito.
- **Ambiente:** reduz kWh e também água (~1.080 L/mês a menos na família de referência).

### A2: Aquecedor solar térmico
- **Custo:** ~R$ 3.500 + R$ 100/ano de manutenção; vida útil de ~15 anos, então o payback de 5,8 anos fica bem
  dentro dela.
- **Viabilidade:** precisa de telhado ensolarado (de preferência voltado para o norte), estrutura para o
  reservatório e tubulação de água quente. Famílias que pagam aluguel dependem do proprietário. Programas
  habitacionais e projetos de eficiência energética das distribuidoras (PEE/ANEEL) já instalam esse sistema em
  habitação social.
- **Ambiente:** é o que **mais reduz a potência no pico** (de 5,5 para 1,65 kW de média), o momento em que o sistema
  recorre a termelétricas. Impactos de fabricação (vidro, cobre, alumínio) são baixos, e o equipamento é reciclável.

### A3: Fotovoltaico
- **Custo:** ~R$ 4.400 para 2 módulos. Em 2026, a energia compensada paga 60% do Fio B, e essa cobrança sobe até 2029.
- **Viabilidade:** exige telhado próprio, projeto e homologação na distribuidora. O inversor costuma precisar de
  troca durante a vida útil.
- **Ambiente:** evita mais kWh da rede no ano, mas **não reduz o pico noturno**. Os módulos exigem descarte
  adequado.

### Por que o ganho de CO₂ é pequeno?
A matriz elétrica brasileira é majoritariamente renovável (38,5 g de CO₂/kWh em 2023, segundo o MCTI). Por isso o
principal benefício ambiental das alternativas é **aliviar o pico** e economizar água, mais do que o CO₂ médio
evitado. Deixamos isso explícito para não exagerar o impacto.

---

## 6. Recomendações (as mesmas que o assistente dá)

1. **Comece sempre pelos hábitos (A1):** economia imediata de ~R$ 42/mês sem gastar nada.
2. **Fonte renovável: aquecedor solar (A2)** para a maioria das famílias do público:
   - tem o menor investimento entre as renováveis;
   - ataca diretamente o consumo do banho e o pico de demanda;
   - combinado com os hábitos (A4), tem o **menor payback (4,6 anos)**.
3. **Fotovoltaico (A3)** quando a família tem casa própria, consumo total alto e orçamento ou financiamento. Ele tem
   payback parecido, mas investimento maior e não ajuda no pico.
4. **Famílias com Tarifa Social:** os primeiros 80 kWh já são grátis, então o FV tem pouco ganho real. O assistente
   coloca o FV por último e avisa quando a economia de hábitos cai dentro da faixa gratuita.

A regra está implementada em `energia/alternativas.py → recomendar()`:
1. hábitos primeiro;
2. depois as renováveis com payback dentro da vida útil, da menor para a maior;
3. com Tarifa Social, o FV vai para o fim.

### Sensibilidade
- **Tarifa:** quanto maior, mais rápido tudo se paga.
- **Banhos curtos:** com banhos já curtos (5 min), o aquecedor solar demora mais a se pagar (~10 anos), e o FV
  passa a ser mais vantajoso.
- **Banhos longos:** com banhos longos (12 min), o aquecedor solar se paga em menos de 4 anos.

Por isso o assistente **recalcula com os dados de cada família** em vez de dar uma resposta única.

---

## 7. Limitações

- A tarifa é uma média com tributos. Bandeiras tarifárias, faixas de ICMS e a contribuição de iluminação pública
  ficaram de fora.
- O payback é simples: não considera juros, inflação nem reajustes de tarifa (reajustes tendem a melhorar o payback).
- Fração solar e geração FV são médias anuais. O inverno e o sombreamento reduzem os valores.
- Os preços de equipamentos variam por região e com o tempo.
- A combinação Tarifa Social + compensação FV não foi modelada; a economia do FV nesse caso está superestimada.
- A potência na posição verão (58% da de inverno) é uma aproximação; varia por modelo.
- **Nenhum valor é garantia de economia:** o assistente repete isso em todas as respostas com números.
