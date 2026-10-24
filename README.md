# 🤖 AI-Powered Text-to-SQL Generator using RAG

A production-ready application that converts natural language questions into executable SQL queries using **Retrieval-Augmented Generation (RAG)** and **Large Language Models (LLMs)**.

## 🌟 Key Features

- **Natural Language to SQL**: Ask questions in plain English, get accurate SQL queries
- **RAG Architecture**: Database schema is injected into LLM context for accurate query generation
- **Safety-First Design**: Only read-only SELECT queries are allowed
- **Interactive Web UI**: Built with Streamlit for a clean, responsive interface
- **Real-time Execution**: Queries are executed instantly with results displayed in tables
- **Natural Language Summaries**: AI-generated explanations of query results
- **Sample Business Database**: Pre-populated with Customers, Products, and Orders data

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Interface (Streamlit)                  │
│                    "Show top 3 customers by sales"              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SQL Generator (RAG Engine)                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  1. Retrieve Database Schema (Tables, Columns, Keys)   │    │
│  │  2. Inject Schema into LLM Prompt                      │    │
│  │  3. Generate SQL with Context                          │    │
│  └────────────────────────────────────────────────────────┘    │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Query Validator & Executor                    │
│              (Safety checks + SQLite execution)                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Results Display & Summary                      │
│          (Data table + AI-generated explanation)                │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Database Schema

The application includes a sample business database with three tables:

### **Customers**
- customer_id (PRIMARY KEY)
- name
- email
- region (North, South, East, West)
- registration_date

### **Products**
- product_id (PRIMARY KEY)
- product_name
- category (Electronics, Furniture)
- price
- stock_quantity

### **Orders**
- order_id (PRIMARY KEY)
- customer_id (FOREIGN KEY → Customers)
- product_id (FOREIGN KEY → Products)
- quantity
- order_date
- total_amount

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd text-to-sql-generator
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy the example env file
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 5: Initialize Database
```bash
python database.py
```

This creates `business_data.db` and populates it with sample data.

### Step 6: Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 💡 Example Questions

Try asking these questions:

- "Show me the top 5 customers who spent the most money"
- "What are the total sales by region?"
- "List all products with low stock (less than 50 units)"
- "What are the most popular product categories?"
- "Show me the average order value by customer"
- "Which customers haven't made any orders?"
- "What's the total revenue from electronics?"
- "Show me all orders from September 2023"

## 📁 Project Structure

```
text-to-sql-generator/
│
├── app.py                 # Streamlit web application (main entry point)
├── database.py            # Database initialization and management
├── sql_generator.py       # SQL generation using LangChain + OpenAI
│
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # This file
│
└── business_data.db      # SQLite database (created after initialization)
```

## 🔧 How It Works

### 1. **Schema Retrieval (RAG Component)**
When you ask a question, the system first retrieves the complete database schema:
```python
schema_info = db.get_schema_info()
```

### 2. **Context Injection**
The schema is injected into the LLM prompt as context:
```python
prompt = f"""
You are an expert SQL analyst. Given this database schema:
{schema_info}

Generate SQL for: {user_question}
"""
```

### 3. **SQL Generation**
LangChain orchestrates the LLM call to generate accurate SQL:
```python
sql_query = generator.generate_sql(user_question)
```

### 4. **Safety Validation**
Before execution, queries are validated:
- Must be SELECT statements only
- No DROP, DELETE, INSERT, UPDATE operations
- Syntax checking

### 5. **Execution & Display**
Query is executed against SQLite and results are displayed in a formatted table.

### 6. **AI Summary**
The LLM generates a natural language explanation of the results.

## 🛡️ Security Features

- **Read-Only Operations**: Only SELECT queries are allowed
- **Query Validation**: Automatic safety checks before execution
- **No Schema Modifications**: Database structure cannot be changed through the UI
- **Safe Execution Context**: All queries run in a controlled SQLite environment

## 🔑 API Key Management

Your OpenAI API key should be stored in the `.env` file:

```env
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_MODEL=gpt-4-turbo-preview  # Optional: change model
```

**Never commit your `.env` file to version control!** It's already included in `.gitignore`.

## 🧪 Testing

Test the SQL generator independently:
```bash
python sql_generator.py
```

Test database operations:
```bash
python database.py
```

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure `.env` file exists in project root
- Check that the key is correctly formatted: `OPENAI_API_KEY=sk-...`
- Restart the Streamlit application after adding the key

### Database Not Found
- Run `python database.py` to initialize the database
- Check that `business_data.db` exists in the project directory

### Module Not Found Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Streamlit Won't Start
- Check if port 8501 is already in use
- Try running with a different port: `streamlit run app.py --server.port 8502`

## 📚 Technologies Used

- **Streamlit**: Web application framework
- **LangChain**: LLM orchestration and prompt management
- **OpenAI GPT-4**: Language model for SQL generation
- **SQLite**: Lightweight relational database
- **Pandas**: Data manipulation and display
- **Python-dotenv**: Environment variable management

## 🎯 Why This Project Stands Out for Interviews

✅ **Demonstrates DBMS Knowledge**: Shows understanding of relational databases, foreign keys, joins, and SQL  
✅ **Modern AI Stack**: Uses cutting-edge RAG architecture with LLMs  
✅ **Production-Ready Code**: Includes error handling, validation, and security measures  
✅ **Clean Architecture**: Well-structured code with separation of concerns  
✅ **Business Value**: Solves a real-world problem (business users querying databases)  
✅ **Full-Stack Application**: Combines backend logic with interactive frontend  

## 📈 Future Enhancements

- [ ] Support for multiple database types (PostgreSQL, MySQL)
- [ ] Query history and favorites
- [ ] Advanced visualizations (charts, graphs)
- [ ] Multi-table join optimization
- [ ] Natural language result filtering
- [ ] User authentication and saved queries
- [ ] Export to multiple formats (Excel, JSON, PDF)

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 👨‍💻 Author

Built as a demonstration of modern AI-powered database querying using RAG architecture.

---

**⭐ If you find this project helpful, please give it a star!**
