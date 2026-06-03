import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Desempeño Torreras — SLA 2026",
    page_icon="📊",
    layout="wide"
)

# ── PALETA ──────────────────────────────────────────
C1, C2, C3, C4, C5 = "#002EFF", "#FF3D00", "#43E7B4", "#FD6C98", "#2FCBF1"
DARK = "#0A0F2E"

st.markdown("""
<style>
    .main { background-color: #F0F3FA; }
    .block-container { padding-top: 1.5rem; }
    .metric-card {
        background: white; border-radius: 12px; padding: 1rem 1.2rem;
        border: 1px solid #E4E9F5; box-shadow: 0 1px 6px rgba(0,0,0,.06);
        margin-bottom: 0.5rem;
    }
    .exec-card {
        background: #F0F3FA; border-radius: 10px; padding: 0.85rem 1rem;
        border: 1.5px solid #E4E9F5; position: relative;
    }
    .exec-label { font-size: 10px; font-weight: 800; text-transform: uppercase;
        letter-spacing: .1em; color: #7A83A6; margin-bottom: 4px; }
    .exec-val { font-size: 22px; font-weight: 900; line-height: 1.1; margin-bottom: 4px; }
    .exec-desc { font-size: 11px; color: #7A83A6; }
    .section-title { font-size: 11px; font-weight: 800; color: #7A83A6;
        text-transform: uppercase; letter-spacing: .08em; margin: 1rem 0 0.5rem;
        border-bottom: 1px solid #E4E9F5; padding-bottom: 0.4rem; }
</style>
""", unsafe_allow_html=True)

# ── DATOS BTS ────────────────────────────────────────
bts_data = pd.DataFrame([
    {"Torrera": "QMC",                        "T_Busqueda": 122, "T_Saneamiento": 198, "T_Construccion": 94,  "T_Total": 414, "N_Sitios": 1},
    {"Torrera": "TORRECOM",                   "T_Busqueda": 134, "T_Saneamiento": 96,  "T_Construccion": 127, "T_Total": 357, "N_Sitios": 4},
    {"Torrera": "ATP",                        "T_Busqueda": 195, "T_Saneamiento": 89,  "T_Construccion": 56,  "T_Total": 340, "N_Sitios": 8},
    {"Torrera": "SBA",                        "T_Busqueda": 83,  "T_Saneamiento": 134, "T_Construccion": 80,  "T_Total": 298, "N_Sitios": 5},
    {"Torrera": "Phoenix Tower",              "T_Busqueda": 112, "T_Saneamiento": 107, "T_Construccion": 58,  "T_Total": 277, "N_Sitios": 14},
    {"Torrera": "TP","T_Busqueda": 63,  "T_Saneamiento": 87,  "T_Construccion": 42,  "T_Total": 192, "N_Sitios": 9},
])

# ── DATOS CT ─────────────────────────────────────────
ct_data = pd.DataFrame([
    {"Torrera": "American Tower",             "T_Factibilidad": 18, "T_ValidacionAP": 38, "T_Inicio": 21, "T_FinObra": 84, "T_Total": 161, "N_Sitios": 2},
    {"Torrera": "SDP",                        "T_Factibilidad": 20, "T_ValidacionAP": 22, "T_Inicio": 24, "T_FinObra": 21, "T_Total": 87,  "N_Sitios": 26},
    {"Torrera": "SBA",                        "T_Factibilidad": 18, "T_ValidacionAP": 22, "T_Inicio": 22, "T_FinObra": 28, "T_Total": 85,  "N_Sitios": 4},
    {"Torrera": "Infratel",                   "T_Factibilidad": 6,  "T_ValidacionAP": 23, "T_Inicio": 23, "T_FinObra": 23, "T_Total": 75,  "N_Sitios": 5},
    {"Torrera": "Phoenix Tower",              "T_Factibilidad": 18, "T_ValidacionAP": 19, "T_Inicio": 5,  "T_FinObra": 21, "T_Total": 56,  "N_Sitios": 6},
    {"Torrera": "ATP",                        "T_Factibilidad": 6,  "T_ValidacionAP": 18, "T_Inicio": 7,  "T_FinObra": 12, "T_Total": 43,  "N_Sitios": 7},
    {"Torrera": "TP","T_Factibilidad": 10, "T_ValidacionAP": 11, "T_Inicio": 2,  "T_FinObra": 13, "T_Total": 36,  "N_Sitios": 1},
])

dev_data = pd.DataFrame([
    {"Torrera": "SBA", "N_Devoluciones": 39},
    {"Torrera": "TORRECOM", "N_Devoluciones": 30},
    {"Torrera": "Phoenix Tower", "N_Devoluciones": 12},
    {"Torrera": "TP", "N_Devoluciones": 11},
    {"Torrera": "ATP", "N_Devoluciones": 9},
])

# ── HEADER ───────────────────────────────────────────
st.markdown(f"""
<div style="background:{DARK};padding:1rem 1.5rem;border-radius:12px;
     display:flex;align-items:center;gap:12px;margin-bottom:1.2rem">
  <span style="font-size:20px">📊</span>
  <span style="color:white;font-size:16px;font-weight:800;letter-spacing:.04em">
    Desempeño Torreras — SLA Sitios Nuevos 2026</span>
  <span style="color:rgba(255,255,255,.4);font-size:12px;margin-left:auto">
    Solo estados FNE + LPE · 92 sitios</span>
</div>
""", unsafe_allow_html=True)

# ── RESUMEN EJECUTIVO ─────────────────────────────────
st.markdown('<div class="section-title">🔎 Análisis ejecutivo — Hallazgos clave</div>', unsafe_allow_html=True)

avg_bts = bts_data['T_Total'].mean()
avg_ct  = ct_data['T_Total'].mean()
faster  = "CON TORRERA" if avg_ct < avg_bts else "BTS"
diff    = abs(int(avg_bts - avg_ct))
bottle_bts = bts_data[['T_Busqueda','T_Saneamiento','T_Construccion']].mean()
bottle_bts_name = ['Búsqueda','Saneamiento','Construcción'][bottle_bts.values.argmax()]
bottle_ct  = ct_data[['T_Factibilidad','T_ValidacionAP','T_Inicio','T_FinObra']].mean()
bottle_ct_name  = ['Factibilidad','Validación AP','Inicio Obra','Fin de Obra'][bottle_ct.values.argmax()]

cols = st.columns(6)
exec_items = [
    ("⚡", "Tipo más rápido", faster, f"{diff} días menos en promedio total", C3),
    ("🔥", "Cuello botella BTS", bottle_bts_name, f"Mayor tiempo promedio ({int(bottle_bts.max())} días)", C4),
    ("🔔", "Cuello botella CT", bottle_ct_name, f"Mayor tiempo promedio ({int(bottle_ct.max())} días)", C2),
    ("⚠️", "Paralizados", "12", "Requieren atención inmediata", C2),
    ("📋", "Sin inicio obra", "191", "Pendientes de arranque", C5),
    ("✅", "Finalizados FNE+LPE", "92", "Sitios completados", C3),
]
for col, (ico, label, val, desc, color) in zip(cols, exec_items):
    with col:
        st.markdown(f"""
        <div class="exec-card" style="border-top:3px solid {color}">
            <div class="exec-label">{ico} {label}</div>
            <div class="exec-val" style="color:{color}">{val}</div>
            <div class="exec-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── GRAFICOS APILADOS ─────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown(f'<div class="section-title">📡 Sitios Nuevos BTS — {bts_data["N_Sitios"].sum()} proyectos</div>', unsafe_allow_html=True)
    fig1 = go.Figure()
    for campo, label, color in [
        ("T_Busqueda","T. Búsqueda", C1),
        ("T_Saneamiento","T. Saneamiento", C2),
        ("T_Construccion","T. Construcción", C3),
    ]:
        fig1.add_trace(go.Bar(
            name=label, x=bts_data['Torrera'], y=bts_data[campo],
            marker_color=color, text=bts_data[campo],
            textposition='inside', textfont=dict(size=10, color='black'),
            customdata=bts_data['N_Sitios'],
        ))
    # Add invisible trace for N_Sitios legend
    fig1.add_trace(go.Scatter(
        name='Cantidad de sitios (●)', x=[None], y=[None],
        mode='markers', marker=dict(color='#2FCBF1', size=8, symbol='circle'),
        showlegend=True,
    ))
    fig1.add_trace(go.Scatter(
        name="T. Promedio", x=bts_data['Torrera'], y=bts_data['T_Total'],
        mode='lines+markers+text', line=dict(color=C5, width=2.5),
        marker=dict(size=7, color=C5),
        text=bts_data['T_Total'], textposition='top center',
        textfont=dict(size=11, color='black'),
    ))
    fig1.update_layout(
        barmode='stack', height=380, plot_bgcolor='white', paper_bgcolor='white',
        legend=dict(orientation='h', y=1.08, x=0, font=dict(size=10)),
        margin=dict(t=20, b=80, l=40, r=20),
        yaxis_title="Tiempo (días)",
        annotations=[
            dict(x=row['Torrera'], y=-45, text=f"● {row['N_Sitios']}",
                 showarrow=False, font=dict(size=10, color=C5),
                 xref='x', yref='y', yanchor='top')
            for _, row in bts_data.iterrows()
        ]
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown(f'<div class="section-title">🗼 Collos CON TORRERA — {ct_data["N_Sitios"].sum()} proyectos</div>', unsafe_allow_html=True)
    fig2 = go.Figure()
    for campo, label, color in [
        ("T_Factibilidad","T. Factibilidad", C1),
        ("T_ValidacionAP","T. Validación AP", C2),
        ("T_Inicio","T. Inicio", C3),
        ("T_FinObra","T. Adecuaciones", C4),
    ]:
        fig2.add_trace(go.Bar(
            name=label, x=ct_data['Torrera'], y=ct_data[campo],
            marker_color=color, text=ct_data[campo],
            textposition='inside', textfont=dict(size=10, color='black'),
        ))
    # Add invisible trace for N_Sitios legend
    fig2.add_trace(go.Scatter(
        name='Cantidad de sitios (●)', x=[None], y=[None],
        mode='markers', marker=dict(color='#2FCBF1', size=8, symbol='circle'),
        showlegend=True,
    ))
    fig2.add_trace(go.Scatter(
        name="T. Total", x=ct_data['Torrera'], y=ct_data['T_Total'],
        mode='lines+markers+text', line=dict(color=C5, width=2.5),
        marker=dict(size=7, color=C5),
        text=ct_data['T_Total'], textposition='top center',
        textfont=dict(size=11, color='black'),
    ))
    fig2.update_layout(
        barmode='stack', height=380, plot_bgcolor='white', paper_bgcolor='white',
        legend=dict(orientation='h', y=1.08, x=0, font=dict(size=10)),
        margin=dict(t=20, b=80, l=40, r=20),
        yaxis_title="Tiempo (días)",
        annotations=[
            dict(x=row['Torrera'], y=-20, text=f"● {row['N_Sitios']}",
                 showarrow=False, font=dict(size=10, color=C5),
                 xref='x', yref='y', yanchor='top')
            for _, row in ct_data.iterrows()
        ]
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── RANKING ───────────────────────────────────────────
st.markdown('<div class="section-title">📊 Ranking — Tiempo promedio total por torrera (mayor a menor)</div>', unsafe_allow_html=True)

rank_df = pd.DataFrame([
    {"Torrera": "QMC",                         "BTS": 414, "CT": 0},
    {"Torrera": "TORRECOM",                    "BTS": 357, "CT": 0},
    {"Torrera": "ATP",                         "BTS": 340, "CT": 43},
    {"Torrera": "American Tower",              "BTS": 0,   "CT": 161},
    {"Torrera": "SBA",                         "BTS": 298, "CT": 85},
    {"Torrera": "SDP",                         "BTS": 0,   "CT": 87},
    {"Torrera": "Infratel",                    "BTS": 0,   "CT": 75},
    {"Torrera": "Phoenix Tower",               "BTS": 277, "CT": 56},
    {"Torrera": "TP", "BTS": 192, "CT": 36},
]).sort_values(by=['BTS','CT'], ascending=False)

fig3 = go.Figure()
fig3.add_trace(go.Bar(
    name="BTS (promedio)", y=rank_df['Torrera'], x=rank_df['BTS'],
    orientation='h', marker_color=C1,
    text=rank_df['BTS'].apply(lambda x: str(x) if x>0 else ''),
    textposition='inside', textfont=dict(size=10, color='black'),
))
fig3.add_trace(go.Bar(
    name="CON TORRERA (promedio)", y=rank_df['Torrera'], x=rank_df['CT'],
    orientation='h', marker_color=C3,
    text=rank_df['CT'].apply(lambda x: str(x) if x>0 else ''),
    textposition='inside', textfont=dict(size=10, color='black'),
))
fig3.update_layout(
    barmode='group', height=340, plot_bgcolor='white', paper_bgcolor='white',
    legend=dict(orientation='h', y=1.08, x=0, font=dict(size=10)),
    margin=dict(t=10, b=60, l=200, r=20),
    xaxis_title="Días promedio",
)
st.plotly_chart(fig3, use_container_width=True)

# ── DEVOLUCIONES ──────────────────────────────────────
st.markdown('<div class="section-title">🔄 N° de devoluciones por torrera</div>', unsafe_allow_html=True)

fig4 = go.Figure(go.Bar(
    x=dev_data['Torrera'], y=dev_data['N_Devoluciones'],
    marker_color=C1, marker_line_color=C1, marker_line_width=1,
    text=dev_data['N_Devoluciones'],
    textposition='inside', textfont=dict(size=11, color='white'),
))
fig4.update_layout(
    height=280, plot_bgcolor='white', paper_bgcolor='white',
    margin=dict(t=30, b=40, l=40, r=20),
    yaxis_title="N° devoluciones",
    showlegend=False,
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown(f'<p style="text-align:center;color:#7A83A6;font-size:11px;margin-top:1rem">Dashboard SLA 2026 · Solo estados FNE + LPE · 92 sitios</p>', unsafe_allow_html=True)
