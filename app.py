import streamlit as st
import matplotlib.pyplot as plt

# ------------------ Financial Logic ------------------

def calculate_sip(monthly_investment, annual_rate, years):
    months = years * 12
    monthly_rate = annual_rate / 12 / 100
    future_value = sum([
        monthly_investment * ((1 + monthly_rate) ** (months - i))
        for i in range(months)
    ])
    invested = monthly_investment * months
    return round(invested, 2), round(future_value - invested, 2), round(future_value, 2)

def calculate_swp(initial_amount, monthly_withdrawal, annual_rate, years):
    months = years * 12
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
    return round(principal, 2), round(future_value - principal, 2), round(future_value, 2)

# ------------------ Chart Generator ------------------

def pie_chart(labels, values, title):
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.subheader(title)
    st.pyplot(fig)

# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="Financial Calculator", page_icon="💸", layout="centered")
st.title("💸 Financial Calculator")
option = st.radio("Choose Calculator", ["SIP", "SWP", "Lump Sum"])

# ------------------ SIP ------------------
if option == "SIP":
    st.subheader("📈 SIP Calculator")
    mi = st.number_input("Monthly Investment (₹)", min_value=0.0, step=100.0)
    rate = st.number_input("Expected Annual Return (%)", min_value=0.0, step=0.1)
    years = st.number_input("Investment Duration (Years)", min_value=1, step=1)
    if st.button("Calculate SIP"):
        invested, returns, total = calculate_sip(mi, rate, years)
        st.success(f"Total Value: ₹{total}")
        pie_chart(["Invested", "Returns"], [invested, returns], "SIP Breakdown")

# ------------------ SWP ------------------
elif option == "SWP":
    st.subheader("📉 SWP Calculator")
    ia = st.number_input("Initial Investment (₹)", min_value=0.0, step=100.0)
    mw = st.number_input("Monthly Withdrawal (₹)", min_value=0.0, step=100.0)
    rate = st.number_input("Expected Annual Return (%)", min_value=0.0, step=0.1)
    years = st.number_input("Withdrawal Duration (Years)", min_value=1, step=1)
    if st.button("Calculate SWP"):
        withdrawn, balance = calculate_swp(ia, mw, rate, years)
        st.success(f"Remaining Balance: ₹{balance}")
        pie_chart(["Withdrawn", "Remaining"], [withdrawn, balance], "SWP Breakdown")

# ------------------ Lump Sum ------------------
else:
    st.subheader("💼 Lump Sum Calculator")
    principal = st.number_input("Principal Amount (₹)", min_value=0.0, step=100.0)
    rate = st.number_input("Expected Annual Return (%)", min_value=0.0, step=0.1)
    years = st.number_input("Investment Duration (Years)", min_value=1, step=1)
    if st.button("Calculate Lump Sum"):
        invested, returns, total = calculate_lump_sum(principal, rate, years)
        st.success(f"Total Value: ₹{total}")
        pie_chart(["Invested", "Returns"], [invested, returns], "Lump Sum Breakdown")

# ------------------ Footer ------------------
st.markdown("---")
st.caption("Built with ❤️ by BusyBeingMe")