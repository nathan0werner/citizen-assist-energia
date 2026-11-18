# Checklist antes da entrega

O enunciado exige que a equipe confira dados, cálculos e referências. Marque cada item.

## Dados (energia/dados.py → rode `python scripts/gerar_analise.py` depois de mudar)
- [ ] **Tarifa:** hoje usamos R$ 1,09/kWh (valor de referência da equipe). Abra a página de tarifas da ANEEL e confira a tarifa B1 residencial (TE + TUSD).
  Uma conta de luz real (total ÷ kWh) é a melhor checagem. Ajuste `tarifa_kwh` se necessário.
- [ ] **Faixas de ICMS em SP** para consumo residencial: usamos 12% como aproximação.
- [ ] **Lei 15.235/2025:** confirme a gratuidade de 80 kWh e os critérios no site do Planalto ou da ANEEL.
- [ ] **Fator de emissão MCTI:** veja se já existe a média anual de 2024/2025 e atualize `fator_emissao_kg_kwh`.
- [ ] **Irradiação em São Paulo:** consulte o CRESESB SunData com o CEP/coordenadas e confirme os ~4,6 kWh/m²/dia.
- [ ] **Preços:** preencha `data/pesquisa_precos.csv` com pelo menos 3 orçamentos reais de aquecedor solar e de FV
  (loja/site, data, valor) e ajuste `custo_aquecedor_solar` e `custo_fv_r_kwp` pela média.
- [ ] **Potência verão/inverno:** confira na tabela do INMETRO ou na embalagem de um chuveiro comum.
- [ ] **PROCEL PPH 2019:** confirme a participação do chuveiro no consumo residencial e cite o número exato.

## Links
- [ ] Abra cada link de `docs/referencias.md`; troque os que estiverem quebrados.

## Entrega
- [ ] Nomes e RMs no README e no `entrega.txt`.
- [ ] Testes com usuários feitos e `testes_usuarios/` preenchido.
- [ ] Vídeo com até 3:00, **não listado**, link testado numa aba anônima.
- [ ] Repositório **público** (ou com acesso liberado ao professor), link testado numa aba anônima.
- [ ] `python -m unittest discover -s tests` passando.
- [ ] Apagar este arquivo da entrega final, ou deixá-lo com tudo marcado como evidência de verificação.
