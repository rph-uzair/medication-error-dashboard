# ================================================================
#  FDA Adverse Event Dashboard
#  Author : Muhammad Uzair RPh (PharmD)
#  Org    : University of Peshawar
#  Data   : FDA AEMS · Q3 2025 – Q1 2026
#  Stack  : Python · Pandas · Plotly · Streamlit
# ================================================================

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import os, warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="FDA Adverse Event Dashboard",
    page_icon="💊", layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root{
  --bg0:#04080F;--bg1:#070C17;--card:#0B1524;
  --b1:#1A2D45;--b2:#203552;
  --sky:#0EA5E9;--skyd:rgba(14,165,233,.10);--skyg:rgba(14,165,233,.22);
  --grn:#10B981;--grnd:rgba(16,185,129,.10);
  --pnk:#EC4899;--pnkd:rgba(236,72,153,.10);
  --amb:#F59E0B;--ambd:rgba(245,158,11,.10);
  --vio:#8B5CF6;--viod:rgba(139,92,246,.10);
  --t1:#F1F5F9;--t2:#CBD5E1;--t3:#94A3B8;--t4:#64748B;--t5:#334155;
  --fn:'Plus Jakarta Sans',sans-serif;--mono:'JetBrains Mono',monospace;
}
html,body,[data-testid="stAppViewContainer"]{
  background:var(--bg0)!important;font-family:var(--fn)!important;color:var(--t1)!important;
}
[data-testid="stAppViewContainer"]{
  background:
    radial-gradient(ellipse 90% 55% at 8% 0%,rgba(14,165,233,.07) 0%,transparent 55%),
    radial-gradient(ellipse 65% 45% at 92% 100%,rgba(139,92,246,.05) 0%,transparent 55%),
    var(--bg0)!important;
}
[data-testid="stHeader"]{background:transparent!important;}
[data-testid="stDecoration"]{display:none!important;}
[data-testid="stSidebar"]{background:var(--bg1)!important;border-right:1px solid var(--b1)!important;}
[data-testid="stSidebar"] *{font-family:var(--fn)!important;}
[data-testid="stSidebar"] label{
  font-size:10px!important;font-weight:600!important;
  letter-spacing:.09em!important;text-transform:uppercase!important;color:var(--t4)!important;
}
.block-container{padding:1.6rem 2.2rem 3rem!important;max-width:1440px!important;}
[data-testid="stTabs"]>div:first-child{border-bottom:1px solid var(--b1)!important;gap:0!important;}
button[data-baseweb="tab"]{
  font-family:var(--fn)!important;font-size:12.5px!important;font-weight:500!important;
  color:var(--t4)!important;background:transparent!important;border:none!important;
  border-bottom:2px solid transparent!important;padding:10px 22px 12px!important;margin-bottom:-1px!important;
}
button[data-baseweb="tab"]:hover{color:var(--t2)!important;}
button[aria-selected="true"][data-baseweb="tab"]{
  color:var(--sky)!important;border-bottom:2px solid var(--sky)!important;background:var(--skyd)!important;
}
[data-testid="stTabPanel"]{padding-top:24px!important;}
[data-testid="stTextInput"] input{
  background:var(--card)!important;border:1px solid var(--b2)!important;
  border-radius:8px!important;color:var(--t1)!important;
  font-family:var(--fn)!important;font-size:13px!important;
}
[data-testid="stTextInput"] input:focus{
  border-color:var(--sky)!important;box-shadow:0 0 0 3px var(--skyd)!important;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"]{
  background:var(--skyd)!important;border:1px solid rgba(14,165,233,.3)!important;
  color:#93C5FD!important;border-radius:4px!important;font-size:11px!important;
}
/* Data table — explicit bright text */
[data-testid="stDataFrame"]{border:1px solid var(--b1)!important;border-radius:10px!important;overflow:hidden!important;}
[data-testid="stDataFrame"] table{background:var(--card)!important;}
[data-testid="stDataFrame"] th{
  background:#0B1524!important;color:#94A3B8!important;
  font-family:var(--mono)!important;font-size:11px!important;font-weight:600!important;
}
[data-testid="stDataFrame"] td{
  color:#CBD5E1!important;font-family:var(--mono)!important;font-size:11.5px!important;
}
[data-testid="stDownloadButton"] button{
  background:var(--skyd)!important;border:1px solid rgba(14,165,233,.3)!important;
  color:#93C5FD!important;border-radius:8px!important;font-family:var(--fn)!important;
  font-size:12px!important;font-weight:500!important;padding:8px 18px!important;
}
[data-testid="stDownloadButton"] button:hover{background:var(--skyg)!important;border-color:var(--sky)!important;}
hr{border:none!important;border-top:1px solid var(--b1)!important;margin:1.2rem 0!important;}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:var(--bg0);}
::-webkit-scrollbar-thumb{background:var(--b2);border-radius:4px;}
</style>
""", unsafe_allow_html=True)


# ── CONSISTENT COLOR PALETTE ────────────────────────────────────
# Age group colors — used in BOTH pie chart AND referenced consistently
AGE_COLORS = {
    '0–18':  '#38BDF8',   # light sky
    '19–35': '#A78BFA',   # violet
    '36–50': '#34D399',   # emerald
    '51–65': '#FCD34D',   # amber
    '65+':   '#F87171',   # rose
}
AGE_ORDER  = ['0–18','19–35','36–50','51–65','65+']

# Drug bars   → sky blue gradient
SKY = [[0,'#061829'],[.5,'#0369A1'],[1,'#38BDF8']]
# Reaction bars → violet gradient (NOT red — avoids confusion with female)
VIO = [[0,'#130A2A'],[.5,'#5B21B6'],[1,'#C4B5FD']]

# Base chart layout — NO xaxis / yaxis / legend keys
BASE = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Plus Jakarta Sans,sans-serif', color='#94A3B8', size=11),
    title_font=dict(family='Plus Jakarta Sans', color='#E2E8F0', size=13),
    margin=dict(t=44, b=30, l=8, r=8),
    hoverlabel=dict(bgcolor='#0B1524', bordercolor='#203552',
                    font=dict(family='Plus Jakarta Sans', color='#F1F5F9', size=12)),
)
AX = dict(
    gridcolor='#0F1A2E', linecolor='#1A2D45',
    tickcolor='#1A2D45',
    tickfont=dict(color='#94A3B8', size=11),
    title_font=dict(color='#64748B')
)
LEG = dict(bgcolor='rgba(0,0,0,0)', orientation='v',
           x=1.02, y=.5, font=dict(color='#94A3B8', size=11))
LBL = dict(color='#94A3B8', size=11, family='JetBrains Mono')


# ── UI COMPONENTS ───────────────────────────────────────────────
def kpi(label, value, sub, color, icon):
    pal = {
        "sky":  ("#0EA5E9","rgba(14,165,233,.08)","rgba(14,165,233,.22)"),
        "grn":  ("#10B981","rgba(16,185,129,.08)","rgba(16,185,129,.22)"),
        "pnk":  ("#EC4899","rgba(236,72,153,.08)", "rgba(236,72,153,.22)"),
        "amb":  ("#F59E0B","rgba(245,158,11,.08)","rgba(245,158,11,.22)"),
        "vio":  ("#8B5CF6","rgba(139,92,246,.08)","rgba(139,92,246,.22)"),
        "cyan": ("#06B6D4","rgba(6,182,212,.08)","rgba(6,182,212,.22)"),
    }
    c, bg, br = pal.get(color, pal["sky"])
    st.markdown(f"""
    <div style="background:#0B1524;border:1px solid {br};border-radius:12px;
                padding:20px 20px 16px;position:relative;overflow:hidden;">
      <div style="position:absolute;top:0;right:0;width:70px;height:70px;
                  background:{bg};border-radius:0 12px 0 70px;"></div>
      <div style="position:absolute;top:13px;right:14px;font-size:20px;opacity:.65">{icon}</div>
      <div style="font-size:10px;font-weight:600;color:#475569;letter-spacing:.09em;
                  text-transform:uppercase;margin-bottom:9px">{label}</div>
      <div style="font-size:26px;font-weight:700;color:{c};letter-spacing:-.03em;
                  line-height:1;margin-bottom:5px;font-family:'JetBrains Mono',monospace">{value}</div>
      <div style="font-size:11px;color:#64748B">{sub}</div>
    </div>""", unsafe_allow_html=True)


def sh(title, sub="", icon=""):
    s = f'<span style="font-size:11px;color:#475569;margin-left:4px">{sub}</span>' if sub else ""
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;margin:26px 0 14px">
      <span style="font-size:16px">{icon}</span>
      <span style="font-size:14px;font-weight:600;color:#F1F5F9;letter-spacing:-.02em">{title}</span>
      {s}
      <div style="flex:1;height:1px;background:linear-gradient(to right,#1A2D45,transparent);margin-left:8px"></div>
    </div>""", unsafe_allow_html=True)


def risk_pill(level):
    cfg = {
        "CRITICAL": ("#F43F5E","rgba(244,63,94,.14)","rgba(244,63,94,.28)"),
        "HIGH":     ("#F59E0B","rgba(245,158,11,.14)","rgba(245,158,11,.28)"),
        "MEDIUM":   ("#0EA5E9","rgba(14,165,233,.14)","rgba(14,165,233,.28)"),
        "LOW":      ("#10B981","rgba(16,185,129,.14)","rgba(16,185,129,.28)"),
    }
    c,bg,br = cfg.get(level, cfg["LOW"])
    return f'<span style="padding:3px 10px;border-radius:5px;font-size:10px;font-weight:700;letter-spacing:.07em;background:{bg};border:1px solid {br};color:{c}">{level}</span>'


def get_risk(n, p95, p75, p50):
    if n >= p95: return "CRITICAL"
    if n >= p75: return "HIGH"
    if n >= p50: return "MEDIUM"
    return "LOW"


# ── DATA (memory-efficient) ──────────────────────────────────────
@st.cache_data(show_spinner=False)
def load():
    dl,rl,xl = [],[],[]
    for q in ['25Q3','25Q4','26Q1']:
        dp,rp,xp = f'data/DEMO{q}.txt',f'data/DRUG{q}.txt',f'data/REAC{q}.txt'
        if not os.path.exists(dp): continue
        d = pd.read_csv(dp,sep='$',encoding='latin-1',low_memory=False,
            usecols=lambda c: c.strip().lower() in ['primaryid','age','age_cod','sex'])
        r = pd.read_csv(rp,sep='$',encoding='latin-1',low_memory=False,
            usecols=lambda c: c.strip().lower() in ['primaryid','drugname','role_cod'])
        x = pd.read_csv(xp,sep='$',encoding='latin-1',low_memory=False,
            usecols=lambda c: c.strip().lower() in ['primaryid','pt'])
        for f in [d,r,x]:
            f.columns = f.columns.str.lower().str.strip()
            f['quarter'] = q
        dl.append(d); rl.append(r); xl.append(x)
    return (pd.concat(dl,ignore_index=True),
            pd.concat(rl,ignore_index=True),
            pd.concat(xl,ignore_index=True))


@st.cache_data(show_spinner=False)
def clean(demo, drug, reac):
    demo = demo[demo['age_cod']=='YR'].copy()
    demo['age'] = pd.to_numeric(demo['age'],errors='coerce')
    demo = demo.dropna(subset=['age'])
    demo = demo[(demo['age']>=1)&(demo['age']<=110)]
    # age_group as STRING not Categorical — avoids Streamlit rendering issues
    demo['age_group'] = pd.cut(demo['age'],[0,18,35,50,65,110],
                               labels=AGE_ORDER).astype(str)
    demo['sex']    = demo['sex'].map({'M':'Male','F':'Female'})
    demo           = demo.dropna(subset=['sex'])
    demo['period'] = demo['quarter'].map(
        {'25Q3':'Q3 2025','25Q4':'Q4 2025','26Q1':'Q1 2026'})
    pri = drug[drug['role_cod']=='PS'][['primaryid','drugname']].copy()
    pri['drugname'] = pri['drugname'].str.upper().str.strip()
    pri = pri[pri['drugname'].str.len()>2].drop_duplicates(subset=['primaryid','drugname'])
    rc  = reac[['primaryid','pt']].copy()
    rc['pt'] = rc['pt'].str.title().str.strip()
    rc  = rc.dropna(subset=['pt'])
    m   = demo.merge(pri,on='primaryid',how='inner').merge(rc,on='primaryid',how='inner')
    return m.drop_duplicates(subset=['primaryid','drugname','pt'])


with st.spinner('Loading FDA data...'):
    D0,DR0,RC0 = load()
    DF = clean(D0,DR0,RC0)


# ── SIDEBAR ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:4px 0 20px;border-bottom:1px solid #1A2D45;margin-bottom:20px">
      <div style="font-size:15px;font-weight:700;color:#F1F5F9;letter-spacing:-.02em;margin-bottom:3px">
        💊 FDA Adverse Event
      </div>
      <div style="font-size:12px;color:#475569">Safety Dashboard</div>
      <div style="margin-top:14px;padding-top:12px;border-top:1px solid #0F1A2E">
        <div style="font-size:12px;font-weight:600;color:#CBD5E1">Muhammad Uzair RPh (PharmD)</div>
        <div style="font-size:11px;color:#475569;margin-top:3px">University of Peshawar</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    periods = sorted(DF['period'].dropna().unique().tolist())
    sel_p   = st.multiselect("Time Period",   periods,         default=periods)
    sel_a   = st.multiselect("Age Group",     AGE_ORDER,       default=AGE_ORDER)
    sel_s   = st.multiselect("Patient Sex",   ['Male','Female'],default=['Male','Female'])
    top_n   = st.slider("Top N Results", min_value=5, max_value=25, value=15, step=1, key="topn")

    st.markdown("""
    <div style="margin-top:18px;padding:13px 15px;background:rgba(14,165,233,.06);
                border:1px solid rgba(14,165,233,.15);border-radius:8px">
      <div style="font-size:10px;font-weight:600;color:#0EA5E9;letter-spacing:.08em;
                  text-transform:uppercase;margin-bottom:7px">Data Source</div>
      <div style="font-size:11px;color:#475569;line-height:1.7">
        FDA Adverse Event<br>Monitoring System (AEMS)<br>
        <span style="color:#10B981;font-weight:500">● Q3 2025 · Q4 2025 · Q1 2026</span>
      </div>
    </div>""", unsafe_allow_html=True)


# ── FILTER ──────────────────────────────────────────────────────
F = DF[
    (DF['period'].isin(sel_p)) &
    (DF['age_group'].isin(sel_a)) &
    (DF['sex'].isin(sel_s))
].copy()


# ── HEADER ──────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            padding-bottom:18px;border-bottom:1px solid #1A2D45;margin-bottom:22px">
  <div>
    <div style="font-size:20px;font-weight:700;color:#F1F5F9;letter-spacing:-.03em">
      FDA Adverse Event Dashboard
    </div>
    <div style="font-size:12px;color:#475569;margin-top:3px">
      Muhammad Uzair RPh (PharmD) &nbsp;·&nbsp; University of Peshawar
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:14px">
    <div style="text-align:right">
      <div style="font-size:10px;color:#334155;letter-spacing:.07em;text-transform:uppercase;font-weight:600">Total Records</div>
      <div style="font-size:14px;color:#0EA5E9;font-weight:700;font-family:'JetBrains Mono',monospace;margin-top:2px">{len(DF):,}</div>
    </div>
    <div style="padding:6px 12px;background:rgba(16,185,129,.08);
                border:1px solid rgba(16,185,129,.22);border-radius:6px;
                font-size:10px;color:#6EE7B7;font-weight:700;letter-spacing:.05em">● LIVE</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── TABS ────────────────────────────────────────────────────────
t1,t2,t3,t4,t5 = st.tabs([
    "📊   Overview",
    "🔍   Drug Safety Search",
    "⚡   Drug Comparison",
    "🚨   High Risk Alerts",
    "📋   Data Explorer",
])


# ════════════════════════════════════════════════════════════════
# TAB 1 · OVERVIEW
# ════════════════════════════════════════════════════════════════
with t1:
    sh("Key Metrics","Aggregate statistics across selected filters","📊")
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi("Total Reports",    f"{len(F):,}",                    "Adverse event records",      "sky", "📋")
    with c2: kpi("Unique Drugs",     f"{F['drugname'].nunique():,}",    "Distinct substances",        "cyan","💊")
    with c3: kpi("Unique Reactions", f"{F['pt'].nunique():,}",          "Distinct adverse reactions", "vio", "⚠️")
    with c4: kpi("Male Reports",     f"{len(F[F['sex']=='Male']):,}",   "Male patient records",       "sky", "👨")
    with c5: kpi("Female Reports",   f"{len(F[F['sex']=='Female']):,}","Female patient records",     "pnk", "👩")

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── Drug bar + Age donut ──
    sh(f"Top {top_n} Drugs · Reports by Age Group","","💊")
    col1,col2 = st.columns([3,2],gap="large")

    with col1:
        td = F['drugname'].value_counts().head(top_n).reset_index()
        td.columns = ['Drug','Reports']
        fig = go.Figure(go.Bar(
            x=td['Reports'], y=td['Drug'], orientation='h',
            marker=dict(color=td['Reports'],colorscale=SKY,showscale=False,line=dict(width=0)),
            text=td['Reports'].apply(lambda x:f'{x:,}'),
            textposition='outside', textfont=LBL,
            hovertemplate='<b>%{y}</b><br>%{x:,} reports<extra></extra>'
        ))
        fig.update_layout(**BASE, title=f"Top {top_n} Drugs by Report Volume", height=420,
                          xaxis=dict(**AX,showgrid=True),
                          yaxis=dict(**AX,showgrid=False,categoryorder='total ascending'))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Use consistent AGE_COLORS — same colors will be used in heatmap annotation
        ag_counts = F['age_group'].value_counts()
        ag_labels = [a for a in AGE_ORDER if a in ag_counts.index]
        ag_values = [ag_counts.get(a,0) for a in ag_labels]
        ag_colors = [AGE_COLORS[a] for a in ag_labels]

        fig2 = go.Figure(go.Pie(
            labels=ag_labels, values=ag_values, hole=.52,
            marker=dict(colors=ag_colors, line=dict(color='#04080F',width=2)),
            textinfo='percent', textfont=dict(size=12,color='#F1F5F9'),
            hovertemplate='<b>%{label}</b><br>%{value:,} reports<br>%{percent}<extra></extra>',
            sort=False
        ))
        fig2.add_annotation(text=f"<b>{len(F):,}</b>",x=.5,y=.5,showarrow=False,
                            font=dict(size=14,color='#F1F5F9',family='JetBrains Mono'))
        fig2.update_layout(**BASE, title="Reports by Age Group", height=420,
                           showlegend=True, legend=LEG)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Reactions bar + Gender donut ──
    sh(f"Top {top_n} Adverse Reactions · Gender Split","","⚠️")
    col1,col2 = st.columns([3,2],gap="large")

    with col1:
        # VIOLET gradient — clearly different from gender colors
        tr = F['pt'].value_counts().head(top_n).reset_index()
        tr.columns = ['Reaction','Reports']
        fig3 = go.Figure(go.Bar(
            x=tr['Reports'], y=tr['Reaction'], orientation='h',
            marker=dict(color=tr['Reports'],colorscale=VIO,showscale=False,line=dict(width=0)),
            text=tr['Reports'].apply(lambda x:f'{x:,}'),
            textposition='outside', textfont=LBL,
            hovertemplate='<b>%{y}</b><br>%{x:,} reports<extra></extra>'
        ))
        fig3.update_layout(**BASE, title=f"Top {top_n} Adverse Reactions", height=420,
                           xaxis=dict(**AX,showgrid=True),
                           yaxis=dict(**AX,showgrid=False,categoryorder='total ascending'))
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        # Male = Sky Blue · Female = Pink — clearly distinct from reactions (violet)
        sx = F['sex'].value_counts().reset_index()
        sx.columns = ['Sex','Reports']
        gender_colors = {'Male':'#38BDF8','Female':'#F472B6'}
        sx_colors = [gender_colors.get(s,'#94A3B8') for s in sx['Sex']]

        fig4 = go.Figure(go.Pie(
            labels=sx['Sex'], values=sx['Reports'], hole=.52,
            marker=dict(colors=sx_colors, line=dict(color='#04080F',width=2)),
            textinfo='percent+label', textfont=dict(size=12,color='#F1F5F9'),
            hovertemplate='<b>%{label}</b><br>%{value:,} reports<br>%{percent}<extra></extra>'
        ))
        fig4.update_layout(**BASE, title="Reports by Gender", height=420, showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

    # ── Quarterly trend ──
    sh("Quarterly Reporting Trend","","📈")
    qorder = ['Q3 2025','Q4 2025','Q1 2026']
    trend = F.groupby('period').size().reset_index(name='Reports')
    trend['period'] = pd.Categorical(trend['period'],categories=qorder,ordered=True)
    trend = trend.sort_values('period')
    fig5 = go.Figure(go.Bar(
        x=trend['period'], y=trend['Reports'], width=.38,
        marker=dict(color=['#075985','#0369A1','#0EA5E9'],line=dict(width=0)),
        text=trend['Reports'].apply(lambda x:f'{x:,}'),
        textposition='outside', textfont=dict(color='#94A3B8',size=13,family='JetBrains Mono'),
        hovertemplate='<b>%{x}</b><br>%{y:,}<extra></extra>'
    ))
    fig5.update_layout(**BASE, title="Total Reports by Quarter", height=300,
                       xaxis=dict(**AX,showgrid=False),
                       yaxis=dict(**AX,showgrid=True))
    st.plotly_chart(fig5, use_container_width=True)

    # ── Heatmap — x-axis age groups colored to match the pie chart legend ──
    sh("Drug Reports by Age Group","Each color = one age group · same colors as legend above","🎨")

    top15 = F['drugname'].value_counts().head(15).index.tolist()
    heat  = (F[F['drugname'].isin(top15)]
             .groupby(['drugname','age_group']).size().reset_index(name='Reports'))
    pivot = heat.pivot(index='drugname',columns='age_group',values='Reports').fillna(0)
    col_order = [a for a in AGE_ORDER if a in pivot.columns]
    pivot = pivot[col_order]
    # Sort by total reports
    pivot = pivot.loc[pivot.sum(axis=1).sort_values().index]

    fig6 = go.Figure()
    for age in col_order:
        fig6.add_trace(go.Bar(
            name=age,
            y=pivot.index.tolist(),
            x=pivot[age].tolist(),
            orientation='h',
            marker=dict(color=AGE_COLORS[age], opacity=0.88, line=dict(width=0)),
            hovertemplate='<b>%{y}</b><br>' + age + ': %{x:,.0f} reports<extra></extra>'
        ))

    fig6.update_layout(**BASE)
    fig6.update_layout(
        title="Top 15 Drugs · Reports by Age Group (Stacked)",
        barmode='stack',
        height=520,
        margin=dict(t=44, b=60, l=8, r=8),
        showlegend=True,
        legend=dict(
            bgcolor='rgba(0,0,0,0)', orientation='h',
            x=0.5, xanchor='center', y=-0.12,
            font=dict(color='#94A3B8', size=12)
        ),
        xaxis=dict(**AX, showgrid=True, title_text='Number of Reports'),
        yaxis=dict(**AX, showgrid=False)
    )
    st.plotly_chart(fig6, use_container_width=True)


# ════════════════════════════════════════════════════════════════
# TAB 2 · DRUG SAFETY SEARCH
# ════════════════════════════════════════════════════════════════
with t2:
    sh("Drug Safety Search","Type any drug name to get its complete adverse event profile","🔍")
    st.markdown("""
    <div style="padding:14px 18px;background:rgba(14,165,233,.05);
                border:1px solid rgba(14,165,233,.15);border-radius:9px;margin-bottom:18px">
      <div style="font-size:12px;color:#94A3B8;line-height:1.7">
        Search any drug from the FDA AEMS database (Q3 2025 – Q1 2026). Results include
        total reports, top reactions, age distribution, quarterly trend and risk classification.
      </div>
    </div>""", unsafe_allow_html=True)

    query = st.text_input("",
        placeholder="Type a drug name — e.g.  ASPIRIN  ·  METFORMIN  ·  OZEMPIC  ·  HUMIRA",
        label_visibility="collapsed")

    if query:
        q_up    = query.strip().upper()
        matches = sorted([d for d in DF['drugname'].unique() if q_up in d])
        if not matches:
            st.markdown(f"""
            <div style="padding:22px;background:rgba(244,63,94,.06);border:1px solid rgba(244,63,94,.15);
                        border-radius:10px;text-align:center">
              <div style="font-size:15px;color:#F43F5E;font-weight:600;margin-bottom:6px">No results</div>
              <div style="font-size:12px;color:#64748B">
                "<b style='color:#CBD5E1'>{query}</b>" not found.
                Try a generic name or partial spelling.
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            sel  = st.selectbox(f"{len(matches)} match(es) found:", matches)
            ddf  = DF[DF['drugname']==sel]
            vc   = DF['drugname'].value_counts()
            p95,p75,p50 = vc.quantile(.95),vc.quantile(.75),vc.quantile(.50)
            tot  = len(ddf)
            risk = get_risk(tot,p95,p75,p50)

            st.markdown(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;
                        padding:16px 20px;background:#0B1524;border:1px solid #203552;
                        border-radius:11px;margin:16px 0">
              <div>
                <div style="font-size:10px;color:#334155;letter-spacing:.09em;
                            text-transform:uppercase;font-weight:600;margin-bottom:5px">Drug</div>
                <div style="font-size:19px;font-weight:700;color:#F1F5F9;
                            font-family:'JetBrains Mono',monospace">{sel}</div>
              </div>
              <div style="text-align:center">
                <div style="font-size:10px;color:#334155;letter-spacing:.09em;
                            text-transform:uppercase;font-weight:600;margin-bottom:6px">Risk Level</div>
                {risk_pill(risk)}
              </div>
              <div style="text-align:right">
                <div style="font-size:10px;color:#334155;letter-spacing:.09em;
                            text-transform:uppercase;font-weight:600;margin-bottom:5px">Total Reports</div>
                <div style="font-size:19px;font-weight:700;color:#0EA5E9;
                            font-family:'JetBrains Mono',monospace">{tot:,}</div>
              </div>
            </div>""", unsafe_allow_html=True)

            c1,c2,c3,c4 = st.columns(4)
            mn = len(ddf[ddf['sex']=='Male'])
            fn = len(ddf[ddf['sex']=='Female'])
            with c1: kpi("Total Reports",    f"{tot:,}",               "Adverse events","sky","📋")
            with c2: kpi("Unique Reactions", f"{ddf['pt'].nunique():,}","Distinct reactions","vio","⚠️")
            with c3: kpi("Male Reports",     f"{mn:,}", f"{round(mn/max(tot,1)*100,1)}% of total","sky","👨")
            with c4: kpi("Female Reports",   f"{fn:,}", f"{round(fn/max(tot,1)*100,1)}% of total","pnk","👩")

            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            col1,col2 = st.columns(2,gap="large")

            with col1:
                sh(f"Top Reactions","","⚠️")
                tr2 = ddf['pt'].value_counts().head(12).reset_index()
                tr2.columns=['Reaction','Reports']
                fig = go.Figure(go.Bar(
                    x=tr2['Reports'],y=tr2['Reaction'],orientation='h',
                    marker=dict(color=tr2['Reports'],colorscale=VIO,showscale=False,line=dict(width=0)),
                    text=tr2['Reports'].apply(lambda x:f'{x:,}'),
                    textposition='outside',textfont=LBL,
                    hovertemplate='<b>%{y}</b><br>%{x:,}<extra></extra>'
                ))
                fig.update_layout(**BASE,title="Top 12 Adverse Reactions",height=380,
                                  xaxis=dict(**AX,showgrid=True),
                                  yaxis=dict(**AX,showgrid=False,categoryorder='total ascending'))
                st.plotly_chart(fig,use_container_width=True)

            with col2:
                sh(f"Age Distribution","","👥")
                ag2_counts = ddf['age_group'].value_counts()
                ag2_labels = [a for a in AGE_ORDER if a in ag2_counts.index]
                ag2_values = [ag2_counts.get(a,0) for a in ag2_labels]
                ag2_colors = [AGE_COLORS[a] for a in ag2_labels]
                fig2 = go.Figure(go.Pie(
                    labels=ag2_labels,values=ag2_values,hole=.50,
                    marker=dict(colors=ag2_colors,line=dict(color='#04080F',width=2)),
                    textinfo='percent',textfont=dict(size=12,color='#F1F5F9'),
                    hovertemplate='<b>%{label}</b><br>%{value:,}<br>%{percent}<extra></extra>',
                    sort=False
                ))
                fig2.update_layout(**BASE,title="Age Group Breakdown",height=380,
                                   showlegend=True,legend=LEG)
                st.plotly_chart(fig2,use_container_width=True)

            sh(f"Quarterly Trend","","📈")
            qt = ddf.groupby('period').size().reset_index(name='Reports')
            qt['period'] = pd.Categorical(qt['period'],categories=qorder,ordered=True)
            qt = qt.sort_values('period')
            fig3 = go.Figure(go.Bar(
                x=qt['period'],y=qt['Reports'],width=.35,
                marker=dict(color=['#075985','#0369A1','#0EA5E9'],line=dict(width=0)),
                text=qt['Reports'].apply(lambda x:f'{x:,}'),
                textposition='outside',textfont=dict(color='#94A3B8',size=12,family='JetBrains Mono'),
                hovertemplate='<b>%{x}</b><br>%{y:,}<extra></extra>'
            ))
            fig3.update_layout(**BASE,title="Reports by Quarter",height=280,
                               xaxis=dict(**AX,showgrid=False),
                               yaxis=dict(**AX,showgrid=True))
            st.plotly_chart(fig3,use_container_width=True)

            csv = ddf[['age','age_group','sex','period','pt']].rename(columns={
                'age':'Age','age_group':'Age Group','sex':'Sex',
                'period':'Quarter','pt':'Adverse Reaction'}).to_csv(index=False)
            st.download_button(f"⬇  Export {sel} Safety Report (.csv)",
                               csv,f"{sel.replace(' ','_')}_report.csv","text/csv")
    else:
        st.markdown("""
        <div style="text-align:center;padding:50px 20px">
          <div style="font-size:38px;margin-bottom:14px;opacity:.2">🔍</div>
          <div style="font-size:14px;font-weight:600;color:#334155;margin-bottom:7px">
            Type a drug name above to begin
          </div>
          <div style="font-size:12px;color:#1E3350">
            Try: ASPIRIN · METFORMIN · OZEMPIC · HUMIRA · KEYTRUDA · DUPIXENT
          </div>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# TAB 3 · DRUG COMPARISON
# ════════════════════════════════════════════════════════════════
with t3:
    sh("Drug Comparison","Compare two drugs side by side","⚡")
    top200 = DF['drugname'].value_counts().head(200).index.tolist()
    col1,col2 = st.columns(2,gap="large")
    with col1: drug_a = st.selectbox("Drug A",top200,index=0,key="da")
    with col2: drug_b = st.selectbox("Drug B",top200,index=1,key="db")

    if drug_a==drug_b:
        st.warning("Please select two different drugs.")
    else:
        da  = DF[DF['drugname']==drug_a]
        db  = DF[DF['drugname']==drug_b]
        vc2 = DF['drugname'].value_counts()
        p95b,p75b,p50b = vc2.quantile(.95),vc2.quantile(.75),vc2.quantile(.50)
        ra = get_risk(len(da),p95b,p75b,p50b)
        rb = get_risk(len(db),p95b,p75b,p50b)

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:14px 0">
          <div style="padding:15px 18px;background:#0B1524;border:1px solid #203552;border-radius:10px">
            <div style="font-size:10px;color:#334155;letter-spacing:.08em;
                        text-transform:uppercase;font-weight:600;margin-bottom:5px">Drug A</div>
            <div style="font-size:16px;font-weight:700;color:#38BDF8;
                        font-family:'JetBrains Mono',monospace;margin-bottom:8px">{drug_a}</div>
            <div style="display:flex;align-items:center;gap:10px">
              {risk_pill(ra)}<span style="font-size:12px;color:#94A3B8">{len(da):,} reports</span>
            </div>
          </div>
          <div style="padding:15px 18px;background:#0B1524;border:1px solid #203552;border-radius:10px">
            <div style="font-size:10px;color:#334155;letter-spacing:.08em;
                        text-transform:uppercase;font-weight:600;margin-bottom:5px">Drug B</div>
            <div style="font-size:16px;font-weight:700;color:#A78BFA;
                        font-family:'JetBrains Mono',monospace;margin-bottom:8px">{drug_b}</div>
            <div style="display:flex;align-items:center;gap:10px">
              {risk_pill(rb)}<span style="font-size:12px;color:#94A3B8">{len(db):,} reports</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        col1,col2 = st.columns(2,gap="large")
        with col1:
            sh(drug_a,"Top 10 adverse reactions","💊")
            ta = da['pt'].value_counts().head(10).reset_index()
            ta.columns=['Reaction','Reports']
            fig = go.Figure(go.Bar(
                x=ta['Reports'],y=ta['Reaction'],orientation='h',
                marker=dict(color='#38BDF8',opacity=.8,line=dict(width=0)),
                text=ta['Reports'].apply(lambda x:f'{x:,}'),
                textposition='outside',textfont=LBL,
                hovertemplate='<b>%{y}</b><br>%{x:,}<extra></extra>'
            ))
            fig.update_layout(**BASE,title=f"{drug_a} · Top 10 Reactions",height=360,
                              xaxis=dict(**AX,showgrid=True),
                              yaxis=dict(**AX,showgrid=False,categoryorder='total ascending'))
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            sh(drug_b,"Top 10 adverse reactions","💊")
            tb = db['pt'].value_counts().head(10).reset_index()
            tb.columns=['Reaction','Reports']
            fig2 = go.Figure(go.Bar(
                x=tb['Reports'],y=tb['Reaction'],orientation='h',
                marker=dict(color='#A78BFA',opacity=.8,line=dict(width=0)),
                text=tb['Reports'].apply(lambda x:f'{x:,}'),
                textposition='outside',textfont=LBL,
                hovertemplate='<b>%{y}</b><br>%{x:,}<extra></extra>'
            ))
            fig2.update_layout(**BASE,title=f"{drug_b} · Top 10 Reactions",height=360,
                               xaxis=dict(**AX,showgrid=True),
                               yaxis=dict(**AX,showgrid=False,categoryorder='total ascending'))
            st.plotly_chart(fig2,use_container_width=True)

        sh("Head-to-Head Metrics","","📊")
        metrics = {
            'Total Reports':    (len(da),len(db)),
            'Unique Reactions': (da['pt'].nunique(),db['pt'].nunique()),
            'Male %':  (round(len(da[da['sex']=='Male'])/max(len(da),1)*100,1),
                        round(len(db[db['sex']=='Male'])/max(len(db),1)*100,1)),
            'Female %':(round(len(da[da['sex']=='Female'])/max(len(da),1)*100,1),
                        round(len(db[db['sex']=='Female'])/max(len(db),1)*100,1)),
        }
        rows=""
        for m,(va,vb) in metrics.items():
            w  = "A" if va>=vb else "B"
            ha = "font-weight:700;color:#38BDF8" if w=="A" else "color:#475569"
            hb = "font-weight:700;color:#A78BFA" if w=="B" else "color:#475569"
            sa = f"{va:,}" if isinstance(va,int) else f"{va}%"
            sb = f"{vb:,}" if isinstance(vb,int) else f"{vb}%"
            rows+=f"""
            <tr>
              <td style="padding:10px 14px;color:#94A3B8;font-size:12px;border-bottom:1px solid #0A1220">{m}</td>
              <td style="padding:10px 14px;text-align:center;font-size:13px;
                         font-family:'JetBrains Mono',monospace;border-bottom:1px solid #0A1220;{ha}">{sa}</td>
              <td style="padding:10px 14px;text-align:center;font-size:13px;
                         font-family:'JetBrains Mono',monospace;border-bottom:1px solid #0A1220;{hb}">{sb}</td>
            </tr>"""
        st.markdown(f"""
        <table style="width:100%;border-collapse:collapse;background:#0B1524;
                      border:1px solid #203552;border-radius:10px;overflow:hidden">
          <thead><tr style="background:#070C17">
            <th style="padding:11px 14px;text-align:left;font-size:10px;color:#475569;
                       letter-spacing:.08em;text-transform:uppercase;font-weight:600;
                       border-bottom:1px solid #1A2D45">Metric</th>
            <th style="padding:11px 14px;text-align:center;font-size:10px;color:#38BDF8;
                       letter-spacing:.08em;text-transform:uppercase;font-weight:600;
                       border-bottom:1px solid #1A2D45">{drug_a}</th>
            <th style="padding:11px 14px;text-align:center;font-size:10px;color:#A78BFA;
                       letter-spacing:.08em;text-transform:uppercase;font-weight:600;
                       border-bottom:1px solid #1A2D45">{drug_b}</th>
          </tr></thead>
          <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# TAB 4 · HIGH RISK ALERTS
# ════════════════════════════════════════════════════════════════
with t4:
    sh("High Risk Drug Alerts","Drugs flagged by adverse event volume","🚨")
    st.markdown("""
    <div style="padding:13px 17px;background:rgba(244,63,94,.05);
                border:1px solid rgba(244,63,94,.14);border-radius:9px;margin-bottom:20px">
      <div style="font-size:12px;color:#94A3B8;line-height:1.8">
        Risk is calculated from each drug's report volume relative to the full database percentiles.&nbsp;
        <span style="color:#F43F5E;font-weight:600">CRITICAL</span> = top 5% &nbsp;·&nbsp;
        <span style="color:#F59E0B;font-weight:600">HIGH</span> = top 25% &nbsp;·&nbsp;
        <span style="color:#0EA5E9;font-weight:600">MEDIUM</span> = top 50% &nbsp;·&nbsp;
        <span style="color:#10B981;font-weight:600">LOW</span> = below median
      </div>
    </div>""", unsafe_allow_html=True)

    dv = F['drugname'].value_counts().reset_index()
    dv.columns=['Drug','Reports']
    p95r,p75r,p50r = dv['Reports'].quantile(.95),dv['Reports'].quantile(.75),dv['Reports'].quantile(.50)
    dv['Risk'] = dv['Reports'].apply(lambda x: get_risk(x,p95r,p75r,p50r))

    # Fast groupby — NOT per-drug loop which hangs on 5000+ drugs
    top_rxn = (F.groupby('drugname')['pt']
               .apply(lambda x: x.value_counts().index[0] if len(x)>0 else 'N/A')
               .to_dict())
    dv['Top Reaction'] = dv['Drug'].map(top_rxn).fillna('N/A')

    c1,c2,c3,c4 = st.columns(4)
    for col,lvl,color,icon in [
        (c1,'CRITICAL','pnk','🔴'),(c2,'HIGH','amb','🟠'),
        (c3,'MEDIUM','sky','🟡'),(c4,'LOW','grn','🟢')
    ]:
        with col: kpi(f"{lvl} Risk",f"{len(dv[dv['Risk']==lvl]):,}",f"{lvl.lower()} risk drugs",color,icon)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    lvl_config = [
        ('CRITICAL','#F43F5E','🔴','Highest severity — immediate attention'),
        ('HIGH',    '#F59E0B','🟠','Elevated report volume — monitor closely'),
        ('MEDIUM',  '#0EA5E9','🔵','Moderate report volume — routine monitoring'),
        ('LOW',     '#10B981','🟢','Low report volume — standard surveillance'),
    ]

    for lvl,color,icon,desc in lvl_config:
        subset = dv[dv['Risk']==lvl].head(20)
        cnt    = len(dv[dv['Risk']==lvl])
        if cnt == 0: continue
        with st.expander(f"{icon}  {lvl} RISK — {cnt:,} drugs total · showing top 20 · {desc}", expanded=(lvl in ['CRITICAL','HIGH'])):
            rows=""
            for i,(_, row) in enumerate(subset.iterrows(),1):
                rows+=f"""
                <tr>
                  <td style="padding:9px 14px;color:#475569;font-size:11px;border-bottom:1px solid #0A1220">{i:02d}</td>
                  <td style="padding:9px 14px;color:#E2E8F0;font-size:12px;font-weight:600;border-bottom:1px solid #0A1220">{row['Drug']}</td>
                  <td style="padding:9px 14px;text-align:right;color:{color};font-size:13px;font-weight:700;border-bottom:1px solid #0A1220">{int(row['Reports']):,}</td>
                  <td style="padding:9px 14px;border-bottom:1px solid #0A1220">{risk_pill(lvl)}</td>
                  <td style="padding:9px 14px;color:#94A3B8;font-size:11px;border-bottom:1px solid #0A1220">{row['Top Reaction']}</td>
                </tr>"""
            st.markdown(
                f'<table style="width:100%;border-collapse:collapse;background:#0B1524;border:1px solid #203552;border-radius:10px;overflow:hidden">'
                f'<thead><tr style="background:#070C17">'
                f'<th style="padding:9px 14px;text-align:left;font-size:10px;color:#475569;letter-spacing:.08em;text-transform:uppercase;border-bottom:1px solid #1A2D45">#</th>'
                f'<th style="padding:9px 14px;text-align:left;font-size:10px;color:#475569;letter-spacing:.08em;text-transform:uppercase;border-bottom:1px solid #1A2D45">Drug Name</th>'
                f'<th style="padding:9px 14px;text-align:right;font-size:10px;color:#475569;letter-spacing:.08em;text-transform:uppercase;border-bottom:1px solid #1A2D45">Reports</th>'
                f'<th style="padding:9px 14px;text-align:left;font-size:10px;color:#475569;letter-spacing:.08em;text-transform:uppercase;border-bottom:1px solid #1A2D45">Risk</th>'
                f'<th style="padding:9px 14px;text-align:left;font-size:10px;color:#475569;letter-spacing:.08em;text-transform:uppercase;border-bottom:1px solid #1A2D45">Top Reaction</th>'
                f'</tr></thead><tbody>' + rows + '</tbody></table>',
                unsafe_allow_html=True
            )

    st.download_button("⬇  Export Full Risk Report (.csv)",
                       dv.to_csv(index=False),"fda_risk_alerts.csv","text/csv")


# ════════════════════════════════════════════════════════════════
# TAB 5 · DATA EXPLORER  — root cause fix: Categorical → str
# ════════════════════════════════════════════════════════════════
with t5:
    sh("Public Safety Summary","What the FDA data shows — in plain language","📋")

    total   = len(F)
    n_drugs = F['drugname'].nunique()
    n_reac  = F['pt'].nunique()
    top_drug = F['drugname'].value_counts().index[0] if total>0 else 'N/A'
    top_reac = F['pt'].value_counts().index[0] if total>0 else 'N/A'
    top_age  = F['age_group'].value_counts().index[0] if total>0 else 'N/A'

    st.info(
        f"Between **Q3 2025 and Q1 2026**, the FDA received **{total:,}** adverse event reports "
        f"covering **{n_drugs:,}** unique drugs and **{n_reac:,}** distinct reactions. "
        f"The most reported drug was **{top_drug}** and the most common adverse reaction was **{top_reac}**. "
        f"The age group with the highest report volume was **{top_age}**."
    )

    # ── Top 10 Drugs & Reactions ──
    sh("Top 10 Most Reported Drugs & Reactions","Based on current filters","💊")
    col1, col2 = st.columns(2, gap="large")

    with col1:
        td10 = F['drugname'].value_counts().head(10).reset_index()
        td10.columns = ['Drug','Reports']
        fig_d = go.Figure(go.Bar(
            x=td10['Reports'], y=td10['Drug'], orientation='h',
            marker=dict(color=td10['Reports'], colorscale=SKY, showscale=False, line=dict(width=0)),
            text=td10['Reports'].apply(lambda x:f'{x:,}'),
            textposition='outside', textfont=LBL,
            hovertemplate='<b>%{y}</b><br>%{x:,} reports<extra></extra>'
        ))
        fig_d.update_layout(**BASE, title="Top 10 Drugs", height=380,
                            xaxis=dict(**AX, showgrid=True),
                            yaxis=dict(**AX, showgrid=False, categoryorder='total ascending'))
        st.plotly_chart(fig_d, use_container_width=True)

    with col2:
        tr10 = F['pt'].value_counts().head(10).reset_index()
        tr10.columns = ['Reaction','Reports']
        fig_r = go.Figure(go.Bar(
            x=tr10['Reports'], y=tr10['Reaction'], orientation='h',
            marker=dict(color=tr10['Reports'], colorscale=VIO, showscale=False, line=dict(width=0)),
            text=tr10['Reports'].apply(lambda x:f'{x:,}'),
            textposition='outside', textfont=LBL,
            hovertemplate='<b>%{y}</b><br>%{x:,} reports<extra></extra>'
        ))
        fig_r.update_layout(**BASE, title="Top 10 Adverse Reactions", height=380,
                            xaxis=dict(**AX, showgrid=True),
                            yaxis=dict(**AX, showgrid=False, categoryorder='total ascending'))
        st.plotly_chart(fig_r, use_container_width=True)

    # ── Who Is Most Affected ──
    sh("Who Is Most Affected","Age group and gender breakdown","👥")
    col1, col2 = st.columns(2, gap="large")

    with col1:
        ag_counts = F['age_group'].value_counts()
        ag_labels = [a for a in AGE_ORDER if a in ag_counts.index]
        ag_values = [int(ag_counts[a]) for a in ag_labels]
        ag_colors = [AGE_COLORS[a] for a in ag_labels]
        fig_age = go.Figure(go.Bar(
            x=ag_values, y=ag_labels,
            orientation='h',
            marker=dict(color=ag_colors, line=dict(width=0)),
            text=[f'{v:,}' for v in ag_values],
            textposition='outside', textfont=LBL,
            hovertemplate='<b>%{y}</b><br>%{x:,} reports<extra></extra>'
        ))
        fig_age.update_layout(**BASE, title="Reports by Age Group", height=320,
                              xaxis=dict(**AX, showgrid=True),
                              yaxis=dict(**AX, showgrid=False))
        st.plotly_chart(fig_age, use_container_width=True)

    with col2:
        male_n   = len(F[F['sex']=='Male'])
        female_n = len(F[F['sex']=='Female'])
        c1,c2 = st.columns(2)
        with c1: kpi("Male Reports",   f"{male_n:,}",   f"{round(male_n/max(total,1)*100,1)}% of total","sky","👨")
        with c2: kpi("Female Reports", f"{female_n:,}", f"{round(female_n/max(total,1)*100,1)}% of total","pnk","👩")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        fig_sex = go.Figure(go.Pie(
            labels=['Male','Female'],
            values=[male_n, female_n],
            hole=.52,
            marker=dict(colors=['#38BDF8','#F472B6'], line=dict(color='#04080F',width=2)),
            textinfo='percent+label', textfont=dict(size=13,color='#F1F5F9'),
            hovertemplate='<b>%{label}</b><br>%{value:,}<extra></extra>'
        ))
        fig_sex.update_layout(**BASE, title="Gender Split", height=280, showlegend=False)
        st.plotly_chart(fig_sex, use_container_width=True)

    # ── Download ──
    sh("Download the Data","Export the complete filtered dataset","⬇️")
    export = F[['age_group','sex','period','drugname','pt']].copy()
    export.columns = ['Age Group','Sex','Quarter','Drug Name','Adverse Reaction']
    export = export.astype(str)
    st.download_button(
        "⬇  Download Full Filtered Dataset (.csv)",
        export.to_csv(index=False),
        "fda_adverse_events.csv","text/csv"
    )



# ── FOOTER ──────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:48px;padding:16px 0;border-top:1px solid #0F1A2E;
            display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px">
  <div style="font-size:11px">
    <span style="color:#94A3B8;font-weight:500">Muhammad Uzair RPh (PharmD)</span>
    <span style="color:#1A2D45"> · University of Peshawar</span>
  </div>
  <div style="font-size:11px;color:#1A2D45">
    Source: <span style="color:#334155">FDA Adverse Event Monitoring System (AEMS) · Public Dataset</span>
  </div>
</div>
""", unsafe_allow_html=True)