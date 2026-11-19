# Roteiro do vídeo técnico (máx. 3:00, YouTube não listado)

**Dica:** grave a tela com o OBS (ou com o Win+G do Windows), com a voz de um integrante. Deixe o
`python app_web.py` aberto e as perguntas copiadas antes de começar. Ensaie com cronômetro.

| Tempo | Tela | Fala (sugestão) |
|---|---|---|
| 0:00–0:20 | Título + README | "Somos o grupo ___. Na disciplina de Energias Renováveis, o Citizen Assist AI ganhou um módulo para famílias de baixa renda da Grande SP que usam chuveiro elétrico, um dos maiores gastos da conta e o principal responsável pelo pico das 18 às 21h." |
| 0:20–0:55 | `docs/analise_energetica.md`, seção 3 | "Para uma família de 4 pessoas com banho de 8 minutos e chuveiro de 5.500 watts, a energia é potência vezes tempo: 5,5 kW vezes 16 horas, ou seja, 88 kWh por mês, cerca de 40% da conta. Os dados vêm do INMETRO, da ANEEL, do CRESESB e do MCTI. O que é estimativa está marcado no arquivo parametros.csv." |
| 0:55–1:35 | Tabela de resultados | "Comparamos para a mesma necessidade e o mesmo período: hábitos, aquecedor solar e placas fotovoltaicas. Com tarifa de R$ 1,09 por kWh, os hábitos economizam R$ 48 por mês sem custo. Pesquisamos preços reais: o kit fotovoltaico de 2,48 kWp custa R$ 4.159 e se paga em 4,7 anos, mas não reduz o pico noturno. O aquecedor solar de 300 litros custa R$ 5.624 e se paga em 8 anos, mas tira o chuveiro do horário de pico. Numa casa de 2 pessoas, só os hábitos compensam. Como a rede brasileira é limpa, o CO₂ evitado é modesto; o ganho maior é aliviar o pico." |
| 1:35–2:30 | **Demo** no navegador | Digite: "somos 3 pessoas, banho de 10 minutos, chuveiro 6800 W, conta de R$ 150 com 160 kWh" → "compare as alternativas" → "tenho tarifa social" → "limitações". Fala: "O assistente usa os dados da família e as mesmas funções da análise. A recomendação muda: com Tarifa Social, os primeiros 80 kWh são grátis e a placa fotovoltaica vai para o fim. Toda resposta mostra fontes e avisa que é estimativa." |
| 2:30–2:55 | `testes_usuarios/registro_ajustes.md` | "Testamos com 2 pessoas por mensagem. As duas entenderam os números e as dicas e deram nota 5, mas nenhuma percebeu que a economia é uma estimativa. Por isso deixamos o aviso em destaque. Uma participante que trabalha com energia solar lembrou que, com bateria, a placa ajuda à noite; corrigimos o texto para deixar claro que o nosso kit é sem bateria." |
| 2:55–3:00 | README | "Recomendação: comece pelos hábitos; para investir, o assistente compara placa e aquecedor solar para a sua casa. Obrigado!" |

> Se os números mudarem (por exemplo, depois de corrigir um parâmetro), rode `python scripts/gerar_analise.py`
> e atualize as falas.
