"""
Multi-Agent AI Helpdesk (IBM Granite)
Professional AI-powered enterprise helpdesk system for hackathon demo
"""

import streamlit as st
import time
from agents import process_ticket_pipeline
from utils import (
    validate_ticket_input, 
    log_ticket_to_csv, 
    get_ticket_statistics,
    get_example_tickets,
    format_confidence_display,
    format_category_badge,
    create_sample_logs_if_empty,
    clean_markdown_text
)
from granite_client import test_granite_connection, get_model_info
import logging
from datetime import datetime
from typing import Dict, Any
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config
st.set_page_config(
    page_title="AI Helpdesk | IBM Granite",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern hackathon-ready CSS
def apply_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            font-family: 'Inter', sans-serif;
            color: #ffffff;
        }
        
        .main-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 1rem 2rem;
        }
        
        .hero-section {
            text-align: center;
            padding: 3rem 0;
            margin-bottom: 2rem;
            background: linear-gradient(135deg, rgba(0, 199, 183, 0.1) 0%, rgba(0, 122, 116, 0.05) 100%);
            border-radius: 24px;
            border: 1px solid rgba(0, 199, 183, 0.2);
            backdrop-filter: blur(10px);
        }
        
        .hero-title {
            font-size: 4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #00C7B7, #00E5D1, #007A74);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            letter-spacing: -0.02em;
        }
        
        .hero-subtitle {
            font-size: 1.3rem;
            color: rgba(255, 255, 255, 0.8);
            font-weight: 400;
            margin-bottom: 0;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2rem;
            margin: 2rem 0;
        }
        
        .stat-card {
            background: rgba(45, 45, 66, 0.6);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            border: 1px solid rgba(0, 199, 183, 0.3);
            backdrop-filter: blur(20px);
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-4px);
            border-color: rgba(0, 199, 183, 0.6);
            box-shadow: 0 20px 40px rgba(0, 199, 183, 0.15);
        }
        
        .stat-value {
            font-size: 3rem;
            font-weight: 700;
            color: #00C7B7;
            margin-bottom: 0.5rem;
            display: block;
        }
        
        .stat-label {
            font-size: 1rem;
            color: rgba(255, 255, 255, 0.7);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .section-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #ffffff;
            margin: 3rem 0 2rem 0;
            text-align: center;
            position: relative;
        }
        
        .section-header::after {
            content: '';
            position: absolute;
            bottom: -0.5rem;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 3px;
            background: linear-gradient(135deg, #00C7B7, #007A74);
            border-radius: 2px;
        }
        
        .agent-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .agent-card {
            background: rgba(45, 45, 66, 0.5);
            border-radius: 16px;
            padding: 2rem;
            border: 1px solid rgba(0, 199, 183, 0.2);
            transition: all 0.3s ease;
            text-align: center;
        }
        
        .agent-card:hover {
            transform: translateY(-4px);
            border-color: rgba(0, 199, 183, 0.5);
            background: rgba(45, 45, 66, 0.7);
        }
        
        .agent-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            display: block;
        }
        
        .agent-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #00C7B7;
            margin-bottom: 0.8rem;
        }
        
        .agent-desc {
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.7);
            line-height: 1.5;
        }
        
        .input-section {
            background: rgba(45, 45, 66, 0.4);
            border-radius: 20px;
            padding: 2.5rem;
            margin: 2rem 0;
            border: 1px solid rgba(0, 199, 183, 0.2);
        }
        
        .custom-button {
            background: linear-gradient(135deg, #00C7B7, #007A74) !important;
            color: white !important;
            border: none !important;
            padding: 0.8rem 2rem !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 8px 25px rgba(0, 199, 183, 0.3) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }
        
        .custom-button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 35px rgba(0, 199, 183, 0.4) !important;
        }
        
        .results-container {
            background: rgba(30, 30, 47, 0.8);
            border-radius: 20px;
            padding: 2.5rem;
            margin: 2rem 0;
            border: 1px solid rgba(0, 199, 183, 0.3);
            backdrop-filter: blur(20px);
        }
        
        .response-card {
            background: rgba(45, 45, 66, 0.6);
            border-radius: 16px;
            padding: 2rem;
            border-left: 4px solid #00C7B7;
            color: #ffffff;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            margin: 1rem 0;
        }
        
        .category-badge {
            padding: 0.5rem 1.2rem;
            border-radius: 25px;
            font-weight: 600;
            font-size: 0.95rem;
            display: inline-block;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .category-it { background: linear-gradient(135deg, #2196F3, #1976D2); color: white; }
        .category-hr { background: linear-gradient(135deg, #4CAF50, #388E3C); color: white; }
        .category-finance { background: linear-gradient(135deg, #FF9800, #F57C00); color: white; }
        .category-admin { background: linear-gradient(135deg, #9C27B0, #7B1FA2); color: white; }
        .category-other { background: linear-gradient(135deg, #607D8B, #455A64); color: white; }
        
        .confidence-high { 
            color: #4CAF50; 
            font-weight: 700; 
            font-size: 1.3rem;
            text-shadow: 0 2px 4px rgba(76, 175, 80, 0.3);
        }
        .confidence-medium { 
            color: #FF9800; 
            font-weight: 700; 
            font-size: 1.3rem;
            text-shadow: 0 2px 4px rgba(255, 152, 0, 0.3);
        }
        .confidence-low { 
            color: #F44336; 
            font-weight: 700; 
            font-size: 1.3rem;
            text-shadow: 0 2px 4px rgba(244, 67, 54, 0.3);
        }
        
        .feedback-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin: 2rem 0;
        }
        
        .feedback-btn {
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid rgba(0, 199, 183, 0.3);
            background: rgba(45, 45, 66, 0.5);
            color: white;
            font-weight: 500;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .feedback-btn:hover {
            background: rgba(0, 199, 183, 0.2);
            border-color: rgba(0, 199, 183, 0.6);
        }
        
        /* Streamlit overrides */
        .stSelectbox > div > div {
            background-color: rgba(45, 45, 66, 0.6) !important;
            border: 1px solid rgba(0, 199, 183, 0.3) !important;
            border-radius: 12px !important;
            color: white !important;
        }
        
        .stTextArea > div > div {
            background-color: rgba(45, 45, 66, 0.6) !important;
            border: 1px solid rgba(0, 199, 183, 0.3) !important;
            border-radius: 12px !important;
            color: white !important;
        }
        
        .stTextArea textarea {
            color: white !important;
            background-color: transparent !important;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Progress bar styling */
        .stProgress > div > div > div > div {
            background: linear-gradient(135deg, #00C7B7, #007A74);
        }
    </style>
    """, unsafe_allow_html=True)

def render_hero_section():
    """Render the hero banner"""
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🤖 Multi-Agent AI Helpdesk</div>
        <div class="hero-subtitle">Enterprise-Grade Support Automation • Powered by IBM Granite</div>
    </div>
    """, unsafe_allow_html=True)

def render_stats_panel():
    """Render the statistics panel"""
    stats = get_ticket_statistics()
    
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card">
            <span class="stat-value">{}</span>
            <div class="stat-label">Total Tickets</div>
        </div>
        <div class="stat-card">
            <span class="stat-value">{}</span>
            <div class="stat-label">Avg Confidence</div>
        </div>
        <div class="stat-card">
            <span class="stat-value">{}%</span>
            <div class="stat-label">Escalation Rate</div>
        </div>
    </div>
    """.format(stats["total_tickets"], stats["average_confidence"], stats["escalation_rate"]), unsafe_allow_html=True)

def render_agent_overview():
    """Render the multi-agent system overview"""
    st.markdown('<div class="section-header">🧠 Multi-Agent AI System</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="agent-grid">
        <div class="agent-card">
            <span class="agent-icon">🎯</span>
            <div class="agent-title">Classifier</div>
            <div class="agent-desc">Categorizes tickets into IT/HR/Finance/Admin/Other using IBM Granite</div>
        </div>
        <div class="agent-card">
            <span class="agent-icon">📚</span>
            <div class="agent-title">Retriever</div>
            <div class="agent-desc">Searches knowledge base for relevant company policies</div>
        </div>
        <div class="agent-card">
            <span class="agent-icon">💬</span>
            <div class="agent-title">Responder</div>
            <div class="agent-desc">Generates professional replies using retrieved context</div>
        </div>
        <div class="agent-card">
            <span class="agent-icon">⚡</span>
            <div class="agent-title">Confidence</div>
            <div class="agent-desc">Evaluates response quality and triggers escalation</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the enhanced sidebar"""
    with st.sidebar:
        st.markdown("## ⚙️ System Dashboard")
        
        # Model info
        model_info = get_model_info()
        st.info(f"""
        **🤖 Model**: Granite 3.3B Instruct  
        **🌡️ Temperature**: {model_info['temperature']}  
        **📊 Max Tokens**: {model_info['max_tokens']}  
        **⚡ Method**: Greedy Decoding
        """)
        
        # Connection test
        if st.button("🧪 Test IBM Connection", use_container_width=True):
            with st.spinner("Testing connection..."):
                if test_granite_connection():
                    st.success("✅ Connected to IBM Granite")
                else:
                    st.error("❌ Connection Failed")
        
        st.markdown("---")
        
        # Recent activity
        st.markdown("## 📊 Recent Activity")
        stats = get_ticket_statistics()
        if stats["recent_tickets"]:
            for ticket in stats["recent_tickets"][-3:]:
                with st.expander(f"📝 {ticket['category']}", expanded=False):
                    st.caption(ticket['timestamp'])
                    st.write(ticket['ticket_text'][:80] + "...")

def main():
    """Main application function"""
    
    # Initialize
    create_sample_logs_if_empty()
    apply_custom_css()
    
    # Sidebar
    render_sidebar()
    
    # Main content
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Hero section
    render_hero_section()
    
    # Stats
    st.markdown('<div class="section-header">📊 System Performance</div>', unsafe_allow_html=True)
    render_stats_panel()
    
    # Agent overview
    render_agent_overview()
    
    # Ticket submission
    st.markdown('<div class="section-header">📝 Submit Support Ticket</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        
        # Example selection
        examples = get_example_tickets()
        example_options = ["💡 Choose an example or type your own..."] + [f"🎫 {ex}" for ex in examples]
        
        selected_example = st.selectbox(
            "Quick Examples:",
            example_options,
            help="Select a pre-made example or choose the first option to type your own ticket"
        )
        
        # Text input
        if selected_example.startswith("🎫"):
            default_text = selected_example[2:]
        else:
            default_text = ""
        
        ticket_text = st.text_area(
            "Describe your issue:",
            value=default_text,
            height=120,
            placeholder="Example: I can't access the VPN from home...",
            help="Describe your issue in detail. Our AI agents will analyze and provide assistance."
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Submit button
    if st.button("🚀 PROCESS WITH AI AGENTS", type="primary", use_container_width=True):
        is_valid, error_message = validate_ticket_input(ticket_text)
        
        if not is_valid:
            st.error(f"❌ {error_message}")
        else:
            with st.spinner("🤖 AI agents processing your ticket..."):
                progress_bar = st.progress(0)
                
                try:
                    progress_bar.progress(25)
                    results = process_ticket_pipeline(ticket_text)
                    progress_bar.progress(100)
                    
                    st.success("✅ Ticket processed successfully!")
                    
                    # Results
                    st.markdown('<div class="section-header">🤖 AI Processing Results</div>', unsafe_allow_html=True)
                    st.markdown('<div class="results-container">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown("#### 🎯 Classification")
                        category = results["category"]
                        badge_class = f"category-{category.lower()}"
                        st.markdown(f'<span class="category-badge {badge_class}">{category}</span>', unsafe_allow_html=True)
                        
                        st.markdown("#### 📊 Confidence Score")
                        conf_text, conf_color = format_confidence_display(results["confidence_score"])
                        conf_class = f"confidence-{conf_color.replace('green', 'high').replace('orange', 'medium').replace('red', 'low')}"
                        st.markdown(f'<div class="{conf_class}">{conf_text}</div>', unsafe_allow_html=True)
                        
                        if results["needs_escalation"]:
                            st.warning("⚠️ **Escalation Required**")
                        else:
                            st.success("✅ **Resolved by AI**")
                    
                    with col2:
                        st.markdown("#### 💬 AI Response")
                        cleaned_reply = clean_markdown_text(results["reply"])
                        st.markdown(f'<div class="response-card">{cleaned_reply}</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Agent details
                    with st.expander("🔍 View Agent Processing Details", expanded=False):
                        tab1, tab2, tab3, tab4 = st.tabs(["🎯 Classification", "📚 Retrieval", "💬 Response", "📊 Confidence"])
                        
                        with tab1:
                            st.info(f"**Category**: {results['category']}")
                        with tab2:
                            st.info(f"**Context Retrieved**: {len(results['context'])} characters")
                        with tab3:
                            st.info(f"**Response Length**: {len(results['reply'])} characters")
                        with tab4:
                            st.info(f"**Confidence Score**: {results['confidence_score']}")
                    
                    # Log ticket
                    log_ticket_to_csv(results)
                    
                    # Feedback
                    st.markdown("### 💭 Rate this response")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button("👍 Helpful", use_container_width=True):
                            st.success("Thanks!")
                    with col2:
                        if st.button("👎 Not Helpful", use_container_width=True):
                            st.info("We'll improve!")
                    with col3:
                        if st.button("🔄 Try Again", use_container_width=True):
                            st.rerun()
                    with col4:
                        if st.button("📧 Escalate", use_container_width=True):
                            st.info("Escalated!")
                    
                except Exception as e:
                    st.error(f"❌ Processing Error: {str(e)}")
                finally:
                    progress_bar.empty()
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0; opacity: 0.6;">
        <p style="font-size: 1.1rem; font-weight: 600;">🤖 Multi-Agent AI Helpdesk System</p>
        <p style="color: #00C7B7;">Powered by IBM Granite</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 