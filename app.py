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
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="Financial Calculator", layout="wide")

# Centered Title
st.markdown("<h1 style='text-align: center;'>💸 Financial Calculator</h1>", unsafe_allow_html=True)

# Layout: Left (Inputs) | Right (Chart)
left, right = st.columns(2)

with left:
    st.subheader("📈 SIP Calculator")
    mi = st.number_input("Monthly Investment (₹)", min_value=0.0, step=0.01, format="%.2f")
    rate = st.number_input("Expected Annual Return (%)", min_value=0.0, step=0.01, format="%.2f")
    years = st.number_input("Investment Duration (Years)", min_value=0.0, step=0.01, format="%.2f")
    calculate = st.button("Calculate SIP")

if calculate:
    invested, returns, total = calculate_sip(mi, rate, years)

    with right:
        st.subheader("📊 SIP Breakdown")
        pie_chart(["Invested", "Returns"], [invested, returns])

    # Results Table
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
        "Value": [f"{mi:.2f}", f"{rate:.2f}", f"{years:.2f}", f"{invested:.2f}", f"{returns:.2f}", f"{total:.2f}"]
    })
    st.table(df)

# Footer
st.markdown("---")
st.caption("Built with ❤️ by BusyBeingMe")
