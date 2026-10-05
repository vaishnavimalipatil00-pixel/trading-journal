import streamlit as st
import pandas as pd
from datetime import date

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Educational Trading Journal",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# SESSION STORAGE
# =========================================================

if "trades" not in st.session_state:
    st.session_state.trades = []


# =========================================================
# FUNCTIONS
# =========================================================

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


# =========================================================
# SIDEBAR
# =========================================================

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


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("📊 Educational Trading Journal")

    st.caption(
        "For educational and study purposes only."
    )

    df = pd.DataFrame(
        st.session_state.trades
    )

    if df.empty:

        st.info(
            "No trades yet. Go to Add Trade to create your first trade."
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

        if total_profit >= 0:

            st.success(
                f"💰 Total Profit: ${total_profit:,.2f}"
            )

        else:

            st.error(
                f"📉 Total Loss: ${abs(total_profit):,.2f}"
            )

        st.subheader("📋 Trade History")

        st.dataframe(
            df,
            use_container_width=True
        )


# =========================================================
# ADD TRADE
# =========================================================

elif page == "Add Trade":

    st.title("➕ Add Trade")

    trade_date = st.date_input(
        "📅 Trade Date",
        date.today()
    )

    col1, col2 = st.columns(2)

    with col1:

        symbol = st.text_input(
            "Symbol",
            "XAUUSD"
        )

        order = st.selectbox(
            "Order Type",
            [
                "BUY",
                "SELL"
            ]
        )

        entry = st.number_input(
            "Entry Price",
            min_value=0.0,
            value=0.0,
            step=0.01
        )

        stop_loss = st.number_input(
            "Stop Loss (SL)",
            min_value=0.0,
            value=0.0,
            step=0.01
        )

    with col2:

        take_profit = st.number_input(
            "Take Profit (TP)",
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
            "Trade Result",
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
        "📷 Upload Trading Chart",
        type=[
            "png",
            "jpg",
            "jpeg"
        ]
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

                "Risk:Reward": round(
                    rr,
                    2
                ),

                "P&L": round(
                    pnl,
                    2
                ),

                "Notes": notes

            }

            st.session_state.trades.append(
                trade
            )

            st.success(
                "✅ Trade saved successfully!"
            )

            if screenshot:

                st.image(
                    screenshot,
                    caption="Trading Chart",
                    use_container_width=True
                )


# =========================================================
# CALENDAR
# =========================================================

elif page == "Calendar":

    st.title("📅 Trading Calendar")

    selected_date = st.date_input(
        "Select Date",
        date.today()
    )

    df = pd.DataFrame(
        st.session_state.trades
    )

    if df.empty:

        st.info(
            "No trades available."
        )

    else:

        daily = df[
            df["Date"] ==
            str(selected_date)
        ]

        if daily.empty:

            st.info(
                "No trades on this date."
            )

        else:

            st.dataframe(
                daily,
                use_container_width=True
            )

            daily_profit = daily[
                "P&L"
            ].sum()

            if daily_profit >= 0:

                st.success(
                    f"💰 Daily Profit: ${daily_profit:,.2f}"
                )

            else:

                st.error(
                    f"📉 Daily Loss: ${abs(daily_profit):,.2f}"
                )


# =========================================================
# BUY HISTORY
# =========================================================

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

        buys = df[
            df["Order"] == "BUY"
        ]

        if buys.empty:

            st.info(
                "No BUY trades."
            )

        else:

            st.dataframe(
                buys,
                use_container_width=True
            )

            profit = buys["P&L"].sum()

            st.metric(
                "BUY P&L",
                f"${profit:,.2f}"
            )


# =========================================================
# SELL HISTORY
# =========================================================

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

        sells = df[
            df["Order"] == "SELL"
        ]

        if sells.empty:

            st.info(
                "No SELL trades."
            )

        else:

            st.dataframe(
                sells,
                use_container_width=True
            )

            profit = sells["P&L"].sum()

            st.metric(
                "SELL P&L",
                f"${profit:,.2f}"
            )


# =========================================================
# WEEKLY OVERVIEW
# =========================================================

elif page == "Weekly Overview":

    st.title("📊 Weekly Profit Overview")

    st.caption(
        "All profit and loss values are displayed in USD ($)."
    )

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

        # Create week

        df["Week"] = (
            df["Date"]
            .dt.to_period("W")
            .astype(str)
        )

        # Calculate weekly P&L

        weekly = (
            df.groupby("Week")["P&L"]
            .sum()
            .reset_index()
        )

        # Add cumulative profit

        weekly["Cumulative P&L"] = (
            weekly["P&L"].cumsum()
        )

        # -----------------------------------------
        # TOTAL PROFIT
        # -----------------------------------------

        total_profit = weekly["P&L"].sum()

        st.subheader("💰 Total Performance")

        if total_profit >= 0:

            st.success(
                f"Total Profit: ${total_profit:,.2f}"
            )

        else:

            st.error(
                f"Total Loss: ${abs(total_profit):,.2f}"
            )

        # -----------------------------------------
        # WEEKLY CARDS
        # -----------------------------------------

        st.subheader("📅 Weekly Results")

        for _, row in weekly.iterrows():

            week = row["Week"]
            profit = row["P&L"]

            if profit >= 0:

                st.success(
                    f"📈 {week}   →   +${profit:,.2f}"
                )

            else:

                st.error(
                    f"📉 {week}   →   -${abs(profit):,.2f}"
                )

        # -----------------------------------------
        # WEEKLY BAR CHART
        # -----------------------------------------

        st.subheader(
            "📊 Weekly Profit / Loss"
        )

        chart_data = weekly.set_index(
            "Week"
        )[["P&L"]]

        st.bar_chart(
            chart_data
        )

        # -----------------------------------------
        # CUMULATIVE CHART
        # -----------------------------------------

        st.subheader(
            "📈 Cumulative Profit"
        )

        cumulative_data = weekly.set_index(
            "Week"
        )[["Cumulative P&L"]]

        st.line_chart(
            cumulative_data
        )

        # -----------------------------------------
        # TABLE
        # -----------------------------------------

        st.subheader(
            "📋 Weekly Statistics"
        )

        display_weekly = weekly.copy()

        display_weekly["P&L"] = (
            display_weekly["P&L"]
            .apply(
                lambda x: f"${x:,.2f}"
            )
        )

        display_weekly["Cumulative P&L"] = (
            display_weekly["Cumulative P&L"]
            .apply(
                lambda x: f"${x:,.2f}"
            )
        )

        st.dataframe(
            display_weekly,
            use_container_width=True
        )
