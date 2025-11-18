import os
import pymysql
from dotenv import load_dotenv
from few_shots import few_shots
from langchain_google_genai import GoogleGenerativeAI

load_dotenv()

# ------------------- DATABASE CONNECTION -------------------
def run_sql(query):
    conn = pymysql.connect(
        host="127.0.0.1",   # Force TCP, avoid socket issues
        port=3306,
        user="root",
        password="",        # Empty password for Codespaces MySQL
        database="global_tshirts"
    )
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    return result


# ------------------- GEMINI LLM (2.5 Flash) -------------------
llm = GoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.environ["GOOGLE_API_KEY"],
    temperature=0.1
)


# ------------------- MAIN CHAIN FUNCTION -------------------
def get_few_shot_db_chain():

    def chain(question):

        # -------- BUILD FEW-SHOT PROMPT BLOCK --------
        few_shot_text = ""
        for ex in few_shots:
            few_shot_text += (
                "\nQuestion: " + ex["Question"] +
                "\nSQLQuery: " + ex["SQLQuery"] +
                "\nSQLResult: " + ex["SQLResult"] +
                "\nAnswer: " + ex["Answer"] + "\n"
            )

        # -------- STEP 1: Generate SQL Query --------
        prompt = f"""
You are a MySQL expert.

Below are example Q&A pairs:
{few_shot_text}

Using the examples as a guide,
produce ONLY the SQLQuery for this new question:

Question: {question}

Return ONLY the SQL query text — 
no backticks, no ```sql blocks, no explanations, no labels.
"""

        raw_sql = llm.invoke(prompt)
        sql_query = str(raw_sql).strip()

        # ---- CLEAN SQL OUTPUT ----

        # Remove code fences
        sql_query = sql_query.replace("```sql", "")
        sql_query = sql_query.replace("```", "")
        sql_query = sql_query.strip()

        # Remove accidental labels
        if sql_query.lower().startswith("sqlquery:"):
            sql_query = sql_query[9:].strip()

        # Keep only from first SQL keyword
        for keyword in ["SELECT", "UPDATE", "DELETE", "INSERT"]:
            pos = sql_query.upper().find(keyword)
            if pos != -1:
                sql_query = sql_query[pos:]
                break

        print("\nGenerated SQL:", sql_query)

        # -------- STEP 2: Execute SQL Query --------
        try:
            sql_result = run_sql(sql_query)
        except Exception as e:
            return "SQL ERROR: " + str(e)

        # -------- STEP 3: Convert SQL Result → Final Answer --------
        answer_prompt = f"""
Question: {question}
SQLQuery: {sql_query}
SQLResult: {sql_result}

Provide the final answer in one short sentence.
"""

        final_answer = llm.invoke(answer_prompt)
        return final_answer

    return chain
