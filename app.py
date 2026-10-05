import streamlit as st
import pandas as pd
from PIL import Image
import re

st.set_page_config(
    page_title="Educational Trading Journal",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Educational Trading Journal")
st.caption("For educational and study purposes only.")

st.divider()

# -----------------------------
# IMAGE UPLOAD
# -----------------------------

st.subheader("📷 Upload Trading Chart")

uploaded_file = st.file_uploader(
    "Upload a screenshot of your trading chart",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Trading Chart",
        use_container_width=True
    )

    st.success("Chart uploaded successfully.")

    st.divider()

    # -----------------------------
    # TRADE INFORMATION
    # -----------------------------

    st.subheader("📝 Trade Information")

    col1, col2 = st.columns(2)

    with col1:

        symbol = st.text_input(
            "Symbol",
            value="XAUUSD"
        )

        trade_type = st.selectbox(
            "Order Type",
            ["Buy", "Sell"]
        )

        entry_price = st.number_input(
            "Entry Price",
            min_value=0.0,
            format="%.5f"
        )

        stop_loss = st.number_input(
            "Stop Loss (SL)",
            min_value=0.0,
            format="%.5f"
        )

    with col2:

        take_profit = st.number_input(
            "Take Profit (TP)",
            min_value=0.0,
            format="%.5f"
        )

        exit_price = st.number_input(
            "Exit Price",
            min_value=0.0,
            format="%.5f"
        )

        quantity = st.number_input(
            "Quantity / Lot Size",
            min_value=0.01,
            value=0.01
        )

        trade_date = st.date_input(
            "Trade Date"
        )

    notes = st.text_area(
        "Trade Notes"
    )

    # -----------------------------
    # CALCULATIONS
    # -----------------------------

    if st.button("📊 Analyze Trade"):

        if entry_price <= 0:
            st.error("Please enter an entry price.")

        else:

            if trade_type == "Buy":

                risk = abs(entry_price - stop_loss)
                reward = abs(take_profit - entry_price)

                if exit_price > 0:
                    pnl = (exit_price - entry_price) * quantity
                else:
                    pnl = 0

            else:

                risk = abs(stop_loss - entry_price)
                reward = abs(entry_price - take_profit)

                if exit_price > 0:
                    pnl = (entry_price - exit_price) * quantity
                else:
                    pnl = 0

            if risk > 0:

                risk_reward = reward / risk

            else:

                risk_reward = 0

            # -----------------------------
            # RESULTS
            # -----------------------------

            st.divider()

            st.subheader("📈 Trade Analysis")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Entry",
                f"{entry_price:.5f}"
            )

            c2.metric(
                "Stop Loss",
                f"{stop_loss:.5f}"
            )

            c3.metric(
                "Take Profit",
                f"{take_profit:.5f}"
            )

            c4.metric(
                "Risk : Reward",
                f"1 : {risk_reward:.2f}"
            )

            st.divider()

            if exit_price > 0:

                if pnl >= 0:

                    st.success(
                        f"Trade Result: PROFIT — {pnl:.2f}"
                    )

                else:

                    st.error(
                        f"Trade Result: LOSS — {pnl:.2f}"
                    )

            else:

                st.info(
                    "Exit price not entered. P/L cannot be calculated yet."
                )

            # -----------------------------
            # SAVE TRADE
            # -----------------------------

            trade_data = pd.DataFrame([{

                "Date": str(trade_date),
                "Symbol": symbol,
                "Order": trade_type,
                "Entry": entry_price,
                "SL": stop_loss,
                "TP": take_profit,
                "Exit": exit_price,
                "Quantity": quantity,
                "Risk_Reward": round(risk_reward, 2),
                "P&L": round(pnl, 2),
                "Notes": notes

            }])

            st.subheader("📋 Order History")

            st.dataframe(
                trade_data,
                use_container_width=True
            )

            csv = trade_data.to_csv(index=False)

            st.download_button(
                "⬇️ Download Trade History",
                csv,
                "trading_journal.csv",
                "text/csv"
            )
