# app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# ---------- DATABASE ----------
def get_db_connection():
    conn = sqlite3.connect("bank.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------- MODELS ----------
class Account(BaseModel):
    name: str
    ifsc_code: str
    balance: float


class Transaction(BaseModel):
    account_number: int
    amount: float
    type: str  # deposit / withdraw


# ---------- INIT DB ----------
def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            account_number INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            ifsc_code TEXT,
            balance REAL
        )
    """)
    conn.commit()
    conn.close()


init_db()


# ---------- ROUTES ----------

# Create account
@app.post("/accounts")
def create_account(account: Account):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO customers (name, ifsc_code, balance) VALUES (?, ?, ?)",
        (account.name, account.ifsc_code, account.balance)
    )

    conn.commit()
    acc_id = cursor.lastrowid
    conn.close()

    return {"message": "Account created", "account_number": acc_id}


# Get all accounts
@app.get("/accounts")
def get_accounts():
    conn = get_db_connection()
    accounts = conn.execute("SELECT * FROM customers").fetchall()
    conn.close()

    return [dict(acc) for acc in accounts]


# Get single account
@app.get("/accounts/{account_id}")
def get_account(account_id: int):
    conn = get_db_connection()
    acc = conn.execute(
        "SELECT * FROM customers WHERE account_number = ?",
        (account_id,)
    ).fetchone()
    conn.close()

    if acc is None:
        raise HTTPException(status_code=404, detail="Account not found")

    return dict(acc)


# Update account
@app.put("/accounts/{account_id}")
def update_account(account_id: int, account: Account):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE customers SET name=?, ifsc_code=?, balance=? WHERE account_number=?",
        (account.name, account.ifsc_code, account.balance, account_id)
    )

    conn.commit()
    conn.close()

    return {"message": "Account updated"}


# Delete account
@app.delete("/accounts/{account_id}")
def delete_account(account_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM customers WHERE account_number=?",
        (account_id,)
    )

    conn.commit()
    conn.close()

    return {"message": "Account deleted"}


# Transactions
@app.post("/transactions")
def transaction(txn: Transaction):
    conn = get_db_connection()
    cursor = conn.cursor()

    acc = cursor.execute(
        "SELECT * FROM customers WHERE account_number=?",
        (txn.account_number,)
    ).fetchone()

    if acc is None:
        raise HTTPException(status_code=404, detail="Account not found")

    balance = acc["balance"]

    if txn.type == "deposit":
        balance += txn.amount
    elif txn.type == "withdraw":
        if txn.amount > balance:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        balance -= txn.amount
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    cursor.execute(
        "UPDATE customers SET balance=? WHERE account_number=?",
        (balance, txn.account_number)
    )

    conn.commit()
    conn.close()

    return {"message": "Transaction successful", "new_balance": balance}