## Participantes:

Celso Augusto Valadão Faria de Almeida

Hudsoney Silva

Isabella Alves Montalvão

Marco Antônio Soares de Brito

# 🍅 Projeto Tomate Goiás: Análise Integrada e Modelagem Preditiva

Este relatório consolida quatro bases sobre a cultura do tomate em Goiás, integrando área colhida e quantidade produzida para os segmentos industrial e de mesa. A proposta foi organizar um fluxo único de análise, desde a documentação dos dados até a modelagem preditiva, de forma interpretável e pronta para apresentação.

| PERÍODO COBERTO        | 2012 a 2022             |
|------------------------|-------------------------|
| LOCALIDADES            | 5 macrorregiões goianas |
| OBSERVAÇÕES INTEGRADAS | 110                     |
| DOCUMENTO GERADO EM    | 13/05/2026 19:41        |


## 📋1. Contexto e proposta analítica

Os arquivos descrevem duas cadeias produtivas com dinâmicas diferentes. O tomate industrial tende a operar em escalas de área e volume maiores, apoiado em fluxo logístico e processamento agroindustrial. Já o tomate de mesa costuma responder mais diretamente à oferta in natura, à especialização local e à volatilidade de mercado. A integração entre essas bases permite avaliar tamanho, estabilidade e eficiência relativa de cada segmento.

Após a leitura dos arquivos originais, os dados foram convertidos do formato amplo para uma base analítica única em formato longo, com as colunas
localidade, tipo_tomate, ano, area_ha, quantidade_t e produtividade_t_ha. Marcadores - foram tratados como ausentes e os valores com separador de milhar em ponto foram padronizados antes das análises.

## 2. Documentação das bases
## 2.1 Resumo dos datasets de origem

| Arquivo                    | Tipo de tomate | Indicador            | Linhas | Colunas | Período   | Localidades | Células com '-' |
|----------------------------|----------------|----------------------|--------|---------|-----------|-------------|-----------------|
| area_tomate_industrial.csv | Industrial     | Área colhida         | 5      | 13      | 2012-2022 | 5           | 15              |
| area_tomate_de_mesa.csv    | Mesa           | Área colhida         | 5      | 13      | 2012-2022 | 5           | 18              |
| tomate_industrial.csv      | Industrial     | Quantidade produzida | 5      | 13      | 2012-2022 | 5           | 14              |
| tomate_de_mesa.csv         | Mesa           | Quantidade produzida | 5      | 13      | 2012-2022 | 5           | 18              |

## 3. Qualidade e cobertura dos dados

A base integrada possui 110 combinações região-ano-tipo, das quais 77 (70,0%) têm área e produção simultaneamente disponíveis. Foramidentificados 33 valores ausentes em área, 32 em produção e 36 em produtividade. As ausências se concentram no hiato de 2019 paraambos os segmentos e em 2020 para tomate de mesa.

## 3.1 Cobertura completa por ano e segmento

| Ano  | Industrial completos | Mesa completos |   
|------|----------------------|----------------|
| 2012 | 5                    | 4              |
| 2013 | 5                    | 4              |
| 2014 | 4                    | 4              |
| 2015 | 4                    | 4              |
| 2016 | 3                    | 4              |
| 2017 | 4                    | 4              |
| 2018 | 4                    | 4              |
| 2019 | 0                    | 0              |
| 2020 | 3                    | 0              |
| 2021 | 3                    | 4              |
| 2022 | 5                    | 5              |

## 3.2 Outliers óbvios identificados pelo critério IQR

Os outliers abaixo não foram removidos automaticamente, porque podem refletir tanto anomalias de medição quanto eventos produtivosreais. Eles merecem validação adicional junto à fonte original antes de qualquer uso decisório de alto impacto.

| variavel      | tipo_tomate | localidade      | ano  | valor |
|---------------|-------------|-----------------|------|-------|
| Produtividade | Industrial  | NORTE GOIANO    | 2012 | 50,00 |
| Produtividade | Industrial  | NORTE GOIANO    | 2013 | 62,20 |
| Produtividade | Industrial  | LESTE GOIANO    | 2017 | 58,19 |
| Produtividade | Industrial  | NOROESTE GOIANO | 2018 | 0,05  |
| Produtividade | Mesa        | NORTE GOIANO    | 2012 | 40,00 |
| Produtividade | Mesa        | NORTE GOIANO    | 2013 | 40,00 |

## 4. Estatística descritiva e interpretação
## Área colhida

Área colhida mede a extensão da área efetivamente colhida em cada macrorregião e ano. A tabela resume os principais indicadoresdescritivos separados entre tomate industrial e tomate de mesa.

| Tipo de tomate | n válido | Média    | Mediana  | Moda           | Desvio padrão | Variância    | Mínimo | Q1     | Q2       | Q3       | Máximo |
|----------------|----------|----------|----------|----------------|---------------|--------------|--------|--------|----------|----------|--------|
| Industrial     | 40       | 3.064,30 | 3.375,50 | 0,40 (freq. 2) | 2.389,23      | 5.708.442,88 | 0      | 404,50 | 3.375,50 | 5.156,75 | 7.617  |
| Mesa           | 37       | 210,41   | 160,00   | 5 (freq.4)     | 186,80        | 34.895,69    | 0      | 53,00  | 160,00   | 304,00   | 658    |

**Média.** A média de área colhida foi de 3.064,30 ha no tomate industrial e 210,41 ha no tomate de mesa. Esse resultado resume o patamartípico de operação do período e mostra como o segmento industrial trabalha em escala mais alta, enquanto o tomate de mesa opera comestrutura mais enxuta e dispersa entre as macrorregiões.

**Mediana.** A mediana ficou em 3.375,50 ha para o industrial e 160,00 ha para o de mesa. Como a mediana é menos sensível a extremos, elarevela o ponto central mais representativo da série e ajuda a separar o padrão recorrente de oscilações ocasionais do cultivo.

**Moda.** A moda observada para área colhida foi 0, 40 (freq. 2) no segmento industrial e 5 (freq. 4) no de mesa. Quando não há moda única,isso sinaliza uma distribuição mais espalhada; quando há repetição, indica um nível de operação que voltou a aparecer ao longo dos anose regiões.

**Desvio padrão.** O desvio padrão de área colhida alcançou 2.389,23 ha no industrial e 186,80 ha no de mesa. Na prática, isso medevolatilidade: quanto maior o valor, maior a oscilação entre safras e regiões, algo importante para avaliar previsibilidade operacional esensibilidade a choques produtivos.

**Variância.** A variância foi de 5.708.442,88 ha no tomate industrial e 34.895,69 ha no tomate de mesa. Como ela amplia matematicamenteas diferenças em torno da média, confirma o quanto a série industrial é heterogênea e quantifica a amplitude estrutural entre contextosagrícolas distintos.

**Mínimo.** O menor valor de área colhida foi 0 ha no industrial e 0 ha no de mesa. Os mínimos ajudam a localizar momentos ou áreas debaixa atividade e, no contexto agrícola, podem refletir recuo de cultivo, ausência de colheita ou registros muito pontuais.

**Q1.** O primeiro quartil (Q1) ficou em 404,50 ha para o industrial e 53,00 ha para o de mesa. Isso significa que 25% das observações ficaramabaixo desse patamar, útil para entender a base inferior de desempenho e a diferença entre áreas de menor escala em cada cadeia.

**Q2.** O segundo quartil (Q2), equivalente à mediana, foi 3.375,50 ha no industrial e 160,00 ha no de mesa. Esse ponto divide a distribuiçãoao meio e reforça o nível central em que a maior parte das safras tende a se posicionar.

**Q3.** O terceiro quartil (Q3) atingiu 5.156,75 ha para o tomate industrial e 304,00 ha para o tomate de mesa. Ele marca a fronteira superiorde 75% das observações e ajuda a reconhecer quando a cadeia começa a entrar em um nível alto de escala ou eficiência.

**Máximo.** O valor máximo de área colhida foi 7.617 ha no industrial e 658 ha no de mesa. Os máximos destacam os picos de desempenhoobservados e evidenciam o potencial de expansão produtiva quando área, logística e condições agronômicas se alinham favoravelmente.

## Quantidade produzida

Quantidade produzida representa o volume anual de tomate colhido. A tabela resume os principais indicadores descritivos separadosentre tomate industrial e tomate de mesa.

| Tipo de tomate | n válido | Média      | Mediana    | Moda                        | Desvio padrão | Variância         | Mínimo | Q1        | Q2         | Q3         | Máximo |
|----------------|----------|------------|------------|-----------------------------|---------------|-------------------|--------|-----------|------------|------------|--------|
| Industrial     | 41       | 281.115,56 | 298.840,00 | 0 (freq.2)                  | 235.306,57    | 55.369.181.108,75 | 0      | 32.100,00 | 298.840,00 | 447.231,00 | 1.013  |
| Mesa           | 37       | 16.674,89  | 11.979,00  | 200,475,19.000... (freq. 2) | 15.146,58     | 229.418.924,21    | 0      | 3.273,00  | 11.979,00  | 26.015,00  | 53.76  |

**Média.** A média de quantidade produzida foi de 281.115,56 t no tomate industrial e 16.674,89 t no tomate de mesa. Esse resultado resumeo patamar típico de operação do período e mostra como o segmento industrial trabalha em escala mais alta, enquanto o tomate de mesaopera com estrutura mais enxuta e dispersa entre as macrorregiões.

**Mediana.** A mediana ficou em 298.840,00 t para o industrial e 11.979,00 t para o de mesa. Como a mediana é menos sensível a extremos,ela revela o ponto central mais representativo da série e ajuda a separar o padrão recorrente de oscilações ocasionais do cultivo.

**Moda.** A moda observada para quantidade produzida foi 0 (freq. 2) no segmento industrial e 200, 475, 19.000... (freq. 2) no de mesa.Quando não há moda única, isso sinaliza uma distribuição mais espalhada; quando há repetição, indica um nível de operação que voltou aaparecer ao longo dos anos e regiões.

**Desvio padrão.** O desvio padrão de quantidade produzida alcançou 235.306,57 t no industrial e 15.146,58 t no de mesa. Na prática, issomede volatilidade: quanto maior o valor, maior a oscilação entre safras e regiões, algo importante para avaliar previsibilidade operacional esensibilidade a choques produtivos.

**Variância.** A variância foi de 55.369.181.108,75 t no tomate industrial e 229.418.924,21 t no tomate de mesa. Como ela ampliamatematicamente as diferenças em torno da média, confirma o quanto a série industrial é heterogênea e quantifica a amplitude estruturalentre contextos agrícolas distintos.

**Mínimo.** O menor valor de quantidade produzida foi 0 t no industrial e 0 t no de mesa. Os mínimos ajudam a localizar momentos ou áreasde baixa atividade e, no contexto agrícola, podem refletir recuo de cultivo, ausência de colheita ou registros muito pontuais.

**Q1.** O primeiro quartil (Q1) ficou em 32.100,00 t para o industrial e 3.273,00 t para o de mesa. Isso significa que 25% das observaçõesficaram abaixo desse patamar, útil para entender a base inferior de desempenho e a diferença entre áreas de menor escala em cadacadeia.

**Q2.** O segundo quartil (Q2), equivalente à mediana, foi 298.840,00 t no industrial e 11.979,00 t no de mesa. Esse ponto divide a distribuiçãoao meio e reforça o nível central em que a maior parte das safras tende a se posicionar.

**Q3.** O terceiro quartil (Q3) atingiu 447.231,00 t para o tomate industrial e 26.015,00 t para o tomate de mesa. Ele marca a fronteira superiorde 75% das observações e ajuda a reconhecer quando a cadeia começa a entrar em um nível alto de escala ou eficiência.

**Máximo.** O valor máximo de quantidade produzida foi 1.013.730 t no industrial e 53.763 t no de mesa. Os máximos destacam os picos dedesempenho observados e evidenciam o potencial de expansão produtiva quando área, logística e condições agronômicas se alinhamfavoravelmente.

## Produtividade

Produtividade relaciona produção e área, sintetizando eficiência agrícola. A tabela resume os principais indicadores descritivos separadosentre tomate industrial e tomate de mesa.

| Tipo de tomate | n válido | Média | Mediana | Moda           | Desvio padrão | Variância | Mínimo | Q1    | Q2    | Q3    | Máximo |
|----------------|----------|-------|---------|----------------|---------------|-----------|--------|-------|-------|-------|--------|
| Industrial     | 38       | 81,51 | 86,39   | 80,00 (freq.3) | 17,61         | 310,01    | 0,05   | 79,40 | 86,39 | 90,66 | 99,44  |
| Mesa           | 36       | 77,25 | 77,10   | 95,00 (freq.4) | 14,34         | 205,70    | 40,00  | 71,85 | 77,10 | 85,74 | 103,00 |

**Média.** A média de produtividade foi de 81,51 t/ha no tomate industrial e 77,25 t/ha no tomate de mesa. Esse resultado resume o patamartípico de operação do período e mostra como o segmento industrial trabalha em escala mais alta, enquanto o tomate de mesa opera comestrutura mais enxuta e dispersa entre as macrorregiões.

**Mediana.** A mediana ficou em 86,39 t/ha para o industrial e 77,10 t/ha para o de mesa. Como a mediana é menos sensível a extremos, elarevela o ponto central mais representativo da série e ajuda a separar o padrão recorrente de oscilações ocasionais do cultivo.

**Moda.** A moda observada para produtividade foi 80,00 (freq. 3) no segmento industrial e 95,00 (freq. 4) no de mesa. Quando não há modaúnica, isso sinaliza uma distribuição mais espalhada; quando há repetição, indica um nível de operação que voltou a aparecer ao longo dosanos e regiões.

**Desvio padrão.** O desvio padrão de produtividade alcançou 17,61 t/ha no industrial e 14,34 t/ha no de mesa. Na prática, isso medevolatilidade: quanto maior o valor, maior a oscilação entre safras e regiões, algo importante para avaliar previsibilidade operacional esensibilidade a choques produtivos.

**Variância.** A variância foi de 310,01 t/ha no tomate industrial e 205,70 t/ha no tomate de mesa. Como ela amplia matematicamente asdiferenças em torno da média, confirma o quanto a série industrial é heterogênea e quantifica a amplitude estrutural entre contextosagrícolas distintos.

**Mínimo.** O menor valor de produtividade foi 0,05 t/ha no industrial e 40,00 t/ha no de mesa. Os mínimos ajudam a localizar momentos ouáreas de baixa atividade e, no contexto agrícola, podem refletir recuo de cultivo, ausência de colheita ou registros muito pontuais.

**Q1.** O primeiro quartil (Q1) ficou em 79,40 t/ha para o industrial e 71,85 t/ha para o de mesa. Isso significa que 25% das observaçõesficaram abaixo desse patamar, útil para entender a base inferior de desempenho e a diferença entre áreas de menor escala em cadacadeia.

**Q2.** O segundo quartil (Q2), equivalente à mediana, foi 86,39 t/ha no industrial e 77,10 t/ha no de mesa. Esse ponto divide a distribuiçãoao meio e reforça o nível central em que a maior parte das safras tende a se posicionar.

**Q3.** O terceiro quartil (Q3) atingiu 90,66 t/ha para o tomate industrial e 85,74 t/ha para o tomate de mesa. Ele marca a fronteira superiorde 75% das observações e ajuda a reconhecer quando a cadeia começa a entrar em um nível alto de escala ou eficiência.

**Máximo.** O valor máximo de produtividade foi 99,44 t/ha no industrial e 103,00 t/ha no de mesa. Os máximos destacam os picos dedesempenho observados e evidenciam o potencial de expansão produtiva quando área, logística e condições agronômicas se alinhamfavoravelmente.

## 5. Dashboard de visualização

<img width="2488" height="1767" alt="image" src="https://github.com/user-attachments/assets/e9dcdab4-fb4e-4938-8cd1-f16ed071eb08" />

Gráfico 1: a área colhida do tomate industrial domina a série histórica e apresenta picos mais intensos, enquanto o tomate de mesaopera em patamar muito menor e com lacuna visível em 2019-2020.

Gráfico 2: a produção acompanha a escala da área, mas também evidencia diferenças de rendimento, sobretudo quando o tomateindustrial mantém volumes altos mesmo em anos de retração parcial de área.

Gráfico 3: a distribuição da produtividade mostra que ambos os segmentos trabalham em faixas relativamente próximas, embora oindustrial exiba maior dispersão e sensibilidade a registros extremos.

Gráfico 4: a relação entre área e produção é fortemente positiva; o gráfico em escala logarítmica revela que os dois segmentos seguema mesma lógica estrutural, mas com níveis muito diferentes de escala.

## 6. Modelagem preditiva
O problema preditivo escolhido foi de **regressão:** prever a quantidade_t a partir de área colhida, ano, localidade e tipo de tomate. Essaformulação é apropriada porque a variável-alvo é contínua e porque a produção depende diretamente de escala cultivada, contextoregional e sazonalidade temporal.

Foram avaliados dois algoritmos. O **Random Forest Regressor** é adequado por capturar relações não lineares e interações entre variáveissem exigir forte suposição paramétrica. O **Gradient Boosting Regressor** foi incluído porque costuma ter ótimo desempenho em dadostabulares com poucos registros, combinando árvores sequenciais para corrigir erros residuais do modelo anterior. Em ambos os casos, oalvo foi transformado com log1p para reduzir assimetria e estabilizar a escala da produção.

O conjunto de modelagem utilizou 57 observações para treino e 20 para teste. As features empregadas foram ano, área colhida, localidadee tipo de tomate. O melhor desempenho ficou com Random Forest Regressor, com MAE (Mean Absolute Error) de 20.780,81 t, RMSE (Root Mean Square Error) de 32.466,27 t e R² de0,9641.

## 6.1 Métricas de avaliação

| Algoritmo                   | MAE (t)   | RMSE (t)  | R²     |   |
|-----------------------------|-----------|-----------|--------|---|
| Random Forest Regressor     | 20.780,81 | 32.466,27 | 0,9641 |   |
| Gradient Boosting Regressor | 19.943,68 | 32.729,74 | 0,9635 |   |

## 6.2 Gráficos de real versus previsto

<img width="2311" height="963" alt="image" src="https://github.com/user-attachments/assets/bc6076f3-ddba-4374-8399-c51decfe3d54" />

Nos gráficos de real versus previsto, quanto mais próximos os pontos ficam da diagonal, melhor a aderência. O Random Forest seaproximou mais dessa linha na amostra de teste, sugerindo melhor captura dos padrões de produção presentes nos dados.

## 6.3 Gráficos de resíduos

<img width="2307" height="963" alt="image" src="https://github.com/user-attachments/assets/67605ad3-7a04-423f-b3cb-e12e235692ee" />

Os resíduos do melhor modelo ficaram mais concentrados em torno de zero, sinalizando menor viés sistemático. Ainda assim, os maioresdesvios aparecem nas observações de escala muito elevada, o que é esperado em séries agrícolas com forte heterogeneidade regional.

## 6.4 Importância das variáveis no melhor modelo

<img width="1593" height="873" alt="image" src="https://github.com/user-attachments/assets/140ed271-b03e-4fc3-9f45-b7e4a7dd1bb2" />

A importância das variáveis reforça quais atributos mais ajudam a explicar a produção. Em geral, a área colhida aparece como principalmotor preditivo, seguida de localidade e tipo de tomate, o que é coerente com a lógica agronômica do problema.

## 6.5 Comparação e limitações

Entre os algoritmos testados, **Random Forest Regressor** apresentou o melhor equilíbrio entre erro absoluto, erro quadrático e poderexplicativo. O resultado sugere que a relação entre área, localidade e produção é fortemente não linear e beneficia modelos baseados emárvores. As principais limitações do estudo são o tamanho reduzido da amostra, os hiatos de 2019-2020 e a ausência de variáveisclimáticas, tecnológicas, de preços e manejo, que poderiam elevar a capacidade preditiva em estudos futuros.

## 7. Conclusões gerais

Os dados mostram que o tomate industrial domina a escala de cultivo em Goiás, tanto em área quanto em produção, enquanto o tomatede mesa opera em dimensão menor, porém com produtividade média próxima em vários contextos. A análise descritiva indica forteheterogeneidade no segmento industrial, ao passo que o tomate de mesa se comporta de forma mais compacta, embora também sujeitoa lacunas importantes de informação.

Visualmente, a série temporal deixa claro que a base tem interrupções que afetam a leitura de tendência, mas ainda assim preserva umsinal robusto de associação entre área colhida e produção. Na etapa preditiva, modelos de árvore superaram abordagens linearesexploratórias e ofereceram melhor ajuste para a estrutura tabular disponível. O relatório final, portanto, sustenta tanto uma leituradescritiva quanto uma aplicação prática de previsão, com transparência sobre restrições e oportunidades de melhoria.
