import streamlit as st
import pandas as pd
from datetime import date

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="Educational Trading Journal",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# SESSION STORAGE
# --------------------------------------------------

if "trades" not in st.session_state:
    st.session_state.trades = []

if "selected_date" not in st.session_state:
    st.session_state.selected_date = date.today()

# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def calculate_pnl(order, entry, exit_price, quantity):
    if exit_price <= 0:
        return 0.0

    if order == "BUY":
        return (exit_price - entry) * quantity

    return (entry - exit_price) * quantity


def calculate_risk_reward(order, entry, sl, tp):
    if order == "BUY":
        risk = abs(entry - sl)
        reward = abs(tp - entry)
    else:
        risk = abs(sl - entry)
        reward = abs(entry - tp)

    if risk == 0:
        return 0.0

    return reward / risk


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("📊 Trading Journal")

page = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Calendar",
        "Add Trade",
        "Buy History",
        "Sell History",
        "Weekly Overview"
    ]
)

# ==================================================
# DASHBOARD
# ==================================================

if page == "Dashboard":

    st.title("📊 Educational Trading Journal")

    st.write(
        "Track your trades, review your charts and study your performance."
    )

    st.info(
        "⚠️ Educational and study purposes only. "
        "This application does not provide financial advice."
    )

    st.divider()

    df = pd.DataFrame(st.session_state.trades)

    if df.empty:

        st.subheader("Welcome 👋")

        st.write(
            "You don't have any trades yet."
        )

        st.write(
            "Go to **Add Trade** to record your first trade."
        )

    else:

        total_trades = len(df)

        winning_trades = len(
            df[df["P&L"] > 0]
        )

        losing_trades = len(
            df[df["P&L"] < 0]
        )

        total_pnl = df["P&L"].sum()

        if total_trades > 0:
            win_rate = (
                winning_trades /
                total_trades
            ) * 100
        else:
            win_rate = 0

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Trades",
            total_trades
        )

        col2.metric(
            "Winning Trades",
            winning_trades
        )

        col3.metric(
            "Losing Trades",
            losing_trades
        )

        col4.metric(
            "Win Rate",
            f"{win_rate:.1f}%"
        )

        st.divider()

        if total_pnl >= 0:
            st.success(
                f"Total Profit: {total_pnl:.2f}"
            )
        else:
            st.error(
                f"Total Loss: {total_pnl:.2f}"
            )

        st.subheader("📋 Recent Trades")

        st.dataframe(
            df,
            use_container_width=True
        )

# ==================================================
# ADD TRADE
# ==================================================

elif page == "Add Trade":

    st.title("➕ Add Trade")

    trade_date = st.date_input(
        "📅 Trade Date",
        value=date.today()
    )

    col1, col2 = st.columns(2)

    with col1:

        symbol = st.text_input(
            "Symbol",
            value="XAUUSD"
        )

        order = st.selectbox(
            "Order Type",
            ["BUY", "SELL"]
        )

        entry = st.number_input(
            "Entry Price",
            min_value=0.0,
            value=0.0,
            step=0.01
        )

        stop_loss = st.number_input(
            "Stop Loss",
            min_value=0.0,
            value=0.0,
            step=0.01
        )

    with col2:

        take_profit = st.number_input(
            "Take Profit",
            min_value=0.0,
            value=0.0,
            step=0.01
        )

        exit_price = st.number_input(
            "Exit Price",
            min_value=0.0,
            value=0.0,
            step=0.01
        )

        quantity = st.number_input(
            "Lot / Quantity",
            min_value=0.01,
            value=0.01,
            step=0.01
        )

        result = st.selectbox(
            "Result",
            [
                "OPEN",
                "WIN",
                "LOSS",
                "BREAKEVEN"
            ]
        )

    notes = st.text_area(
        "📝 Trade Notes"
    )

    screenshot = st.file_uploader(
        "📷 Upload Chart Screenshot",
        type=["png", "jpg", "jpeg"]
    )

    st.divider()

    if st.button(
        "💾 Save Trade",
        type="primary"
    ):

        if entry <= 0:

            st.error(
                "Please enter a valid Entry Price."
            )

        elif stop_loss <= 0:

            st.error(
                "Please enter a valid Stop Loss."
            )

        elif take_profit <= 0:

            st.error(
                "Please enter a valid Take Profit."
            )

        else:

            pnl = calculate_pnl(
                order,
                entry,
                exit_price,
                quantity
            )

            rr = calculate_risk_reward(
                order,
                entry,
                stop_loss,
                take_profit
            )

            trade = {
                "Date": str(trade_date),
                "Symbol": symbol,
                "Order": order,
                "Entry": entry,
                "SL": stop_loss,
                "TP": take_profit,
                "Exit": exit_price,
                "Quantity": quantity,
                "Result": result,
                "Risk:Reward": round(rr, 2),
                "P&L": round(pnl, 2),
                "Notes": notes
            }

            st.session_state.trades.append(
                trade
            )

            st.success(
                "✅ Trade saved successfully!"
            )

            if screenshot is not None:

                st.image(
                    screenshot,
                    caption="Uploaded Trading Chart",
                    use_container_width=True
                )

# ==================================================
# CALENDAR
# ==================================================

elif page == "Calendar":

    st.title("📅 Trading Calendar")

    selected_date = st.date_input(
        "Select Date",
        value=date.today()
    )

    df = pd.DataFrame(
        st.session_state.trades
    )

    if df.empty:

        st.info(
            "No trades have been added yet."
        )

    else:

        daily_trades = df[
            df["Date"] ==
            str(selected_date)
        ]

        st.subheader(
            f"Trades on {selected_date}"
        )

        if daily_trades.empty:

            st.info(
                "No trades recorded on this date."
            )

        else:

            st.dataframe(
                daily_trades,
                use_container_width=True
            )

            daily_pnl = daily_trades[
                "P&L"
            ].sum()

            if daily_pnl >= 0:

                st.success(
                    f"Daily Profit: {daily_pnl:.2f}"
                )

            else:

                st.error(
                    f"Daily Loss: {daily_pnl:.2f}"
                )

# ==================================================
# BUY HISTORY
# ==================================================

elif page == "Buy History":

    st.title("📈 BUY History")

    df = pd.DataFrame(
        st.session_state.trades
    )

    if df.empty:

        st.info(
            "No trades available."
        )

    else:

        buy_df = df[
            df["Order"] == "BUY"
        ]

        if buy_df.empty:

            st.info(
                "No BUY trades available."
            )

        else:

            st.dataframe(
                buy_df,
                use_container_width=True
            )

            buy_pnl = buy_df["P&L"].sum()

            st.metric(
                "BUY P&L",
                f"{buy_pnl:.2f}"
            )

# ==================================================
# SELL HISTORY
# ==================================================

elif page == "Sell History":

    st.title("📉 SELL History")

    df = pd.DataFrame(
        st.session_state.trades
    )

    if df.empty:

        st.info(
            "No trades available."
        )

    else:

        sell_df = df[
            df["Order"] == "SELL"
        ]

        if sell_df.empty:

            st.info(
                "No SELL trades available."
            )

        else:

            st.dataframe(
                sell_df,
                use_container_width=True
            )

            sell_pnl = sell_df["P&L"].sum()

            st.metric(
                "SELL P&L",
                f"{sell_pnl:.2f}"
            )

# ==================================================
# WEEKLY OVERVIEW
# ==================================================

elif page == "Weekly Overview":

    st.title("📊 Weekly Overview")

    df = pd.DataFrame(
        st.session_state.trades
    )

    if df.empty:

        st.info(
            "Add trades to see your weekly performance."
        )

    else:

        df["Date"] = pd.to_datetime(
            df["Date"]
        )

        df["Week"] = (
            df["Date"]
            .dt.to_period("W")
            .astype(str)
        )

        weekly = (
            df.groupby("Week")["P&L"]
            .sum()
            .reset_index()
        )

        st.subheader(
            "💰 Weekly Profit / Loss"
        )

        st.dataframe(
            weekly,
            use_container_width=True
        )

        st.subheader(
            "📈 Weekly Performance Chart"
        )

        chart_data = weekly.set_index(
            "Week"
        )

        st.bar_chart(
            chart_data["P&L"]
        )

        st.subheader(
            "📊 Cumulative Profit / Loss"
        )

        weekly["Cumulative P&L"] = (
            weekly["P&L"].cumsum()
        )

        cumulative_data = (
            weekly.set_index("Week")
        )

        st.line_chart(
            cumulative_data[
                "Cumulative P&L"
            ]
        )
