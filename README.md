# 🧠 Natural Language to SQL Chatbot

The **NL-to-SQL Chatbot** is a web-based assistant that allows users to query **MySQL databases** using **plain English**.  
Instead of writing SQL manually, users can simply ask questions, and the chatbot will:  

1. **Understand** the natural language input.  
2. **Generate SQL queries** using an AI model (Google Gemini).  
3. **Execute queries** on the connected MySQL database.  
4. **Display results** in an interactive, user-friendly table.  
5. Provide a **one-click copy button** for generated SQL queries.  

---

## 🚀 Features
- 🔹 **Natural Language Querying** – “Show me all employees in the Sales department” → generates SQL.  
- 🔹 **MySQL Database Access** – Works with any schema inside MySQL (switch databases via connection string).  
- 🔹 **Interactive Chat Interface** – Conversation-style Q&A with query history.  
- 🔹 **Schema Awareness** – Displays MySQL schema (tables + columns) for guidance.  
- 🔹 **Copy SQL** – One-click copy button (📋 → ✅) on each generated SQL block.  
- 🔹 **Result Visualization** – Clean tabular results with auto-formatting.  
- 🔹 **Error Handling** – Clear feedback for invalid queries or DB issues.  

---

## 🛠️ Tech Stack
- **Frontend**: React (Vite) + TailwindCSS  
- **Backend**: Flask / FastAPI (Python)  
- **Database**: MySQL  
- **AI Model**: Google Gemini (e.g., `gemini-1.5-pro` / `gemini-1.5-flash`)  

---

## 💡 Example Queries
- “Show me all records from the employees table.”  
- “Count how many orders were placed last month.”  
- “Find the top 5 customers by total salary.”  
- “List products with inventory less than 10.”  
- “Get the average salary by department.”  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/sakshi-kolawale/NL-to-SQL-Chatbot.git
cd nl-to-sql-chatbot
