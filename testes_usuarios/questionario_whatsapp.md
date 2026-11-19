# Questionário por mensagem (WhatsApp)

Versão do teste para quem não pode usar o assistente na hora (ver [README.md](README.md)).

- As respostas abaixo são as que o assistente dá de verdade (`energia/assistente.py`, versão de 18/11/2026). Só a
  lista de fontes foi retirada, para a mensagem não ficar longa demais.
- As perguntas 1 a 4 verificam a **compreensão**: a resposta está no texto. As perguntas 5 a 8 coletam **opinião**.
- Não pedimos nome, só a idade aproximada.

---

```
Oi! Tô fazendo um trabalho da faculdade: um assistente que ajuda famílias a gastar menos com o chuveiro elétrico. Queria sua opinião sincera, leva 5 minutinhos 🙏

Imagina que você perguntou isso pro assistente. Lê a resposta dele e depois responde as perguntas lá embaixo.

━━━━━━━━━━━━━━
📱 PERGUNTA 1: "Quanto gasta meu chuveiro? Somos 4 pessoas, banho de 8 minutos, chuveiro 5500 W"

🤖 RESPOSTA:
🚿 Seu chuveiro de 5500 W usado 8 min por pessoa, por 4 pessoas, funciona cerca de 16 horas por mês.
• Energia: 5,50 kW × 16 h ≈ 88 kWh/mês (≈ 40% do consumo da casa).
• Cada banho de 8 min custa ≈ R$ 0,80.
• Na conta: ≈ R$ 95,92/mês só com banho.
⚠️ Valores aproximados. Não são garantia de economia.

━━━━━━━━━━━━━━
📱 PERGUNTA 2: "Dicas para economizar no banho"

🤖 RESPOSTA:
✅ Dicas de custo zero para o banho:
1. Banho de até 5 minutos por pessoa (desligue ao se ensaboar).
2. Use a posição verão nos meses quentes (out–mar): a potência cai de 5500 W para 3200 W.
3. Evite banhos entre 18h e 21h quando possível: é o horário de pico da rede.
4. Não faça gambiarra na resistência: troque só pela original.
📉 Para sua casa, isso economiza ≈ R$ 48,50 por mês (R$ 582 por ano), sem gastar nada.
💧 Bônus: ≈ 1,1 mil litros de água a menos por mês.

━━━━━━━━━━━━━━
📱 PERGUNTA 3: "Vale a pena colocar placa solar?"

🤖 RESPOSTA:
🔆 Placas solares geram eletricidade de dia; o que não é usado vai para a rede e volta como crédito na conta.
• Investimento ≈ R$ 4.159 pelo kit (sem instalação); economia ≈ R$ 81,53/mês.
• Payback simples: 4,7 anos.
• Comparando: aquecedor solar custa R$ 5.624 e tem payback de 8 anos.
🏠 Exige telhado próprio, sem sombra, e liberação da companhia de energia.
⚠️ A instalação é cobrada à parte. Não ajuda no horário de pico (18h–21h), porque gera de dia e o banho é à noite.

━━━━━━━━━━━━━━
❓ AGORA ME RESPONDE:

1. Quanto o chuveiro dessa família gasta por mês, em reais?
2. O que dá pra fazer para economizar SEM gastar dinheiro?
3. Pra essa família, vale a pena placa solar? Por quê?
4. Essa economia é garantida?
5. Teve alguma palavra ou número que você não entendeu?
6. De 1 a 5, quão fácil foi entender?
7. De 1 a 5, isso seria útil na sua casa?
8. O que você mudaria?

Pode responder por áudio se preferir! E me fala só sua idade aproximada (não precisa nome) 😊
```

---

## Respostas esperadas (para corrigir as perguntas 1 a 4)

| Pergunta | Resposta certa |
|---|---|
| 1 | Cerca de R$ 96 por mês |
| 2 | Banho de até 5 min, posição verão nos meses quentes, evitar 18h–21h |
| 3 | Pode valer: se paga em ~4,7 anos, mas precisa de telhado próprio e a instalação é cobrada à parte |
| 4 | Não, são valores aproximados |
