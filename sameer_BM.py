import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Bandhan Bank | Credit Risk Dashboard",
    page_icon="🏦",
    layout="wide"
)

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SIMULATION CONTROLS ---
st.sidebar.header("⚙️ Credit Score Simulator")
st.sidebar.markdown("Adjust the parameters to see how the decision changes.")

# Input Sliders for the 5 Key Dimensions (Defaulted to JSPL Analysis)
score_financial = st.sidebar.slider("Financial Strength (30%)", 0.0, 10.0, 8.0)
score_industry = st.sidebar.slider("Industry Outlook (20%)", 0.0, 10.0, 6.0)
score_management = st.sidebar.slider("Management Quality (15%)", 0.0, 10.0, 8.0)
score_collateral = st.sidebar.slider("Collateral / Security (20%)", 0.0, 10.0, 0.0) # Default 0 for Unsecured
score_strategy = st.sidebar.slider("Strategic Fit (15%)", 0.0, 10.0, 2.0)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Try increasing 'Collateral' to 10 to see if the loan gets approved.")

# --- CALCULATION ENGINE ---
# Weights based on the report
w_fin, w_ind, w_mgt, w_col, w_str = 0.30, 0.20, 0.15, 0.20, 0.15

# Calculate Weighted Score
total_score = (
    (score_financial * w_fin) +
    (score_industry * w_ind) +
    (score_management * w_mgt) +
    (score_collateral * w_col) +
    (score_strategy * w_str)
)

# Determine Recommendation
if total_score >= 7.5:
    decision = "APPROVED"
    color = "green"
elif total_score >= 5.0:
    decision = "REVIEW / CAUTION"
    color = "orange"
else:
    decision = "REJECT"
    color = "red"

# --- MAIN DASHBOARD LAYOUT ---

# Header Section
c1, c2 = st.columns([1, 5])
with c1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Bandhan_Bank_Logo.svg/1200px-Bandhan_Bank_Logo.svg.png", width=100) # Placeholder logo logic
with c2:
    st.title("Credit Evaluation: Jindal Steel & Power (JSPL)")
    st.markdown(f"**Facility:** Unsecured Term Loan | **Amount:** ₹1,415 Cr")

st.markdown("---")

# Row 1: Key Financial Metrics (Static Data for JSPL)
st.subheader("📊 Key Risk Indicators (Q2 FY26)")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(label="Net Debt / EBITDA", value="1.48x", delta="0.68x (YoY)", delta_color="inverse")
with kpi2:
    st.metric(label="Altman Z-Score", value="2.92", delta="Grey Zone", delta_color="off")
with kpi3:
    st.metric(label="Ohlson O-Score (Prob. Default)", value="< 1%", delta="Low Risk", delta_color="normal")
with kpi4:
    st.metric(label="Beneish M-Score (GMI)", value="> 1.0", delta="Margin Pressure", delta_color="inverse")

st.markdown("---")

# Row 2: Visualizations
col_gauge, col_radar = st.columns([1, 1])

with col_gauge:
    st.subheader("Credit Decision Engine")
    
    # Plotly Gauge Chart
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = total_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Final Credit Score<br><span style='font-size:0.8em;color:{color}'>{decision}</span>"},
        delta = {'reference': 7.5, 'increasing': {'color': "green"}},
        gauge = {
            'axis': {'range': [None, 10]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 5], 'color': "#ffcccb"},  # Red zone
                {'range': [5, 7.5], 'color': "#ffe4b5"}, # Orange zone
                {'range': [7.5, 10], 'color': "#90ee90"} # Green zone
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': 7.5
            }
        }
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

    # Text Explanation
    if decision == "REJECT":
        st.error(f"❌ **Action:** {decision}. The score of {total_score:.2f} is below the approval threshold of 7.5.")
    elif decision == "APPROVED":
        st.success(f"✅ **Action:** {decision}. The proposal meets the bank's risk acceptance criteria.")
    else:
        st.warning(f"⚠️ **Action:** {decision}. Additional collateral or covenants required.")

with col_radar:
    st.subheader("Risk Component Analysis")
    
    # Plotly Radar Chart
    categories = ['Financial Strength', 'Industry Outlook', 'Management Quality', 'Collateral', 'Strategic Fit']
    values = [score_financial, score_industry, score_management, score_collateral, score_strategy]
    
    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='JSPL Score',
        line_color='blue'
    ))
    
    # Add a "Benchmark" line (Ideal Candidate)
    fig_radar.add_trace(go.Scatterpolar(
        r=[8, 8, 8, 10, 8],
        theta=categories,
        name='Ideal Threshold',
        line_color='green',
        line_dash='dot'
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=True
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# --- ADVANCED METRICS EXPLAINER ---
with st.expander("📚 View Detailed Methodology for Advanced Models"):
    st.markdown("""
    ### 1. Altman Z-Score (Manufacturing)
    Used to predict bankruptcy risk.
    * **Formula:** $1.2A + 1.4B + 3.3C + 0.6D + 1.0E$
    * **Current Score:** **2.92** (Grey Zone)
    * *Implication:* The company is safe today but vulnerable to cyclical downturns.

    ### 2. Ohlson O-Score
    Uses logistic regression to estimate Probability of Default (PD).
    * **Result:** **< 1%**
    * *Implication:* JSPL is "Too Big To Fail" in the immediate term, but this does not guarantee repayment of unsecured debt.
    
    ### 3. Beneish M-Score
    Forensic accounting tool to detect earnings manipulation.
    * **Red Flag:** **Gross Margin Index (GMI) > 1**
    * *Implication:* Margins are deteriorating, increasing the temptation to manipulate earnings.
    """)