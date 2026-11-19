# Citizen Assist AI

Assistente de terminal, feito em Python, que orienta **pessoas idosas (60 anos ou mais) e seus familiares** sobre saúde no SUS, transporte gratuito e direitos. Ele usa só informações de fontes oficiais, sempre mostra a fonte e a data de verificação e **não coleta dados pessoais**.

> Global Solution 2026.2 · Pensamento Computacional e Automação com Python (desafio CitizenTech)

## Integrantes

| Nome | RM |
|------|----|
| Gabriel Villas | 571603 |
| Nathan Werner | 572925 |

## Público e problema

**Público:** pessoas com 60 anos ou mais e os familiares que cuidam delas.

**Problema:** muitas pessoas idosas não sabem como fazer o Cartão SUS, onde tomar vacina, como pegar remédio de graça, se têm direito ao ônibus gratuito ou ao BPC. A informação existe, mas fica espalhada em vários sites, escrita em linguagem técnica, e golpistas se aproveitam dessa dúvida (por exemplo, com falsas "provas de vida" do INSS).

## ODS relacionados

- **ODS 3 – Saúde e bem-estar** (Cartão SUS, vacinação, Farmácia Popular, SAMU)
- **ODS 10 – Redução das desigualdades** (BPC, atendimento prioritário, acesso simples a serviços públicos)
- **ODS 11 – Cidades e comunidades sustentáveis** (transporte gratuito e acessível)
- **ODS 16 – Paz, justiça e instituições eficazes** (denúncia de violência contra a pessoa idosa)

## Como executar

Precisa de Python 3.8 ou superior. Não usa bibliotecas externas.

```bash
python main.py
```

Menu principal:

1. Fazer uma pergunta (texto livre)
2. Navegar por categorias
3. Ver indicadores
4. Exportar atendimentos (CSV)
0. Sair (pede uma nota de facilidade de 1 a 5)

## Estrutura

```
citizen-assist-ai/
├── README.md
├── main.py                  # cria os objetos e mostra o menu
├── orientacao.py            # classe Orientacao
├── base_conhecimento.py     # classe BaseConhecimento + normalizar()
├── assistente.py            # classe Assistente (atendimento, histórico, indicadores, CSV)
└── data/
    ├── base_conhecimento.json   # 13 orientações, 3 categorias
    ├── historico.json           # atendimentos registrados
    ├── avaliacoes.json          # notas de facilidade (criado ao sair)
    └── atendimentos.csv         # gerado pela opção 4 do menu
```

### Classes (composição)

```
Assistente
 └── base: BaseConhecimento
      └── orientacoes: [Orientacao, Orientacao, ...]
```

| Classe | Atributos | Métodos |
|--------|-----------|---------|
| `Orientacao` | id, categoria, titulo, palavras_chave, resposta, documentos, onde, fonte, verificado_em | `exibir()` |
| `BaseConhecimento` | caminho, orientacoes | `carregar()`, `categorias()`, `por_categoria()`, `pontuar()`, `buscar()` |
| `Assistente` | nome, base, historico, avaliacoes | `perguntar()`, `navegar()`, `registrar()`, `indicadores()`, `exportar_csv()`, `avaliar()` |

## Regra de pontuação

A pergunta, as palavras-chave e o título são normalizados com `normalizar()`: minúsculas, sem acentos e sem pontuação.

| Regra | Pontos |
|-------|--------|
| Palavra-chave da orientação aparece na pergunta | +3 |
| Palavra da pergunta (4 letras ou mais) aparece no título | +1 |
| Melhor orientação com 6 pontos ou mais | Confiança **ALTA** |
| Melhor orientação com 3 a 5 pontos | Confiança **MÉDIA** |
| Nenhuma com 3 pontos | "Não encontrei" + sugestão de categorias |

`buscar()` devolve uma lista de tuplas `(pontos, orientacao)` em ordem decrescente. O assistente mostra a melhor orientação e até 2 alternativas.

Ajustes que fizemos em relação ao enunciado:
- além de `?!.,;:()`, também removemos `- / " '`;
- as palavras da pergunta viram um `set`, então uma palavra repetida só soma ponto uma vez no título.

**Exemplo:** "Como faço o cartão do SUS?" → orientação 1 recebe +3 (`cartao do sus`) +3 (`sus`) +1 (`cartao` está no título) = **7 pontos, ALTA**. A palavra "como" tem 4 letras, mas não está no título, então não soma.

## Regras de atendimento

- Todas as telas têm "0 para voltar".
- Opção fora da faixa, letras, resposta vazia ou s/n inválido não encerram o programa.
- Pergunta com 8 ou mais dígitos ou com `@` é recusada e **não é registrada**.
- Toda resposta mostra a fonte, a data de verificação e o aviso de que o assistente não é canal oficial.
- Se o JSON da base estiver ausente ou corrompido, o programa avisa e continua aberto, sem travar. Se o histórico estiver corrompido, começa uma lista nova.

## Histórico e indicadores

Cada atendimento é salvo em `data/historico.json` com: `data`, `origem` (pergunta/categoria), `pergunta`, `id_orientacao`, `encontrou`, `ajudou`, `tentativas` e `tempo_segundos`.

- **Tentativas:** quantas perguntas ou alternativas a pessoa precisou até resolver (ou desistir).
- **Tempo:** `time.time()` no início do atendimento e `round(time.time() - inicio, 1)` no fim.

Indicadores: resposta encontrada (%), taxa de acerto (%), tempo médio para encontrar (só dos atendimentos que ajudaram), tentativas por atendimento, facilidade de uso (média das notas) e lista de dúvidas sem solução.

## Integrações com outras disciplinas

Não houve.

## Fontes consultadas

- Ministério da Saúde (Cartão SUS, vacinação, Farmácia Popular, SAMU): https://www.gov.br/saude
- Meu SUS Digital: https://meususdigital.saude.gov.br
- Estatuto da Pessoa Idosa (Lei 10.741/2003): https://www.planalto.gov.br/ccivil_03/leis/2003/l10.741.htm
- INSS (BPC e prova de vida): https://www.gov.br/inss
- Ministério dos Direitos Humanos (Disque 100): https://www.gov.br/mdh

## Resultado do teste com usuários

Testamos com **PREENCHER** pessoas de fora da equipe, em **PREENCHER** atendimentos. Não registramos nomes nem dados pessoais.

| Indicador | Resultado |
|-----------|-----------|
| Resposta encontrada | PREENCHER % |
| Taxa de acerto (ajudou) | PREENCHER % |
| Tempo médio para encontrar | PREENCHER s |
| Tentativas por atendimento | PREENCHER |
| Facilidade de uso | PREENCHER / 5 |

**Dúvidas sem solução:** PREENCHER

**Melhoria feita a partir do teste:** PREENCHER (ex.: incluímos a palavra-chave "..." na orientação X porque a pergunta "..." não era encontrada).

## Limitações

- A busca compara palavras exatas: erros de digitação ("cartera") e sinônimos que não estão nas palavras-chave não são reconhecidos.
- Palavras-chave curtas (como "sus" ou "app") podem fazer uma orientação ganhar pontos em perguntas sobre outro assunto.
- Regras que mudam de cidade para cidade (ônibus grátis entre 60 e 64 anos, credencial de estacionamento) só são explicadas de forma geral.
- Pessoas idosas com pouca familiaridade com tecnologia podem ter dificuldade de usar o terminal sem ajuda.
- A base é estática: se uma regra oficial mudar, alguém precisa atualizar o JSON e a data de verificação.
- Não é um canal oficial e não substitui o atendimento dos órgãos públicos.

## Vídeo técnico

PREENCHER (link do YouTube, não listado)
