import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# --- PAGE SETUP ---
st.set_page_config(page_title="Credit Risk Dashboard", layout="wide", page_icon="🏦")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stMetric {background-color: #f8f9fa; border-left: 5px solid #004b8d; padding: 10px; border-radius: 5px;}
    h1 {color: #004b8d;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: INPUTS (Defaults set to generate Score 4.55) ---
st.sidebar.header("⚙️ Simulation Parameters")
s_fin = st.sidebar.slider("Financial Strength (25%)", 0.0, 10.0, 8.0)    # Strong but rising debt
s_ind = st.sidebar.slider("Industry/Predictive (20%)", 0.0, 10.0, 6.0)   # Grey Zone Z-Score
s_mgt = st.sidebar.slider("Mgmt & Forensic (15%)", 0.0, 10.0, 7.0)       # Margin Pressure
s_col = st.sidebar.slider("Collateral (25%)", 0.0, 10.0, 0.0)            # UNSECURED (0)
s_str = st.sidebar.slider("Strategic Fit (15%)", 0.0, 10.0, 2.0)         # Mismatch

# Calculate Weighted Score
score = (s_fin * 0.25) + (s_ind * 0.20) + (s_mgt * 0.15) + (s_col * 0.25) + (s_str * 0.15)

# Decision Logic
if score >= 7.5:
    status, color, bg, icon, msg = "APPROVED", "#28a745", "#e8f5e9", "✅", "Meets all risk criteria."
elif score >= 5.0:
    status, color, bg, icon, msg = "REVIEW", "#ffc107", "#fff3e0", "⚠️", "Requires collateral/covenants."
else:
    status, color, bg, icon, msg = "REJECT", "#dc3545", "#ffebee", "❌", "High Risk: Unsecured & Low Strategic Fit."

# --- HEADER: LOGOS & TITLE ---
c1, c2, c3 = st.columns([1, 4, 1])
with c1: st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Bandhan_Bank_Logo.svg/1200px-Bandhan_Bank_Logo.svg.png", width=120)
with c2: 
    st.markdown(f"<h1 style='text-align: center;'>Credit Evaluation Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; color: gray;'>Proposal: ₹1,415 Cr Unsecured Term Loan</h4>", unsafe_allow_html=True)
with c3: st.image("https://upload.wikimedia.org/wikipedia/commons/2/25/Jindal_Steel_%26_Power_Logo.jpg", width=120)
st.markdown("---")

# --- SECTION 1: SCORE & DECISION ---
col_L, col_R = st.columns([1, 1.5])

# LEFT: Riskometer
with col_L:
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=score,
        title={'text': "<b>AI CREDIT SCORE</b>"},
        gauge={'axis': {'range': [None, 10]}, 'bar': {'color': color}, 
               'steps': [{'range': [0, 5], 'color': "#ffebee"}, {'range': [5, 7.5], 'color': "#fff3e0"}, {'range': [7.5, 10], 'color': "#e8f5e9"}],
               'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 7.5}}))
    fig.update_layout(height=250, margin=dict(l=20,r=20,t=30,b=20))
    st.plotly_chart(fig, use_container_width=True)

# RIGHT: Rational Card
with col_R:
    st.markdown(f"""
    <div style="background-color: {bg}; padding: 20px; border-radius: 15px; border: 2px solid {color}; text-align: center; margin-top: 10px;">
        <h2 style="color: {color}; margin:0;">{icon} {status}</h2>
        <h1 style="font-size: 3.5em; margin: 0;">{score:.2f} <span style="font-size: 0.3em; color: gray;">/ 10</span></h1>
        <hr style="border-top: 1px solid {color};">
        <p style="font-size: 1.2em; font-weight: 500; color: #333;">Rationale: {msg}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- SECTION 2: KEY METRICS & GRAPHS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Net Debt / EBITDA", "1.48x", "Worsening", delta_color="inverse")
m2.metric("Altman Z-Score", "2.92", "Grey Zone", delta_color="off")
m3.metric("Ohlson O-Score", "< 1%", "Safe", delta_color="normal")
m4.metric("Strategic Fit", "Low", "Mismatch", delta_color="inverse")

# Graphs
g1, g2 = st.columns(2)
with g1:
    st.markdown("**1. Financial Trend: Debt Rising**")
    df_trend = pd.DataFrame({'Year': ['FY23', 'FY24', 'FY25'], 'Debt': [9500, 10200, 14156], 'EBITDA': [11000, 12500, 9500]})
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=df_trend['Year'], y=df_trend['EBITDA'], name='EBITDA', marker_color='#004b8d', opacity=0.6))
    fig1.add_trace(go.Scatter(x=df_trend['Year'], y=df_trend['Debt'], name='Net Debt', line=dict(color='red', width=3)))
    fig1.update_layout(height=300, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig1, use_container_width=True)

with g2:
    st.markdown("**2. Risk Component Analysis**")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatterpolar(r=[s_fin, s_ind, s_mgt, s_col, s_str], theta=['Financial', 'Industry', 'Mgmt', 'Collateral', 'Strategy'], fill='toself', name='Actual'))
    fig2.add_trace(go.Scatterpolar(r=[8, 8, 8, 10, 8], theta=['Financial', 'Industry', 'Mgmt', 'Collateral', 'Strategy'], name='Ideal', line_dash='dot'))
    fig2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), height=300, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig2, use_container_width=True)
