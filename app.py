
import streamlit as st
import json
import os

DB_FILE = "users.json"
PRODUCTS_FILE = "products.json"
ORDERS_FILE = "orders.json"

def init_files():
    for file in [DB_FILE, PRODUCTS_FILE, ORDERS_FILE]:
        if not os.path.exists(file):
            with open(file, "w") as f:
                json.dump({}, f)

def load_data(file):
    with open(file, "r") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def signup():
    st.subheader("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Manufacturer", "Wholesaler", "Retailer", "User"])
    if st.button("Sign Up"):
        users = load_data(DB_FILE)
        if username in users:
            st.warning("Username already exists!")
        else:
            users[username] = {"password": password, "role": role}
            save_data(DB_FILE, users)
            st.success("Signed up successfully! Please log in.")

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        users = load_data(DB_FILE)
        if username in users and users[username]["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = users[username]["role"]
            st.success(f"Welcome {username} ({users[username]['role']})!")
        else:
            st.error("Invalid credentials!")

def add_product():
    st.subheader("Add Product")
    name = st.text_input("Product Name")
    qty = st.number_input("Quantity", min_value=1)
    if st.button("Add Product"):
        products = load_data(PRODUCTS_FILE)
        products[name] = products.get(name, 0) + qty
        save_data(PRODUCTS_FILE, products)
        st.success(f"Added {qty} of {name}")

def place_order():
    st.subheader("Place Order")
    products = load_data(PRODUCTS_FILE)
    if not products:
        st.info("No products available")
        return
    product = st.selectbox("Select Product", list(products.keys()))
    qty = st.number_input("Quantity", min_value=1)
    if st.button("Order"):
        if products[product] >= qty:
            products[product] -= qty
            save_data(PRODUCTS_FILE, products)
            orders = load_data(ORDERS_FILE)
            user_orders = orders.get(st.session_state["username"], [])
            user_orders.append({"product": product, "quantity": qty})
            orders[st.session_state["username"]] = user_orders
            save_data(ORDERS_FILE, orders)
            st.success("Order placed!")
        else:
            st.error("Not enough stock")

def main():
    st.title("Inventory Management System")

    init_files()

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"]:
        st.sidebar.write(f"Logged in as: {st.session_state['username']} ({st.session_state['role']})")
        if st.sidebar.button("Logout"):
            st.session_state["logged_in"] = False
            st.experimental_rerun()

        if st.session_state["role"] == "Manufacturer":
            add_product()
        else:
            place_order()
    else:
        action = st.sidebar.radio("Choose Action", ["Login", "Sign Up"])
        if action == "Login":
            login()
        else:
            signup()

if __name__ == "__main__":
    main()
