import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import base64
from pathlib import Path

st.set_page_config(page_title="Observatório Piauí", page_icon="bandeira.png", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .block-container { padding-top: 1rem; }
    .rodape {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: #1a1d27; color: #8899aa; font-size: 0.78rem;
        text-align: center; padding: 6px 0; border-top: 1px solid #2a2d3e;
        z-index: 999;
    }
</style>
<div class='rodape'>
    Projeto para a Superintendência &nbsp;|&nbsp; Candidato: <strong>Leonardo</strong>
    &nbsp;|&nbsp; Dados: IBGE/SICONFI/DATASUS — 2022-2025
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("municipios_piaui.csv")
    df["codigo_ibge"] = df["codigo"].astype(str)
    return df

@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-22-mun.json"
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

df = load_data()
geojson = load_geojson()

pop = df["populacao_estimada_2025"].sum()
idhm_medio = df["idhm"].mean()

def img_b64(path):
    try:
        return base64.b64encode(Path(path).read_bytes()).decode()
    except Exception:
        return ""

b64 = img_b64("bandeira.png")
flag_html = f'<img src="data:image/png;base64,{b64}" style="height:80px;width:auto;object-fit:contain;display:block;">' if b64 else ""

n_mun = len(df)
pop_str = f"{pop/1e6:.2f} M"
idhm_str = f"{idhm_medio:.3f}"

st.markdown(
    f'<div style="display:flex;align-items:center;gap:28px;padding:10px 0 12px 0;border-bottom:1px solid #2a2d3e;margin-bottom:14px;">'
    f'<div style="flex-shrink:0;">{flag_html}</div>'
    f'<div style="flex:1;">'
    f'<div style="font-size:1.75rem;font-weight:700;color:#000000;;line-height:1.1;text-shadow:none;">Observatório Piauí</div>'
    f'<div style="font-size:0.82rem;color:#8899aa;margin-top:4px;">Feito por Leonardo Cid exclusivamente para a SURPI/DF</div>'
    f'</div>'
    f'<div style="border-left:2px solid #2a2d3e;padding-left:20px;min-width:100px;">'
    f'<div style="font-size:0.65rem;color:#8899aa;text-transform:uppercase;letter-spacing:.06em;">Municípios</div>'
    f'<div style="font-size:1.55rem;font-weight:700;color:#00b4d8;">{n_mun}</div>'
    f'</div>'
    f'<div style="border-left:2px solid #2a2d3e;padding-left:20px;min-width:155px;">'
    f'<div style="font-size:0.65rem;color:#8899aa;text-transform:uppercase;letter-spacing:.06em;">População estimada 2025</div>'
    f'<div style="font-size:1.55rem;font-weight:700;color:#00b4d8;">{pop_str}</div>'
    f'</div>'
    f'<div style="border-left:2px solid #2a2d3e;padding-left:20px;min-width:110px;">'
    f'<div style="font-size:0.65rem;color:#8899aa;text-transform:uppercase;letter-spacing:.06em;">IDHM médio</div>'
    f'<div style="font-size:1.55rem;font-weight:700;color:#00b4d8;">{idhm_str}</div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True,
)

INDICADORES = {
    "IDHM (2010)": ("idhm", ".3f", "RdYlGn"),
    "PIB per capita – R$ (2023)": ("pib_per_capita", ",.0f", "Blues"),
    "Populacao estimada (2025)": ("populacao_estimada_2025", ",.0f", "Oranges"),
    "Densidade demografica – hab/km² (2022)": ("densidade_hab_km2", ",.2f", "Purples"),
    "Escolarizacao 6-14 anos – % (2022)": ("escolarizacao_pct", ".1f", "Greens"),
    "Mortalidade infantil – por mil NV (2023)": ("mortalidade_infantil", ".1f", "YlOrRd"),
    "Receitas brutas – R$ (2024)": ("receitas_brutas", ",.0f", "Teal"),
    "Despesas brutas – R$ (2024)": ("despesas_brutas", ",.0f", "Burg"),
    "Area territorial – km² (2025)": ("area_km2", ",.1f", "gray"),
}

col_sel, col_busca = st.columns([2, 2])
with col_sel:
    ind_label = st.selectbox("Indicador:", list(INDICADORES.keys()))
with col_busca:
    busca = st.text_input("Buscar município:", "")

col_field, fmt, colorscale = INDICADORES[ind_label]
df_plot = df.copy()
if busca:
    df_plot = df_plot[df_plot["municipio"].str.contains(busca, case=False, na=False)]

col_map, col_table = st.columns([3, 2])

with col_map:
    if geojson:
        fig = px.choropleth_mapbox(
            df_plot,
            geojson=geojson,
            locations="codigo_ibge",
            featureidkey="properties.id",
            color=col_field,
            hover_name="municipio",
            hover_data={
                "prefeito": True,
                "populacao_estimada_2025": ":,.0f",
                "idhm": ":.3f",
                "pib_per_capita": ":,.0f",
                "codigo_ibge": False,
            },
            color_continuous_scale=colorscale,
            mapbox_style="carto-darkmatter",
            zoom=5.3,
            center={"lat": -7.2, "lon": -42.5},
            opacity=0.75,
            labels={
                col_field: ind_label,
                "populacao_estimada_2025": "Pop. estimada",
                "pib_per_capita": "PIB per capita",
                "prefeito": "Prefeito",
            },
        )
        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor="#0f1117",
            font_color="white",
            coloraxis_colorbar=dict(
                title=dict(text=ind_label.split("–")[0].strip(), font=dict(color="white")),
                tickfont=dict(color="white"),
            ),
            height=520,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("GeoJSON nao pode ser carregado.")

with col_table:
    st.markdown(f"#### Top municípios — {ind_label.split('–')[0].strip()}")
    df_top = (
        df_plot[["municipio", "prefeito", col_field]]
        .dropna(subset=[col_field])
        .sort_values(col_field, ascending=False)
        .reset_index(drop=True)
    )
    df_top.index += 1
    df_top.columns = ["Município", "Prefeito", ind_label.split("(")[0].strip()]
    st.dataframe(df_top, use_container_width=True, height=480)

st.divider()
st.markdown("#### Ficha do Município")
mun_sel = st.selectbox(
    "Selecione o município:",
    sorted(df["municipio"].tolist()),
    index=sorted(df["municipio"].tolist()).index("Teresina"),
)
row = df[df["municipio"] == mun_sel].iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Populacao (2022)", f"{int(row['populacao_censo_2022']):,}".replace(",", "."))
c2.metric("Pop. estimada (2025)", f"{int(row['populacao_estimada_2025']):,}".replace(",", "."))
c3.metric("IDHM", f"{row['idhm']:.3f}" if pd.notna(row["idhm"]) else "—")
c4.metric("PIB per capita", f"R$ {row['pib_per_capita']:,.0f}".replace(",", ".") if pd.notna(row["pib_per_capita"]) else "—")

c5, c6, c7, c8 = st.columns(4)
c5.metric("Area (km²)", f"{row['area_km2']:,.1f}".replace(",", "."))
c6.metric("Densidade (hab/km²)", f"{row['densidade_hab_km2']:,.2f}" if pd.notna(row["densidade_hab_km2"]) else "—")
c7.metric("Escolarizacao 6-14 anos", f"{row['escolarizacao_pct']:.1f}%" if pd.notna(row["escolarizacao_pct"]) else "—")
c8.metric("Mortalidade infantil", f"{row['mortalidade_infantil']:.1f}" if pd.notna(row["mortalidade_infantil"]) else "—")

c9, c10 = st.columns(2)
c9.metric("Receitas brutas (2024)", f"R$ {row['receitas_brutas']:,.0f}" if pd.notna(row["receitas_brutas"]) else "—")
c10.metric("Despesas brutas (2024)", f"R$ {row['despesas_brutas']:,.0f}" if pd.notna(row["despesas_brutas"]) else "—")

st.caption(f"**Prefeito(a):** {row['prefeito']} &nbsp;|&nbsp; **Codigo IBGE:** {row['codigo']} &nbsp;|&nbsp; **Gentilico:** {row['gentilico']}")

st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
