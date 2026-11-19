# Registro de comentários e ajustes

> Preencha depois dos testes. Cada linha é um problema observado → o ajuste feito no código ou no texto.

## Resumo dos testes

Formato usado: **teste por mensagem (WhatsApp)**, com as respostas reais do assistente e 4 perguntas de compreensão
+ 4 de opinião (ver [README.md](README.md)). Fichas individuais: [P1](P1.md), [P2](P2.md).

| Participante | Q1 Gasto | Q2 Economizar sem gastar | Q3 Placa solar | Q4 É garantido? | Clareza (1–5) | Utilidade (1–5) |
|---|---|---|---|---|---|---|
| P1 (19–20 anos) | ✅ | ✅ | ⚠️ parcial | ❌ | 5 | 5 |
| P2 (19–20 anos, trabalha com energia solar) | ✅ | ✅ | ✅ | ❌ | 5 | 5 |
| **Total / média** | 2 de 2 | 2 de 2 | 1 de 2 + 1 parcial | **0 de 2** | **5,0** | **5,0** |

## Problemas → ajustes

| # | O que observamos (quem) | Ajuste realizado | Arquivo | Retestado? |
|---|---|---|---|---|
| 1 | Achou que a economia era **garantida**; o aviso de estimativa passou despercebido (P1 e P2) | Aviso reescrito em destaque: "ATENÇÃO: é uma ESTIMATIVA, a economia NÃO é garantida", explicando do que o valor depende | `energia/assistente.py` (`AVISO`) | Pendente (próximos participantes) |
| 2 | Na placa solar, focou só na economia e não citou telhado nem instalação; as condições estavam no fim da resposta (P1) | Condições movidas para o **início** da resposta, em lista de verificação ("só vale se você tiver..."), e payback explicado como "tempo para o dinheiro voltar, sem contar a instalação". Teste automático garante que as condições aparecem antes dos números | `energia/assistente.py` (`r_fv`), `tests/test_energia.py` | Pendente |
| 3 | Disse que é errado afirmar que a placa solar não ajuda no pico, porque com bateria a energia do dia pode ser usada à noite (P2) | Texto corrigido: a limitação vale para o kit modelado, **on-grid sem bateria**; sistemas com bateria podem ajudar no pico, mas custam bem mais e não foram modelados. Incluído nas limitações da análise e do assistente | `energia/alternativas.py`, `energia/assistente.py`, `docs/analise_energetica.md` | Não se aplica (correção técnica) |
| 4 | Sugeriu, além do banho, desligar da tomada aparelhos em stand-by (P2) | Acrescentada a dica 5 ("fora do banho: tire da tomada aparelhos em stand-by"), sem cálculo, porque está fora do escopo do banho | `energia/assistente.py` (`r_habitos`) | Não se aplica |

### Principais aprendizados até agora
- As 2 pessoas entenderam os números de consumo e as dicas de hábitos (perguntas 1 e 2).
- As 2 deram nota máxima de clareza, mas **nenhuma percebeu que os valores são estimativas** (pergunta 4). O texto
  parecer claro não significa que a mensagem principal sobre limitações chegou.
- As versões testadas eram a primeira; o próximo participante deve receber a versão ajustada para conferir se o
  ajuste 1 resolveu o problema.

### Ajustes já previstos na versão inicial (feitos antes dos testes, a partir de revisão interna)
Estes **não** vieram de usuários. Ficam aqui para separar o que foi decisão de projeto do que veio dos testes.
- Toda resposta com números mostra quais dados foram **estimados** e um exemplo de como informar os próprios.
- Termos técnicos explicados na própria frase ("payback = tempo para o investimento se pagar").
- Botões de sugestão na interface web para quem não sabe o que perguntar.
- A tarifa é calculada a partir da conta do usuário ("R$ X com Y kWh") em vez de pedir "tarifa por kWh".
- Correção de bug (18/11/2026): "dicas para economizar no banho" abria a comparação completa em vez das dicas,
  porque a palavra "economizar" era reconhecida antes de "dicas". A ordem das intenções foi ajustada e o caso
  virou teste automático em `tests/test_energia.py`.
