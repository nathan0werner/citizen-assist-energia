# Roteiro do vídeo técnico (3:00, YouTube não listado)

Narração sincronizada com o arquivo `video_sem_som.mp4` (gravação automática da tela). Os tempos abaixo são os
momentos em que cada cena aparece no vídeo. Fale num ritmo tranquilo: cada trecho cabe no tempo indicado.

| Tempo | O que aparece na tela | O que falar |
|---|---|---|
| **0:00–0:05** | Abertura com o título | "Olá! Somos Gabriel e Nathan, da turma 1CCPK. Este é o módulo de energia do Citizen Assist AI." |
| **0:05–0:20** | README: público e problema (destacado) | "Nosso público são famílias de baixa renda da Grande São Paulo que usam chuveiro elétrico. Ele é um dos maiores gastos da conta e é usado no horário de pico, das 18 às 21 horas." |
| **0:20–0:38** | Análise: tabela de fórmulas | "Aplicamos os conceitos da disciplina. Energia é potência vezes tempo: um chuveiro de 5,5 quilowatts ligado 16 horas por mês gasta 88 quilowatts-hora, cerca de 40% da conta. Também calculamos o aquecimento da água, a geração solar e o payback." |
| **0:38–0:55** | Análise: tabela de dados e premissas | "Cada dado tem origem indicada: ANEEL, INMETRO, CRESESB e MCTI. O que é estimativa está marcado como estimado. Os preços dos equipamentos vieram de anúncios reais que pesquisamos." |
| **0:55–1:18** | Tabela de resultados (família de 4 pessoas) | "Comparamos as alternativas para a mesma necessidade e o mesmo período. Mudar hábitos economiza 48 reais por mês sem custo. A placa solar custa 4.159 reais e se paga em 4,7 anos. O aquecedor solar custa 5.624 e se paga em 8 anos, mas é o que mais alivia o horário de pico." |
| **1:18–1:35** | Caso real: casa de 2 pessoas | "Também testamos a casa de um integrante, com 2 pessoas e chuveiro fraco. Ali, nenhum equipamento se paga bem, e o melhor é só mudar hábitos. Por isso o assistente calcula para cada família." |
| **1:35–1:50** | Demonstração: digitando os dados no chat | "Agora a demonstração. O usuário informa quantas pessoas moram na casa, o tempo de banho, a potência do chuveiro e o valor da conta. O assistente calcula a tarifa real a partir da conta." |
| **1:50–2:11** | Demonstração: comparação e recomendação | "Ao pedir a comparação, ele mostra a economia, o investimento e o tempo de retorno de cada opção, e recomenda uma ordem: primeiro hábitos, depois a fonte renovável que faz mais sentido, sempre com as fontes." |
| **2:11–2:22** | Demonstração: "tenho tarifa social" | "Se a família tem Tarifa Social, os primeiros 80 quilowatts-hora já são grátis. O assistente refaz as contas e muda a recomendação." |
| **2:22–2:30** | Demonstração: limitações | "E ele sempre mostra as limitações: são estimativas, não garantias." |
| **2:30–2:55** | Testes com usuários e ajustes | "Testamos com 3 pessoas. Todas entenderam os números, com nota média 5 de clareza. Mas, na primeira versão, ninguém percebeu que a economia era uma estimativa. Deixamos o aviso em destaque e, no reteste, a pessoa acertou. Também corrigimos o texto sobre placas com bateria, por sugestão de uma participante." |
| **2:55–3:00** | Tela final: recomendação | "Recomendação: comece pelos hábitos. Obrigado!" |

## Como gravar a voz por cima

**Opção mais fácil (Windows):**
1. Abra o `video_sem_som.mp4` no player de vídeo, em tela cheia.
2. Aperte **Windows + Alt + M** para ligar o microfone e **Windows + Alt + R** para começar a gravar.
3. Dê play e leia a narração seguindo os tempos da tabela.
4. Aperte **Windows + Alt + R** para parar. O vídeo com a voz fica em **Vídeos → Capturas**.

**Opção com editor (Clipchamp, que já vem no Windows 11, ou CapCut):**
1. Importe o `video_sem_som.mp4`.
2. Grave a narração no próprio editor (ou no celular) e coloque o áudio na linha do tempo, embaixo do vídeo.
3. Exporte em 1080p ou 720p.

Depois suba no YouTube como **"Não listado"** e mande o link para colocar no README e no `entrega.txt`.

> Se os números mudarem, rode `python scripts/gerar_analise.py` e atualize as falas.
