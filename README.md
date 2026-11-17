# Citizen Assist AI · Módulo de Energia 💡

**Global Solution 2026.2 · Ciência da Computação (1CC) · FIAP**
**Contribuição da disciplina: Soluções em Energias Renováveis e Sustentáveis**

Orientações para famílias de baixa renda gastarem menos com o **banho quente**. O módulo compara mudança de
hábitos, **aquecedor solar** e **energia fotovoltaica** com cálculos, fontes e limitações, tudo integrado ao chat
do Citizen Assist AI.

## 👥 Integrantes

| Nome completo | RM |
|---|---|
| _NOME 1_ | _RM00000_ |
| _NOME 2_ | _RM00000_ |
| _NOME 3_ | _RM00000_ |

📺 **Vídeo (até 3 min):** _cole aqui o link não listado do YouTube_

---

## 🎯 Público e problema

- **Público:** famílias de baixa renda da Grande São Paulo que usam **chuveiro elétrico**, incluindo
  beneficiárias da Tarifa Social (CadÚnico).
- **Necessidade energética:** o chuveiro (4.500–7.500 W) é um dos maiores consumos da casa e é usado no horário de
  pico (18h–21h). Na família de referência (4 pessoas, 8 min, 5.500 W), o banho gasta **88 kWh/mês, cerca de 40% da
  conta**.
- **Como ajudamos:** o assistente calcula o gasto **da própria família**, compara alternativas para a mesma
  necessidade e período e recomenda a melhor, sempre mostrando fontes e limitações.

## ⚡ Funcionalidades de energia no assistente

| O usuário pergunta | O assistente responde com |
|---|---|
| "Quanto gasta meu chuveiro?" | kWh/mês (E = P × t), custo por banho e por mês, % da conta, ΔT da água |
| "Somos 3 pessoas, banho de 10 min, chuveiro 6800 W, conta de R$ 150 com 160 kWh" | Atualiza o perfil e recalcula tudo (a tarifa é tirada da própria conta) |
| "Dicas para economizar" | Alternativa A1 (hábitos): economia em kWh, R$ e litros de água |
| "Vale a pena aquecedor solar?" | Alternativa A2: fração solar, investimento, payback, saldo em 10 anos, efeito no pico |
| "E placa solar?" | Alternativa A3: nº de módulos, geração, Fio B (Lei 14.300), payback |
| "Compare as alternativas" | Tabela A0–A4 + recomendação ordenada e justificada |
| "Tenho tarifa social" | Aplica a gratuidade de 80 kWh (Lei 15.235/2025) e ajusta a recomendação |
| "Impacto ambiental" | CO₂ evitado, potência no pico, água |
| "Fontes" / "Limitações" / "Meus dados" / "Reiniciar" | Referências, premissas, dados usados e limpeza da sessão |

Toda resposta com números traz **fontes** e o aviso de que são **estimativas, não garantias**.

## ▶️ Como executar

Precisa só de **Python 3.9+**, sem bibliotecas externas.

```bash
# 1) Chat no navegador (com gráfico da comparação)
python app_web.py
# abra http://localhost:8000

# 2) Chat no terminal
python app_cli.py

# 3) Gerar as tabelas da análise (CSV + Markdown)
python scripts/gerar_analise.py

# 4) Testes automáticos (cálculos e respostas)
python -m unittest discover -s tests -v
```

## 📁 Organização

```
energia/
  dados.py           parâmetros com unidade, origem e marcação ESTIMADO/PUBLICADO
  calculos.py        fórmulas (energia, ΔT, conta, FV, payback, CO2)
  alternativas.py    comparação A0–A4 e regra de recomendação
  assistente.py      chat: entende a pergunta, extrai dados, responde com fontes e limitações
  referencias.py     referências citadas
app_web.py / web/    interface web (servidor só com biblioteca padrão)
app_cli.py           interface de terminal
scripts/gerar_analise.py
data/                parametros.csv, resultados_cenario_base.csv, sensibilidade.csv, pesquisa_precos.csv
docs/
  analise_energetica.md   ← contexto, dados, cálculos, comparação, justificativas, limitações
  resultados_gerados.md   tabelas geradas pelo código
  referencias.md          lista de fontes
  roteiro_video.md        roteiro do vídeo de 3 min
testes_usuarios/     protocolo, fichas e registro de ajustes
tests/               testes automáticos
```

## 📊 Resultado principal (família de referência, tarifa estimada de R$ 0,95/kWh)

| Alternativa | Economia/mês | Investimento | Payback | CO₂ evitado/ano |
|---|---:|---:|---:|---:|
| A1 Hábitos (5 min + posição verão) | R$ 42,28 | R$ 0 | imediato | 20,6 kg |
| A2 Aquecedor solar 🌱 | R$ 58,52 | R$ 3.500 | 5,8 anos | 28,5 kg |
| A3 Fotovoltaico 1,1 kWp 🌱 | R$ 71,06 | R$ 4.400 | 5,8 anos | 40,7 kg |
| A4 Hábitos + aquecedor solar 🌱 | R$ 71,20 | R$ 3.500 | 4,6 anos | 34,6 kg |

**Recomendação:**
1. Hábitos primeiro.
2. Aquecedor solar como fonte renovável: menor investimento e o único que reduz o pico das 18h–21h.
3. Fotovoltaico para quem tem casa própria e consumo alto.
4. Com Tarifa Social, o FV vai por último.

Detalhes e justificativas em [`docs/analise_energetica.md`](docs/analise_energetica.md).

## ⚠️ Limitações

São estimativas, não garantias. A tarifa é uma média, os preços variam e o clima muda. O payback é simples, sem
juros nem inflação. A combinação Tarifa Social + FV não foi modelada. Lista completa em
[`docs/analise_energetica.md#7-limitações`](docs/analise_energetica.md).

## 🧪 Testes com usuários

Protocolo, fichas e ajustes em [`testes_usuarios/`](testes_usuarios/). Os testes não coletam nome, endereço nem
documentos: os participantes são identificados como P1, P2...

## 📚 Referências

[`docs/referencias.md`](docs/referencias.md)

## 🤖 Uso de IA generativa

Usamos IA generativa como apoio na escrita de código e textos. Todos os dados, cálculos e referências foram
conferidos pela equipe (checklist em [`VERIFICAR.md`](VERIFICAR.md)).
