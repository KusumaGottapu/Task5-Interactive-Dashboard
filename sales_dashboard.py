
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load dataset
df = pd.read_csv("sales_data.csv")

# Dashboard title
st.title("📊 Sales Analytics Dashboard")
st.write("Interactive Business Sales Performance Analysis")

# Sidebar filters
st.sidebar.header("Dashboard Filters")

products = st.sidebar.multiselect(
    "Select Products",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

regions = st.sidebar.multiselect(
    "Select Regions",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

categories = st.sidebar.multiselect(
    "Select Categories",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Filter dataset
filtered_df = df[
    (df["Product"].isin(products)) &
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories))
]

st.subheader("📌 Key Performance Indicators")

if not filtered_df.empty:

    total_sales = filtered_df["Sales"].sum()
    total_orders = filtered_df["Order_ID"].nunique()
    total_quantity = filtered_df["Quantity"].sum()
    average_sales = filtered_df["Sales"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"₹{total_sales:,.0f}")
    col2.metric("Total Orders", total_orders)
    col3.metric("Quantity Sold", total_quantity)
    col4.metric("Average Sales", f"₹{average_sales:,.0f}")

    st.divider()

    # Sales by Product
    st.subheader("Sales by Product")

    product_sales = (
        filtered_df.groupby("Product", as_index=False)["Sales"].sum()
    )

    fig1 = px.bar(
        product_sales,
        x="Product",
        y="Sales",
        color="Product",
        title="Product Sales Performance"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Sales by Region
    col5, col6 = st.columns(2)

    with col5:
        region_sales = (
            filtered_df.groupby("Region", as_index=False)["Sales"].sum()
        )

        fig2 = px.pie(
            region_sales,
            names="Region",
            values="Sales",
            title="Sales Distribution by Region"
        )

        st.plotly_chart(fig2, use_container_width=True)

    # Sales by Category
    with col6:
        category_sales = (
            filtered_df.groupby("Category", as_index=False)["Sales"].sum()
        )

        fig3 = px.bar(
            category_sales,
            x="Category",
            y="Sales",
            color="Category",
            title="Sales by Category"
        )

        st.plotly_chart(fig3, use_container_width=True)

    # Sales table
    st.subheader("📋 Sales Data")
    st.dataframe(filtered_df, use_container_width=True)

    # Business insights
    st.subheader("💡 Business Insights")

    best_product = product_sales.loc[
        product_sales["Sales"].idxmax(), "Product"
    ]

    best_region = region_sales.loc[
        region_sales["Sales"].idxmax(), "Region"
    ]

    st.write("🏆 Best Performing Product:", best_product)
    st.write("📍 Highest Sales Region:", best_region)
    st.write("💰 Total Revenue: ₹", f"{total_sales:,.0f}")

else:
    st.warning("No data available. Please select at least one filter.")

st.success("Dashboard loaded successfully!")
