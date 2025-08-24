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

def calculate_swp(initial_amount, monthly_withdrawal, annual_rate, years):
    months = int(years * 12)
    monthly_rate = annual_rate / 12 / 100
    balance = initial_amount
    for _ in range(months):
        balance = balance * (1 + monthly_rate) - monthly_withdrawal
        if balance < 0:
            break
    withdrawn = monthly_withdrawal * months
    return round(withdrawn, 2), round(balance, 2)

def calculate_lump_sum(principal, annual_rate, years):
    future_value = principal * ((1 + annual_rate / 100) ** years)
    returns = future_value - principal
    return round(principal, 2), round(returns, 2), round(future_value, 2)

# ------------------ Chart Generator ------------------

def pie_chart(labels, values):
    fig, ax = plt.subplots(figsize=(2.5, 2.5))  # Smaller chart
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="Financial Calculator", layout="wide")

# Inject CSS for equal-height columns
st.markdown("""
    <style>
    .equal-height {
        display: flex;
        align-items: stretch;
        gap: 2rem;
    }
    .equal-height > div {
        flex: 1;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>💸 Financial Calculator</h1>", unsafe_allow_html=True)

calc_type = st.radio("Choose Calculator", ["SIP", "SWP", "Lump Sum"], horizontal=True)

# Begin equal-height layout
st.markdown('<div class="equal-height">', unsafe_allow_html=True)
left, right = st.columns(2)

# ------------------ SIP ------------------
if calc_type == "SIP":
    with left:
        st.subheader("📈 SIP Calculator")
        mi = st.number_input("Monthly Investment (₹)", min_value=0.0, step=0.01, format="%.2f", placeholder="Enter number")
        rate = st.number_input("Expected Annual Return (%)", min_value=0.0, step=0.01, format="%.2f", placeholder="Enter number")
        years = st.number_input("Investment Duration (Years)", min_value=0.0, step=0.01, format="%.2f", placeholder="Enter number")
        calculate = st.button("Calculate SIP")

    with right:
        st.subheader("📊 SIP Breakdown")
        chart_placeholder = st.empty()
        if calculate:
            invested, returns, total = calculate_sip(mi, rate, years)
            with chart_placeholder:
                pie_chart(["Invested", "Returns"], [invested, returns])

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

# ------------------ SWP ------------------
elif calc_type == "SWP":
    with left:
        st.subheader("📉 SWP Calculator")
        ia = st.number_input("Initial Investment (₹)", min_value=0.0, step=0.01, format="%.2f", placeholder="Enter number")
        mw = st.number_input("Monthly Withdrawal (₹)", min_value=0.0, step=0.01, format="%.2f", placeholder="Enter number")
        rate = st.number_input("Expected Annual Return (%)", min_value=0.0, step=0.01, format="%.2f", placeholder="Enter number")
        years = st.number_input("Withdrawal Duration (Years)", min_value=0.0, step=0.01, format="%.2f", placeholder="Enter number")
        calculate = st.button("Calculate SWP")

    with right:
        st.subheader("📊 SWP Breakdown")
        chart_placeholder = st.empty()
        if calculate:
            withdrawn, balance = calculate_swp(ia, mw, rate, years)
            with chart_placeholder:
                pie_chart(["Withdrawn", "Remaining"], [withdrawn, balance])

    if calculate:
        st.markdown("### 📋 Results Summary")
        df = pd.DataFrame({
            "Description": [
                "Initial Investment (₹)",
                "Monthly Withdrawal (₹)",
                "Expected Annual Return (%)",
                "Withdrawal Duration (Years)",
                "Total Withdrawn (₹)",
                "Remaining Balance (₹)"
            ],
            "Value": [
                f"{ia:,.2f}",
                f"{mw:,.2f}",
                f"{rate:,.2f}",
                f"{years:,.2f}",
                f"{withdrawn:,.0f}",
                f"{balance:,.0f}"
            ]
        })
        st.table(df)

# ------------------ Lump Sum ------------------
else:
    with left:
        st.subheader("💼 Lump Sum Calculator")
        principal = st.number_input("Principal Amount (₹)", min_value=0.0, step=0.01, format="%.2f", placeholder="Enter number")
        rate = st.number_input("Expected Annual Return (%)", min_value=0.0, step=0.01, format="%.2f", placeholder="Enter number")
        years = st.number_input("Investment Duration (Years)", min_value=0.0, step=0.01, format="%.2f", placeholder="Enter number")
        calculate = st.button("Calculate Lump Sum")

    with right:
        st.subheader("📊 Lump Sum Breakdown")
        chart_placeholder = st.empty()
        if calculate:
            invested, returns, total = calculate_lump_sum(principal, rate, years)
            with chart_placeholder:
                pie_chart(["Invested", "Returns"], [invested, returns])

    if calculate:
        st.markdown("### 📋 Results Summary")
        df = pd.DataFrame({
            "Description": [
                "Principal Amount (₹)",
                "Expected Annual Return (%)",
                "Investment Duration (Years)",
                "Total Invested (₹)",
                "Returns Earned (₹)",
                "Total Value (₹)"
            ],
            "Value": [
                f"{principal:,.2f}",
                f"{rate:,.2f}",
                f"{years:,.2f}",
                f"{invested:,.0f}",
                f"{returns:,.0f}",
                f"{total:,.0f}"
            ]
        })
        st.table(df)

# End equal-height layout
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Built with ❤️ by BusyBeingMe")
