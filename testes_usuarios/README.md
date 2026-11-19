# Testes com usuários

> **Equipe:** este diretório traz o **protocolo** e os **modelos** prontos. Os registros precisam ser preenchidos
> com testes **reais**: não inventem respostas. Com 4 a 6 participantes já dá para tirar boas conclusões.

## Objetivo
Verificar se o público entende as orientações de energia e as acha úteis, e ajustar o assistente com base nisso.

## Participantes
- 4 a 6 pessoas do público ou próximas dele: moradores de casa com chuveiro elétrico; de preferência alguém
  com Tarifa Social e alguém com mais de 50 anos.
- **Privacidade:** nada de nome, endereço, CPF ou foto da conta. Identifique como P1, P2... e registre só a faixa
  etária e se usa chuveiro elétrico ou tem Tarifa Social. Peça autorização verbal antes.

## Como aplicar (10–15 min por pessoa)
1. Explique em uma frase: "É um assistente que ajuda a gastar menos com o banho. Queremos ver se ele é fácil de entender."
2. Abra `python app_web.py` no celular ou notebook e entregue para a pessoa usar sozinha.
3. Peça as tarefas do [roteiro_tarefas.md](roteiro_tarefas.md), sem ajudar. Anote onde ela travou.
4. No final, faça as perguntas da [ficha_registro.md](ficha_registro.md).
5. Registre cada participante numa cópia da ficha (`P1.md`, `P2.md`...).
6. Junte os problemas em [registro_ajustes.md](registro_ajustes.md), corrija o código e, se possível, teste de novo.

### Alternativa: teste por mensagem (sem rodar o programa)
Se não der para a pessoa usar o assistente na hora, mande pelo WhatsApp as **respostas reais** do assistente
(geradas pelo próprio código) e as perguntas de compreensão. Registre na ficha que o teste foi "por mensagem". Esse
formato avalia se as orientações são **compreensíveis**, mas não avalia a navegação no chat; deixe isso claro no
registro.

## Métricas
- Tarefas concluídas sem ajuda (de 5).
- Nota de clareza (1–5) e de utilidade (1–5).
- Se a pessoa consegue explicar com as próprias palavras a recomendação e uma limitação (sim/não).
