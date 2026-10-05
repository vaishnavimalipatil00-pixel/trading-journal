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

def calculate_risk_reward(order, entry, sl, tp):

    if entry <= 0 or sl <= 0 or tp <= 0:
        return 0.0

    if order == "BUY":
        risk = abs(entry - sl)
        reward = abs(tp - entry)
    else:
        risk = abs(sl - entry)
        reward = abs(entry - tp)

    if risk == 0:
        return 0.0

    return reward / risk


def currency_symbol(currency):

    if currency == "USD ($)":
        return "$"

    if currency == "INR (₹)":
        return "₹"

    if currency == "USDT":
        return "USDT "

    return ""


def format_money(value, currency):

    return f"{currency_symbol(currency)}{value:,.2f}"


def get_trade_dataframe():

    if not st.session_state.trades:
        return pd.DataFrame()

    return pd.DataFrame(st.session_state.trades)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📊 Trading Journal")

st.sidebar.caption(
    "Educational & Study Purpose Only"
)

page = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Calendar",
        "Add Trade",
        "Buy History",
        "Sell History",
        "Weekly Overview",
        "Delete Trade"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("📊 Educational Trading Journal")

    st.caption(
        "For educational and study purposes only. "
        "This journal is not financial advice."
    )

    df = get_trade_dataframe()

    if df.empty:

        st.info(
            "No trades yet. Go to Add Trade to create your first trade."
        )

    else:

        total_trades = len(df)

        winning_trades = len(
            df[df["Result"] == "WIN"]
        )

        losing_trades = len(
            df[df["Result"] == "LOSS"]
        )

        breakeven_trades = len(
            df[df["Result"] == "BREAKEVEN"]
        )

        win_rate = (
            winning_trades / total_trades * 100
            if total_trades > 0
            else 0
        )

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

        st.subheader("💰 Overall P/L")

        currencies = [
            "USD ($)",
            "INR (₹)",
            "USDT"
        ]

        cols = st.columns(3)

        for i, currency in enumerate(currencies):

            currency_df = df[
                df["Currency"] == currency
            ]

            total = currency_df["P&L"].sum()

            cols[i].metric(
                currency,
                format_money(total, currency)
            )

        st.divider()

        st.subheader("📋 Trade History")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# ADD TRADE
# =========================================================

elif page == "Add Trade":

    st.title("➕ Add Trade")

    st.caption(
        "Enter your trade information and actual P/L."
    )

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
            ["BUY", "SELL"]
        )

        currency = st.selectbox(
            "💱 Currency",
            [
                "USD ($)",
                "INR (₹)",
                "USDT"
            ]
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

    with col2:

        quantity = st.number_input(
            "Lot / Quantity",
            min_value=0.01,
            value=0.01,
            step=0.01
        )

        entry = st.number_input(
            "Entry Price",
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

    st.subheader("🎯 Trade Levels")

    col1, col2 = st.columns(2)

    with col1:

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

    st.subheader("💰 Trade Profit / Loss")

    profit_loss = st.number_input(
        f"Enter P/L in {currency}",
        value=0.0,
        step=0.01
    )

    st.info(
        "Profit example: 25.50 | Loss example: -25.50"
    )

    notes = st.text_area(
        "📝 Trade Notes"
    )

    screenshot = st.file_uploader(
        "📷 Upload Trading Chart",
        type=["png", "jpg", "jpeg"]
    )

    if entry > 0 and stop_loss > 0 and take_profit > 0:

        rr = calculate_risk_reward(
            order,
            entry,
            stop_loss,
            take_profit
        )

        st.info(
            f"🎯 Risk : Reward = 1 : {rr:.2f}"
        )

    st.divider()

    if st.button(
        "💾 Save Trade",
        type="primary",
        use_container_width=True
    ):

        if not symbol.strip():

            st.error(
                "Please enter a symbol."
            )

        elif entry <= 0:

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

            rr = calculate_risk_reward(
                order,
                entry,
                stop_loss,
                take_profit
            )

            # Create unique trade ID
            trade_id = len(
                st.session_state.trades
            ) + 1

            trade = {

                "Trade ID": trade_id,

                "Date": str(trade_date),

                "Symbol": symbol.upper(),

                "Order": order,

                "Currency": currency,

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
                    profit_loss,
                    2
                ),

                "Notes": notes

            }

            st.session_state.trades.append(
                trade
            )

            st.success(
                f"✅ Trade #{trade_id} saved successfully!"
            )

            st.write(
                f"**P/L:** {format_money(profit_loss, currency)}"
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

    df = get_trade_dataframe()

    if df.empty:

        st.info(
            "No trades available."
        )

    else:

        daily = df[
            df["Date"] == str(selected_date)
        ]

        if daily.empty:

            st.info(
                "No trades on this date."
            )

        else:

            st.subheader(
                f"Trades on {selected_date}"
            )

            st.dataframe(
                daily,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            st.subheader("💰 Daily P/L")

            currencies = [
                "USD ($)",
                "INR (₹)",
                "USDT"
            ]

            cols = st.columns(3)

            for i, currency in enumerate(currencies):

                currency_df = daily[
                    daily["Currency"] == currency
                ]

                total = currency_df["P&L"].sum()

                cols[i].metric(
                    currency,
                    format_money(total, currency)
                )


# =========================================================
# BUY HISTORY
# =========================================================

elif page == "Buy History":

    st.title("📈 BUY History")

    df = get_trade_dataframe()

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
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            st.subheader("💰 BUY P/L")

            currencies = [
                "USD ($)",
                "INR (₹)",
                "USDT"
            ]

            cols = st.columns(3)

            for i, currency in enumerate(currencies):

                total = buys[
                    buys["Currency"] == currency
                ]["P&L"].sum()

                cols[i].metric(
                    currency,
                    format_money(total, currency)
                )


# =========================================================
# SELL HISTORY
# =========================================================

elif page == "Sell History":

    st.title("📉 SELL History")

    df = get_trade_dataframe()

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
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            st.subheader("💰 SELL P/L")

            currencies = [
                "USD ($)",
                "INR (₹)",
                "USDT"
            ]

            cols = st.columns(3)

            for i, currency in enumerate(currencies):

                total = sells[
                    sells["Currency"] == currency
                ]["P&L"].sum()

                cols[i].metric(
                    currency,
                    format_money(total, currency)
                )


# =========================================================
# WEEKLY OVERVIEW
# =========================================================

elif page == "Weekly Overview":

    st.title("📊 Weekly Profit Overview")

    st.caption(
        "USD, INR and USDT are shown separately."
    )

    df = get_trade_dataframe()

    if df.empty:

        st.info(
            "Add trades to see weekly performance."
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

        tab_usd, tab_inr, tab_usdt = st.tabs(
            [
                "💵 USD",
                "🇮🇳 INR",
                "🪙 USDT"
            ]
        )

        for tab, currency, prefix in [
            (tab_usd, "USD ($)", "$"),
            (tab_inr, "INR (₹)", "₹"),
            (tab_usdt, "USDT", "USDT ")
        ]:

            with tab:

                currency_df = df[
                    df["Currency"] == currency
                ].copy()

                if currency_df.empty:

                    st.info(
                        f"No {currency} trades available."
                    )

                    continue

                weekly = (
                    currency_df
                    .groupby("Week")["P&L"]
                    .sum()
                    .reset_index()
                )

                weekly["Cumulative P&L"] = (
                    weekly["P&L"].cumsum()
                )

                total = weekly["P&L"].sum()

                st.metric(
                    f"Total {currency} P/L",
                    f"{prefix}{total:,.2f}"
                )

                st.subheader(
                    f"📊 Weekly {currency} P/L"
                )

                chart = weekly.set_index(
                    "Week"
                )[["P&L"]]

                st.bar_chart(chart)

                st.subheader(
                    f"📈 Cumulative {currency} P/L"
                )

                cumulative = weekly.set_index(
                    "Week"
                )[["Cumulative P&L"]]

                st.line_chart(cumulative)

                st.subheader(
                    "📋 Weekly Statistics"
                )

                display = weekly.copy()

                display["P&L"] = display[
                    "P&L"
                ].apply(
                    lambda x:
                    f"{prefix}{x:,.2f}"
                )

                display["Cumulative P&L"] = display[
                    "Cumulative P&L"
                ].apply(
                    lambda x:
                    f"{prefix}{x:,.2f}"
                )

                st.dataframe(
                    display,
                    use_container_width=True,
                    hide_index=True
                )


# =========================================================
# DELETE TRADE
# =========================================================

elif page == "Delete Trade":

    st.title("🗑️ Delete Trade")

    st.warning(
        "⚠️ Be careful: deleted trades cannot be recovered "
        "from this version of the journal."
    )

    df = get_trade_dataframe()

    if df.empty:

        st.info(
            "There are no trades to delete."
        )

    else:

        st.subheader(
            "Select the trade you want to delete"
        )

        # Create readable trade options

        trade_options = {}

        for index, trade in df.iterrows():

            trade_id = trade["Trade ID"]

            label = (
                f"Trade #{trade_id} | "
                f"{trade['Date']} | "
                f"{trade['Symbol']} | "
                f"{trade['Order']} | "
                f"{format_money(trade['P&L'], trade['Currency'])}"
            )

            trade_options[label] = trade_id

        selected_trade = st.selectbox(
            "Select Trade",
            list(trade_options.keys())
        )

        selected_id = trade_options[
            selected_trade
        ]

        st.divider()

        # Find selected trade

        selected_rows = df[
            df["Trade ID"] == selected_id
        ]

        if not selected_rows.empty:

            selected = selected_rows.iloc[0]

            st.subheader(
                "📋 Selected Trade"
            )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Trade ID",
                f"#{selected['Trade ID']}"
            )

            col2.metric(
                "Symbol",
                selected["Symbol"]
            )

            col3.metric(
                "Order",
                selected["Order"]
            )

            col4.metric(
                "P/L",
                format_money(
                    selected["P&L"],
                    selected["Currency"]
                )
            )

            st.write(
                f"**Date:** {selected['Date']}"
            )

            st.write(
                f"**Entry:** {selected['Entry']}"
            )

            st.write(
                f"**SL:** {selected['SL']}"
            )

            st.write(
                f"**TP:** {selected['TP']}"
            )

            st.write(
                f"**Result:** {selected['Result']}"
            )

            st.write(
                f"**Notes:** {selected['Notes']}"
            )

            st.divider()

            confirm = st.checkbox(
                "I confirm that I want to delete this trade."
            )

            if confirm:

                if st.button(
                    "🗑️ DELETE SELECTED TRADE",
                    type="primary"
                ):

                    # Remove selected trade

                    st.session_state.trades = [
                        trade
                        for trade in st.session_state.trades
                        if trade["Trade ID"] != selected_id
                    ]

                    st.success(
                        f"✅ Trade #{selected_id} deleted successfully."
                    )

                    st.rerun()
