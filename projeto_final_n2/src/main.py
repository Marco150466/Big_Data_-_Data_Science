import pandas as pd
from pathlib import Path

# Configuração de caminhos (usa o caminho relativo para funcionar em qualquer PC)
BASE_DIR = Path(__file__).resolve().parent.parent if "src" in str(Path(__file__).resolve()) else Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "data" / "tomate_consolidado_limpo.csv"

def analise_estatistica_completa():
    if not FILE_PATH.exists():
        print(f"[ERRO] Arquivo não encontrado: {FILE_PATH}")
        return

    # Carrega os dados consolidados
    df = pd.read_csv(FILE_PATH, sep=";", encoding="utf-8")
    
    # Variáveis relevantes para o estudo
    colunas = [
        "Area_Colhida_Mesa_ha", "Qtd_Produzida_Mesa_t", 
        "Area_Colhida_Ind_ha", "Qtd_Produzida_Ind_t"
    ]

    resultados = []

    for col in colunas:
        series = df[col].dropna()
        
        # Cálculo da Moda (pode haver mais de uma, pegamos a primeira)
        moda = series.mode()
        moda_val = moda[0] if not moda.empty else 0
        
        stats = {
            "Variável": col.replace("_", " "),
            "Média": series.mean(),
            "Mediana": series.median(),
            "Moda": moda_val,
            "Desvio Padrão": series.std(),
            "Variância": series.var(),
            "Mínimo": series.min(),
            "Q1 (25%)": series.quantile(0.25),
            "Q3 (75%)": series.quantile(0.75),
            "Máximo": series.max()
        }
        resultados.append(stats)

    # Criando um DataFrame com os resultados para formatar a saída
    df_final = pd.DataFrame(resultados).set_index("Variável")
    
    print("\n" + "="*100)
    print("      ANÁLISE ESTATÍSTICA COMPLETA - PRODUÇÃO DE TOMATE EM GOIÁS      ")
    print("="*100)
    
    # Exibe a tabela formatada (arredondada para 2 casas decimais)
    print(df_final.T.round(2).to_string())
    
    print("\n" + "="*100)
    print("DICA PARA O RELATÓRIO:")
    print("- Variância alta: Indica que o setor é muito instável ou desigual entre regiões.")
    print("- Quartis: Se o Q3 estiver muito longe do Máximo, você tem 'Outliers' (regiões gigantes).")
    print("="*100)

if __name__ == "__main__":
    analise_estatistica_completa()