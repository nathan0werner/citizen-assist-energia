# Resultados gerados automaticamente

> Arquivo gerado por `python scripts/gerar_analise.py`. Não edite à mão: mude os parâmetros em `energia/dados.py` e rode o script de novo.

## Cenário 1 – Família de referência, tarifa cheia

4 pessoas, banho de 8 min, chuveiro de 5.500 W sempre no inverno, consumo total de 220 kWh/mês, tarifa de referência de R$ 1,09/kWh. Período de referência: 1 mês (e 1 ano); horizonte de investimento: 10 anos.

| Alt. | Descrição | Banho (kWh/mês) | Conta (R$/mês) | Economia (R$/mês) | Economia (R$/ano) | Investimento (R$) | Payback | Saldo 10 anos (R$) | CO₂ evitado (kg/ano) | Potência média no pico (kW) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A0 | Situação atual (chuveiro elétrico) | 88,0 | 239,80 | 0,00 | 0,00 | 0,00 | — | 0,00 | 0,0 | 5,50 |
| A1 | Hábitos: banho de 5 min + posição verão 6 meses/ano | 43,5 | 191,30 | 48,50 | 582,06 | 0,00 | imediato | 5.820,60 | 20,6 | 4,35 |
| A2 | Aquecedor solar térmico (300 L) com apoio elétrico 🌱 | 26,4 | 172,66 | 67,14 | 805,73 | 5.624,00 | 8,0 anos | 1.433,28 | 28,5 | 1,65 |
| A3 | Kit fotovoltaico on-grid 2,48 kWp 🌱 | 88,0 | 158,27 | 81,53 | 978,38 | 4.159,00 | 4,7 anos | 4.624,84 | 40,7 | 5,50 |
| A4 | Combinação: hábitos (A1) + aquecedor solar (A2) 🌱 | 13,1 | 158,10 | 81,70 | 980,35 | 5.624,00 | 6,4 anos | 3.179,46 | 34,6 | 1,31 |

## Cenário 2 – Mesma família com a Tarifa Social (80 kWh/mês grátis)

| Alt. | Descrição | Banho (kWh/mês) | Conta (R$/mês) | Economia (R$/mês) | Economia (R$/ano) | Investimento (R$) | Payback | Saldo 10 anos (R$) | CO₂ evitado (kg/ano) | Potência média no pico (kW) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A0 | Situação atual (chuveiro elétrico) | 88,0 | 152,60 | 0,00 | 0,00 | 0,00 | — | 0,00 | 0,0 | 5,50 |
| A1 | Hábitos: banho de 5 min + posição verão 6 meses/ano | 43,5 | 104,10 | 48,51 | 582,06 | 0,00 | imediato | 5.820,60 | 20,6 | 4,35 |
| A2 | Aquecedor solar térmico (300 L) com apoio elétrico 🌱 | 26,4 | 85,46 | 67,14 | 805,73 | 5.624,00 | 8,0 anos | 1.433,28 | 28,5 | 1,65 |
| A3 | Kit fotovoltaico on-grid 2,48 kWp 🌱 | 88,0 | 71,07 | 81,53 | 978,38 | 4.159,00 | 4,7 anos | 4.624,84 | 40,7 | 5,50 |
| A4 | Combinação: hábitos (A1) + aquecedor solar (A2) 🌱 | 13,1 | 70,90 | 81,70 | 980,35 | 5.624,00 | 6,4 anos | 3.179,46 | 34,6 | 1,31 |

> No cenário 2, a economia do fotovoltaico (A3) foi calculada com a tarifa cheia, porque a combinação gratuidade + compensação de créditos não foi modelada; por isso o valor está **superestimado**.

## Cenário 3 – Casa de um integrante da equipe (2 pessoas)

2 pessoas, banho de 8 min, chuveiro de baixa potência (4.500 W, **estimado**: a equipe descreveu como "fraquinho"), consumo total de 83,1 kWh/mês (referência informada pela equipe).

| Alt. | Descrição | Banho (kWh/mês) | Conta (R$/mês) | Economia (R$/mês) | Economia (R$/ano) | Investimento (R$) | Payback | Saldo 10 anos (R$) | CO₂ evitado (kg/ano) | Potência média no pico (kW) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A0 | Situação atual (chuveiro elétrico) | 36,0 | 90,58 | 0,00 | 0,00 | 0,00 | — | 0,00 | 0,0 | 4,50 |
| A1 | Hábitos: banho de 5 min + posição verão 6 meses/ano | 17,8 | 70,74 | 19,84 | 238,12 | 0,00 | imediato | 2.381,21 | 8,4 | 3,56 |
| A2 | Aquecedor solar térmico (300 L) com apoio elétrico 🌱 | 10,8 | 63,11 | 27,47 | 329,62 | 5.624,00 | 24,5 anos | -3.327,84 | 11,6 | 1,35 |
| A3 | Kit fotovoltaico on-grid 2,48 kWp 🌱 | 36,0 | 59,91 | 30,67 | 368,01 | 4.159,00 | 15,5 anos | -1.478,94 | 15,3 | 4,50 |
| A4 | Combinação: hábitos (A1) + aquecedor solar (A2) 🌱 | 5,3 | 57,16 | 33,42 | 401,05 | 5.624,00 | 18,7 anos | -2.613,48 | 14,2 | 1,07 |

> Recomendação do código para este caso: A1 → A3. Com pouco uso de água quente, o aquecedor solar de 300 L não se paga dentro da vida útil (15 anos) e sai da recomendação.

## Sensibilidade (payback em anos)

| Tarifa (R$/kWh) | Banho (min) | Fração solar | Payback A2 | Payback A3 | Payback A4 |
|---:|---:|---:|---:|---:|---:|
| 0,90 | 5 | 0,7 | 17,8 | 10,3 | 15,9 |
| 0,90 | 8 | 0,7 | 9,9 | 5,9 | 7,9 |
| 0,90 | 12 | 0,7 | 6,3 | 3,7 | 4,7 |
| 1,09 | 5 | 0,7 | 13,9 | 8,1 | 12,5 |
| 1,09 | 8 | 0,6 | 9,5 | 4,7 | 6,8 |
| 1,09 | 8 | 0,7 | 8,0 | 4,7 | 6,4 |
| 1,09 | 8 | 0,8 | 6,9 | 4,7 | 6,0 |
| 1,09 | 12 | 0,7 | 5,1 | 3,0 | 3,9 |
| 1,30 | 5 | 0,7 | 11,2 | 6,6 | 10,1 |
| 1,30 | 8 | 0,7 | 6,5 | 3,9 | 5,3 |
| 1,30 | 12 | 0,7 | 4,2 | 2,5 | 3,2 |

Tabela completa (27 combinações) em `data/sensibilidade.csv`.
