import streamlit as st
import pandas as pd
from datetime import date

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Trading Journal",
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

    elif currency == "INR (₹)":
        return "₹"

    elif currency == "USDT":
        return "USDT "

    return ""


def format_money(value, currency):

    symbol = currency_symbol(currency)

    return f"{symbol}{value:,.2f}"


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
        "Weekly Overview"
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

    df = pd.DataFrame(
        st.session_state.trades
    )

    if df.empty:

        st.info(
            "No trades yet. Go to ➕ Add Trade to create your first trade."
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
            winning_trades /
            total_trades
        ) * 100 if total_trades > 0 else 0

        # -----------------------------------------
        # MAIN METRICS
        # -----------------------------------------

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

        # -----------------------------------------
        # CURRENCY TOTALS
        # -----------------------------------------

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

            with cols[i]:

                st.metric(
                    currency,
                    format_money(
                        total,
                        currency
                    )
                )

        st.divider()

        # -----------------------------------------
        # TRADE HISTORY
        # -----------------------------------------

        st.subheader("📋 Trade History")

        display_df = df.copy()

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# ADD TRADE
# =========================================================

elif page == "Add Trade":

    st.title("➕ Add Trade")

    st.caption(
        "Enter the trade details and the actual Profit/Loss shown by your platform."
    )

    # -----------------------------------------
    # BASIC DETAILS
    # -----------------------------------------

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

    # -----------------------------------------
    # SL / TP
    # -----------------------------------------

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

    # -----------------------------------------
    # PROFIT / LOSS
    # -----------------------------------------

    st.subheader("💰 Trade Profit / Loss")

    profit_loss = st.number_input(
        f"Enter P/L in {currency}",
        value=0.0,
        step=0.01
    )

    st.info(
        "Example: If your broker shows +25.50 USD, enter 25.50. "
        "For a loss, enter -25.50."
    )

    # -----------------------------------------
    # NOTES
    # -----------------------------------------

    notes = st.text_area(
        "📝 Trade Notes",
        placeholder="Example: Breakout + retest, good entry, followed trading plan..."
    )

    # -----------------------------------------
    # SCREENSHOT
    # -----------------------------------------

    screenshot = st.file_uploader(
        "📷 Upload Trading Chart / Trade Screenshot",
        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )

    st.divider()

    # -----------------------------------------
    # PREVIEW
    # -----------------------------------------

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

    # -----------------------------------------
    # SAVE TRADE
    # -----------------------------------------

    if st.button(
        "💾 Save Trade",
        type="primary",
        use_container_width=True
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

        elif profit_loss == 0 and result == "WIN":

            st.warning(
                "WIN trade has ₹/$/USDT 0.00 P/L. "
                "Please check the Profit/Loss value."
            )

        else:

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
                "✅ Trade saved successfully!"
            )

            st.write(
                f"**P/L:** {format_money(profit_loss, currency)}"
            )

            # -----------------------------------------
            # SHOW SCREENSHOT
            # -----------------------------------------

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

            st.subheader(
                f"Trades on {selected_date}"
            )

            st.dataframe(
                daily,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            # -----------------------------------------
            # DAILY CURRENCY TOTALS
            # -----------------------------------------

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

                with cols[i]:

                    st.metric(
                        currency,
                        format_money(
                            total,
                            currency
                        )
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

                currency_df = buys[
                    buys["Currency"] == currency
                ]

                profit = currency_df[
                    "P&L"
                ].sum()

                with cols[i]:

                    st.metric(
                        currency,
                        format_money(
                            profit,
                            currency
                        )
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

                currency_df = sells[
                    sells["Currency"] == currency
                ]

                profit = currency_df[
                    "P&L"
                ].sum()

                with cols[i]:

                    st.metric(
                        currency,
                        format_money(
                            profit,
                            currency
                        )
                    )


# =========================================================
# WEEKLY OVERVIEW
# =========================================================

elif page == "Weekly Overview":

    st.title("📊 Weekly Profit Overview")

    st.caption(
        "Profit and Loss are separated by currency. "
        "USD, INR and USDT are not combined."
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

        # -----------------------------------------
        # CREATE WEEK
        # -----------------------------------------

        df["Week"] = (
            df["Date"]
            .dt.to_period("W")
            .astype(str)
        )

        # -----------------------------------------
        # CURRENCY TABS
        # -----------------------------------------

        tab_usd, tab_inr, tab_usdt = st.tabs(
            [
                "💵 USD",
                "🇮🇳 INR",
                "🪙 USDT"
            ]
        )

        # =================================================
        # USD
        # =================================================

        with tab_usd:

            currency = "USD ($)"

            currency_df = df[
                df["Currency"] == currency
            ].copy()

            if currency_df.empty:

                st.info(
                    "No USD trades available."
                )

            else:

                weekly = (
                    currency_df
                    .groupby("Week")["P&L"]
                    .sum()
                    .reset_index()
                )

                weekly[
                    "Cumulative P&L"
                ] = weekly["P&L"].cumsum()

                total_profit = weekly[
                    "P&L"
                ].sum()

                st.metric(
                    "Total USD P/L",
                    format_money(
                        total_profit,
                        currency
                    )
                )

                st.subheader(
                    "📊 Weekly USD P/L"
                )

                chart_data = weekly.set_index(
                    "Week"
                )[["P&L"]]

                st.bar_chart(
                    chart_data
                )

                st.subheader(
                    "📈 Cumulative USD P/L"
                )

                cumulative_data = weekly.set_index(
                    "Week"
                )[["Cumulative P&L"]]

                st.line_chart(
                    cumulative_data
                )

                st.subheader(
                    "📋 USD Weekly Statistics"
                )

                display_weekly = weekly.copy()

                display_weekly["P&L"] = (
                    display_weekly["P&L"]
                    .apply(
                        lambda x:
                        f"${x:,.2f}"
                    )
                )

                display_weekly[
                    "Cumulative P&L"
                ] = (
                    display_weekly[
                        "Cumulative P&L"
                    ]
                    .apply(
                        lambda x:
                        f"${x:,.2f}"
                    )
                )

                st.dataframe(
                    display_weekly,
                    use_container_width=True,
                    hide_index=True
                )

        # =================================================
        # INR
        # =================================================

        with tab_inr:

            currency = "INR (₹)"

            currency_df = df[
                df["Currency"] == currency
            ].copy()

            if currency_df.empty:

                st.info(
                    "No INR trades available."
                )

            else:

                weekly = (
                    currency_df
                    .groupby("Week")["P&L"]
                    .sum()
                    .reset_index()
                )

                weekly[
                    "Cumulative P&L"
                ] = weekly["P&L"].cumsum()

                total_profit = weekly[
                    "P&L"
                ].sum()

                st.metric(
                    "Total INR P/L",
                    format_money(
                        total_profit,
                        currency
                    )
                )

                st.subheader(
                    "📊 Weekly INR P/L"
                )

                chart_data = weekly.set_index(
                    "Week"
                )[["P&L"]]

                st.bar_chart(
                    chart_data
                )

                st.subheader(
                    "📈 Cumulative INR P/L"
                )

                cumulative_data = weekly.set_index(
                    "Week"
                )[["Cumulative P&L"]]

                st.line_chart(
                    cumulative_data
                )

                st.subheader(
                    "📋 INR Weekly Statistics"
                )

                display_weekly = weekly.copy()

                display_weekly["P&L"] = (
                    display_weekly["P&L"]
                    .apply(
                        lambda x:
                        f"₹{x:,.2f}"
                    )
                )

                display_weekly[
                    "Cumulative P&L"
                ] = (
                    display_weekly[
                        "Cumulative P&L"
                    ]
                    .apply(
                        lambda x:
                        f"₹{x:,.2f}"
                    )
                )

                st.dataframe(
                    display_weekly,
                    use_container_width=True,
                    hide_index=True
                )

        # =================================================
        # USDT
        # =================================================

        with tab_usdt:

            currency = "USDT"

            currency_df = df[
                df["Currency"] == currency
            ].copy()

            if currency_df.empty:

                st.info(
                    "No USDT trades available."
                )

            else:

                weekly = (
                    currency_df
                    .groupby("Week")["P&L"]
                    .sum()
                    .reset_index()
                )

                weekly[
                    "Cumulative P&L"
                ] = weekly["P&L"].cumsum()

                total_profit = weekly[
                    "P&L"
                ].sum()

                st.metric(
                    "Total USDT P/L",
                    format_money(
                        total_profit,
                        currency
                    )
                )

                st.subheader(
                    "📊 Weekly USDT P/L"
                )

                chart_data = weekly.set_index(
                    "Week"
                )[["P&L"]]

                st.bar_chart(
                    chart_data
                )

                st.subheader(
                    "📈 Cumulative USDT P/L"
                )

                cumulative_data = weekly.set_index(
                    "Week"
                )[["Cumulative P&L"]]

                st.line_chart(
                    cumulative_data
                )

                st.subheader(
                    "📋 USDT Weekly Statistics"
                )

                display_weekly = weekly.copy()

                display_weekly["P&L"] = (
                    display_weekly["P&L"]
                    .apply(
                        lambda x:
                        f"USDT {x:,.2f}"
                    )
                )

                display_weekly[
                    "Cumulative P&L"
                ] = (
                    display_weekly[
                        "Cumulative P&L"
                    ]
                    .apply(
                        lambda x:
                        f"USDT {x:,.2f}"
                    )
                )

                st.dataframe(
                    display_weekly,
                    use_container_width=True,
                    hide_index=True
                )
