import streamlit as st
from google import genai
from database_utils import load_csv_to_db, get_schema_details, execute_query
from sql import clean_ai_sql
# --- CONFIG ---
MODEL_ID = "gemini-3-flash-preview" 
API_KEY = "AIzaSyCoeyFXIPgPi5mW3Bg1KjfnF_Yioxhbvvs"
client = genai.Client(api_key=API_KEY)
DB_PATH = "library_data.db"
CSV_FILE = "electronics_data.csv"  # Ensure your 3k+ CSV is in the same folder!

st.set_page_config(page_title="Library SQL Agent", layout="wide")
st.title("📚 Product Library AI Analyst")

# 1. Initialize the Library
try:
    cols = load_csv_to_db(CSV_FILE, DB_PATH)
    st.sidebar.success(f"Library Loaded: {CSV_FILE}")
    st.sidebar.write(f"Indexed Columns: {', '.join(cols)}")
except FileNotFoundError:
    st.error(f"Error: Could not find '{CSV_FILE}' in the folder.")
    st.stop()

# 2. Get AI Context
schema = get_schema_details(DB_PATH)

user_query = st.text_input("Search or analyze your library:", "How many products are in each category?")

if user_query:
    # 1. Define the history/context FIRST
    history = f"System: Use this schema to write SQLite queries: {schema}\nUser: {user_query}"

# 2. NOW start the loop
    for attempt in range(3):
        with st.status(f"Analyst Thinking (Attempt {attempt+1})...") as status:
        # Pylance is happy now because 'history' exists!
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=f"{history}\n\nInstruction: Provide ONLY raw SQL code."
        )
    # NEW: Apply the cleaner here
    raw_response = response.text
    sql = clean_ai_sql(raw_response)

    # Now execute the cleaned query
    result = execute_query(DB_PATH, sql)
    history = f"You are an expert analyst. The table is called 'library'. Schema: {schema}"
    
    with st.status("Searching library...") as status:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=f"{history}\n\nUser Question: {user_query}\n\nInstruction: Provide ONLY raw SQLite code."
        )
        sql = response.text.replace("```sql", "").replace("```", "").strip()
        
        result = execute_query(DB_PATH, sql)
        
        if isinstance(result, str) and "SQL_ERROR" in result:
            status.update(label="Retrying logic...", state="error")
            # (Self-healing logic could go here)
            st.error(result)
        else:
            status.update(label="Found it!", state="complete")
            st.subheader("Analysis View")
            
            c1, c2 = st.columns([1, 1])
            with c1:
                st.dataframe(result, use_container_width=True)
            with c2:
                if not result.empty and len(result.columns) >= 2:
                    st.bar_chart(result, x=result.columns[0], y=result.columns[1])
            
            with st.expander("Show SQL Code"):
                st.code(sql, language="sql")