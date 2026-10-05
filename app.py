import streamlit as st
import pandas as pd
from datetime import date, timedelta
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Trading Journal",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("📊 Educational Trading Journal")
st.caption("For educational and study purposes only.")

# =========================================================
# SESSION STORAGE
# =========================================================

if "trades" not in st.session_state:
    st.session_state.trades = []

if "screenshots" not in st.session_state:
    st.session_state.screenshots = {}

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📚 Trading Journal")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📅 Calendar",
        "➕ Add Trade",
        "📈 Buy History",
        "📉 Sell History",
        "📊 Weekly Overview"
    ]
)

# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.header("🏠 Dashboard")

    df = pd.DataFrame(st.session_state.trades)

    if df.empty:

        st.info(
            "No trades yet. Go to 'Add Trade' to record your first trade."
        )

    else:

        total_trades = len(df)

        winning_trades = len(
            df[df["P&L"] > 0]
        )

        losing_trades = len(
            df[df["P&L"] < 0]
        )

        total_profit = df["P&L"].sum()

        win_rate = (
            winning_trades / total_trades * 100
            if total_trades > 0 else 0
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Total Trades",
            total_trades
        )

        c2.metric(
            "Winning Trades",
            winning_trades
        )

        c3.metric(
            "Losing Trades",
            losing_trades
        )

        c4.metric(
            "Win Rate",
            f"{win_rate:.1f}%"
        )

        st.divider()

        st.subheader("💰 Total P&L")

        if total_profit >= 0:
            st.success(
                f"Profit: {total_profit:.2f}"
            )
        else:
            st.error(
                f"Loss: {total_profit:.2f}"
            )

        st.divider()

        # P&L graph

        df["Date"] = pd.to_datetime(df["Date"])

        daily_profit = (
            df.groupby("Date")["P&L"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            daily_profit,
            x="Date",
            y="P&L",
            markers=True,
            title="📈 Daily Profit / Loss"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# =========================================================
# ADD TRADE
# =========================================================

elif page == "➕ Add Trade":

    st.header("➕ Add New Trade")

    selected_date = st.date_input(
        "📅 Trade Date",
        date.today()
    )

    col1, col2 = st.columns(2)

    with col1:

        symbol = st.text_input(
            "Symbol",
            "XAUUSD"
        )

        order_type = st.selectbox(
            "Order Type",
            [
                "BUY",
                "SELL"
            ]
        )

        entry = st.number_input(
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
            "Lot / Quantity",
            min_value=0.01,
            value=0.01
        )

        result = st.selectbox(
            "Trade Result",
            [
                "WIN",
                "LOSS",
                "BREAKEVEN",
                "OPEN"
            ]
        )

    notes = st.text_area(
        "📝 Trade Notes"
    )

    screenshot = st.file_uploader(
        "📷 Upload Trading Chart",
        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )

    if st.button(
        "💾 Save Trade"
    ):

        # Calculate P&L

        if result == "WIN" or result == "LOSS":

            if order_type == "BUY":

                pnl = (
                    exit_price - entry
                ) * quantity

            else:

                pnl = (
                    entry - exit_price
                ) * quantity

        else:

            pnl = 0

        # Calculate risk

        if order_type == "BUY":

            risk = abs(
                entry - stop_loss
            )

            reward = abs(
                take_profit - entry
            )

        else:

            risk = abs(
                stop_loss - entry
            )

            reward = abs(
                entry - take_profit
            )

        if risk > 0:

            risk_reward = reward / risk

        else:

            risk_reward = 0

        trade = {

            "Date": str(selected_date),

            "Symbol": symbol,

            "Order": order_type,

            "Entry": entry,

            "SL": stop_loss,

            "TP": take_profit,

            "Exit": exit_price,

            "Quantity": quantity,

            "Result": result,

            "P&L": round(
                pnl,
                2
            ),

            "Risk Reward": round(
                risk_reward,
                2
            ),

            "Notes": notes

        }

        st.session_state.trades.append(
            trade
        )

        # Save screenshot in session

        if screenshot:

            st.session_state.screenshots[
                str(selected_date)
            ] = screenshot.getvalue()

        st.success(
            "✅ Trade saved successfully!"
        )

# =========================================================
# CALENDAR
# =========================================================

elif page == "📅 Calendar":

    st.header("📅 Trading Calendar")

    selected_date = st.date_input(
        "Select Trading Date",
        date.today()
    )

    df = pd.DataFrame(
        st.session_state.trades
    )

    if not df.empty:

        day_trades = df[
            df["Date"] ==
            str(selected_date)
        ]

        st.subheader(
            f"Trades on {selected_date}"
        )

        if day_trades.empty:

            st.info(
                "No trades recorded for this date."
            )

        else:

            st.dataframe(
                day_trades,
                use_container_width=True
            )

            daily_pnl = day_trades[
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

            # Display screenshot

            if str(selected_date) in st.session_state.screenshots:

                st.subheader(
                    "📷 Trading Chart"
                )

                st.image(
                    st.session_state.screenshots[
                        str(selected_date)
                    ],
                    use_container_width=True
                )

# =========================================================
# BUY HISTORY
# =========================================================

elif page == "📈 Buy History":

    st.header("📈 BUY History")

    df = pd.DataFrame(
        st.session_state.trades
    )

    if df.empty:

        st.info(
            "No trades available."
        )

    else:

        buys = df[
            df["Order"] == "BUY"
        ]

        st.dataframe(
            buys,
            use_container_width=True
        )

        if not buys.empty:

            st.metric(
                "BUY P&L",
                f"{buys['P&L'].sum():.2f}"
            )

# =========================================================
# SELL HISTORY
# =========================================================

elif page == "📉 Sell History":

    st.header("📉 SELL History")

    df = pd.DataFrame(
        st.session_state.trades
    )

    if df.empty:

        st.info(
            "No trades available."
        )

    else:

        sells = df[
            df["Order"] == "SELL"
        ]

        st.dataframe(
            sells,
            use_container_width=True
        )

        if not sells.empty:

            st.metric(
                "SELL P&L",
                f"{sells['P&L'].sum():.2f}"
            )

# =========================================================
# WEEKLY OVERVIEW
# =========================================================

elif page == "📊 Weekly Overview":

    st.header("📊 Weekly Profit Overview")

    df = pd.DataFrame(
        st.session_state.trades
    )

    if df.empty:

        st.info(
            "Add some trades first to see your weekly performance."
        )

    else:

        df["Date"] = pd.to_datetime(
            df["Date"]
        )

        # Week number

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
            "💰 Weekly P&L"
        )

        st.dataframe(
            weekly,
            use_container_width=True
        )

        # Weekly graph

        fig = px.bar(
            weekly,
            x="Week",
            y="P&L",
            title="📊 Weekly Profit / Loss"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Cumulative P&L

        weekly["Cumulative P&L"] = (
            weekly["P&L"].cumsum()
        )

        st.subheader(
            "📈 Cumulative Performance"
        )

        fig2 = px.line(
            weekly,
            x="Week",
            y="Cumulative P&L",
            markers=True,
            title="Cumulative P&L"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )
