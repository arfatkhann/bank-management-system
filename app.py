
import streamlit as st
import pandas as pd
from main import Bank


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="NovaBank | Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================== CUSTOM CSS ====================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--st-background-color, #f5f7fb);
    color: var(--st-text-color, #172033);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Theme-aware headings */
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4,
[data-testid="stMain"] p,
[data-testid="stMain"] label {
    color: var(--st-text-color, #172033);
}

[data-testid="stCaptionContainer"] p {
    color: var(--st-secondary-text-color, #64748b);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--st-background-color, #f5f7fb);
    border-right: 1px solid var(--st-border-color, #e2e8f0);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: var(--st-text-color, #172033);
}

/* Metric cards */
[data-testid="stMetric"] {
    background: var(--st-card-background-color, #ffffff);
    border: 1px solid var(--st-border-color, #e2e8f0);
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 4px 16px rgba(20, 35, 60, 0.04);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: var(--st-secondary-text-color, #64748b);
}

[data-testid="stMetricValue"] {
    color: var(--st-text-color, #172033);
    font-weight: 750;
}

/* Balance card */
.hero-card {
    background: linear-gradient(120deg, #172554, #3730a3, #6366f1);
    color: white !important;
    padding: 30px;
    border-radius: 22px;
    margin: 10px 0 25px;
    box-shadow: 0 12px 28px rgba(55, 48, 163, 0.18);
}

.hero-card * {
    color: white !important;
}

.hero-label {
    font-size: 13px;
    opacity: 0.85;
    letter-spacing: 1px;
}

.hero-balance {
    font-size: clamp(28px, 4vw, 40px);
    font-weight: 800;
    margin: 12px 0;
}

.hero-account {
    font-size: 13px;
    opacity: 0.9;
}

/* Generic cards */
.section-card {
    background: var(--st-card-background-color, #ffffff);
    color: var(--st-text-color, #172033);
    border: 1px solid var(--st-border-color, #e2e8f0);
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 16px;
}

.eyebrow {
    color: var(--st-secondary-text-color, #64748b);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

.small-muted {
    color: var(--st-secondary-text-color, #64748b);
    font-size: 12px;
}

/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    border-radius: 9px;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    border-radius: 10px;
    min-height: 43px;
    font-weight: 600;
}

/* Tables */
[data-testid="stDataFrame"] {
    border: 1px solid var(--st-border-color, #e2e8f0);
    border-radius: 12px;
    overflow: hidden;
}

hr {
    border-color: var(--st-border-color, #e2e8f0);
}

@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }

    .hero-card {
        padding: 22px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==================== SESSION STATE ====================

if "accounts" not in st.session_state:
    try:
        st.session_state.accounts = Bank.load_data()
    except (ValueError, OSError) as error:
        st.error(f"Database error: {error}")
        st.stop()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ==================== HELPER ====================

def heading(title, subtitle):
    st.title(title)
    st.caption(subtitle)


# ==================== CREATE ACCOUNT ====================

def create_account():
    heading(
        "Create your account",
        "Open your NovaBank demo account."
    )

    with st.form("create_account_form"):
        name = st.text_input("Full name")

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input(
                "Age",
                min_value=1,
                max_value=120,
                value=18
            )

        with col2:
            email = st.text_input("Email address")

        pin = st.text_input(
            "Create 4-digit PIN",
            type="password",
            max_chars=4
        )

        submitted = st.form_submit_button(
            "Create account →",
            type="primary",
            use_container_width=True
        )

    if submitted:
        try:
            account = Bank.create_account(
                st.session_state.accounts,
                name,
                age,
                email,
                pin
            )

            st.success("Account created successfully!")
            st.write("Your account number:")
            st.code(account["accountNo"])
            st.warning("Please save your account number.")

        except (ValueError, OSError) as error:
            st.error(str(error))


# ==================== LOGIN ====================

def login():
    heading(
        "Welcome back 👋",
        "Login to access your banking dashboard."
    )

    with st.form("login_form"):
        account_number = st.text_input("Account number")

        pin = st.text_input(
            "4-digit PIN",
            type="password",
            max_chars=4
        )

        submitted = st.form_submit_button(
            "Secure login →",
            type="primary",
            use_container_width=True
        )

    if submitted:
        account = Bank.authenticate(
            st.session_state.accounts,
            account_number,
            pin
        )

        if account:
            st.session_state.logged_in = account["accountNo"]
            st.session_state.page = "Dashboard"
            st.rerun()
        else:
            st.error("Invalid account number or PIN.")


# ==================== DASHBOARD ====================

def dashboard(account):
    heading(
        f"Welcome, {account['name'].split()[0]} 👋",
        "Here is your financial overview."
    )

    transactions = account.get("transactions", [])

    # Calculate total deposits and withdrawals
    deposits = sum(
        float(t["amount"])
        for t in transactions
        if t["type"] == "Deposit"
    )

    withdrawals = sum(
        float(t["amount"])
        for t in transactions
        if t["type"] == "Withdrawal"
    )

    # Total money moved through the account
    total_money_transacted = deposits + withdrawals

    # Balance card
    st.markdown(f"""
    <div class="hero-card">
        <div class="hero-label">AVAILABLE BALANCE</div>
        <div class="hero-balance">₹{account['balance']:,.2f}</div>
        <div class="hero-account">
            Account number: {account['accountNo']}
        </div>
        <div style="margin-top:20px;font-size:12px;opacity:0.85">
            NOVABANK · PERSONAL ACCOUNT
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Four summary cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Deposits",
        f"₹{deposits:,.2f}"
    )

    col2.metric(
        "Total Withdrawals",
        f"₹{withdrawals:,.2f}"
    )

    col3.metric(
        "Total Money Transacted",
        f"₹{total_money_transacted:,.2f}"
    )

    col4.metric(
        "Total Transactions",
        len(transactions)
    )

    st.write("")
    st.subheader("Quick actions")

    action1, action2, action3 = st.columns(3)

    with action1:
        if st.button("＋ Deposit money", use_container_width=True):
            st.session_state.page = "Deposit"
            st.rerun()

    with action2:
        if st.button("↗ Withdraw money", use_container_width=True):
            st.session_state.page = "Withdraw"
            st.rerun()

    with action3:
        if st.button("▤ View history", use_container_width=True):
            st.session_state.page = "Transactions"
            st.rerun()

    st.write("")
    st.subheader("Recent transactions")

    if transactions:
        recent = list(reversed(transactions[-5:]))

        for transaction in recent:
            is_deposit = transaction["type"] == "Deposit"
            symbol = "+" if is_deposit else "−"
            color = "#10b981" if is_deposit else "#ef4444"

            st.markdown(f"""
            <div class="section-card">
                <div style="display:flex;
                            justify-content:space-between;
                            align-items:center;
                            gap:12px;">
                    <div>
                        <strong>{transaction['type']}</strong>
                        <div class="small-muted">
                            {transaction.get('date', 'Date unavailable')}
                        </div>
                    </div>
                    <div style="font-weight:700;color:{color};">
                        {symbol}₹{float(transaction['amount']):,.2f}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No transactions yet.")


# ==================== DEPOSIT ====================

def deposit_page(account):
    heading(
        "Deposit money",
        "Add money to your demo account."
    )

    st.metric(
        "Current Balance",
        f"₹{account['balance']:,.2f}"
    )

    with st.form("deposit_form"):
        amount = st.number_input(
            "Deposit amount (₹)",
            min_value=0.0,
            max_value=10000.0,
            value=0.0,
            step=100.0
        )

        submitted = st.form_submit_button(
            "Confirm deposit",
            type="primary",
            use_container_width=True
        )

    if submitted:
        try:
            Bank.deposit(
                st.session_state.accounts,
                account,
                amount
            )
            st.success(f"₹{amount:,.2f} deposited successfully!")
            st.rerun()
        except (ValueError, OSError) as error:
            st.error(str(error))


# ==================== WITHDRAW ====================

def withdraw_page(account):
    heading(
        "Withdraw money",
        "Withdraw from your available balance."
    )

    st.metric(
        "Available Balance",
        f"₹{account['balance']:,.2f}"
    )

    with st.form("withdraw_form"):
        amount = st.number_input(
            "Withdrawal amount (₹)",
            min_value=0.0,
            value=0.0,
            step=100.0
        )

        submitted = st.form_submit_button(
            "Confirm withdrawal",
            type="primary",
            use_container_width=True
        )

    if submitted:
        try:
            Bank.withdraw(
                st.session_state.accounts,
                account,
                amount
            )
            st.success(f"₹{amount:,.2f} withdrawn successfully!")
            st.rerun()
        except (ValueError, OSError) as error:
            st.error(str(error))


# ==================== TRANSACTION HISTORY ====================

def transactions_page(account):
    heading(
        "Transaction history",
        "Review all your account activity."
    )

    transactions = account.get("transactions", [])

    if not transactions:
        st.info("No transactions to display.")
        return

    df = pd.DataFrame(list(reversed(transactions)))

    for column in ["amount", "balance"]:
        if column in df.columns:
            df[column] = df[column].apply(
                lambda value: f"₹{float(value):,.2f}"
            )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# ==================== SETTINGS ====================

def settings_page(account):
    heading(
        "Account settings",
        "Manage your personal information."
    )

    with st.form("settings_form"):
        name = st.text_input(
            "Full name",
            value=account["name"]
        )

        email = st.text_input(
            "Email address",
            value=account["email"]
        )

        new_pin = st.text_input(
            "New 4-digit PIN (optional)",
            type="password",
            max_chars=4
        )

        submitted = st.form_submit_button(
            "Save changes",
            type="primary",
            use_container_width=True
        )

    if submitted:
        try:
            Bank.update_account(
                st.session_state.accounts,
                account,
                name,
                email,
                new_pin
            )
            st.success("Account details updated!")
            st.rerun()
        except (ValueError, OSError) as error:
            st.error(str(error))

    st.divider()
    st.subheader("Danger zone")

    confirm = st.checkbox(
        "I understand that account deletion is permanent."
    )

    if st.button("Delete account"):
        if confirm:
            try:
                Bank.delete_account(
                    st.session_state.accounts,
                    account
                )
                st.session_state.logged_in = None
                st.session_state.page = "Dashboard"
                st.success("Account deleted successfully.")
                st.rerun()
            except OSError as error:
                st.error(f"Could not save changes: {error}")
        else:
            st.warning("Please confirm before deleting.")


# ==================== MAIN APP ====================

if st.session_state.logged_in is None:

    with st.sidebar:
        st.markdown("## 🏦 NovaBank")
        st.caption("PERSONAL BANKING")
        st.divider()

        auth_page = st.radio(
            "Get started",
            ["Login", "Create account"],
            label_visibility="collapsed"
        )

        st.divider()
        st.caption("Bank Management System · Demo")

    if auth_page == "Login":
        login()
    else:
        create_account()

else:
    account = next(
        (
            item for item in st.session_state.accounts
            if item["accountNo"] == st.session_state.logged_in
        ),
        None
    )

    if account is None:
        st.session_state.logged_in = None
        st.rerun()

    with st.sidebar:
        st.markdown("## 🏦 NovaBank")
        st.caption("PERSONAL BANKING")
        st.divider()

        st.markdown("### YOUR ACCOUNT")
        st.write(f"👤 {account['name']}")
        st.caption(f"Account: {account['accountNo']}")

        page = st.radio(
            "NAVIGATION",
            [
                "Dashboard",
                "Deposit",
                "Withdraw",
                "Transactions",
                "Settings"
            ],
            key="navigation"
        )

        st.divider()

        if st.button("↪ Logout", use_container_width=True):
            st.session_state.logged_in = None
            st.session_state.page = "Dashboard"
            st.rerun()

        st.caption("NovaBank Demo")

    # Display selected page
    if page == "Dashboard":
        dashboard(account)
    elif page == "Deposit":
        deposit_page(account)
    elif page == "Withdraw":
        withdraw_page(account)
    elif page == "Transactions":
        transactions_page(account)
    elif page == "Settings":
        settings_page(account)
