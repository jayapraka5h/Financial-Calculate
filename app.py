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
    fig, ax = plt.subplots(figsize=(5, 5))  # Bigger chart
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="Financial Calculator", layout="wide")

# Inject CSS for layout
st.markdown("""
    <style>
    .flex-container {
        display: flex;
        gap: 2rem;
        margin-top: 20px;
    }
    .flex-child {
        flex: 1;
        min-height: 500px;
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    .bottom-table {
        margin-top: 40px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>💸 Financial Calculator</h1>", unsafe_allow_html=True)

calc_type = st.radio("Choose Calculator", ["SIP", "SWP", "Lump Sum"], horizontal=True)

# Begin layout
st.markdown('<div class="flex-container">', unsafe_allow_html=True)

# Left: Inputs
st.markdown('<div class="flex-child">', unsafe_allow_html=True)
st.subheader("📈 Enter Your Details")

calculate = False
if calc_type == "SIP":
    mi = st.number_input("Monthly Investment (₹)", min_value=0.0, step=0.01, format="%.2f")
    rate = st.number_input("Expected Annual Return (%)", min_value=0.0, step=0.01, format="%.2f")
    years = st.number_input("Investment Duration (Years)", min_value=0.0, step=0.01, format="%.2f")
    calculate = st.button("Calculate SIP")

elif calc_type == "SWP":
    ia = st.number_input("Initial Investment (₹)", min_value=0.0, step=0.01, format="%.2f")
    mw = st.number_input("Monthly Withdrawal (₹)", min_value=0.0, step=0.01, format="%.2f")
    rate = st.number_input("Expected Annual Return (%)", min_value=0.0, step=0.01, format="%.2f")
    years = st.number_input("Withdrawal Duration (Years)", min_value=0.0, step=0.01, format="%.2f")
    calculate = st.button("Calculate SWP")

else:
    principal = st.number_input("Principal Amount (₹)", min_value=0.0, step=0.01, format="%.2f")
    rate = st.number_input("Expected Annual Return (%)", min_value=0.0, step=0.01, format="%.2f")
    years = st.number_input("Investment Duration (Years)", min_value=0.0, step=0.01, format="%.2f")
    calculate = st.button("Calculate Lump Sum")

st.markdown('</div>', unsafe_allow_html=True)

# Right: Chart
st.markdown('<div class="flex-child">', unsafe_allow_html=True)
st.subheader("📊 Investment Breakdown")

if calculate:
    if calc_type == "SIP":
        invested, returns, total = calculate_sip(mi, rate, years)
        pie_chart(["Invested", "Returns"], [invested, returns])
    elif calc_type == "SWP":
        withdrawn, balance = calculate_swp(ia, mw, rate, years)
        pie_chart(["Withdrawn", "Remaining"], [withdrawn, balance])
    else:
        invested, returns, total = calculate_lump_sum(principal, rate, years)
        pie_chart(["Invested", "Returns"], [invested, returns])
else:
    st.markdown("Pie chart will appear here after calculation.")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Bottom: Results Table
if calculate:
    st.markdown('<div class="bottom-table">', unsafe_allow_html=True)
    st.markdown("### 📋 Results Summary")

    if calc_type == "SIP":
        df = pd.DataFrame({
            "Description": [
                "Monthly Investment (₹)",
                "Expected Annual Return (%)",
                "Investment Duration (Years)",
                "Total Invested (₹)",
                "Returns Earned (₹)"
            ],
            "Value": [
                f"{mi:,.2f}",
                f"{rate:,.2f}",
                f"{years:,.2f}",
                f"{invested:,.0f}",
                f"{returns:,.0f}"
            ]
        })

    elif calc_type == "SWP":
        df = pd.DataFrame({
            "Description": [
                "Initial Investment (₹)",
                "Monthly Withdrawal (₹)",
                "Expected Annual Return (%)",
                "Withdrawal Duration (Years)",
                "Total Withdrawn (₹)"
            ],
            "Value": [
                f"{ia:,.2f}",
                f"{mw:,.2f}",
                f"{rate:,.2f}",
                f"{years:,.2f}",
                f"{withdrawn:,.0f}"
            ]
        })

    else:
        df = pd.DataFrame({
            "Description": [
                "Principal Amount (₹)",
                "Expected Annual Return (%)",
                "Investment Duration (Years)",
                "Total Invested (₹)",
                "Returns Earned (₹)"
            ],
            "Value": [
                f"{principal:,.2f}",
                f"{rate:,.2f}",
                f"{years:,.2f}",
                f"{invested:,.0f}",
                f"{returns:,.0f}"
            ]
        })

    st.table(df)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Built with ❤️ by BusyBeingMe")
