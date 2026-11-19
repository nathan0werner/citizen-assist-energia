# Registro de comentários e ajustes

> Preencha depois dos testes. Cada linha é um problema observado → o ajuste feito no código ou no texto.

## Resumo dos testes

Formato usado: **teste por mensagem (WhatsApp)**, com as respostas reais do assistente e 4 perguntas de compreensão
+ 4 de opinião (ver [README.md](README.md)). Fichas individuais: [P1](P1.md), [P2](P2.md), [P3](P3.md). P1 e P2 receberam a primeira versão; P3 recebeu a
versão ajustada após o P1.

| Participante | Q1 Gasto | Q2 Economizar sem gastar | Q3 Placa solar | Q4 É garantido? | Clareza (1–5) | Utilidade (1–5) |
|---|---|---|---|---|---|---|
| P1 (19–20 anos) | ✅ | ✅ | ⚠️ parcial | ❌ | 5 | 5 |
| P2 (19–20 anos, trabalha com energia solar) | ✅ | ✅ | ✅ | ❌ | 5 | 5 |
| P3 (29 anos) · versão ajustada | ✅ | ✅ | ⚠️ parcial | ✅ | 5 | 4 |
| **Total / média** | 3 de 3 | 3 de 3 | 1 de 3 + 2 parciais | **1 de 3** (0 de 2 na 1ª versão; 1 de 1 na ajustada) | **5,0** | **4,7** |

## Problemas → ajustes

| # | O que observamos (quem) | Ajuste realizado | Arquivo | Retestado? |
|---|---|---|---|---|
| 1 | Achou que a economia era **garantida**; o aviso de estimativa passou despercebido (P1 e P2) | Aviso reescrito em destaque: "ATENÇÃO: é uma ESTIMATIVA, a economia NÃO é garantida", explicando do que o valor depende | `energia/assistente.py` (`AVISO`) | **Sim (P3):** acertou que é estimativa |
| 2 | Na placa solar, focou só na economia e não citou telhado nem instalação; as condições estavam no fim da resposta (P1) | Condições movidas para o **início** da resposta, em lista de verificação ("só vale se você tiver..."), e payback explicado como "tempo para o dinheiro voltar, sem contar a instalação". Teste automático garante que as condições aparecem antes dos números | `energia/assistente.py` (`r_fv`), `tests/test_energia.py` | Sim (P3): ainda não citou as condições; sem efeito claro |
| 3 | Disse que é errado afirmar que a placa solar não ajuda no pico, porque com bateria a energia do dia pode ser usada à noite (P2) | Texto corrigido: a limitação vale para o kit modelado, **on-grid sem bateria**; sistemas com bateria podem ajudar no pico, mas custam bem mais e não foram modelados. Incluído nas limitações da análise e do assistente | `energia/alternativas.py`, `energia/assistente.py`, `docs/analise_energetica.md` | Não se aplica (correção técnica) |
| 4 | Sugeriu, além do banho, desligar da tomada aparelhos em stand-by (P2) | Acrescentada a dica 5 ("fora do banho: tire da tomada aparelhos em stand-by"), sem cálculo, porque está fora do escopo do banho | `energia/assistente.py` (`r_habitos`) | Não se aplica |

### Principais aprendizados
- As 3 pessoas entenderam os números de consumo e as dicas de hábitos (perguntas 1 e 2).
- Clareza média de 5,0 e utilidade de 4,7.
- Na primeira versão, **nenhuma das 2 pessoas percebeu que os valores são estimativas**, apesar da nota máxima de
  clareza. Com o aviso reescrito em destaque, a pessoa que testou a versão ajustada acertou. É um bom sinal, mas,
  com só 1 reteste, não é uma prova.
- Mesmo com as condições da placa solar no início da resposta, as pessoas respondem "vale a pena" olhando só para a
  economia. Uma melhoria futura seria o assistente perguntar primeiro se a pessoa tem telhado próprio, antes de
  mostrar os números.
- Limitação dos testes: amostra pequena (3 pessoas de 19 a 29 anos) e teste por mensagem, sem uso direto do chat.
