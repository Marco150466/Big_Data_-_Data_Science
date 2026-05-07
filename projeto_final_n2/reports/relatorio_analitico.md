# Relatorio Analitico - Produção de Tomate por Regiões de Goiás (2012-2022)
## Resumo Analitico
A base de dados apresenta informacoes consolidadas sobre a cultura do tomate no estado de Goias por Regiao de Planejamento (periodo de 2012 a 2022). O cultivo e analisado sob duas oticas distintas: o tomate de mesa (consumo in natura) e o tomate industrial (destinado ao processamento industrial). Ela e altamente adequada para analises macroeconomicas e de distribuicao geografica do agronegocio goiano.
**Fonte dos dados de entrada:** Banco de Dados Estatisticos de Goias (BDE/IMB) - [https://www.imb.go.gov.br/bde/](https://www.imb.go.gov.br/bde/)

## Dimensao da Base Consolidada
- **Registros Totais (Regioes x Anos):** 55
- **Colunas Analisadas:** 8

## Dicionario de Dados

| Coluna | Tipo | Descricao |
|---|---|---|
| Regiao | str | Regiao de Planejamento do Estado de Goias. |
| Ano | int64 | Ano da safra agricola analisada (2012 a 2022). |
| Qtd_Produzida_Mesa_t | float64 | Quantidade produzida de tomate de mesa em toneladas (t). |
| Area_Colhida_Mesa_ha | float64 | Area de tomate de mesa colhida em hectares (ha). |
| Qtd_Produzida_Ind_t | float64 | Quantidade produzida de tomate industrial em toneladas (t). |
| Area_Colhida_Ind_ha | float64 | Area de tomate industrial colhida em hectares (ha). |
| Produtividade_Mesa_tha | float64 | Produtividade calculada para tomate de mesa em toneladas por hectare (t/ha). |
| Produtividade_Industrial_tha | float64 | Produtividade calculada para tomate industrial em toneladas por hectare (t/ha). |

## Estatistica Descritiva

### Area_Colhida_Mesa_ha

- **Registros Validos:** 55
- **Valores Faltantes:** 0
- **Media:** 141,55
- **Mediana:** 53,00
- **Moda:** 0,00
- **Desvio Padrao:** 182,18
- **Variancia:** 33.191,10
- **Minimo:** 0,00
- **Q1 (Primeiro Quartil - 25%):** 0,00
- **Q2 (Mediana - 50%):** 53,00
- **Q3 (Terceiro Quartil - 75%):** 268,00
- **Maximo:** 658,00

**Interpretacao Estatistica:**
A media ficou acima da mediana, indicando assimetria positiva influenciada por regioes de alta producao concentrada. O desvio padrao indica alta variabilidade e disparidade produtiva acentuada entre as regioes goianas. O valor minimo historico registrado foi de 0.00, enquanto o recorde maximo de 658.00 foi registrado na regiao LESTE GOIANO no ano de 2022. Metade das regioes registrou valores inferiores a mediana (53.00), e o limiar das 25% maiores se inicia em 268.00.

### Qtd_Produzida_Mesa_t

- **Registros Validos:** 55
- **Valores Faltantes:** 0
- **Media:** 10.875,65
- **Mediana:** 3.169,00
- **Moda:** 0,00
- **Desvio Padrao:** 14.707,42
- **Variancia:** 216.308.327,75
- **Minimo:** 0,00
- **Q1 (Primeiro Quartil - 25%):** 0,00
- **Q2 (Mediana - 50%):** 3.169,00
- **Q3 (Terceiro Quartil - 75%):** 20.347,50
- **Maximo:** 53.763,00

**Interpretacao Estatistica:**
A media ficou acima da mediana, indicando assimetria positiva influenciada por regioes de alta producao concentrada. O desvio padrao indica alta variabilidade e disparidade produtiva acentuada entre as regioes goianas. O valor minimo historico registrado foi de 0.00, enquanto o recorde maximo de 53763.00 foi registrado na regiao LESTE GOIANO no ano de 2022. Metade das regioes registrou valores inferiores a mediana (3169.00), e o limiar das 25% maiores se inicia em 20347.50.

### Produtividade_Mesa_tha

- **Registros Validos:** 55
- **Valores Faltantes:** 0
- **Media:** 48,85
- **Mediana:** 68,79
- **Moda:** 0,00
- **Desvio Padrao:** 38,91
- **Variancia:** 1.513,69
- **Minimo:** 0,00
- **Q1 (Primeiro Quartil - 25%):** 0,00
- **Q2 (Mediana - 50%):** 68,79
- **Q3 (Terceiro Quartil - 75%):** 81,80
- **Maximo:** 103,00

**Interpretacao Estatistica:**
A media ficou abaixo da mediana, indicando assimetria negativa influenciada por dados menores. O desvio padrao indica dispersao moderada. O valor minimo historico registrado foi de 0.00, enquanto o recorde maximo de 103.00 foi registrado na regiao NORTE GOIANO no ano de 2016. Metade das regioes registrou valores inferiores a mediana (68.79), e o limiar das 25% maiores se inicia em 81.80.

### Area_Colhida_Ind_ha

- **Registros Validos:** 55
- **Valores Faltantes:** 0
- **Media:** 2.357,04
- **Mediana:** 2.140,00
- **Moda:** 0,00
- **Desvio Padrao:** 2.373,69
- **Variancia:** 5.634.388,22
- **Minimo:** 0,00
- **Q1 (Primeiro Quartil - 25%):** 0,00
- **Q2 (Mediana - 50%):** 2.140,00
- **Q3 (Terceiro Quartil - 75%):** 3.970,50
- **Maximo:** 7.617,00

**Interpretacao Estatistica:**
A media ficou acima da mediana, indicando assimetria positiva influenciada por regioes de alta producao concentrada. O desvio padrao indica alta variabilidade e disparidade produtiva acentuada entre as regioes goianas. O valor minimo historico registrado foi de 0.00, enquanto o recorde maximo de 7617.00 foi registrado na regiao SUL GOIANO no ano de 2022. Metade das regioes registrou valores inferiores a mediana (2140.00), e o limiar das 25% maiores se inicia em 3970.50.

### Qtd_Produzida_Ind_t

- **Registros Validos:** 55
- **Valores Faltantes:** 0
- **Media:** 199.893,53
- **Mediana:** 54.400,00
- **Moda:** 0,00
- **Desvio Padrao:** 235.560,62
- **Variancia:** 55.488.806.820,77
- **Minimo:** 0,00
- **Q1 (Primeiro Quartil - 25%):** 0,00
- **Q2 (Mediana - 50%):** 54.400,00
- **Q3 (Terceiro Quartil - 75%):** 335.298,50
- **Maximo:** 1.013.730,00

**Interpretacao Estatistica:**
A media ficou acima da mediana, indicando assimetria positiva influenciada por regioes de alta producao concentrada. O desvio padrao indica alta variabilidade e disparidade produtiva acentuada entre as regioes goianas. O valor minimo historico registrado foi de 0.00, enquanto o recorde maximo de 1013730.00 foi registrado na regiao SUL GOIANO no ano de 2019. Metade das regioes registrou valores inferiores a mediana (54400.00), e o limiar das 25% maiores se inicia em 335298.50.

### Produtividade_Industrial_tha

- **Registros Validos:** 55
- **Valores Faltantes:** 0
- **Media:** 61,41
- **Mediana:** 79,20
- **Moda:** 0,00
- **Desvio Padrao:** 106,71
- **Variancia:** 11.387,52
- **Minimo:** 0,00
- **Q1 (Primeiro Quartil - 25%):** 0,00
- **Q2 (Mediana - 50%):** 79,20
- **Q3 (Terceiro Quartil - 75%):** 88,04
- **Maximo:** 772,42

**Interpretacao Estatistica:**
A media ficou abaixo da mediana, indicando assimetria negativa influenciada por dados menores. O desvio padrao indica alta variabilidade e disparidade produtiva acentuada entre as regioes goianas. O valor minimo historico registrado foi de 0.00, enquanto o recorde maximo de 772.42 foi registrado na regiao SUL GOIANO no ano de 2012. Metade das regioes registrou valores inferiores a mediana (79.20), e o limiar das 25% maiores se inicia em 88.04.

## Conclusao
A analise estatistica descritiva consolidada sobre a producao de tomates de mesa e industrial por Regioes de Planejamento de Goias (2012-2022) permitiu identificar com alta precisao a disparidade regional do cultivo. A presenca marcante de assimetria positiva indica a forte concentracao de algumas regioes chave na lideranca do volume colhido de tomate do estado. Esses dados organizados estruturam o pipeline perfeito para a execucao das proximas etapas de modelagem preditiva baseadas em series temporais.