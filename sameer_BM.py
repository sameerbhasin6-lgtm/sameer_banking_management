import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Bandhan Bank Credit Committee | JSPL Evaluation",
    page_icon="🏦",
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .block-container {padding-top: 1rem;}
    .stMetric {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #004b8d;
    }
    .decision-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SIMULATION CONTROLS ---
st.sidebar.header("⚙️ Score Simulator")
st.sidebar.markdown("Adjust inputs to simulate committee voting:")

score_financial = st.sidebar.slider("Financial Strength (30%)", 0.0, 10.0, 8.0)
score_industry = st.sidebar.slider("Industry Outlook (20%)", 0.0, 10.0, 6.0)
score_management = st.sidebar.slider("Management Quality (15%)", 0.0, 10.0, 8.0)
score_collateral = st.sidebar.slider("Collateral / Security (20%)", 0.0, 10.0, 0.0) 
score_strategy = st.sidebar.slider("Strategic Fit (15%)", 0.0, 10.0, 2.0)

# Weights
w_fin, w_ind, w_mgt, w_col, w_str = 0.30, 0.20, 0.15, 0.20, 0.15
total_score = (score_financial * w_fin) + (score_industry * w_ind) + \
              (score_management * w_mgt) + (score_collateral * w_col) + (score_strategy * w_str)

# Decision Logic & Rationale
if total_score >= 7.5:
    decision = "APPROVED"
    color = "#28a745" # Green
    bg_color = "#e8f5e9"
    rationale = "Proposal meets all risk acceptance criteria."
    icon = "✅"
elif total_score >= 5.0:
    decision = "REVIEW / CAUTION"
    color = "#ffc107" # Amber
    bg_color = "#fff3e0"
    rationale = "Marginal score; requires additional Collateral or Covenants."
    icon = "⚠️"
else:
    decision = "REJECT"
    color = "#dc3545" # Red
    bg_color = "#ffebee"
    rationale = "Critical structural mismatch (Unsecured) & rising leverage risks."
    icon = "❌"

# --- TOP SECTION: LOGOS & TITLE ---
col_logo1, col_title, col_logo2 = st.columns([1, 4, 1])

with col_logo1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Bandhan_Bank_Logo.svg/1200px-Bandhan_Bank_Logo.svg.png", use_container_width=True)

with col_title:
    st.markdown("<h1 style='text-align: center; color: #004b8d;'>Credit Evaluation Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Borrower: Jindal Steel & Power (JSPL) | Request: ₹1,415 Cr Unsecured</h4>", unsafe_allow_html=True)

with col_logo2:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/25/Jindal_Steel_%26_Power_Logo.jpg", use_container_width=True)

st.markdown("---")

# --- SECTION 1: SPLIT VIEW (GAUGE LEFT | DECISION RIGHT) ---
col_left, col_right = st.columns([1, 1.5])

# LEFT SIDE: RISKOMETER (GAUGE)
with col_left:
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = total_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "<b>AI CREDIT SCORE</b>"},
        gauge = {
            'axis': {'range': [None, 10], 'tickwidth': 1},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 5], 'color': "#ffebee"},
                {'range': [5, 7.5], 'color': "#fff3e0"},
                {'range': [7.5, 10], 'color': "#e8f5e9"}],
            'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 7.5}}))
    
    fig_gauge.update_layout(height=280, margin=dict(l=20,r=20,t=30,b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

# RIGHT SIDE: DECISION & RATIONALE
with col_right:
    # Using HTML/CSS for a clean "Card" look
    st.markdown(f"""
    <div style="
        background-color: {bg_color}; 
        padding: 30px; 
        border-radius: 15px; 
        border: 2px solid {color};
        text-align: center;
        margin-top: 20px;">
        <h2 style="color: {color}; margin:0;">{icon} {decision}</h2>
        <h1 style="font-size: 3em; margin: 10px 0;">{total_score:.2f} <span style="font-size: 0.4em; color: gray;">/ 10</span></h1>
        <hr style="border-top: 1px solid {color};">
        <h4 style="color: #333;">Rationale:</h4>
        <p style="font-size: 1.2em; font-weight: 500;">{rationale}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- SECTION 2: KEY METRICS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Net Debt / EBITDA", "1.48x", "0.68x (Worsening)", delta_color="inverse")
m2.metric("Altman Z-Score", "2.92", "Grey Zone", delta_color="off")
m3.metric("Ohlson O-Score", "< 1%", "Low Default Prob.", delta_color="normal")
m4.metric("Strategic Fit", "Low", "Unsecured Mismatch", delta_color="inverse")

st.markdown("---")

# --- SECTION 3: DETAILED GRAPHS ---
st.subheader("📈 Quantitative & Strategic Analysis")

g1, g2 = st.columns(2)

# GRAPH 1: Financial Trend
with g1:
    st.markdown("**1. JSPL Financial Trend: Debt is Rising**")
    data_trend = pd.DataFrame({
        'Year': ['FY23', 'FY24', 'FY25', 'Q2 FY26 (Ann.)'],
        'Net Debt (Cr)': [9500, 10200, 12500, 14156],
        'EBITDA (Cr)': [11000, 12500, 11800, 9500]
    })
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=data_trend['Year'], y=data_trend['Net Debt (Cr)'], name='Net Debt', line=dict(color='red', width=3)))
    fig_trend.add_trace(go.Bar(x=data_trend['Year'], y=data_trend['EBITDA (Cr)'], name='EBITDA', marker_color='#004b8d', opacity=0.6))
    fig_trend.update_layout(barmode='overlay', height=350, legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig_trend, use_container_width=True)

# GRAPH 2: Peer Comparison
with g2:
    st.markdown("**2. Leverage Comparison (Net Debt/EBITDA)**")
    data_peer = pd.DataFrame({
        'Company': ['JSPL', 'Tata Steel', 'JSW Steel'],
        'Leverage Ratio': [1.48, 2.50, 2.80],
    })
    fig_peer = px.bar(data_peer, x='Company', y='Leverage Ratio', color='Company', 
                      color_discrete_map={'JSPL':'#28a745', 'Tata Steel':'#6c757d', 'JSW Steel':'#6c757d'},
                      text='Leverage Ratio')
    fig_peer.update_traces(texttemplate='%{text}x', textposition='outside')
    fig_peer.update_layout(showlegend=False, height=350, yaxis=dict(range=[0, 3.5]))
    st.plotly_chart(fig_peer, use_container_width=True)

g3, g4 = st.columns(2)

# GRAPH 3: Radar Chart
with g3:
    st.markdown("**3. Risk Component Analysis**")
    categories = ['Financials', 'Industry', 'Management', 'Collateral', 'Strategy']
    values = [score_financial, score_industry, score_management, score_collateral, score_strategy]
    ideal = [8, 8, 8, 10, 8]
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=values, theta=categories, fill='toself', name='Current Proposal', line_color='red'))
    fig_radar.add_trace(go.Scatterpolar(r=ideal, theta=categories, name='Ideal Profile', line_color='green', line_dash='dot'))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), height=350, showlegend=True, legend=dict(orientation="h", y=-0.1))
    st.plotly_chart(fig_radar, use_container_width=True)

# GRAPH 4: Strategic Mismatch
with g4:
    st.markdown("**4. Bandhan Bank Strategic Fit**")
    labels = ['Secured (Target)', 'Unsecured (Avoiding)']
    values = [60, 40] 
    fig_donut = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker_colors=['#004b8d', '#dc3545'])])
    fig_donut.update_layout(annotations=[dict(text='Bank\nStrategy', x=0.5, y=0.5, font_size=15, showarrow=False)], height=350, showlegend=True)
    st.plotly_chart(fig_donut, use_container_width=True)
