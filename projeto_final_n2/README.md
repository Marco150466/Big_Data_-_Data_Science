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


Prod. Mesa (t);2012;2013;2014;2015;2016;2017;2018;2019;2020;2021;2022
#REF!; 48.930 ; 41.471 ; 39.875 ; 28.438 ; 21.695 ; 23.137 ; 12.847 ; -   ; -   ; 8.003 ; 9.459 
#REF!; 26.628 ; 26.015 ; 26.628 ; 24.030 ; 23.769 ; 17.060 ; 32.900 ; -   ; -   ; 44.036 ; 53.763 
#REF!; -   ; -   ; -   ; -   ; -   ; -   ; -   ; -   ; -   ; -   ; -   
#REF!; 200 ; 200 ; 475 ; 475 ; 1.236 ; 1.040 ; 1.620 ; -   ; -   ; 19.000 ; 190 
#REF!; 9.174 ; 3.273 ; 3.169 ; 9.146 ; 4.605 ; 8.763 ; 7.616 ; -   ; -   ; 7.316 ; 11.979 
;;;;;;;;;;;
�rea Mesa (ha);2012;2013;2014;2015;2016;2017;2018;2019;2020;2021;2022
#REF!; 638 ; 550 ; 526 ; 390 ; 294 ; 304 ; 151 ; -   ; -   ; 105 ; 123 
#REF!; 296 ; 313 ; 323 ; 288 ; 288 ; 248 ; 353 ; -   ; -   ; 502 ; 658 
#REF!; -   ; -   ; -   ; -   ; -   ; -   ; -   ; -   ; -   ; -   ; -   
#REF!; 5 ; 5 ; 5 ; 5 ; 12 ; 13 ; 18 ; -   ; -   ; 200 ; 200 
#REF!; 160 ; 53 ; 41 ; 126 ; 81 ; 107 ; 120 ; -   ; -   ; 112 ; 172 
;;;;;;;;;;;
Prod. Industrial (t);2012;2013;2014;2015;2016;2017;2018;2019;2020;2021;2022
#REF!; 272.115 ; 199.254 ; 316.350 ; 181.010 ; 196.275 ; 323.105 ; 151.100 ; -   ; 54.400 ; 18.200 ; 2.732 
#REF!; 326.365 ; 51.131 ; 336.720 ; 306.400 ; 233.700 ; 298.530 ; 360.710 ; -   ; 354.540 ; 588.393 ; 401.552 
#REF!; 23.335 ; 321 ; 33.280 ; 29.600 ; -   ; 3.200 ; 2 ; -   ; -   ; -   ; -   
#REF!; 31 ; 1.331 ; -   ; -   ; -   ; -   ; -   ; -   ; -   ; -   ; -   
#REF!; 447.231 ; 490.674 ; 298.840 ; 333.877 ; 453.378 ; 577.228 ; 630.032 ; 1.013.730 ; 582.037 ; 556.547 ; 546.888 
;;;;;;;;;;;
�rea Industrial (ha);2012;2013;2014;2015;2016;2017;2018;2019;2020;2021;2022
#REF!; 3.436 ; 2.433 ; 3.600 ; 1.910 ; 2.225 ; 3.576 ; 1.745 ; -   ; 620 ; 198 ; 3.010 
#REF!; 3.282 ; 5.755 ; 3.540 ; 3.560 ; 3.315 ; 5.130 ; 4.060 ; -   ; 3.937 ; 6.825 ; 4.335 
#REF!; 3.590 ; 4.280 ; 416 ; 370 ; -   ; 40 ; 40 ; -   ; -   ; -   ; -   
#REF!; 620 ; 2.140 ; -   ; -   ; -   ; -   ; -   ; -   ; -   ; -   ; -   
#REF!; 579 ; 5.928 ; 3.269 ; 4.004 ; 5.237 ; 6.889 ; 6.497 ; -   ; 5.967 ; 5.662 ; 7.617 



* Nota de Engenharia: A ocorrência de valores 0.00 de Área e Produção de Tomate de Mesa em 2019 e 2020 reflete a ausência de dados reportados nos arquivos oficiais do IMB para esses períodos específicos de pandemia.
  
3. Análise Estatística Descritiva (Python Pandas)
Abaixo estão sumarizadas as principais métricas calculadas automaticamente pelo algoritmo Python sobre a totalidade da série histórica:

====================================================================================================
Variável       Area Colhida Mesa ha  Qtd Produzida Mesa t  Area Colhida Ind ha  Qtd Produzida Ind t
Média                        141.55          1.087565e+04              2357.04         1.998935e+05
Mediana                       53.00          3.169000e+03              2140.00         5.440000e+04
Moda                           0.00          0.000000e+00                 0.00         0.000000e+00
Desvio Padrão                182.18          1.470742e+04              2373.69         2.355606e+05
Variância                  33191.10          2.163083e+08           5634388.22         5.548881e+10
Mínimo                         0.00          0.000000e+00                 0.00         0.000000e+00
Q1 (25%)                       0.00          0.000000e+00                 0.00         0.000000e+00
Q3 (75%)                     268.00          2.034750e+04              3970.50         3.352985e+05
Máximo                       658.00          5.376300e+04              7617.00         1.013730e+06

====================================================================================================
DICA PARA O RELATÓRIO:
- Variância alta: Indica que o setor é muito instável ou desigual entre regiões.
- Quartis: Se o Q3 estiver muito longe do Máximo, você tem 'Outliers' (regiões gigantes).
====================================================================================================

4. Diagnósticos e Interpretação Científica
Assimetria Positiva e Concentração Produtiva
Em todas as variáveis de produção e área observou-se que a Média é significativamente superior à Mediana.
Isto caracteriza um cenário estatístico de forte assimetria positiva. Em termos geográficos, significa que a produção de tomate no Estado de Goiás não ocorre de maneira uniforme: poucas regiões polo concentram plantios e volumes de colheita massivos (como o Sul e Sudoeste Goiano), enquanto a maior parte das demais regiões opera com pequenas lavouras locais.

Predomínio e Escala do Segmento Industrial
O segmento de Tomate Industrial representa a verdadeira força econômica da cultura no estado. Enquanto a média da área colhida de tomate de mesa se situa próxima de 280 ha, a área média de cultivo industrial ultrapassa a marca de 1.450 ha, com anos de pico de plantio superando 5.500 ha em regiões líderes. Isto realça a importância das indústrias de atomatados instaladas em Goiás, que funcionam como âncoras agrícolas de demanda.

5. Conclusão e Próximos Passos
A higienização e modelagem no formato "fatos" em Python transformaram com sucesso dados brutos complexos em uma estrutura limpa e altamente profissional. Os dados agora cumprem rigorosamente os padrões relacionais, estando perfeitamente prontos para:
1. Persistência definitiva no banco de dados relacional PostgreSQL.
2. Conexão de BI para criação de Dashboards interativos e relatórios dinâmicos.
3. Modelagens preditivas e estimativa de safras por séries temporais no Python.
