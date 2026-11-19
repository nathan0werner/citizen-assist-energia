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
| Tarifa final | R$ 1,09/kWh | Estimado | Valor de referência informado pela equipe (R$ 90,62 ÷ 83,1 kWh). Checagem: R$ 725,18/MWh (B1 Enel SP, 2025) × 1,0902 (reajuste de 2026) ≈ R$ 0,79/kWh sem tributos; com ICMS, PIS/COFINS, bandeira e iluminação pública fica na faixa de R$ 0,95–1,10 |
| Gratuidade da Tarifa Social | 80 kWh/mês | Publicado | Lei 15.235/2025 |
| Custo de disponibilidade | 30 / 50 / 100 kWh | Publicado | ANEEL REN 1.000/2021 (mono/bi/trifásico) |
| Fração solar do aquecedor | 70% | Estimado | Faixa típica de 60–80% para São Paulo (NBR 15569, PBE) |
| Aquecedor solar 300 L + 2 placas (kit, sem instalação) | R$ 5.624 | Publicado (anúncio) | Mercado Livre, consulta em 18/11/2026 (`data/pesquisa_precos.csv`) |
| Irradiação em São Paulo | 4,6 kWh/m²/dia | Publicado | CRESESB SunData / Atlas Solar INPE 2017 |
| Performance ratio do FV | 0,75 | Estimado | Faixa típica de 0,70–0,80 (Manual de Engenharia FV, CRESESB) |
| Kit FV on-grid 2,48 kWp com microinversor | R$ 4.159 (kit, sem instalação) | Publicado (anúncio) | Neosolar, consulta em 18/11/2026. 4 módulos + microinversores; instalação por integrador cobrada à parte |
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
| Geração fotovoltaica | E = kWp × H × PR × 30 | 2,48 × 4,6 × 0,75 × 30 ≈ 257 kWh/mês (o fabricante estima ~260 kWh/mês, faixa de 208 a 312: o cálculo confere) |
| Payback simples | invest. ÷ (economia anual − manutenção) | 5.624 ÷ (67,14 × 12 − 100) ≈ 8,0 anos |
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
| A2 | Aquecedor solar térmico 300 L com apoio elétrico (kit pesquisado) | **Fonte renovável (solar térmica)** |
| A3 | Kit fotovoltaico on-grid de 2,48 kWp (menor kit pesquisado) | **Fonte renovável (solar FV)** |
| A4 | A1 + A2 | Combinação |

### Resultado: família de referência, tarifa cheia

| Alt. | Banho (kWh/mês) | Economia (R$/mês) | Economia (R$/ano) | Investimento | Payback | Saldo em 10 anos | CO₂ evitado (kg/ano) | Potência média no pico |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A0 | 88,0 | — | — | — | — | — | — | 5,50 kW |
| A1 | 43,5 | 48,50 | 582,06 | R$ 0 | imediato | R$ 5.821 | 20,6 | 4,35 kW |
| A2 🌱 | 26,4 | 67,14 | 805,73 | R$ 5.624 | 8,0 anos | R$ 1.433 | 28,5 | 1,65 kW |
| A3 🌱 | 88,0* | 81,53 | 978,38 | R$ 4.159 | 4,7 anos | R$ 4.625 | 40,7 | 5,50 kW |
| A4 🌱 | 13,1 | 81,70 | 980,35 | R$ 5.624 | 6,4 anos | R$ 3.179 | 34,6 | 1,31 kW |

\* O FV não muda o consumo do chuveiro: gera energia de dia, que volta como crédito. Para comparar a **mesma
necessidade**, só a energia do banho (88 kWh) entra como compensada. O kit gera ~257 kWh/mês; o restante abate
o consumo de outros aparelhos ou vira crédito, mas não foi contado na comparação.

Tabela completa, cenário com Tarifa Social e sensibilidade: [`resultados_gerados.md`](resultados_gerados.md).

---

## 5. Custos, viabilidade e impactos ambientais

### A1: Hábitos
- **Custo:** zero. **Economia:** ~51% da energia do banho.
- **Viabilidade:** alta, mas depende de todos os moradores aderirem e manterem o hábito.
- **Ambiente:** reduz kWh e também água (~1.080 L/mês a menos na família de referência).

### A2: Aquecedor solar térmico
- **Custo:** R$ 5.624 pelo kit de 300 L (sem instalação) + R$ 100/ano de manutenção. O payback de 8,0 anos fica
  dentro da vida útil (~15 anos), mas a instalação, não incluída, aumenta esse prazo.
- **Viabilidade:** precisa de telhado ensolarado (de preferência voltado para o norte), estrutura para o
  reservatório e tubulação de água quente. Famílias que pagam aluguel dependem do proprietário. Programas
  habitacionais e projetos de eficiência energética das distribuidoras (PEE/ANEEL) já instalam esse sistema em
  habitação social.
- **Ambiente:** é o que **mais reduz a potência no pico** (de 5,5 para 1,65 kW de média), o momento em que o sistema
  recorre a termelétricas. Impactos de fabricação (vidro, cobre, alumínio) são baixos, e o equipamento é reciclável.

### A3: Fotovoltaico
- **Custo:** R$ 4.159 pelo kit de 2,48 kWp (só equipamentos; instalação e homologação à parte). Só para o banho
  bastariam ~1,1 kWp, mas o kit pesquisado era o menor disponível. Em 2026, a energia compensada paga 60% do Fio B,
  e essa cobrança sobe até 2029.
- **Viabilidade:** exige telhado próprio, projeto e homologação na distribuidora. O inversor costuma precisar de
  troca durante a vida útil.
- **Ambiente:** evita mais kWh da rede no ano, mas, **sem bateria, não reduz o pico noturno**. Sistemas com
  bateria (híbridos) guardam a energia do dia para a noite, mas custam bem mais e não foram modelados (apontado no
  teste com o participante P2). Os módulos e baterias exigem descarte adequado.

### Por que o ganho de CO₂ é pequeno?
A matriz elétrica brasileira é majoritariamente renovável (38,5 g de CO₂/kWh em 2023, segundo o MCTI). Por isso o
principal benefício ambiental das alternativas é **aliviar o pico** e economizar água, mais do que o CO₂ médio
evitado. Deixamos isso explícito para não exagerar o impacto.

---

## 6. Recomendações (as mesmas que o assistente dá)

1. **Comece sempre pelos hábitos (A1):** economia imediata de ~R$ 48/mês sem gastar nada.
2. **Fonte renovável, com os preços pesquisados: kit fotovoltaico (A3)** para a família de referência:
   - menor investimento (R$ 4.159) e menor payback (4,7 anos) entre as renováveis;
   - exige telhado próprio sem sombra e, **sem bateria, não reduz o pico noturno**.
3. **Aquecedor solar (A2):** payback de 8,0 anos (6,4 anos junto com os hábitos), só pelo kit, sem instalação.
   Continua sendo a melhor opção para **aliviar o pico das 18h–21h** e para **famílias com Tarifa Social**: com os
   primeiros 80 kWh grátis, o ganho real do FV é pequeno.
4. **Atenção ao preço:** os dois preços são só dos kits; a instalação é cobrada à parte nos dois casos, então os
   paybacks reais são maiores. O resultado A3 × A2 depende muito dos preços, por isso o assistente mostra os dois e
   explica a diferença.

A regra está implementada em `energia/alternativas.py → recomendar()`:
1. hábitos primeiro;
2. depois as renováveis com payback dentro da vida útil, da menor para a maior;
3. com Tarifa Social, o FV vai para o fim.

### Caso real: casa de um integrante (2 pessoas)
Testamos a mesma análise numa casa de um integrante da equipe: 2 pessoas, banho de 8 min e chuveiro de baixa
potência (4.500 W, estimado) num consumo total de 83,1 kWh/mês. Detalhes no Cenário 3 de
[`resultados_gerados.md`](resultados_gerados.md).

| Alternativa | Economia/mês | Investimento | Payback |
|---|---:|---:|---:|
| A1 Hábitos | R$ 19,84 | R$ 0 | imediato |
| A2 Aquecedor solar 300 L | R$ 27,47 | R$ 5.624 | 24,5 anos (passa da vida útil) |
| A3 Kit fotovoltaico 2,48 kWp | R$ 30,67 | R$ 4.159 | 15,5 anos (dentro da vida útil de 25 anos) |
| A4 Hábitos + aquecedor | R$ 33,42 | R$ 5.624 | 18,7 anos |

**Conclusão:**
- Com pouca gente e chuveiro fraco, o banho gasta só ~36 kWh/mês. O aquecedor solar de 300 L **não se paga** dentro
  da vida útil, e o kit FV demora 15,5 anos, porque a conta já é pequena (o mínimo faturado também limita a
  compensação).
- Nesse caso, a recomendação prática é **mudar hábitos**. Investir em energia renovável só faz sentido
  financeiramente com um equipamento menor e mais barato do que os pesquisados.
- É por isso que o assistente recalcula para cada família em vez de dar uma resposta fixa.

### Sensibilidade
- **Tarifa:** quanto maior, mais rápido tudo se paga.
- **Banhos curtos:** com banhos já curtos (5 min), o aquecedor solar leva ~14 anos para se pagar, quase a vida útil
  inteira; o FV leva ~8 anos.
- **Banhos longos:** com banhos longos (12 min), o aquecedor solar se paga em ~5 anos e o FV em ~3 anos.
- **Fração solar:** entre 60% e 80%, o payback do aquecedor solar vai de 9,5 para 6,9 anos.

Por isso o assistente **recalcula com os dados de cada família** em vez de dar uma resposta única.

---

## 7. Limitações

- A tarifa é uma média com tributos. Bandeiras tarifárias, faixas de ICMS e a contribuição de iluminação pública
  ficaram de fora.
- O payback é simples: não considera juros, inflação nem reajustes de tarifa (reajustes tendem a melhorar o payback).
- Fração solar e geração FV são médias anuais. O inverno e o sombreamento reduzem os valores.
- Os preços vêm de 1 anúncio de cada equipamento (nov/2026). O aquecedor solar não inclui instalação, e a instalação
  também não está no kit FV (o anúncio indica contratar um integrador). Preços variam por região e com o tempo.
- Sistemas fotovoltaicos com bateria não foram modelados (só o kit on-grid pesquisado).
- A combinação Tarifa Social + compensação FV não foi modelada; a economia do FV nesse caso está superestimada.
- A potência na posição verão (58% da de inverno) é uma aproximação; varia por modelo.
- O aquecedor solar foi modelado só com o kit de 300 L pesquisado. Para casas com 1 ou 2 pessoas, um kit menor e mais barato
  pode ter payback melhor do que o calculado.
- **Nenhum valor é garantia de economia:** o assistente repete isso em todas as respostas com números.
