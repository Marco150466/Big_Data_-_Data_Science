# 🍅 Projeto Tomate Goiás: Análise Integrada e Modelagem Preditiva

Este relatório consolida quatro bases sobre a cultura do tomate em Goiás, integrando área colhida e quantidade produzida para ossegmentos industrial e de mesa. A proposta foi organizar um fluxo único de análise, desde a documentação dos dados até a modelagempreditiva, de forma interpretável e pronta para apresentação.

| PERÍODO COBERTO        | 2012 a 2022             |
|------------------------|-------------------------|
| LOCALIDADES            | 5 macrorregiões goianas |
| OBSERVAÇÕES INTEGRADAS | 110                     |
| DOCUMENTO GERADO EM    | 13/05/2026 19:41        |


## 📋1. Contexto e proposta analítica

Os arquivos descrevem duas cadeias produtivas com dinâmicas diferentes. O tomate industrial tende a operar em escalas de área e volumemaiores, apoiado em fluxo logístico e processamento agroindustrial. Já o tomate de mesa costuma responder mais diretamente à oferta innatura, à especialização local e à volatilidade de mercado. A integração entre essas bases permite avaliar tamanho, estabilidade e eficiênciarelativa de cada segmento.

Após a leitura dos arquivos originais, os dados foram convertidos do formato amplo para uma base analítica única em formato longo, comas colunas
localidade, tipo_tomate, ano, area_ha, quantidade_t e produtividade_t_ha. Marcadores - foram tratados como ausentes e os valorescom separador de milhar em ponto foram padronizados antes das análises.

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



## 📋 Visão Geral
O projeto consolida bases de dados do **Instituto Mauro Borges (IMB)**, transformando arquivos de layout horizontal ("wide") em uma base analítica verticalizada ("long").

- **Período:** 2012 a 2022
- **Escopo:** Macrorregiões do Estado de Goiás
- **Tecnologias:** Python (Pandas, Scikit-Learn), Power BI, Markdown.

---

## 🛠️ Engenharia de Dados
Os dados brutos passaram por um rigoroso processo de ETL:
1. **Normalização:** Tratamento de encodings e padronização de separadores decimais.
2. **Pivotagem (Melt):** Conversão de colunas de anos em registros temporais.
3. **Consolidação:** Merge das tabelas de Área e Produção (Mesa e Industrial) em uma única tabela de Fatos.

---

## 📈 Análise Estatística (Resumo)

| Variável Analisada | Média | Mediana | Desvio Padrão | Máximo |
| :--- | :---: | :---: | :---: | :---: |
| **Qtd. Produzida Mesa (t)** | 10.875,65 | 3.169,00 | 14.707,42 | 53.763,00 |
| **Area Colhida Mesa (ha)** | 141,55 | 53,00 | 182,18 | 658,00 |
| **Qtd. Produzida Industrial (t)** | 199.893,53 | 54.400,00 | 235.560,62 | 1.013.730,00 |
| **Area Colhida Industrial (ha)** | 2.357,04 | 2.140,00 | 2.373,69 | 7.617,00 |

> **Interpretação:** A produção industrial domina a escala de cultivo em Goiás. Observa-se uma **assimetria positiva** (média > mediana), indicando que a produção é altamente concentrada em polos agroindustriais específicos.

---

## 🤖 Modelagem Preditiva (Regressão)
Foram testados modelos de Machine Learning para prever a produção com base na área e localidade:

1. **Random Forest Regressor**
2. **Gradient Boosting Regressor** (Melhor performance)

### Métricas de Avaliação:
- **MAE (Mean Absolute Error):** Erro médio absoluto das previsões.
- **RMSE (Root Mean Square Error):** Sensibilidade a grandes erros (outliers).
- **R² Score:** Capacidade explicativa do modelo.

*Os modelos de árvore superaram as abordagens lineares devido à natureza não linear da expansão agrícola e variações regionais.*

---

## 📊 Dashboard (Power BI)
O dashboard interativo permite filtrar a evolução temporal e regional da produtividade (t/ha), destacando os anos de hiato de dados (2019-2020) e a recuperação do setor no pós-pandemia.

---

## 📂 Estrutura de Arquivos
- `tomate_consolidado_limpo.csv`: Base de dados final tratada.
- `main.py`: Script de ETL e análise estatística.
- `modelos_regressao.py`: Treinamento e avaliação de ML.
- `relatorio_tecnico.pdf`: Documentação detalhada dos resultados.

---
**Desenvolvido por:** Grupo de Data Science - FATESG
**Data:** Maio/2026
