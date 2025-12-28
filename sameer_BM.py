import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# --- 1. PAGE CONFIG (Must be the very first command) ---
st.set_page_config(
    page_title="Credit Assessment: JSPL",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CACHE CLEARING UTILITY ---
# If the dashboard feels stuck, the user can click this button
if st.sidebar.button("🔄 Reset / Clear Cache"):
    st.cache_data.clear()
    st.rerun()

# --- 3. CUSTOM CSS FOR COMPACT STYLING ---
st.markdown("""
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    h1 {font-size: 2.2rem !important; margin-bottom: 0px;}
    h4 {font-size: 1.1rem !important; font-weight: 400; color: #555;}
    .stMetric {background-color: #f8f9fa; border-left: 4px solid #004b8d; padding: 8px; border-radius: 5px;}
    /* Card Styling for Decision */
    .decision-card {
        padding: 15px; border-radius: 10px; text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR INPUTS (Defaulted to Score 4.55 - REJECT) ---
st.sidebar.header("⚙️ Evaluation Parameters")

# Sliders set to specific values to generate the 4.55 score
s_fin = st.sidebar.slider("Financial Strength (25%)", 0, 10, 8)     # 8 * 0.25 = 2.00
s_ind = st.sidebar.slider("Industry/Models (20%)", 0, 10, 6)        # 6 * 0.20 = 1.20
s_mgt = st.sidebar.slider("Mgmt & Forensic (15%)", 0, 10, 7)        # 7 * 0.15 = 1.05
s_col = st.sidebar.slider("Collateral (25%)", 0, 10, 0)             # 0 * 0.25 = 0.00 (CRITICAL MISS)
s_str = st.sidebar.slider("Strategic Fit (15%)", 0, 10, 2)          # 2 * 0.15 = 0.30

# Weighted Calculation
score = (s_fin * 0.25) + (s_ind * 0.20) + (s_mgt * 0.15) + (s_col * 0.25) + (s_str * 0.15)

# Decision Logic
if score >= 7.5:
    status = "APPROVED"
    color = "#28a745" # Green
    bg_color = "#e8f5e9"
    icon = "✅"
    rationale = "Meets all risk criteria."
elif score >= 5.0:
    status = "REVIEW"
    color = "#ffc107" # Amber
    bg_color = "#fff3e0"
    icon = "⚠️"
    rationale = "Marginal. Needs Collateral."
else:
    status = "REJECT"
    color = "#dc3545" # Red
    bg_color = "#ffebee"
    icon = "⛔"
    rationale = "High Risk: Unsecured Structure & Strategy Mismatch."

# --- 5. HEADER SECTION (Logos) ---
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    # Bandhan Bank Logo
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Bandhan_Bank_Logo.svg/1200px-Bandhan_Bank_Logo.svg.png", width=130)

with col2:
    st.markdown(f"<h1 style='text-align: center; color: #004b8d;'>Credit Evaluation Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center;'>Borrower: Jindal Steel & Power | Proposal: ₹1,415 Cr (Unsecured)</h4>", unsafe_allow_html=True)

with col3:
    # JSPL Logo
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/25/Jindal_Steel_%26_Power_Logo.jpg", width=130)

st.markdown("---")

# --- 6. SPLIT LAYOUT (Riskometer LEFT | Rationale RIGHT) ---
left_col, right_col = st.columns([1, 1.2])

# LEFT: Compact Riskometer
with left_col:
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "<b>AI CREDIT SCORE</b>", 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [None, 10]},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 5], 'color': "#ffebee"},
                {'range': [5, 7.5], 'color': "#fff3e0"},
                {'range': [7.5, 10], 'color': "#e8f5e9"}
            ],
            'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 7.5}
        }
    ))
    fig_gauge.update_layout(height=220, margin=dict(l=30, r=30, t=30, b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

# RIGHT: Decision Card
with right_col:
    st.markdown(f"""
    <div class="decision-card" style="background-color: {bg_color}; border: 2px solid {color};">
        <h3 style="color: {color}; margin: 0; font-weight: 800;">{icon} {status}</h3>
        <hr style="margin: 10px 0; border-top: 1px solid {color}; opacity: 0.3;">
        <p style="font-size: 1.1rem; color: #333; margin: 0;"><b>Rationale:</b> {rationale}</p>
        <p style="font-size: 0.9rem; color: #666; margin-top: 5px;">Score: <b>{score:.2f}</b> / 10.0</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- 7. METRICS & COMPACT GRAPHS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Net Debt / EBITDA", "1.48x", "Worsening", delta_color="inverse")
m2.metric("Altman Z-Score", "2.92", "Grey Zone", delta_color="off")
m3.metric("Ohlson O-Score", "< 1%", "Safe", delta_color="normal")
m4.metric("Strategic Fit", "Low", "Mismatch", delta_color="inverse")

g1, g2 = st.columns(2)

# Graph 1: Debt Trend (Smaller Height)
with g1:
    st.markdown("**1. Financial Trend: Rising Debt**")
    df_trend = pd.DataFrame({'Year': ['FY23', 'FY24', 'FY25'], 'Debt': [9500, 10200, 14156], 'EBITDA': [11000, 12500, 9500]})
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(x=df_trend['Year'], y=df_trend['EBITDA'], name='EBITDA', marker_color='#004b8d', opacity=0.5))
    fig_trend.add_trace(go.Scatter(x=df_trend['Year'], y=df_trend['Debt'], name='Net Debt', line=dict(color='red', width=3)))
    fig_trend.update_layout(height=250, margin=dict(t=20, b=20, l=20, r=20), legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig_trend, use_container_width=True)

# Graph 2: Risk Radar (Smaller Height)
with g2:
    st.markdown("**2. Risk Gap Analysis**")
    categories = ['Financial', 'Industry', 'Mgmt', 'Collateral', 'Strategy']
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=[s_fin, s_ind, s_mgt, s_col, s_str], theta=categories, fill='toself', name='Actual', line_color=color))
    fig_radar.add_trace(go.Scatterpolar(r=[8, 8, 8, 10, 8], theta=categories, name='Ideal', line_color='green', line_dash='dot'))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), height=250, margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
    st.plotly_chart(fig_radar, use_container_width=True)
