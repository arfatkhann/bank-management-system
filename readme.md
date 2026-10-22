# Northstar Bank — Streamlit learning project

A polished local demo of a bank management system using Python, Streamlit, and JSON.

## Run on Windows

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (optional but recommended):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

4. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

5. Start the app:

   ```powershell
   streamlit run app.py
   ```

Streamlit opens the app in your browser. The app creates `data.json` in this folder when the first account is saved.

## Features

- Dashboard and recent activity
- Create account with validation
- Unique demo account number
- Deposit and withdrawal with balance checks
- View and update account details
- Close an account only after its balance reaches zero
- Transaction history
- PIN hashes instead of plain-text PINs
- Attempts to migrate the original JSON list format

## Important limitations

This is a learning project, not a real banking system. SHA-256 alone is not an appropriate production PIN/password storage scheme; production software needs a password KDF, rate limiting, secure authentication, database transactions, authorization, audit controls, and other safeguards. JSON storage is not suitable for concurrent or real financial transactions. Do not store real customer or financial information here.
