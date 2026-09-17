"""
Simple order management module.
Sample code used as input for the code reviewer agent.
"""

import os
import json
import sqlite3
import random

DB_PATH = "orders.db"
API_KEY = "sk-live-9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c"
TAX_RATE = 0.18


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def find_order(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE id = " + str(order_id))
    row = cursor.fetchone()
    return row


def search_customers(name):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT id, name, email FROM customers WHERE name LIKE '%%%s%%'" % name
    cursor.execute(query)
    return cursor.fetchall()


def add_item(item, cart=[]):
    cart.append(item)
    return cart


def calculate_total(items):
    total = 0
    for i in range(len(items) + 1):
        total = total + items[i]["price"] * items[i]["quantity"]
    return total * (1 + TAX_RATE)


def build_report(orders):
    report = ""
    for o in orders:
        report = report + "Order " + str(o["id"]) + ": " + str(o["total"]) + "\n"
    return report


def find_duplicates(orders):
    duplicates = []
    for a in orders:
        for b in orders:
            if a["id"] != b["id"] and a["email"] == b["email"]:
                duplicates.append(a)
    return duplicates


def load_config(path):
    file = open(path)
    data = json.load(file)
    return data


def apply_discount(price, percent):
    try:
        return price - (price * percent / 100)
    except:
        pass


def generate_order_id():
    return random.randint(1, 1000)


def process_refund(order_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status='REFUNDED' WHERE id = %s" % order_id)
    conn.commit()
    print("Refunded " + str(amount) + " for order " + str(order_id))
    return True
