import streamlit as st
import pandas as pd
import plotly.express as px
import os

from data import TRENDS, INVENTORY, PRICING, WHOLESALERS, get_forecast_data, get_sales_history, CATEGORIES

st.set_page_config(page_title="Trendora", layout="wide")

if "step" not in st.session_state:
    st.session_state.step = "home"

if "role" not in st.session_state:
    st.session_state.role = ""

if "owner_profile" not in st.session_state:
    st.session_state.owner_profile = {}

if "wholesaler_profile" not in st.session_state:
    st.session_state.wholesaler_profile = {}

if "inventory" not in st.session_state:
    st.session_state.inventory = INVENTORY.copy()

if "wholesaler_products" not in st.session_state:
    st.session_state.wholesaler_products = []

if "messages" not in st.session_state:
    st.session_state.messages = []


def show_logo():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        try:
            st.image("Assets/images/logos/image.png", width=280)
        except Exception:
            pass


def home():
    show_logo()

    st.markdown("<h1 style='text-align:center;color:#D4AF37;'>Trendora</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>Your Smart Fashion Business Partner</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Trends. Inventory. Growth.</p>", unsafe_allow_html=True)

    st.divider()

    if st.button("Get Started", use_container_width=True):
        st.session_state.step = "choose_role"
        st.rerun()


def choose_role():
    st.title("Choose Your Role")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Business Owner", use_container_width=True):
            st.session_state.role = "owner"
            st.session_state.step = "owner_signup"
            st.rerun()

    with col2:
        if st.button("Wholesaler", use_container_width=True):
            st.session_state.role = "wholesaler"
            st.session_state.step = "wholesaler_signup"
            st.rerun()


def owner_signup():
    st.title("Business Owner Registration")

    email = st.text_input("Email")
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    phone = st.text_input("Phone Number")

    st.subheader("Business Details")

    business_name = st.text_input("Business Name")
    business_type = st.selectbox("Type of Business", ["Clothing", "Footwear", "Jewellery", "Mixed Fashion Store"])
    location = st.text_input("Location")

    if st.button("Create Owner Account", use_container_width=True):
        if email == "" or name == "" or password == "" or phone == "" or business_name == "" or location == "":
            st.error("Please fill all fields.")
        else:
            st.session_state.owner_profile = {
                "email": email,
                "name": name,
                "phone": phone,
                "business_name": business_name,
                "business_type": business_type,
                "location": location,
            }
            st.session_state.step = "owner_dashboard"
            st.rerun()


def wholesaler_signup():
    st.title("Wholesaler Registration")

    email = st.text_input("Email")
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    phone = st.text_input("Phone Number")

    st.subheader("Business Details")

    business_name = st.text_input("Business Name")
    business_type = st.selectbox("Type of Business", ["Clothing Supplier", "Footwear Supplier", "Jewellery Supplier", "Mixed Wholesaler"])
    location = st.text_input("Location")

    if st.button("Create Wholesaler Account", use_container_width=True):
        if email == "" or name == "" or password == "" or phone == "" or business_name == "" or location == "":
            st.error("Please fill all fields.")
        else:
            st.session_state.wholesaler_profile = {
                "email": email,
                "name": name,
                "phone": phone,
                "business_name": business_name,
                "business_type": business_type,
                "location": location,
            }
            st.session_state.step = "wholesaler_dashboard"
            st.rerun()


def owner_sidebar():
    page = st.sidebar.radio(
        "Business Owner Menu",
        ["Dashboard", "Trends", "Inventory", "Pricing", "Forecast", "Wholesalers", "Messages", "Profile"]
    )

    if st.sidebar.button("Logout"):
        st.session_state.step = "home"
        st.rerun()

    return page


def owner_dashboard():
    page = owner_sidebar()

    if page == "Dashboard":
        dashboard_page()
    elif page == "Trends":
        trends_page()
    elif page == "Inventory":
        inventory_page()
    elif page == "Pricing":
        pricing_page()
    elif page == "Forecast":
        forecast_page()
    elif page == "Wholesalers":
        wholesalers_page()
    elif page == "Messages":
        owner_messages_page()
    elif page == "Profile":
        owner_profile_page()


def dashboard_page():
    st.title("Business Owner Dashboard")

    inventory_df = pd.DataFrame(st.session_state.inventory)
    trends_df = pd.DataFrame(TRENDS)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Products", len(inventory_df))
    c2.metric("Reorder Alerts", len(inventory_df[inventory_df["status"] == "REORDER NOW"]))
    c3.metric("Dead Stock", len(inventory_df[inventory_df["status"] == "DEAD STOCK"]))
    c4.metric("Avg Trend Heat", int(trends_df["heat"].mean()))

    st.divider()

    st.subheader("Trending This Week")

    cols = st.columns(4)

    for i, trend in enumerate(TRENDS[:4]):
        with cols[i]:
            st.success(f"{trend['name']}\n\nHeat: {trend['heat']} | {trend['direction']}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Inventory Status")
        status_count = inventory_df["status"].value_counts().reset_index()
        status_count.columns = ["Status", "Count"]
        fig = px.pie(status_count, values="Count", names="Status", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Trend Heat")
        fig = px.bar(trends_df, x="name", y="heat", color="urgency")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Smart Alerts")

    for item in st.session_state.inventory:
        if item["status"] == "REORDER NOW":
            st.warning(f"{item['name']} needs reorder. Quantity left: {item['qty']}")

        if item["status"] == "DEAD STOCK":
            st.error(f"{item['name']} is dead stock. Consider clearance sale.")


def trends_page():
    st.title("Fashion Trends")

    category = st.selectbox("Filter Category", CATEGORIES)

    filtered = TRENDS

    if category != "All":
        filtered = [t for t in TRENDS if t["category"] == category]

    for trend in filtered:
        st.markdown("---")

        col1, col2 = st.columns([3, 1])

        with col1:
            st.subheader(trend["name"])
            st.write(trend["description"])
            st.write(f"Category: {trend['category']}")
            st.write(f"City: {trend['city']}")
            st.write(f"Tags: {', '.join(trend['tags'])}")

        with col2:
            st.metric("Heat", trend["heat"])
            st.write(trend["direction"])
            st.write(f"Change: {trend['change']}")
            st.write(f"Urgency: {trend['urgency']}")


def inventory_page():
    st.title("Inventory Management")

    st.subheader("Add New Product")

    product_name = st.text_input("Product Name")
    category = st.selectbox("Category", ["Tops", "Bottoms", "Dresses", "Sets", "Outerwear", "Jewellery", "Footwear"])
    qty = st.number_input("Quantity", min_value=0, step=1)
    reorder_point = st.number_input("Reorder Point", min_value=0, step=1)
    cost = st.number_input("Cost Price", min_value=0)
    selling_price = st.number_input("Selling Price", min_value=0)
    image = st.file_uploader("Upload Product Image", type=["png", "jpg", "jpeg"])

    if st.button("Add Product", use_container_width=True):
        if product_name == "":
            st.error("Please enter product name.")
        else:
            image_path = ""

            if image is not None:
                os.makedirs("Uploads", exist_ok=True)
                image_path = os.path.join("Uploads", f"{len(st.session_state.inventory)+1}_{image.name}")
                with open(image_path, "wb") as f:
                    f.write(image.getbuffer())

            status = "HEALTHY"

            if qty == 0:
                status = "OUT OF STOCK"
            elif qty <= reorder_point:
                status = "REORDER NOW"

            new_product = {
                "sku": f"SKU-{len(st.session_state.inventory)+1}",
                "name": product_name,
                "qty": qty,
                "reorder_point": reorder_point,
                "cost": cost,
                "selling_price": selling_price,
                "status": status,
                "category": category,
                "trend_alignment": 50,
                "image_path": image_path,
            }

            st.session_state.inventory.append(new_product)
            st.success("Product added successfully.")
            st.rerun()

    st.divider()

    st.subheader("Current Inventory")

    search = st.text_input("Search Inventory")

    for index, item in enumerate(st.session_state.inventory):
        if search.lower() not in item["name"].lower():
            continue

        st.markdown("---")

        col1, col2 = st.columns([1, 4])

        with col1:
            if item.get("image_path", "") and os.path.exists(item["image_path"]):
                st.image(item["image_path"], width=140)
            else:
                st.write("No Image")

        with col2:
            st.subheader(item["name"])
            st.write(f"SKU: {item['sku']}")
            st.write(f"Category: {item['category']}")
            st.write(f"Quantity: {item['qty']}")
            st.write(f"Selling Price: ₹{item['selling_price']}")
            st.write(f"Status: {item['status']}")

            if item["qty"] == 0:
                st.error("Out of Stock")
            elif item["qty"] <= item["reorder_point"]:
                st.warning("Low Stock")
            else:
                st.success("In Stock")

            if st.button(f"Edit {item['sku']}", key=f"edit_{index}"):
                st.session_state[f"edit_{index}"] = True

            if st.session_state.get(f"edit_{index}", False):
                new_qty = st.number_input("Update Quantity", min_value=0, value=int(item["qty"]), key=f"qty_{index}")
                new_price = st.number_input("Update Selling Price", min_value=0, value=int(item["selling_price"]), key=f"price_{index}")

                if st.button("Save Changes", key=f"save_{index}"):
                    st.session_state.inventory[index]["qty"] = new_qty
                    st.session_state.inventory[index]["selling_price"] = new_price

                    if new_qty == 0:
                        st.session_state.inventory[index]["status"] = "OUT OF STOCK"
                    elif new_qty <= item["reorder_point"]:
                        st.session_state.inventory[index]["status"] = "REORDER NOW"
                    else:
                        st.session_state.inventory[index]["status"] = "HEALTHY"

                    st.session_state[f"edit_{index}"] = False
                    st.success("Updated successfully.")
                    st.rerun()

            if st.button(f"Delete {item['sku']}", key=f"delete_{index}"):
                st.session_state.inventory.pop(index)
                st.success("Deleted successfully.")
                st.rerun()


def pricing_page():
    st.title("Pricing Recommendations")

    df = pd.DataFrame(PRICING)
    st.dataframe(df, use_container_width=True)

    fig = px.bar(df, x="product", y=["your_price", "market_avg", "suggested"], barmode="group")
    st.plotly_chart(fig, use_container_width=True)


def forecast_page():
    st.title("Demand Forecast")

    forecast = get_forecast_data()
    df = pd.DataFrame(forecast)

    st.dataframe(df, use_container_width=True)

    fig = px.line(df, x="weeks", y=df.columns[1:], markers=True)
    st.plotly_chart(fig, use_container_width=True)

    sales = get_sales_history()

    st.subheader("Sales History")
    fig2 = px.line(sales, x="date", y="revenue", markers=True)
    st.plotly_chart(fig2, use_container_width=True)


def wholesalers_page():
    st.title("Wholesalers")

    for wholesaler in WHOLESALERS:
        st.markdown("---")
        st.subheader(wholesaler["name"])
        st.write(f"City: {wholesaler['city']}")
        st.write(f"Rating: {wholesaler['rating']}")
        st.write(f"Speciality: {wholesaler['speciality']}")
        st.write(f"Products: {', '.join(wholesaler['products'])}")

        msg = st.text_area(f"Message to {wholesaler['name']}", key=f"msg_{wholesaler['name']}")

        if st.button(f"Send Message to {wholesaler['name']}", key=f"send_{wholesaler['name']}"):
            if msg == "":
                st.error("Please enter a message.")
            else:
                st.session_state.messages.append({
                    "to": wholesaler["name"],
                    "from": st.session_state.owner_profile.get("business_name", "Business Owner"),
                    "message": msg
                })
                st.success("Message sent.")


def owner_messages_page():
    st.title("Sent Messages")

    if len(st.session_state.messages) == 0:
        st.info("No messages sent yet.")
    else:
        for msg in st.session_state.messages:
            st.markdown("---")
            st.write(f"To: {msg['to']}")
            st.write(f"From: {msg['from']}")
            st.write(f"Message: {msg['message']}")


def owner_profile_page():
    st.title("Business Owner Profile")

    profile = st.session_state.owner_profile

    st.write(f"Name: {profile.get('name', '')}")
    st.write(f"Email: {profile.get('email', '')}")
    st.write(f"Phone: {profile.get('phone', '')}")
    st.write(f"Business Name: {profile.get('business_name', '')}")
    st.write(f"Business Type: {profile.get('business_type', '')}")
    st.write(f"Location: {profile.get('location', '')}")

    st.divider()

    st.subheader("Edit Profile")

    new_name = st.text_input("Edit Name", value=profile.get("name", ""))
    new_phone = st.text_input("Edit Phone", value=profile.get("phone", ""))
    new_business = st.text_input("Edit Business Name", value=profile.get("business_name", ""))
    new_location = st.text_input("Edit Location", value=profile.get("location", ""))

    if st.button("Save Profile", use_container_width=True):
        st.session_state.owner_profile["name"] = new_name
        st.session_state.owner_profile["phone"] = new_phone
        st.session_state.owner_profile["business_name"] = new_business
        st.session_state.owner_profile["location"] = new_location
        st.success("Profile updated.")


def wholesaler_dashboard():
    st.sidebar.title("Wholesaler Menu")

    page = st.sidebar.radio("Navigation", ["Dashboard", "Products", "Messages", "Profile"])

    if st.sidebar.button("Logout"):
        st.session_state.step = "home"
        st.rerun()

    if page == "Dashboard":
        st.title("Wholesaler Dashboard")
        st.metric("Uploaded Products", len(st.session_state.wholesaler_products))
        st.metric("Messages Received", len(st.session_state.messages))

    elif page == "Products":
        st.title("Upload Products")

        product_name = st.text_input("Product Name")
        category = st.selectbox("Category", ["Tops", "Bottoms", "Dresses", "Sets", "Outerwear", "Jewellery", "Footwear"])
        price = st.number_input("Price per Unit", min_value=0)
        moq = st.number_input("Minimum Order Quantity", min_value=0, step=1)

        if st.button("Add Product", use_container_width=True):
            if product_name == "":
                st.error("Please enter product name.")
            else:
                st.session_state.wholesaler_products.append({
                    "name": product_name,
                    "category": category,
                    "price": price,
                    "moq": moq,
                    "wholesaler": st.session_state.wholesaler_profile.get("business_name", "Wholesaler")
                })
                st.success("Product uploaded.")

        st.divider()

        for item in st.session_state.wholesaler_products:
            st.write(item)

    elif page == "Messages":
        st.title("Messages Received")

        found = False

        for msg in st.session_state.messages:
            if msg["to"] == st.session_state.wholesaler_profile.get("business_name", ""):
                found = True
                st.markdown("---")
                st.write(f"From: {msg['from']}")
                st.write(f"Message: {msg['message']}")

        if not found:
            st.info("No messages yet.")

    elif page == "Profile":
        st.title("Wholesaler Profile")
        profile = st.session_state.wholesaler_profile

        st.write(f"Name: {profile.get('name', '')}")
        st.write(f"Email: {profile.get('email', '')}")
        st.write(f"Phone: {profile.get('phone', '')}")
        st.write(f"Business Name: {profile.get('business_name', '')}")
        st.write(f"Business Type: {profile.get('business_type', '')}")
        st.write(f"Location: {profile.get('location', '')}")


if st.session_state.step == "home":
    home()

elif st.session_state.step == "choose_role":
    choose_role()

elif st.session_state.step == "owner_signup":
    owner_signup()

elif st.session_state.step == "wholesaler_signup":
    wholesaler_signup()

elif st.session_state.step == "owner_dashboard":
    owner_dashboard()

elif st.session_state.step == "wholesaler_dashboard":
    wholesaler_dashboard()