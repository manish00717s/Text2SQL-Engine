# 🚀 Quick Start Guide

## ✅ Setup Complete!

Your AI-Powered Text-to-SQL Generator is **running successfully**!

## 📍 Access Your Application

**Your app is now live at:**
- **Local:** http://localhost:8501
- **Network:** http://10.71.157.202:8501

👉 **Open your browser and visit** `http://localhost:8501`

## 🎯 How to Use

### 1. Ask a Question
In the text area, type a natural language question about your business data:

**Examples:**
- "Show me the top 5 customers who spent the most money"
- "What are the total sales by region?"
- "List all products with low stock (less than 50 units)"
- "Which customers haven't made any orders?"

### 2. Generate SQL
Click the "🚀 Generate SQL" button

### 3. View Results
The app will:
- ✅ Generate the SQL query
- ✅ Execute it safely
- ✅ Display results in a table
- ✅ Provide a natural language summary

## 📊 Sample Database Structure

### Customers Table
- customer_id, name, email, region, registration_date

### Products Table
- product_id, product_name, category, price, stock_quantity

### Orders Table
- order_id, customer_id, product_id, quantity, order_date, total_amount

## 🔧 Configuration

Your API key is configured in `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## 🛑 Stop the Application

To stop the Streamlit server:
1. Go to your terminal/command prompt
2. Press `Ctrl + C`

## 🔄 Restart the Application

To run it again anytime:
```powershell
# Option 1: Use the batch file
.\run.bat

# Option 2: Manual command
venv\Scripts\activate
streamlit run app.py
```

## 💡 Tips

- Use the **sidebar** to view database schema and sample data
- Click **example questions** in the sidebar to try them instantly
- Download query results as CSV using the download button
- All queries are **read-only** for safety

## 🎓 What This Demonstrates

✅ **RAG Architecture** - Database schema is injected as context  
✅ **LangChain Integration** - Modern AI orchestration  
✅ **SQL Generation** - Natural language → SQL conversion  
✅ **Database Operations** - SQLite with foreign keys & joins  
✅ **Web Application** - Interactive Streamlit interface  
✅ **Safety Features** - Query validation & read-only mode  

## 📚 Learn More

Check `README.md` for detailed documentation, architecture explanation, and troubleshooting tips.

---

**Enjoy exploring your AI-powered Text-to-SQL Generator!** 🎉
