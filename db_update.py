import streamlit as st
import pandas as pd
import plotly.express as px
from db_helper import insert_expenses, fetch_expenses_for_date, delete_expenses_for_date, fetch_expense_summery, fetch_expenses_by_month_range  # Import only needed functions

st.set_page_config(page_title="Expense Manager", layout="wide")

st.title("💰 Expense Manager")

# Create tabs
tab1, tab2 = st.tabs(["Add/Update Expense", "Expense Analysis"])

# -------------------------------------------
# 📋 Tab 1: Database Updates (Add/Delete)
# -------------------------------------------
with tab1:
    st.header("Manage Expenses")

    # Columns for better layout
    col1, col2 = st.columns(2)

    # ➕ Add Expense Form
    with col1:
        st.subheader("Add/Update Expense")
        date = st.date_input("Expense Date")
        amount = st.number_input("Amount", min_value=0.01, format="%.2f")
        category = st.text_input("Category")
        notes = st.text_area("Notes")

        if st.button("Add Expense"):
            if date and amount and category:
                insert_expenses(str(date), amount, category, notes)
                st.success("Expense added successfully! ✅")
            else:
                st.error("Please fill in all required fields!")

    # 🗑️ Delete Expenses
    with col2:
        st.subheader("Delete Expenses")
        date_to_delete = st.date_input("Select Date to Delete Expenses")

        if st.button("Delete Expenses"):
            delete_expenses_for_date(str(date_to_delete))
            st.success(f"All expenses for {date_to_delete} have been deleted!")

# -------------------------------------------
# 📊 Tab 2: Expense Analysis
# -------------------------------------------
with tab2:
    st.header("Expense Analysis")

    # Create sub-tabs
    analysis_option = st.radio("Select Analysis Type:", ["Date Range", "Month Range"])

    # 📅 Date Range Analysis
    if analysis_option == "Date Range":
        st.subheader("Analyze Expenses for a Date Range")
        col1, col2 = st.columns(2)

        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")

        if st.button("Analyze Date Range"):
            data = fetch_expense_summery(str(start_date), str(end_date))

            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)

                # 📊 Bar Chart
                fig_bar = px.bar(df, x="category", y="total", title="Total Expenses by Category", color="category")
                st.plotly_chart(fig_bar, use_container_width=True)

                # 🥧 Pie Chart
                fig_pie = px.pie(df, names="category", values="total", title="Expense Distribution")
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.warning("No expenses found in the selected range.")

    # 📆 Month Range Analysis
    if analysis_option == "Month Range":
        st.subheader("Analyze Expenses for a Month Range")

        col1, col2 = st.columns(2)

        months = {
            "January": "01", "February": "02", "March": "03", "April": "04",
            "May": "05", "June": "06", "July": "07", "August": "08",
            "September": "09", "October": "10", "November": "11", "December": "12"
        }

        with col1:
            start_month = st.selectbox("Start Month", list(months.keys()))
            start_year = st.number_input("Start Year", min_value=2000, max_value=2050, step=1, value=2024)

        with col2:
            end_month = st.selectbox("End Month", list(months.keys()))
            end_year = st.number_input("End Year", min_value=2000, max_value=2050, step=1, value=2024)

        # ✅ Correcting date format for the query
        start_date = f"{start_year}-{months[start_month]}"  # YYYY-MM format
        end_date = f"{end_year}-{months[end_month]}"  # YYYY-MM format

        if st.button("Analyze Month Range"):
            month_data = fetch_expenses_by_month_range(start_date, end_date)  # ✅ Call function from db_helper.py

            if month_data:
                df = pd.DataFrame(month_data)
                st.dataframe(df)

                # 📊 Bar Chart
                fig_bar_month = px.bar(df, x="category", y="total", title="Total Expenses",
                                       color="category")
                st.plotly_chart(fig_bar_month, use_container_width=True)

                # 🥧 Pie Chart
                fig_pie_month = px.pie(df, names="category", values="total", title="Expense Distribution")
                st.plotly_chart(fig_pie_month, use_container_width=True)
            else:
                st.warning("No expenses found in the selected month range.")