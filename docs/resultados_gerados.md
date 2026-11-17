# Resultados gerados automaticamente

> Arquivo gerado por `python scripts/gerar_analise.py`. Não edite à mão: mude os parâmetros em `energia/dados.py` e rode o script de novo.

## Cenário 1 – Família de referência, tarifa cheia

4 pessoas, banho de 8 min, chuveiro de 5.500 W sempre no inverno, consumo total de 220 kWh/mês, tarifa estimada de R$ 0,95/kWh. Período de referência: 1 mês (e 1 ano); horizonte de investimento: 10 anos.

| Alt. | Descrição | Banho (kWh/mês) | Conta (R$/mês) | Economia (R$/mês) | Economia (R$/ano) | Investimento (R$) | Payback | Saldo 10 anos (R$) | CO₂ evitado (kg/ano) | Potência média no pico (kW) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A0 | Situação atual (chuveiro elétrico) | 88,0 | 209,00 | 0,00 | 0,00 | 0,00 | — | 0,00 | 0,0 | 5,50 |
| A1 | Hábitos: banho de 5 min + posição verão 6 meses/ano | 43,5 | 166,72 | 42,28 | 507,30 | 0,00 | imediato | 5.073,00 | 20,6 | 4,35 |
| A2 | Aquecedor solar térmico (200 L) com apoio elétrico 🌱 | 26,4 | 150,48 | 58,52 | 702,24 | 3.500,00 | 5,8 anos | 2.522,40 | 28,5 | 1,65 |
| A3 | Fotovoltaico on-grid: 2 módulo(s) (1,10 kWp) 🌱 | 88,0 | 137,94 | 71,06 | 852,72 | 4.400,00 | 5,8 anos | 3.127,20 | 40,7 | 5,50 |
| A4 | Combinação: hábitos (A1) + aquecedor solar (A2) 🌱 | 13,1 | 137,80 | 71,20 | 854,43 | 3.500,00 | 4,6 anos | 4.044,30 | 34,6 | 1,31 |

## Cenário 2 – Mesma família com a Tarifa Social (80 kWh/mês grátis)

| Alt. | Descrição | Banho (kWh/mês) | Conta (R$/mês) | Economia (R$/mês) | Economia (R$/ano) | Investimento (R$) | Payback | Saldo 10 anos (R$) | CO₂ evitado (kg/ano) | Potência média no pico (kW) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A0 | Situação atual (chuveiro elétrico) | 88,0 | 133,00 | 0,00 | 0,00 | 0,00 | — | 0,00 | 0,0 | 5,50 |
| A1 | Hábitos: banho de 5 min + posição verão 6 meses/ano | 43,5 | 90,72 | 42,28 | 507,30 | 0,00 | imediato | 5.073,00 | 20,6 | 4,35 |
| A2 | Aquecedor solar térmico (200 L) com apoio elétrico 🌱 | 26,4 | 74,48 | 58,52 | 702,24 | 3.500,00 | 5,8 anos | 2.522,40 | 28,5 | 1,65 |
| A3 | Fotovoltaico on-grid: 2 módulo(s) (1,10 kWp) 🌱 | 88,0 | 61,94 | 71,06 | 852,72 | 4.400,00 | 5,8 anos | 3.127,20 | 40,7 | 5,50 |
| A4 | Combinação: hábitos (A1) + aquecedor solar (A2) 🌱 | 13,1 | 61,80 | 71,20 | 854,43 | 3.500,00 | 4,6 anos | 4.044,30 | 34,6 | 1,31 |

> No cenário 2, a economia do fotovoltaico (A3) foi calculada com a tarifa cheia, porque a combinação gratuidade + compensação de créditos não foi modelada; por isso o valor está **superestimado**.

## Sensibilidade (payback em anos)

| Tarifa (R$/kWh) | Banho (min) | Fração solar | Payback A2 | Payback A3 | Payback A4 |
|---:|---:|---:|---:|---:|---:|
| 0,75 | 5 | 0,7 | 14,2 | 6,9 | 12,6 |
| 0,75 | 8 | 0,7 | 7,7 | 7,7 | 6,1 |
| 0,75 | 12 | 0,7 | 4,8 | 7,3 | 3,6 |
| 0,95 | 5 | 0,7 | 10,3 | 5,1 | 9,3 |
| 0,95 | 8 | 0,6 | 7,0 | 5,8 | 5,0 |
| 0,95 | 8 | 0,7 | 5,8 | 5,8 | 4,6 |
| 0,95 | 8 | 0,8 | 5,0 | 5,8 | 4,4 |
| 0,95 | 12 | 0,7 | 3,7 | 5,6 | 2,8 |
| 1,15 | 5 | 0,7 | 8,1 | 4,0 | 7,3 |
| 1,15 | 8 | 0,7 | 4,7 | 4,7 | 3,7 |
| 1,15 | 12 | 0,7 | 3,0 | 4,6 | 2,3 |

Tabela completa (27 combinações) em `data/sensibilidade.csv`.
