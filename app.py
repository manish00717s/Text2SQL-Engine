"""
Streamlit Web Application for Text-to-SQL Generator.
Main entry point for the application.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import os
import time
from database import DatabaseManager, initialize_db
from sql_generator import SQLGenerator, QueryValidator

# Page configuration
st.set_page_config(
    page_title="AI Text-to-SQL Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, attractive UI
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Header Styles */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: fadeInDown 1s ease-in-out;
    }
    
    .sub-header {
        font-size: 1.3rem;
        text-align: center;
        color: #4a5568;
        margin-bottom: 2rem;
        font-weight: 300;
        animation: fadeInUp 1s ease-in-out;
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-top: 2rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Card Styles */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* SQL Query Box */
    .sql-box {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: none;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.95rem;
        color: #00ff00;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        animation: slideInLeft 0.5s ease-out;
    }
    
    /* Success Box */
    .success-box {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: none;
        box-shadow: 0 8px 20px rgba(76, 175, 80, 0.3);
        color: #2e7d32;
        font-weight: 500;
        animation: bounceIn 0.6s ease-out;
    }
    
    /* Warning Box */
    .warning-box {
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: none;
        box-shadow: 0 8px 20px rgba(255, 152, 0, 0.3);
        color: #e65100;
        font-weight: 500;
    }
    
    /* Error Box */
    .error-box {
        background: linear-gradient(135deg, #ff7675 0%, #d63031 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: none;
        box-shadow: 0 8px 20px rgba(244, 67, 54, 0.3);
        color: white;
        font-weight: 500;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: none;
        box-shadow: 0 8px 20px rgba(33, 150, 243, 0.2);
        color: #1565c0;
        font-weight: 500;
        animation: fadeIn 0.5s ease-in;
    }
    
    /* Button Styles */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 50px;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        font-family: 'Poppins', sans-serif;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.6);
    }
    
    /* Text Input Styles */
    .stTextArea textarea {
        border-radius: 15px;
        border: 2px solid #667eea;
        font-size: 1.1rem;
        padding: 1rem;
        font-family: 'Poppins', sans-serif;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    .stTextArea textarea:focus {
        border-color: #764ba2;
        box-shadow: 0 6px 25px rgba(118, 75, 162, 0.3);
    }
    
    /* Sidebar Styles */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    section[data-testid="stSidebar"] .stButton>button {
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    section[data-testid="stSidebar"] .stButton>button:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateX(5px);
    }
    
    /* DataFrame Styles */
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes bounceIn {
        0% {
            opacity: 0;
            transform: scale(0.3);
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Expander Styles */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        font-weight: 600;
        backdrop-filter: blur(10px);
    }
    
    /* Badge Style */
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .badge-success {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #00695c;
    }
    
    .badge-info {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #283593;
    }
    
    /* Pulse Animation for Generate Button */
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(102, 126, 234, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(102, 126, 234, 0);
        }
    }
    
    /* Metric Cards */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_database():
    """Initialize database (cached to avoid re-initialization)."""
    db_path = "business_data.db"
    
    # Check if database exists
    if not Path(db_path).exists():
        with st.spinner("Initializing database..."):
            initialize_db()
    
    db = DatabaseManager(db_path)
    return db


@st.cache_resource
def initialize_sql_generator(_db):
    """Initialize SQL generator (cached for performance)."""
    schema_info = _db.get_schema_info()
    
    try:
        generator = SQLGenerator(schema_info)
        return generator, None
    except ValueError as e:
        return None, str(e)


def display_header():
    """Display application header."""
    st.markdown("""
        <div class="main-header">
            🤖 AI-Powered Text-to-SQL Generator
        </div>
        <div class="sub-header">
            ✨ Transform natural language into SQL queries using RAG and LLM technology ✨
        </div>
    """, unsafe_allow_html=True)
    
    # Add feature badges
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="badge badge-success">🎯 RAG Architecture</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="badge badge-info">🔒 Safe & Secure</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="badge badge-success">⚡ Real-time</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="badge badge-info">🧠 GPT-4 Powered</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)


def display_sidebar(db):
    """Display sidebar with database information."""
    st.sidebar.markdown("""
        <h1 style='text-align: center; color: white; font-size: 2rem; margin-bottom: 2rem;'>
            📊 Database Hub
        </h1>
    """, unsafe_allow_html=True)
    
    # Database schema
    with st.sidebar.expander("📋 View Database Schema", expanded=False):
        schema = db.get_schema_info()
        st.code(schema, language="text")
    
    # Sample data
    with st.sidebar.expander("👁️ View Sample Data", expanded=False):
        table_choice = st.selectbox("Select Table:", ["Customers", "Products", "Orders"])
        sample_df = db.get_sample_data(table_choice, limit=5)
        st.dataframe(sample_df, width="stretch")
    
    # Example questions
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        <h2 style='text-align: center; color: white; margin-top: 1rem;'>
            💡 Try These Questions
        </h2>
    """, unsafe_allow_html=True)
    
    examples = [
        "Show me the top 5 customers who spent the most money",
        "What are the total sales by region?",
        "List all products with low stock (less than 50 units)",
        "What are the most popular product categories?",
        "Show me the average order value by customer",
        "Which customers haven't made any orders?",
        "What's the total revenue from electronics?",
        "Show me orders placed in September 2023",
    ]
    
    for idx, example in enumerate(examples):
        if st.sidebar.button(f"💬 {example}", key=example, use_container_width=True):
            st.session_state.selected_question = example
    
    # API Key status
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        <h2 style='text-align: center; color: white;'>
            🔑 Configuration Status
        </h2>
    """, unsafe_allow_html=True)
    
    if os.getenv("OPENAI_API_KEY"):
        st.sidebar.markdown("""
            <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; text-align: center;'>
                <h3 style='color: #4ade80; margin: 0;'>✅ API Key Active</h3>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.error("❌ OpenAI API Key not found")
        st.sidebar.info("Please create a .env file with your OPENAI_API_KEY")
    
    # Add stats
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; backdrop-filter: blur(10px);'>
            <p style='margin: 0.3rem 0; color: white;'><strong>🗄️ Tables:</strong> 3</p>
            <p style='margin: 0.3rem 0; color: white;'><strong>👥 Customers:</strong> 8</p>
            <p style='margin: 0.3rem 0; color: white;'><strong>📦 Products:</strong> 10</p>
            <p style='margin: 0.3rem 0; color: white;'><strong>📋 Orders:</strong> 20+</p>
        </div>
    """, unsafe_allow_html=True)


def display_query_interface(db, generator):
    """Display main query interface."""
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 20px; text-align: center; 
                    box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3); margin-bottom: 2rem;'>
            <h2 style='color: white; margin: 0; font-size: 2rem;'>
                💬 Ask a Question About Your Data
            </h2>
            <p style='color: rgba(255,255,255,0.9); margin-top: 0.5rem; font-size: 1.1rem;'>
                Type your question in plain English and let AI do the magic! ✨
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Check if question was selected from sidebar
    default_question = st.session_state.get('selected_question', '')
    if default_question:
        # Clear the selection after using it
        st.session_state.selected_question = ''
    
    # Question input
    user_question = st.text_area(
        "Enter your question in plain English:",
        value=default_question,
        height=100,
        placeholder="Example: Show me the top 3 customers by total spending"
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        generate_button = st.button("🚀 Generate SQL", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.rerun()
    
    if generate_button and user_question.strip():
        # Add loading animation
        with st.spinner("🔄 Analyzing your question..."):
            time.sleep(0.5)
        
        with st.spinner("🧠 Generating SQL query with RAG..."):
            try:
                # Generate SQL
                sql_query = generator.generate_sql(user_question)
                
                # Validate query
                is_safe, safety_error = QueryValidator.is_safe_query(sql_query)
                is_valid, syntax_error = QueryValidator.validate_syntax(sql_query)
                
                if not is_safe:
                    st.markdown(f"""
                        <div class="error-box">
                            <h3 style='margin: 0; color: white;'>🚫 Safety Check Failed</h3>
                            <p style='margin: 0.5rem 0 0 0; color: white;'>{safety_error}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    return
                
                if not is_valid:
                    st.markdown(f"""
                        <div class="error-box">
                            <h3 style='margin: 0; color: white;'>🚫 Syntax Check Failed</h3>
                            <p style='margin: 0.5rem 0 0 0; color: white;'>{syntax_error}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    return
                
                # Display generated SQL
                st.markdown("---")
                st.markdown("""
                    <div class="section-header">
                        <span style='font-size: 2rem;'>🛠️</span> 
                        Generated SQL Query
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                    <div class="sql-box">
                        <pre style='color: #00ff00; margin: 0; font-family: "JetBrains Mono", monospace;'>{sql_query}</pre>
                    </div>
                """, unsafe_allow_html=True)
                
                # Execute query
                with st.spinner("⚙️ Executing query against database..."):
                    result_df, error = db.execute_query(sql_query)
                
                if error:
                    st.markdown(f"""
                        <div class="error-box">
                            <h3 style='margin: 0; color: white;'>❌ Query Execution Error</h3>
                            <p style='margin: 0.5rem 0 0 0; color: white;'>{error}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    return
                
                # Display results
                st.markdown("""
                    <div class="section-header">
                        <span style='font-size: 2rem;'>📊</span> 
                        Query Results
                    </div>
                """, unsafe_allow_html=True)
                
                if result_df is not None and not result_df.empty:
                    st.markdown(f"""
                        <div class="success-box">
                            <h3 style='margin: 0;'>✅ Query executed successfully!</h3>
                            <p style='margin: 0.5rem 0 0 0;'>Found <strong>{len(result_df)}</strong> result(s) in the database.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Display data table
                    st.dataframe(result_df, width="stretch", height=400)
                    
                    # Generate summary
                    with st.spinner("✍️ Generating AI summary..."):
                        summary = generator.generate_summary(
                            user_question,
                            sql_query,
                            len(result_df)
                        )
                    
                    st.markdown("""
                        <div class="section-header">
                            <span style='font-size: 2rem;'>📝</span> 
                            AI-Generated Summary
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class="info-box">
                            <p style='margin: 0; font-size: 1.1rem; line-height: 1.6;'>{summary}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Download option with custom styling
                    csv = result_df.to_csv(index=False)
                    col1, col2, col3 = st.columns([2, 1, 2])
                    with col2:
                        st.download_button(
                            label="📥 Download as CSV",
                            data=csv,
                            file_name="query_results.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                else:
                    st.markdown("""
                        <div class="warning-box">
                            <h3 style='margin: 0;'>⚠️ No Results Found</h3>
                            <p style='margin: 0.5rem 0 0 0;'>Query executed successfully but returned no results. Try a different question!</p>
                        </div>
                    """, unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f"""
                    <div class="error-box">
                        <h3 style='margin: 0; color: white;'>❌ Unexpected Error</h3>
                        <p style='margin: 0.5rem 0 0 0; color: white;'>{str(e)}</p>
                    </div>
                """, unsafe_allow_html=True)
    
    elif generate_button:
        st.markdown("""
            <div class="warning-box">
                <h3 style='margin: 0;'>⚠️ Empty Question</h3>
                <p style='margin: 0.5rem 0 0 0;'>Please enter a question first!</p>
            </div>
        """, unsafe_allow_html=True)


def main():
    """Main application function."""
    # Initialize session state
    if 'selected_question' not in st.session_state:
        st.session_state.selected_question = ''
    
    # Display header
    display_header()
    
    # Initialize database
    db = initialize_database()
    
    # Initialize SQL generator
    generator, error = initialize_sql_generator(db)
    
    # Display sidebar
    display_sidebar(db)
    
    # Check if generator initialized successfully
    if error:
        st.error(f"❌ Configuration Error: {error}")
        st.info("""
        **To fix this:**
        1. Create a `.env` file in the project root
        2. Add your OpenAI API key: `OPENAI_API_KEY=your_key_here`
        3. Restart the application
        
        You can get an API key from: https://platform.openai.com/api-keys
        """)
        return
    
    # Display main interface
    display_query_interface(db, generator)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; text-align: center; 
                box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);">
        <h3 style='color: white; margin-bottom: 1rem;'>Built with Modern Tech Stack</h3>
        <div style='display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;'>
            <span style='color: white; font-weight: 600;'>⚡ Streamlit</span>
            <span style='color: white; font-weight: 600;'>🔗 LangChain</span>
            <span style='color: white; font-weight: 600;'>🤖 OpenAI GPT-4</span>
            <span style='color: white; font-weight: 600;'>🗄️ SQLite</span>
            <span style='color: white; font-weight: 600;'>🎯 RAG Architecture</span>
        </div>
        <p style='color: rgba(255,255,255,0.9); margin-top: 1.5rem; font-size: 1.1rem;'>
            🔒 All queries are executed in read-only mode for maximum safety
        </p>
        <p style='color: rgba(255,255,255,0.8); margin-top: 0.5rem;'>
            Made with ❤️ for intelligent database querying
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
