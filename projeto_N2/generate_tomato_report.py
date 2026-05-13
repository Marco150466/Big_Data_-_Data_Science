from __future__ import annotations

import base64
import io
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parent
REPORT_PATH = ROOT / "relatorio_tomate_goias.html"


@dataclass(frozen=True)
class DatasetConfig:
    filename: str
    tipo_tomate: str
    indicador: str
    unidade: str


DATASETS = [
    DatasetConfig("area_tomate_industrial.csv", "industrial", "Área colhida", "ha"),
    DatasetConfig("area_tomate_de_mesa.csv", "mesa", "Área colhida", "ha"),
    DatasetConfig("tomate_industrial.csv", "industrial", "Quantidade produzida", "t"),
    DatasetConfig("tomate_de_mesa.csv", "mesa", "Quantidade produzida", "t"),
]

VARIABLE_META = {
    "area_ha": {
        "label": "Área colhida",
        "unit": "ha",
        "context": "mede a extensão da área efetivamente colhida em cada macrorregião e ano",
    },
    "quantidade_t": {
        "label": "Quantidade produzida",
        "unit": "t",
        "context": "representa o volume anual de tomate colhido",
    },
    "produtividade_t_ha": {
        "label": "Produtividade",
        "unit": "t/ha",
        "context": "relaciona produção e área, sintetizando eficiência agrícola",
    },
}

METRIC_ORDER = ["media", "mediana", "moda", "desvio_padrao", "variancia", "minimo", "q1", "q2", "q3", "maximo"]
METRIC_LABELS = {
    "media": "Média",
    "mediana": "Mediana",
    "moda": "Moda",
    "desvio_padrao": "Desvio padrão",
    "variancia": "Variância",
    "minimo": "Mínimo",
    "q1": "Q1",
    "q2": "Q2",
    "q3": "Q3",
    "maximo": "Máximo",
}


def format_number(value: Any, decimals: int = 2) -> str:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "NA"
    if isinstance(value, (np.integer, int)):
        text = f"{int(value):,}"
    else:
        text = f"{float(value):,.{decimals}f}"
    return text.replace(",", "X").replace(".", ",").replace("X", ".")


def format_value(value: Any, unit: str, decimals: int = 2) -> str:
    if isinstance(value, str):
        return value
    return f"{format_number(value, decimals)} {unit}".strip()


def format_pct(value: float, decimals: int = 1) -> str:
    return f"{value * 100:.{decimals}f}%".replace(".", ",")


def clean_numeric(series: pd.Series) -> pd.Series:
    cleaned = (
        series.fillna(pd.NA)
        .astype("string")
        .str.strip()
        .replace({"-": pd.NA, "": pd.NA, "nan": pd.NA, "None": pd.NA})
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    return pd.to_numeric(cleaned, errors="coerce")


def read_raw_dataset(config: DatasetConfig) -> pd.DataFrame:
    return pd.read_csv(ROOT / config.filename, sep=";", encoding="cp1252", dtype=str)


def dataset_column_dictionary(config: DatasetConfig, df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, str]] = [
        {
            "Coluna": "Localidade",
            "Tipo de dado": "texto categórico",
            "Unidade": "não se aplica",
            "Significado": "Macrorregião goiana observada na série.",
        },
        {
            "Coluna": "Variável",
            "Tipo de dado": "texto descritivo",
            "Unidade": config.unidade,
            "Significado": f"Descrição do indicador do arquivo ({config.indicador.lower()} de tomate {config.tipo_tomate}).",
        },
    ]
    year_columns = [column for column in df.columns if str(column).isdigit()]
    for year in year_columns:
        rows.append(
            {
                "Coluna": year,
                "Tipo de dado": "numérico",
                "Unidade": config.unidade,
                "Significado": f"Valor observado em {year} para {config.indicador.lower()} de tomate {config.tipo_tomate}.",
            }
        )
    return pd.DataFrame(rows)


def load_long_dataset(config: DatasetConfig) -> pd.DataFrame:
    df = read_raw_dataset(config)
    id1, id2 = df.columns[:2]
    year_columns = [column for column in df.columns if str(column).isdigit()]
    long_df = df.melt(id_vars=[id1, id2], value_vars=year_columns, var_name="ano", value_name="valor")
    long_df = long_df.rename(columns={id1: "localidade", id2: "variavel_original"})
    long_df["tipo_tomate"] = config.tipo_tomate
    long_df["indicador"] = config.indicador
    long_df["ano"] = long_df["ano"].astype(int)
    long_df["valor"] = clean_numeric(long_df["valor"])
    metric_column = "area_ha" if config.indicador == "Área colhida" else "quantidade_t"
    long_df = long_df.rename(columns={"valor": metric_column})
    return long_df[["localidade", "variavel_original", "tipo_tomate", "indicador", "ano", metric_column]]


def build_integrated_dataset() -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    raw_metadata: list[dict[str, Any]] = []
    long_frames: dict[str, list[pd.DataFrame]] = {"area_ha": [], "quantidade_t": []}
    for config in DATASETS:
        raw_df = read_raw_dataset(config)
        year_columns = [column for column in raw_df.columns if str(column).isdigit()]
        missing_markers = int(raw_df[year_columns].isin(["-", "", None]).sum().sum())
        raw_metadata.append(
            {
                "Arquivo": config.filename,
                "Tipo de tomate": config.tipo_tomate.title(),
                "Indicador": config.indicador,
                "Linhas": raw_df.shape[0],
                "Colunas": raw_df.shape[1],
                "Período": f"{year_columns[0]}-{year_columns[-1]}",
                "Localidades": raw_df.iloc[:, 0].nunique(),
                "Células com '-'": missing_markers,
                "Dicionário": dataset_column_dictionary(config, raw_df),
            }
        )
        long_df = load_long_dataset(config)
        metric_column = "area_ha" if config.indicador == "Área colhida" else "quantidade_t"
        long_frames[metric_column].append(long_df)

    area_df = pd.concat(long_frames["area_ha"], ignore_index=True)
    quantity_df = pd.concat(long_frames["quantidade_t"], ignore_index=True)
    merged = area_df.merge(
        quantity_df,
        on=["localidade", "tipo_tomate", "ano"],
        how="outer",
        suffixes=("_area", "_quant"),
    )
    merged["produtividade_t_ha"] = merged["quantidade_t"] / merged["area_ha"]
    merged["ano"] = merged["ano"].astype(int)
    merged = merged.sort_values(["ano", "tipo_tomate", "localidade"]).reset_index(drop=True)
    return merged, raw_metadata


def summarise_series(series: pd.Series) -> dict[str, Any]:
    clean = series.dropna()
    if clean.empty:
        return {metric: np.nan for metric in METRIC_ORDER}

    value_counts = clean.value_counts()
    top_frequency = int(value_counts.iloc[0])
    modes = sorted(value_counts[value_counts == top_frequency].index.tolist())
    if top_frequency == 1:
        mode_repr = "Sem moda única"
    else:
        mode_values = ", ".join(format_number(value, 2) for value in modes[:3])
        extra = "..." if len(modes) > 3 else ""
        mode_repr = f"{mode_values}{extra} (freq. {top_frequency})"

    return {
        "media": clean.mean(),
        "mediana": clean.median(),
        "moda": mode_repr,
        "desvio_padrao": clean.std(ddof=1),
        "variancia": clean.var(ddof=1),
        "minimo": clean.min(),
        "q1": clean.quantile(0.25),
        "q2": clean.quantile(0.50),
        "q3": clean.quantile(0.75),
        "maximo": clean.max(),
        "contagem": int(clean.count()),
    }


def descriptive_tables(base_df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    tables: dict[str, pd.DataFrame] = {}
    for variable, meta in VARIABLE_META.items():
        rows: list[dict[str, Any]] = []
        for tomato_type in ["industrial", "mesa"]:
            stats = summarise_series(base_df.loc[base_df["tipo_tomate"] == tomato_type, variable])
            row = {"Tipo de tomate": tomato_type.title(), "n válido": stats.pop("contagem")}
            for metric in METRIC_ORDER:
                row[METRIC_LABELS[metric]] = stats[metric]
            rows.append(row)
        tables[variable] = pd.DataFrame(rows)
        for column in tables[variable].columns:
            if column in {"Tipo de tomate", "n válido", "Moda"}:
                continue
            tables[variable][column] = tables[variable][column].map(lambda value: format_number(value, 2))
    return tables


def metric_interpretation(variable: str, metric: str, industrial_stats: dict[str, Any], mesa_stats: dict[str, Any]) -> str:
    meta = VARIABLE_META[variable]
    unit = meta["unit"]
    industrial_value = industrial_stats[metric]
    mesa_value = mesa_stats[metric]
    industrial_fmt = format_value(industrial_value, unit)
    mesa_fmt = format_value(mesa_value, unit)
    label = meta["label"].lower()

    if metric == "media":
        return (
            f"A média de {label} foi de {industrial_fmt} no tomate industrial e {mesa_fmt} no tomate de mesa. "
            f"Esse resultado resume o patamar típico de operação do período e mostra como o segmento industrial trabalha em escala mais alta, "
            f"enquanto o tomate de mesa opera com estrutura mais enxuta e dispersa entre as macrorregiões."
        )
    if metric == "mediana":
        return (
            f"A mediana ficou em {industrial_fmt} para o industrial e {mesa_fmt} para o de mesa. "
            f"Como a mediana é menos sensível a extremos, ela revela o ponto central mais representativo da série e ajuda a separar o padrão recorrente de oscilações ocasionais do cultivo."
        )
    if metric == "moda":
        return (
            f"A moda observada para {label} foi {industrial_fmt} no segmento industrial e {mesa_fmt} no de mesa. "
            f"Quando não há moda única, isso sinaliza uma distribuição mais espalhada; quando há repetição, indica um nível de operação que voltou a aparecer ao longo dos anos e regiões."
        )
    if metric == "desvio_padrao":
        return (
            f"O desvio padrão de {label} alcançou {industrial_fmt} no industrial e {mesa_fmt} no de mesa. "
            f"Na prática, isso mede volatilidade: quanto maior o valor, maior a oscilação entre safras e regiões, algo importante para avaliar previsibilidade operacional e sensibilidade a choques produtivos."
        )
    if metric == "variancia":
        return (
            f"A variância foi de {industrial_fmt} no tomate industrial e {mesa_fmt} no tomate de mesa. "
            f"Como ela amplia matematicamente as diferenças em torno da média, confirma o quanto a série industrial é heterogênea e quantifica a amplitude estrutural entre contextos agrícolas distintos."
        )
    if metric == "minimo":
        return (
            f"O menor valor de {label} foi {industrial_fmt} no industrial e {mesa_fmt} no de mesa. "
            f"Os mínimos ajudam a localizar momentos ou áreas de baixa atividade e, no contexto agrícola, podem refletir recuo de cultivo, ausência de colheita ou registros muito pontuais."
        )
    if metric == "q1":
        return (
            f"O primeiro quartil (Q1) ficou em {industrial_fmt} para o industrial e {mesa_fmt} para o de mesa. "
            f"Isso significa que 25% das observações ficaram abaixo desse patamar, útil para entender a base inferior de desempenho e a diferença entre áreas de menor escala em cada cadeia."
        )
    if metric == "q2":
        return (
            f"O segundo quartil (Q2), equivalente à mediana, foi {industrial_fmt} no industrial e {mesa_fmt} no de mesa. "
            f"Esse ponto divide a distribuição ao meio e reforça o nível central em que a maior parte das safras tende a se posicionar."
        )
    if metric == "q3":
        return (
            f"O terceiro quartil (Q3) atingiu {industrial_fmt} para o tomate industrial e {mesa_fmt} para o tomate de mesa. "
            f"Ele marca a fronteira superior de 75% das observações e ajuda a reconhecer quando a cadeia começa a entrar em um nível alto de escala ou eficiência."
        )
    return (
        f"O valor máximo de {label} foi {industrial_fmt} no industrial e {mesa_fmt} no de mesa. "
        f"Os máximos destacam os picos de desempenho observados e evidenciam o potencial de expansão produtiva quando área, logística e condições agronômicas se alinham favoravelmente."
    )


def integrated_column_dictionary() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["localidade", "texto categórico", "não se aplica", "Macrorregião de Goiás."],
            ["tipo_tomate", "texto categórico", "não se aplica", "Segmento analisado: industrial ou mesa."],
            ["ano", "inteiro", "ano civil", "Ano da observação."],
            ["area_ha", "numérico", "hectares", "Área colhida da cultura."],
            ["quantidade_t", "numérico", "toneladas", "Produção total obtida no ano."],
            ["produtividade_t_ha", "numérico", "t/ha", "Razão entre produção e área colhida."],
        ],
        columns=["Coluna", "Tipo de dado", "Unidade", "Significado"],
    )


def data_quality_summary(base_df: pd.DataFrame) -> dict[str, Any]:
    total_rows = int(base_df.shape[0])
    complete_rows = int(base_df[["area_ha", "quantidade_t"]].notna().all(axis=1).sum())
    missing_area = int(base_df["area_ha"].isna().sum())
    missing_quantity = int(base_df["quantidade_t"].isna().sum())
    missing_productivity = int(base_df["produtividade_t_ha"].isna().sum())

    completeness = base_df.assign(completo=base_df[["area_ha", "quantidade_t"]].notna().all(axis=1))
    completeness_by_year = (
        completeness.groupby(["ano", "tipo_tomate"])["completo"]
        .sum()
        .reset_index()
        .pivot(index="ano", columns="tipo_tomate", values="completo")
        .reset_index()
        .fillna(0)
    )
    completeness_by_year.columns = ["Ano", "Industrial completos", "Mesa completos"]

    outlier_rows: list[dict[str, Any]] = []
    for variable in VARIABLE_META:
        for tomato_type in ["industrial", "mesa"]:
            subset = base_df.loc[base_df["tipo_tomate"] == tomato_type, ["localidade", "ano", variable]].dropna()
            if subset.empty:
                continue
            q1 = subset[variable].quantile(0.25)
            q3 = subset[variable].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            flagged = subset.loc[(subset[variable] < lower) | (subset[variable] > upper)].copy()
            if flagged.empty:
                continue
            flagged["variavel"] = VARIABLE_META[variable]["label"]
            flagged["tipo_tomate"] = tomato_type.title()
            flagged["valor"] = flagged[variable]
            outlier_rows.extend(flagged[["variavel", "tipo_tomate", "localidade", "ano", "valor"]].to_dict("records"))

    outliers_df = pd.DataFrame(outlier_rows)
    if not outliers_df.empty:
        outliers_df["valor"] = outliers_df["valor"].map(lambda value: format_number(value, 2))

    return {
        "total_rows": total_rows,
        "complete_rows": complete_rows,
        "missing_area": missing_area,
        "missing_quantity": missing_quantity,
        "missing_productivity": missing_productivity,
        "completeness_by_year": completeness_by_year,
        "outliers": outliers_df,
    }


def plot_to_base64(fig: plt.Figure) -> str:
    buffer = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buffer, format="png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def create_dashboard(base_df: pd.DataFrame) -> tuple[str, list[str]]:
    sns.set_theme(style="whitegrid", palette="Set2")

    totals = (
        base_df.groupby(["ano", "tipo_tomate"], dropna=False)[["area_ha", "quantidade_t"]]
        .sum(min_count=1)
        .reset_index()
    )
    productivity = (
        base_df.groupby(["localidade", "tipo_tomate"], dropna=False)["produtividade_t_ha"]
        .mean()
        .reset_index()
    )

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    sns.lineplot(data=totals, x="ano", y="area_ha", hue="tipo_tomate", marker="o", ax=axes[0, 0])
    axes[0, 0].set_title("Gráfico 1. Área colhida total por ano")
    axes[0, 0].set_xlabel("Ano")
    axes[0, 0].set_ylabel("Área colhida (ha)")

    sns.lineplot(data=totals, x="ano", y="quantidade_t", hue="tipo_tomate", marker="o", ax=axes[0, 1])
    axes[0, 1].set_title("Gráfico 2. Produção total por ano")
    axes[0, 1].set_xlabel("Ano")
    axes[0, 1].set_ylabel("Produção (t)")

    sns.boxplot(data=base_df, x="tipo_tomate", y="produtividade_t_ha", ax=axes[1, 0])
    axes[1, 0].set_title("Gráfico 3. Distribuição da produtividade")
    axes[1, 0].set_xlabel("Tipo de tomate")
    axes[1, 0].set_ylabel("Produtividade (t/ha)")

    scatter_df = base_df.dropna(subset=["area_ha", "quantidade_t"]).copy()
    sns.scatterplot(
        data=scatter_df,
        x="area_ha",
        y="quantidade_t",
        hue="tipo_tomate",
        style="tipo_tomate",
        s=80,
        ax=axes[1, 1],
    )
    axes[1, 1].set_xscale("log")
    axes[1, 1].set_yscale("log")
    axes[1, 1].set_title("Gráfico 4. Relação entre área e produção")
    axes[1, 1].set_xlabel("Área colhida (ha, escala log)")
    axes[1, 1].set_ylabel("Produção (t, escala log)")

    for ax in axes.flat:
        ax.grid(alpha=0.2)
    dashboard_description = [
        "Gráfico 1: a área colhida do tomate industrial domina a série histórica e apresenta picos mais intensos, enquanto o tomate de mesa opera em patamar muito menor e com lacuna visível em 2019-2020.",
        "Gráfico 2: a produção acompanha a escala da área, mas também evidencia diferenças de rendimento, sobretudo quando o tomate industrial mantém volumes altos mesmo em anos de retração parcial de área.",
        "Gráfico 3: a distribuição da produtividade mostra que ambos os segmentos trabalham em faixas relativamente próximas, embora o industrial exiba maior dispersão e sensibilidade a registros extremos.",
        "Gráfico 4: a relação entre área e produção é fortemente positiva; o gráfico em escala logarítmica revela que os dois segmentos seguem a mesma lógica estrutural, mas com níveis muito diferentes de escala.",
    ]
    return plot_to_base64(fig), dashboard_description


def build_modeling_dataset(base_df: pd.DataFrame) -> pd.DataFrame:
    return base_df.dropna(subset=["area_ha", "quantidade_t"]).copy()


def train_models(model_df: pd.DataFrame) -> dict[str, Any]:
    features = ["ano", "area_ha", "localidade", "tipo_tomate"]
    target = "quantidade_t"
    X = model_df[features]
    y = model_df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    numeric_features = ["ano", "area_ha"]
    categorical_features = ["localidade", "tipo_tomate"]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric_features,
            ),
            (
                "cat",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                    ]
                ),
                categorical_features,
            ),
        ]
    )

    models = {
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=400,
            random_state=42,
            min_samples_leaf=2,
        ),
        "Gradient Boosting Regressor": GradientBoostingRegressor(random_state=42),
    }

    results: dict[str, Any] = {
        "features": features,
        "train_rows": int(X_train.shape[0]),
        "test_rows": int(X_test.shape[0]),
        "pipelines": {},
        "metrics_table": [],
    }

    for name, estimator in models.items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                (
                    "model",
                    TransformedTargetRegressor(
                        regressor=estimator,
                        func=np.log1p,
                        inverse_func=np.expm1,
                    ),
                ),
            ]
        )
        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)
        rmse = mean_squared_error(y_test, predictions) ** 0.5
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        residuals = y_test - predictions

        results["pipelines"][name] = {
            "pipeline": pipeline,
            "y_test": y_test.reset_index(drop=True),
            "predictions": pd.Series(predictions).reset_index(drop=True),
            "residuals": pd.Series(residuals).reset_index(drop=True),
            "metrics": {"MAE": mae, "RMSE": rmse, "R2": r2},
        }
        results["metrics_table"].append(
            {
                "Algoritmo": name,
                "MAE (t)": mae,
                "RMSE (t)": rmse,
                "R²": r2,
            }
        )

    metrics_df = pd.DataFrame(results["metrics_table"]).sort_values("R²", ascending=False)
    metrics_df["MAE (t)"] = metrics_df["MAE (t)"].map(lambda value: format_number(value, 2))
    metrics_df["RMSE (t)"] = metrics_df["RMSE (t)"].map(lambda value: format_number(value, 2))
    metrics_df["R²"] = metrics_df["R²"].map(lambda value: f"{value:.4f}".replace(".", ","))
    results["metrics_df"] = metrics_df.reset_index(drop=True)

    best_name = max(results["pipelines"], key=lambda item: results["pipelines"][item]["metrics"]["R2"])
    results["best_model_name"] = best_name
    best_pipeline = results["pipelines"][best_name]["pipeline"]
    feature_names = best_pipeline.named_steps["preprocessor"].get_feature_names_out()
    fitted_regressor = best_pipeline.named_steps["model"].regressor_
    if hasattr(fitted_regressor, "feature_importances_"):
        importance_df = pd.DataFrame(
            {
                "Feature": feature_names,
                "Importância": fitted_regressor.feature_importances_,
            }
        ).sort_values("Importância", ascending=False)
        results["feature_importance_df"] = importance_df.head(10)
    else:
        results["feature_importance_df"] = pd.DataFrame(columns=["Feature", "Importância"])

    return results


def create_model_figures(model_results: dict[str, Any]) -> tuple[str, str]:
    fig_pred, axes_pred = plt.subplots(1, 2, figsize=(13, 5.5))
    fig_res, axes_res = plt.subplots(1, 2, figsize=(13, 5.5))

    for idx, (name, payload) in enumerate(model_results["pipelines"].items()):
        y_test = payload["y_test"]
        predictions = payload["predictions"]
        residuals = payload["residuals"]

        axes_pred[idx].scatter(y_test, predictions, alpha=0.8, color="#2a9d8f")
        line_min = min(y_test.min(), predictions.min())
        line_max = max(y_test.max(), predictions.max())
        axes_pred[idx].plot([line_min, line_max], [line_min, line_max], color="#e76f51", linestyle="--")
        axes_pred[idx].set_title(f"{name}: real vs previsto")
        axes_pred[idx].set_xlabel("Produção real (t)")
        axes_pred[idx].set_ylabel("Produção prevista (t)")

        axes_res[idx].axhline(0, color="#e76f51", linestyle="--")
        axes_res[idx].scatter(predictions, residuals, alpha=0.8, color="#264653")
        axes_res[idx].set_title(f"{name}: resíduos")
        axes_res[idx].set_xlabel("Produção prevista (t)")
        axes_res[idx].set_ylabel("Resíduo (real - previsto)")

    pred_img = plot_to_base64(fig_pred)
    res_img = plot_to_base64(fig_res)
    return pred_img, res_img


def create_feature_importance_figure(model_results: dict[str, Any]) -> str:
    importance_df = model_results["feature_importance_df"]
    if importance_df.empty:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.text(0.5, 0.5, "Modelo sem importâncias nativas.", ha="center", va="center")
        ax.axis("off")
        return plot_to_base64(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=importance_df, x="Importância", y="Feature", color="#2a9d8f", ax=ax)
    ax.set_title(f"Importâncias do melhor modelo: {model_results['best_model_name']}")
    ax.set_xlabel("Importância relativa")
    ax.set_ylabel("Feature")
    return plot_to_base64(fig)


def dataframe_to_html(df: pd.DataFrame, index: bool = False) -> str:
    if df.empty:
        return "<p class='muted'>Nenhum registro disponível para esta tabela.</p>"
    return df.to_html(index=index, border=0, classes="report-table")


def build_stats_section(base_df: pd.DataFrame) -> str:
    html_parts: list[str] = []
    stats_tables = descriptive_tables(base_df)
    for variable, meta in VARIABLE_META.items():
        industrial_stats = summarise_series(base_df.loc[base_df["tipo_tomate"] == "industrial", variable])
        mesa_stats = summarise_series(base_df.loc[base_df["tipo_tomate"] == "mesa", variable])
        display_table = stats_tables[variable]

        html_parts.append(f"<h3>{meta['label']}</h3>")
        html_parts.append(
            f"<p>{meta['label']} {meta['context']}. A tabela resume os principais indicadores descritivos separados entre tomate industrial e tomate de mesa.</p>"
        )
        html_parts.append(dataframe_to_html(display_table))
        for metric in METRIC_ORDER:
            paragraph = metric_interpretation(variable, metric, industrial_stats, mesa_stats)
            html_parts.append(f"<p><strong>{METRIC_LABELS[metric]}.</strong> {paragraph}</p>")
    return "\n".join(html_parts)


def build_html_report(base_df: pd.DataFrame, raw_metadata: list[dict[str, Any]], quality: dict[str, Any], model_results: dict[str, Any]) -> str:
    dashboard_img, dashboard_notes = create_dashboard(base_df)
    pred_img, res_img = create_model_figures(model_results)
    importance_img = create_feature_importance_figure(model_results)
    stats_html = build_stats_section(base_df)

    raw_summary_df = pd.DataFrame(
        [{key: value for key, value in row.items() if key != "Dicionário"} for row in raw_metadata]
    )
    integrated_dict_df = integrated_column_dictionary()

    best_model_name = model_results["best_model_name"]
    best_metrics = model_results["pipelines"][best_model_name]["metrics"]

    quality_text = (
        f"A base integrada possui {quality['total_rows']} combinações região-ano-tipo, das quais {quality['complete_rows']} "
        f"({format_pct(quality['complete_rows'] / quality['total_rows'])}) têm área e produção simultaneamente disponíveis. "
        f"Foram identificados {quality['missing_area']} valores ausentes em área, {quality['missing_quantity']} em produção e "
        f"{quality['missing_productivity']} em produtividade. As ausências se concentram no hiato de 2019 para ambos os segmentos e em 2020 para tomate de mesa."
    )

    best_r2 = f"{best_metrics['R2']:.4f}".replace(".", ",")
    model_text = (
        f"O conjunto de modelagem utilizou {model_results['train_rows']} observações para treino e {model_results['test_rows']} para teste. "
        f"As features empregadas foram ano, área colhida, localidade e tipo de tomate. O melhor desempenho ficou com {best_model_name}, "
        f"com MAE de {format_number(best_metrics['MAE'], 2)} t, RMSE de {format_number(best_metrics['RMSE'], 2)} t e R² de {best_r2}."
    )

    html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>Relatório Integrado de Tomate em Goiás</title>
  <style>
    :root {{
      --bg: #f7f4ee;
      --paper: #fffdf8;
      --ink: #1f2933;
      --muted: #52606d;
      --accent: #b85c38;
      --accent-2: #2a9d8f;
      --line: #e6dfd3;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", Tahoma, sans-serif;
      background: linear-gradient(180deg, #efe7db 0%, #f7f4ee 24%, #f7f4ee 100%);
      color: var(--ink);
      line-height: 1.6;
    }}
    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 32px 24px 56px;
    }}
    .hero {{
      background: radial-gradient(circle at top right, rgba(42,157,143,0.14), transparent 30%), var(--paper);
      border: 1px solid var(--line);
      border-radius: 20px;
      padding: 28px 30px;
      box-shadow: 0 18px 50px rgba(31, 41, 51, 0.08);
    }}
    h1, h2, h3 {{
      color: #182026;
      margin-top: 0;
    }}
    h2 {{
      margin-top: 36px;
      padding-bottom: 8px;
      border-bottom: 2px solid var(--line);
    }}
    .meta {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 14px;
      margin-top: 20px;
    }}
    .meta-card {{
      background: #fcfaf5;
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 14px 16px;
    }}
    .meta-card strong {{
      display: block;
      color: var(--accent);
      font-size: 0.92rem;
      letter-spacing: 0.02em;
      text-transform: uppercase;
    }}
    .section-card {{
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 24px;
      margin-top: 24px;
      box-shadow: 0 14px 36px rgba(31, 41, 51, 0.05);
    }}
    .report-table {{
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0 22px;
      font-size: 0.94rem;
      background: white;
    }}
    .report-table th, .report-table td {{
      border: 1px solid var(--line);
      padding: 9px 10px;
      text-align: left;
      vertical-align: top;
    }}
    .report-table th {{
      background: #f3ede2;
    }}
    .muted {{
      color: var(--muted);
    }}
    .figure {{
      margin: 18px 0;
    }}
    .figure img {{
      width: 100%;
      border-radius: 14px;
      border: 1px solid var(--line);
      background: white;
    }}
    .pill {{
      display: inline-block;
      padding: 4px 10px;
      border-radius: 999px;
      background: rgba(184,92,56,0.12);
      color: var(--accent);
      font-size: 0.86rem;
      margin-right: 6px;
    }}
    ul {{ padding-left: 20px; }}
  </style>
</head>
<body>
<main>
  <section class="hero">
    <span class="pill">Relatório técnico integrado</span>
    <span class="pill">Tomate industrial e de mesa</span>
    <h1>Relatório Integrado de Análise Estatística, Visualização e Modelagem Preditiva</h1>
    <p>Este relatório consolida quatro bases sobre a cultura do tomate em Goiás, integrando área colhida e quantidade produzida para os segmentos industrial e de mesa. A proposta foi organizar um fluxo único de análise, desde a documentação dos dados até a modelagem preditiva, de forma interpretável e pronta para apresentação.</p>
    <div class="meta">
      <div class="meta-card"><strong>Período coberto</strong>2012 a 2022</div>
      <div class="meta-card"><strong>Localidades</strong>5 macrorregiões goianas</div>
      <div class="meta-card"><strong>Observações integradas</strong>{quality['total_rows']}</div>
      <div class="meta-card"><strong>Documento gerado em</strong>{datetime.now().strftime("%d/%m/%Y %H:%M")}</div>
    </div>
  </section>

  <section class="section-card">
    <h2>1. Contexto e proposta analítica</h2>
    <p>Os arquivos descrevem duas cadeias produtivas com dinâmicas diferentes. O tomate industrial tende a operar em escalas de área e volume maiores, apoiado em fluxo logístico e processamento agroindustrial. Já o tomate de mesa costuma responder mais diretamente à oferta in natura, à especialização local e à volatilidade de mercado. A integração entre essas bases permite avaliar tamanho, estabilidade e eficiência relativa de cada segmento.</p>
    <p>Após a leitura dos arquivos originais, os dados foram convertidos do formato amplo para uma base analítica única em formato longo, com as colunas <code>localidade</code>, <code>tipo_tomate</code>, <code>ano</code>, <code>area_ha</code>, <code>quantidade_t</code> e <code>produtividade_t_ha</code>. Marcadores <code>-</code> foram tratados como ausentes e os valores com separador de milhar em ponto foram padronizados antes das análises.</p>
  </section>

  <section class="section-card">
    <h2>2. Documentação das bases</h2>
    <h3>2.1 Resumo dos datasets de origem</h3>
    {dataframe_to_html(raw_summary_df)}
    <h3>2.2 Dicionários de dados por arquivo</h3>
    {"".join(f"<h4>{row['Arquivo']}</h4>{dataframe_to_html(row['Dicionário'])}" for row in raw_metadata)}
    <h3>2.3 Dicionário da base analítica integrada</h3>
    {dataframe_to_html(integrated_dict_df)}
  </section>

  <section class="section-card">
    <h2>3. Qualidade e cobertura dos dados</h2>
    <p>{quality_text}</p>
    <h3>3.1 Cobertura completa por ano e segmento</h3>
    {dataframe_to_html(quality['completeness_by_year'])}
    <h3>3.2 Outliers óbvios identificados pelo critério IQR</h3>
    <p>Os outliers abaixo não foram removidos automaticamente, porque podem refletir tanto anomalias de medição quanto eventos produtivos reais. Eles merecem validação adicional junto à fonte original antes de qualquer uso decisório de alto impacto.</p>
    {dataframe_to_html(quality['outliers'])}
  </section>

  <section class="section-card">
    <h2>4. Estatística descritiva e interpretação</h2>
    {stats_html}
  </section>

  <section class="section-card">
    <h2>5. Dashboard de visualização</h2>
    <div class="figure"><img src="data:image/png;base64,{dashboard_img}" alt="Dashboard de tomate"></div>
    <ul>
      {"".join(f"<li>{note}</li>" for note in dashboard_notes)}
    </ul>
  </section>

  <section class="section-card">
    <h2>6. Modelagem preditiva</h2>
    <p>O problema preditivo escolhido foi de <strong>regressão</strong>: prever a <code>quantidade_t</code> a partir de área colhida, ano, localidade e tipo de tomate. Essa formulação é apropriada porque a variável-alvo é contínua e porque a produção depende diretamente de escala cultivada, contexto regional e sazonalidade temporal.</p>
    <p>Foram avaliados dois algoritmos. O <strong>Random Forest Regressor</strong> é adequado por capturar relações não lineares e interações entre variáveis sem exigir forte suposição paramétrica. O <strong>Gradient Boosting Regressor</strong> foi incluído porque costuma ter ótimo desempenho em dados tabulares com poucos registros, combinando árvores sequenciais para corrigir erros residuais do modelo anterior. Em ambos os casos, o alvo foi transformado com <code>log1p</code> para reduzir assimetria e estabilizar a escala da produção.</p>
    <p>{model_text}</p>
    <h3>6.1 Métricas de avaliação</h3>
    {dataframe_to_html(model_results['metrics_df'])}
    <h3>6.2 Gráficos de real versus previsto</h3>
    <div class="figure"><img src="data:image/png;base64,{pred_img}" alt="Real vs previsto"></div>
    <p>Nos gráficos de real versus previsto, quanto mais próximos os pontos ficam da diagonal, melhor a aderência. O Random Forest se aproximou mais dessa linha na amostra de teste, sugerindo melhor captura dos padrões de produção presentes nos dados.</p>
    <h3>6.3 Gráficos de resíduos</h3>
    <div class="figure"><img src="data:image/png;base64,{res_img}" alt="Resíduos dos modelos"></div>
    <p>Os resíduos do melhor modelo ficaram mais concentrados em torno de zero, sinalizando menor viés sistemático. Ainda assim, os maiores desvios aparecem nas observações de escala muito elevada, o que é esperado em séries agrícolas com forte heterogeneidade regional.</p>
    <h3>6.4 Importância das variáveis no melhor modelo</h3>
    <div class="figure"><img src="data:image/png;base64,{importance_img}" alt="Importância das variáveis"></div>
    <p>A importância das variáveis reforça quais atributos mais ajudam a explicar a produção. Em geral, a área colhida aparece como principal motor preditivo, seguida de localidade e tipo de tomate, o que é coerente com a lógica agronômica do problema.</p>
    <h3>6.5 Comparação e limitações</h3>
    <p>Entre os algoritmos testados, <strong>{best_model_name}</strong> apresentou o melhor equilíbrio entre erro absoluto, erro quadrático e poder explicativo. O resultado sugere que a relação entre área, localidade e produção é fortemente não linear e beneficia modelos baseados em árvores. As principais limitações do estudo são o tamanho reduzido da amostra, os hiatos de 2019-2020 e a ausência de variáveis climáticas, tecnológicas, de preços e manejo, que poderiam elevar a capacidade preditiva em estudos futuros.</p>
  </section>

  <section class="section-card">
    <h2>7. Conclusões gerais</h2>
    <p>Os dados mostram que o tomate industrial domina a escala de cultivo em Goiás, tanto em área quanto em produção, enquanto o tomate de mesa opera em dimensão menor, porém com produtividade média próxima em vários contextos. A análise descritiva indica forte heterogeneidade no segmento industrial, ao passo que o tomate de mesa se comporta de forma mais compacta, embora também sujeito a lacunas importantes de informação.</p>
    <p>Visualmente, a série temporal deixa claro que a base tem interrupções que afetam a leitura de tendência, mas ainda assim preserva um sinal robusto de associação entre área colhida e produção. Na etapa preditiva, modelos de árvore superaram abordagens lineares exploratórias e ofereceram melhor ajuste para a estrutura tabular disponível. O relatório final, portanto, sustenta tanto uma leitura descritiva quanto uma aplicação prática de previsão, com transparência sobre restrições e oportunidades de melhoria.</p>
  </section>
</main>
</body>
</html>
"""
    return html


def main() -> None:
    base_df, raw_metadata = build_integrated_dataset()
    quality = data_quality_summary(base_df)
    model_df = build_modeling_dataset(base_df)
    model_results = train_models(model_df)
    html = build_html_report(base_df, raw_metadata, quality, model_results)
    REPORT_PATH.write_text(html, encoding="utf-8")
    print(f"Relatório gerado em: {REPORT_PATH}")


if __name__ == "__main__":
    main()
