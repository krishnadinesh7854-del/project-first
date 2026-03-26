import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# --- DATABASE CONNECTION ----
engine = create_engine("postgresql+psycopg2://dinesh:VUgcYZp5hqNQFpgVlZINRvDpqmLYMvck@dpg-d6u0ifi4d50c73cje580-a.singapore-postgres.render.com:5432/phonepe_aiml_project")
conn = engine.connect()

#---- SIDEBAR ---
st.sidebar.title("📱 Navigation")
option = st.sidebar.selectbox("Select a page:", ["Home", "Analysis"])

# === HOME PAGE ===
if option == "Home":
    st.title("📊 PhonePe Transaction Insights")

    years = pd.read_sql('SELECT DISTINCT "Year" FROM aggregated_transaction ORDER BY "Year";', conn)
    year = st.selectbox("Select Year", years["Year"])

    query = """
        SELECT "State",
               SUM("Transaction_count") AS total_transactions,
               SUM("Transaction_amount") AS total_amount
        FROM "aggregated_transaction"
        WHERE "Year" = %s
        GROUP BY "State"
        ORDER BY total_transactions DESC;
    """
    df = pd.read_sql(query, conn, params=(year,))

    col1, col2 = st.columns(2)
    col1.plotly_chart(px.bar(df.head(10), x="State", y="total_transactions",
                             title="Top States by Transactions", text="total_transactions"),
                      use_container_width=True)
    col2.plotly_chart(px.bar(df.head(10), x="State", y="total_amount",
                             title="Top States by Amount", text="total_amount"),
                      use_container_width=True)

# == ANALYSIS PAGE ==
elif option == "Analysis":

    st.title("📊 Business Case Studies")

    opt = st.selectbox(
        "Choose Case Study",
        (
            "Decoding Transaction Dynamics on PhonePe",
            "Device Dominance and User Engagement Analysis",
            "Insurance Penetration and Growth Potential Analysis",
            "Transaction Analysis for Market Expansion",
            "User Engagement and Growth Strategy",
        ),
    )

    
    # CASE 1
    
    if opt == "Decoding Transaction Dynamics on PhonePe":

        st.header("State-wise Transaction Analysis")

        years = pd.read_sql('SELECT DISTINCT "Year" FROM aggregated_transaction ORDER BY "Year";', conn)
        year = st.selectbox("Select Year", years["Year"])

        states = pd.read_sql('SELECT DISTINCT "State" FROM aggregated_transaction;', conn)
        state = st.selectbox("Select State", states["State"])

        query = """
            SELECT "Quarter",
                   SUM("Transaction_count") AS total_transactions,
                   SUM("Transaction_amount") AS total_amount
            FROM "aggregated_transaction"
            WHERE "Year"=%s AND "State"=%s
            GROUP BY "Quarter"
            ORDER BY "Quarter";
        """
        df = pd.read_sql(query, conn, params=(year, state))

        col1, col2 = st.columns(2)
        col1.plotly_chart(px.line(df, x="Quarter", y="total_transactions",
                                  markers=True, title="Quarterly Transactions"),
                          use_container_width=True)
        col2.plotly_chart(px.line(df, x="Quarter", y="total_amount",
                                  markers=True, title="Quarterly Amount"),
                          use_container_width=True)

   
    # CASE 2
  
    elif opt == "Device Dominance and User Engagement Analysis":

        st.header("📱 Device & User Insights")

        years = pd.read_sql('SELECT DISTINCT "Year" FROM aggregated_user ORDER BY "Year";', conn)
        year = st.selectbox("Select Year", years["Year"])

        q1 = '''SELECT "Brand", SUM("Count") AS total_users
                FROM aggregated_user
                WHERE "Year"=%s
                GROUP BY "Brand"
                ORDER BY total_users DESC;'''
        df1 = pd.read_sql(q1, conn, params=(year,))
        st.plotly_chart(px.bar(df1, x="Brand", y="total_users", text="total_users",
                               title="Users by Device Brand"), use_container_width=True)

        q2 = '''SELECT "State","Brand", SUM("Count") AS users
                FROM aggregated_user
                WHERE "Year"=%s
                GROUP BY "State","Brand";'''
        df2 = pd.read_sql(q2, conn, params=(year,))
        state = st.selectbox("Select State", df2["State"].unique())
        df2 = df2[df2["State"] == state]
        st.plotly_chart(px.pie(df2, names="Brand", values="users",
                               hole=0.5, title="Brand Share"), use_container_width=True)

   
    # CASE 3
    
    elif opt == "Insurance Penetration and Growth Potential Analysis":

        st.header("🛡 Insurance Growth Insights")

        years = pd.read_sql('SELECT DISTINCT "Year" FROM aggregated_insurance ORDER BY "Year";', conn)
        year = st.selectbox("Select Year", years["Year"])

        q1 = '''SELECT "Quarter", SUM("Amount") AS total_amount
                FROM aggregated_insurance
                WHERE "Year"=%s
                GROUP BY "Quarter";'''
        df1 = pd.read_sql(q1, conn, params=(year,))
        st.plotly_chart(px.line(df1, x="Quarter", y="total_amount", markers=True,
                                title="Quarterly Insurance Growth"), use_container_width=True)

        q2 = '''SELECT "State", SUM("Amount") AS total_amount
                FROM aggregated_insurance
                WHERE "Year"=%s
                GROUP BY "State"
                ORDER BY total_amount DESC LIMIT 10;'''
        df2 = pd.read_sql(q2, conn, params=(year,))
        st.plotly_chart(px.bar(df2, x="State", y="total_amount", text="total_amount",
                               title="Top Insurance States"), use_container_width=True)

   
    # CASE 4
    
    elif opt == "Transaction Analysis for Market Expansion":

        st.header("🌍 Market Expansion Insights")

        years = pd.read_sql('SELECT DISTINCT "Year" FROM aggregated_transaction ORDER BY "Year";', conn)
        year = st.selectbox("Select Year", years["Year"])

        q1 = '''SELECT "State", SUM("Transaction_count") AS total_txns
                FROM aggregated_transaction
                WHERE "Year"=%s
                GROUP BY "State"
                ORDER BY total_txns DESC LIMIT 10;'''
        df1 = pd.read_sql(q1, conn, params=(year,))
        st.plotly_chart(px.bar(df1, x="State", y="total_txns", text="total_txns",
                               title="Top Transaction States"), use_container_width=True)

    
    # CASE 5
    
    elif opt == "User Engagement and Growth Strategy":

        st.header("📈 User Growth Strategy")

        years = pd.read_sql('SELECT DISTINCT "Year" FROM aggregated_user ORDER BY "Year";', conn)
        year = st.selectbox("Select Year", years["Year"])

        q1 = '''SELECT "State", SUM("Count") AS total_users
                FROM aggregated_user
                WHERE "Year"=%s
                GROUP BY "State"
                ORDER BY total_users DESC LIMIT 10;'''
        df1 = pd.read_sql(q1, conn, params=(year,))
        st.plotly_chart(px.bar(df1, x="State", y="total_users", text="total_users",
                               title="Top User States"), use_container_width=True)
        