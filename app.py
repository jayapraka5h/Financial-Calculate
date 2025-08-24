import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# ------------------ Financial Logic ------------------

def calculate_sip(monthly_investment, annual_rate, years):
    months = int(years * 12)
    monthly_rate = annual_rate / 12 / 100
    future_value = sum([
        monthly_investment * ((1 + monthly_rate) ** (months - i))
        for i in range(months)
    ])
    invested = monthly_investment * months
    returns = future_value - invested
    return round(invested, 2), round(returns, 2), round(future_value, 2)

# ------------------ Chart Generator ------------------

def pie_chart(labels, values):
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="Financial Calculator", layout="wide")

# Inject CSS for fixed-height layout
st.markdown("""
    <style>
    .flex-container {
        display: flex;
        gap: 2rem;
        margin-top: 20px;
    }
    .flex-child {
        flex: 1;
        min-height: 420px;
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>💸 SIP Calculator</h1>", unsafe_allow_html=True)

# Input fields
st.markdown('<div class="flex-container">', unsafe_allow_html=True)
st.markdown('<div class="flex-child">', unsafe_allow_html=True)

mi = st.number_input("Monthly Investment (₹)", min_value=0.0, step=0.01, format="%.2f")
rate = st.number_input("Expected Annual Return (%)", min_value=0.0, step=0.01, format="%.2f")
years = st.number_input("Investment Duration (Years)", min_value=0.0, step=0.01, format="%.2f")
calculate = st.button("Calculate SIP")

st.markdown('</div>', unsafe_allow_html=True)

# Chart section
st.markdown('<div class="flex-child">', unsafe_allow_html=True)
if calculate:
    invested, returns, total = calculate_sip(mi, rate, years)
    pie_chart(["Invested", "Returns"], [invested, returns])
else:
    st.markdown("Pie chart will appear here after calculation.")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Results table
if calculate:
    st.markdown("### 📋 Results Summary")
    df = pd.DataFrame({
        "Description": [
            "Monthly Investment (₹)",
            "Expected Annual Return (%)",
            "Investment Duration (Years)",
            "Total Invested (₹)",
            "Returns Earned (₹)",
            "Total Value (₹)"
        ],
        "Value": [
            f"{mi:,.2f}",
            f"{rate:,.2f}",
            f"{years:,.2f}",
            f"{invested:,.0f}",
            f"{returns:,.0f}",
            f"{total:,.0f}"
        ]
    })
    st.table(df)

# Footer
st.markdown("---")
st.caption("Built with ❤️ by BusyBeingMe")
