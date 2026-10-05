import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Educational Trading Journal",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Educational Trading Journal")
st.write("For educational and study purposes only.")

st.divider()

st.subheader("📝 Add Trade")

col1, col2 = st.columns(2)

with col1:
    symbol = st.text_input("Symbol", "XAUUSD")
    trade_type = st.selectbox("Trade Type", ["Buy", "Sell"])
    entry_price = st.number_input("Entry Price", min_value=0.0)

with col2:
    exit_price = st.number_input("Exit Price", min_value=0.0)
    quantity = st.number_input("Quantity", min_value=0.01, value=0.01)
    notes = st.text_area("Trade Notes")

if st.button("Calculate Trade"):
    if entry_price > 0 and exit_price > 0:

        if trade_type == "Buy":
            pnl = (exit_price - entry_price) * quantity
        else:
            pnl = (entry_price - exit_price) * quantity

        st.subheader("📈 Trade Result")

        if pnl >= 0:
            st.success(f"Profit: {pnl:.2f}")
        else:
            st.error(f"Loss: {pnl:.2f}")

        st.write("Symbol:", symbol)
        st.write("Trade Type:", trade_type)
        st.write("Entry Price:", entry_price)
        st.write("Exit Price:", exit_price)
        st.write("Quantity:", quantity)
        st.write("Notes:", notes)
