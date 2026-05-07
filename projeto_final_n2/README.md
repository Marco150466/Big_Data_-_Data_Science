# Projeto Final N2

Projeto simples em Python para:

1. baixar uma base publica
2. calcular estatistica descritiva
3. gerar um relatorio em Markdown
4. salvar os dados no PostgreSQL, se a conexao estiver correta

## Base usada

- Nome: `Titanic Dataset`
- Fonte: <https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv>

## Arquivos principais

- `src/main.py`: faz todo o processo
- `data/titanic.csv`: copia local da base
- `reports/relatorio_analitico.md`: relatorio final

## Como executar

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python src/main.py
```

## PostgreSQL

Se voce ja tem PostgreSQL instalado, edite o arquivo `.env` com:

- host
- porta
- nome do banco
- usuario
- senha

Se a conexao com o banco falhar, o projeto continua funcionando e gera o relatorio normalmente.

## Saida esperada

Ao final da execucao, o projeto:

- salva a base em `data/titanic.csv`
- tenta gravar os dados no PostgreSQL
- gera o arquivo `reports/relatorio_analitico.md`

## Observacao

Se quiser trocar a base no futuro, basta editar as constantes no arquivo `src/main.py`.
