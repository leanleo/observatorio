# Observatório Piauí

Painel interativo de indicadores municipais do estado do Piauí.

**Projeto para a Superintendência | Candidato: Leonardo Cid**

## Funcionalidades

- Mapa coroplético interativo com todos os 224 municípios do Piauí
- 9 indicadores selecionáveis (IDHM, PIB per capita, população, densidade, escolarização, mortalidade infantil, receitas/despesas, área)
- Busca por município
- Ranking (Top municípios) por indicador
- Ficha completa por município
- Tema escuro, layout responsivo

## Dados

| Indicador | Fonte | Ano |
|-----------|-------|-----|
| Área territorial | IBGE | 2025 |
| População (censo) | IBGE Censo | 2022 |
| Densidade demográfica | IBGE Censo | 2022 |
| Pop. estimada | IBGE | 2025 |
| Escolarização 6-14 anos | IBGE Censo | 2022 |
| IDHM | PNUD | 2010 |
| Mortalidade infantil | DATASUS | 2023 |
| Receitas/Despesas brutas | SICONFI/STN | 2024 |
| PIB per capita | IBGE | 2023 |

## Deploy local

```bash
pip install -r requirements.txt
streamlit run app.py
```

