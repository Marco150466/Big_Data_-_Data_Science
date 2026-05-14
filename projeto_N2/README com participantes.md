ANÁLISE DE PRODUÇÃO E ÁREA DE CULTIVO DE TOMATE (MESA VS. INDUSTRIAL) EM GOIÁS (2012-2022)

Celso Augusto Valadão Faria de Almeida

Hudsoney Silva

Isabella Alves Montalvão

Marco Antônio Soares de Brito

TECNOLOGIA EM INTELIGÊNCIA ARTIFICIAL

SERVIÇO NACIONAL DE APRENDIZAGEM INDUSTRIAL – GOIÂNIA – GO – BRAZIL 




1. Visão Geral do Pipeline de Engenharia de Dados
Este relatório documenta a extração, tratamento, modelagem e consolidação das bases de dados de produção de tomate no Estado de Goiás durante o período de 2012 a 2022. Os dados brutos foram obtidos junto ao Instituto Mauro Borges (IMB).
O grande desafio técnico contornado neste projeto consistiu no formato original de distribuição dos arquivos da instituição. As tabelas originais do IMB encontravam-se em layout "largo" (horizontal), onde os anos ocupavam colunas individuais e a primeira coluna representava a localidade (neste caso, as Regiões de Planejamento do Estado de Goiás).

Arquitetura de Solução Desenvolvida em Python:
- Leitura Multi-formato: Tratamento adaptativo de encodings (latin-1 e utf-8) e delimitadores diferentes (;e ,) para carregamento robusto do Pandas.
- Operação de Pivotagem (Melt): Transformação estrutural das colunas horizontais de Anos para registros na vertical, padronizando a granularidade em nível de Região x Ano.
- Normalização de Texto: Limpeza sistemática de acentuações e caracteres especiais com codificação ASCII para evitar falhas de cruzamento (Merge).
- Consolidação Unificada (Merge): Fusão das 4 tabelas de insumo (Área e Produção de Tomate de Mesa e Tomate Industrial) em uma única tabela de Fato Relacional, prevenindo valores nulos e calculando de forma dinâmica as produtividades (t/ha).

2. Resultados da Consolidação (Tabela de Fatos)
Após o processamento sistemático, a base consolidada final de região foi estruturada. Abaixo, apresentamos uma amostra ilustrativa extraída diretamente do arquivo final unificado tomate_consolidado_limpo.csv:


| Prod. Mesa (t)       | 2012    | 2013    | 2014    | 2015    | 2016    | 2017    | 2018    | 2019      | 2020    | 2021    | 2022    |
|----------------------|---------|---------|---------|---------|---------|---------|---------|-----------|---------|---------|---------|
| **CENTRO GOIANO**        | 48.930  | 41.471  | 39.875  | 28.438  | 21.695  | 23.137  | 12.847  | -         | -       | 8.003   | 9.459   |
| **LESTE GOIANO**         | 26.628  | 26.015  | 26.628  | 24.030  | 23.769  | 17.060  | 32.900  | -         | -       | 44.036  | 53.763  |
| **NOROESTE GOIANO**      | -       | -       | -       | -       | -       | -       | -       | -         | -       | -       | -       |
| **NORTE GOIANO**         | 200     | 200     | 475     | 475     | 1.236   | 1.040   | 1.620   | -         | -       | 19.000  | 190     |
| **SUL GOIANO**           | 9.174   | 3.273   | 3.169   | 9.146   | 4.605   | 8.763   | 7.616   | -         | -       | 7.316   | 11.979  |
|                      |         |         |         |         |         |         |         |           |         |         |         |
| **Área Mesa (ha)**       | 2012    | 2013    | 2014    | 2015    | 2016    | 2017    | 2018    | 2019      | 2020    | 2021    | 2022    |
| **CENTRO GOIANO**        | 638     | 550     | 526     | 390     | 294     | 304     | 151     | -         | -       | 105     | 123     |
| **LESTE GOIANO**         | 296     | 313     | 323     | 288     | 288     | 248     | 353     | -         | -       | 502     | 658     |
| **NOROESTE GOIANO**      | -       | -       | -       | -       | -       | -       | -       | -         | -       | -       | -       |
| **NORTE GOIANO**         | 5       | 5       | 5       | 5       | 12      | 13      | 18      | -         | -       | 200     | 200     |
| **SUL GOIANO**           | 160     | 53      | 41      | 126     | 81      | 107     | 120     | -         | -       | 112     | 172     |
|                      |         |         |         |         |         |         |         |           |         |         |         |
| **Prod. Industrial (t)** | **2012**    | **2013**    | **2014**    | **2015**    | **2016**    | **2017**    | **2018**    | **2019**      | **2020**    | **2021**    | **2022**    |
| **CENTRO GOIANO**        | 272.115 | 199.254 | 316.350 | 181.010 | 196.275 | 323.105 | 151.100 | -         | 54.400  | 18.200  | 2.732   |
| **LESTE GOIANO**         | 326.365 | 51.131  | 336.720 | 306.400 | 233.700 | 298.530 | 360.710 | -         | 354.540 | 588.393 | 401.552 |
| **NOROESTE GOIANO**      | 23.335  | 321     | 33.280  | 29.600  | -       | 3.200   | 2       | -         | -       | -       | -       |
| **NORTE GOIANO**         | 31      | 1.331   | -       | -       | -       | -       | -       | -         | -       | -       | -       |
| **SUL GOIANO**           | 447.231 | 490.674 | 298.840 | 333.877 | 453.378 | 577.228 | 630.032 | 1.013.730 | 582.037 | 556.547 | 546.888 |
|                      |         |         |         |         |         |         |         |           |         |         |         |
| **Área Industrial (ha)** | **2012**    | **2013**    | **2014**    | **2015**    | **2016**    | **2017**    | **2018**    | **2019**      | **2020**    | **2021**    | **2022**    |
| **CENTRO GOIANO**        | 3.436   | 2.433   | 3.600   | 1.910   | 2.225   | 3.576   | 1.745   | -         | 620     | 198     | 3.010   |
| **LESTE GOIANO**         | 3.282   | 5.755   | 3.540   | 3.560   | 3.315   | 5.130   | 4.060   | -         | 3.937   | 6.825   | 4.335   |
| **NOROESTE GOIANO**      | 3.590   | 4.280   | 416     | 370     | -       | 40      | 40      | -         | -       | -       | -       |
| **NORTE GOIANO**         | 620     | 2.140   | -       | -       | -       | -       | -       | -         | -       | -       | -       |
| **SUL GOIANO**           | 579     | 5.928   | 3.269   | 4.004   | 5.237   | 6.889   | 6.497   | -         | 5.967   | 5.662   | 7.617   |




* Nota de Engenharia: A ocorrência de valores 0.00 de Área e Produção de Tomate de Mesa em 2019 e 2020 reflete a ausência de dados reportados nos arquivos oficiais do IMB para esses períodos específicos de pandemia.
  
3. Análise Estatística Descritiva (Python Pandas)
Abaixo estão sumarizadas as principais métricas calculadas automaticamente pelo algoritmo Python sobre a totalidade da série histórica:

====================================================================================================
| Variável      | Area Colhida Mesa ha | Qtd Produzida Mesa t | Area Colhida Ind ha | Qtd Produzida Ind t |   |
|---------------|----------------------|----------------------|---------------------|---------------------|---|
| Média         | 141,55               | 1,087565e+04         | 2357,04             | 1,998935e+05        |   |
| Mediana       | 53,00                | 3,169000e+03         | 2140,00             | 5,440000e+04        |   |
| Moda          | 0,00                 | 0,000000e+00         | 0,00                | 0,000000e+00        |   |
| Desvio Padrão | 182,18               | 1,470742e+04         | 2373,69             | 2,355606e+05        |   |
| Variância     | 33191,10             | 2,163083e+08         | 5634388,22          | 5,548881e+10        |   |
| Mínimo        | 0,00                 | 0,000000e+00         | 0,00                | 0,000000e+00        |   |
| Q1 (25%)      | 0,00                 | 0,000000e+00         | 0,00                | 0,000000e+00        |   |
| Q3 (75%)      | 268,00               | 2,034750e+04         | 3970,50             | 3,352985e+05        |   |
| Máximo        | 658,00               | 5,376300e+04         | 7617,00             | 1,013730e+06        |   |


====================================================================================================

Os dados foram submetidos a uma análise descritiva univariada para compreender a
distribuição da produção de tomate (mesa e industrial). Abaixo seguem os resultados e as
interpretações técnicas de cada métrica calculada.

Variável: Area Colhida Mesa (ha)
| Média         | 141,55 | Mediana   | 53,00     | Moda   | 0,00   |   |
|---------------|--------|-----------|-----------|--------|--------|---|
| Desvio Padrão | 182,18 | Variância | 33.191,10 | Mínimo | 0,00   |   |
| Q1 (25%)      | 0,00   | Q3 (75%)  | 268,00    | Máximo | 658,00 |   |

Análise Técnica: A média (141,55) é superior à mediana (53,00), indicando uma assimetria positiva. O
alto desvio padrão em relação à média (CV de 128,71%) revela uma grande heterogeneidade nos
dados entre as regiões de Goiás. O valor máximo de 658,00 comparado ao Q3 (0,00) sugere a
existência de regiões com performance muito acima da massa central (outliers).

Variável: Qtd Produzida Mesa (t)
| Média         | 10.875,65 | Mediana   | 3.169,00       | Moda   | 0,00      |   |
|---------------|-----------|-----------|----------------|--------|-----------|---|
| Desvio Padrão | 14.707,42 | Variância | 216.308.327,75 | Mínimo | 0,00      |   |
| Q1 (25%)      | 0,00      | Q3 (75%)  | 20.347,50      | Máximo | 53.763,00 |   |

Análise Técnica: A média (10.875,65) é superior à mediana (3.169,00), indicando uma assimetria
positiva. O alto desvio padrão em relação à média (CV de 135,23%) revela uma grande
heterogeneidade nos dados entre as regiões de Goiás. O valor máximo de 53.763,00 comparado ao
Q3 (0,00) sugere a existência de regiões com performance muito acima da massa central (outliers).

Variável: Produtividade Mesa (t/ha)
| Média         | 48,85 | Mediana   | 68,79    | Moda   | 0,00   |   |
|---------------|-------|-----------|----------|--------|--------|---|
| Desvio Padrão | 38,91 | Variância | 1.513,69 | Mínimo | 0,00   |   |
| Q1 (25%)      | 0,00  | Q3 (75%)  | 81,80    | Máximo | 103,00 |   |

Análise Técnica: O alto desvio padrão em relação à média (CV de 79,64%) revela uma grande
heterogeneidade nos dados entre as regiões de Goiás. O valor máximo de 103,00 comparado ao Q3
(0,00) sugere a existência de regiões com performance muito acima da massa central (outliers).

Variável: Area Colhida Ind (ha)
| Média         | 2.357,04 | Mediana   | 2.140,00     | Moda   | 0,00     |   |
|---------------|----------|-----------|--------------|--------|----------|---|
| Desvio Padrão | 2.373,69 | Variância | 5.634.388,22 | Mínimo | 0,00     |   |
| Q1 (25%)      | 0,00     | Q3 (75%)  | 3.970,50     | Máximo | 7.617,00 |   |

Análise Técnica: A média (2.357,04) é superior à mediana (2.140,00), indicando uma assimetria
positiva. O alto desvio padrão em relação à média (CV de 100,71%) revela uma grande
heterogeneidade nos dados entre as regiões de Goiás. O valor máximo de 7.617,00 comparado ao Q3
(0,00) sugere a existência de regiões com performance muito acima da massa central (outliers).

Variável: Qtd Produzida Ind (t)
| Média         | 199.893,53 | Mediana   | 54.400,00         | Moda   | 0,00         |   |
|---------------|------------|-----------|-------------------|--------|--------------|---|
| Desvio Padrão | 235.560,62 | Variância | 55.488.806.820,77 | Mínimo | 0,00         |   |
| Q1 (25%)      | 0,00       | Q3 (75%)  | 335.298,50        | Máximo | 1.013.730,00 |   |

Análise Técnica: A média (199.893,53) é superior à mediana (54.400,00), indicando uma assimetria
positiva. O alto desvio padrão em relação à média (CV de 117,84%) revela uma grande
heterogeneidade nos dados entre as regiões de Goiás. O valor máximo de 1.013.730,00 comparado
ao Q3 (0,00) sugere a existência de regiões com performance muito acima da massa central (outliers).

Variável: Produtividade Industrial (t/ha)
| Média         | 61,41  | Mediana   | 79,20     | Moda   | 0,00   |   |
|---------------|--------|-----------|-----------|--------|--------|---|
| Desvio Padrão | 106,71 | Variância | 11.387,52 | Mínimo | 0,00   |   |
| Q1 (25%)      | 0,00   | Q3 (75%)  | 88,04     | Máximo | 772,42 |   |

Análise Técnica: O alto desvio padrão em relação à média (CV de 173,76%) revela uma grande
heterogeneidade nos dados entre as regiões de Goiás. O valor máximo de 772,42 comparado ao Q3
(0,00) sugere a existência de regiões com performance muito acima da massa central (outliers).
