"""
Utility Functions for AI Helpdesk System
Text formatting, file loading, logging, and helper functions
"""

import csv
import os
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
import streamlit as st
import logging

logger = logging.getLogger(__name__)

# Constants
LOGS_FILE = "logs.csv"
KNOWLEDGE_BASE_DIR = "knowledge_base"

def format_display_text(text: str, max_length: int = 300) -> str:
    """
    Format text for display in Streamlit UI with proper truncation
    
    Args:
        text (str): Text to format
        max_length (int): Maximum length before truncation
        
    Returns:
        str: Formatted text
    """
    if not text:
        return "No content available"
    
    # Clean the text
    cleaned_text = text.strip()
    
    # Truncate if too long
    if len(cleaned_text) <= max_length:
        return cleaned_text
    
    return cleaned_text[:max_length] + "..."

def load_knowledge_base_files() -> Dict[str, str]:
    """
    Load all knowledge base files and return as dictionary
    
    Returns:
        dict: Mapping of filename to content
    """
    files_content = {}
    
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        logger.warning(f"Knowledge base directory not found: {KNOWLEDGE_BASE_DIR}")
        return files_content
    
    try:
        for filename in os.listdir(KNOWLEDGE_BASE_DIR):
            if filename.endswith('.txt'):
                file_path = os.path.join(KNOWLEDGE_BASE_DIR, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    files_content[filename] = f.read().strip()
                logger.info(f"Loaded knowledge base file: {filename}")
        
        return files_content
        
    except Exception as e:
        logger.error(f"Error loading knowledge base files: {str(e)}")
        return files_content

def log_ticket_to_csv(ticket_data: Dict[str, Any]) -> None:
    """
    Log ticket processing data to CSV file
    
    Args:
        ticket_data (dict): Dictionary containing ticket processing results
    """
    # Define CSV headers
    headers = [
        "timestamp", 
        "ticket_text", 
        "category", 
        "confidence_score", 
        "final_reply",
        "needs_escalation",
        "escalation_message"
    ]
    
    # Check if file exists to determine if we need to write headers
    file_exists = os.path.exists(LOGS_FILE)
    
    try:
        with open(LOGS_FILE, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            
            # Write headers if file is new
            if not file_exists:
                writer.writeheader()
                logger.info(f"Created new log file: {LOGS_FILE}")
            
            # Prepare row data
            row_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ticket_text": ticket_data.get("original_ticket", "")[:500],  # Limit length
                "category": ticket_data.get("category", ""),
                "confidence_score": ticket_data.get("confidence_score", 0.0),
                "final_reply": ticket_data.get("reply", "")[:1000],  # Limit length
                "needs_escalation": ticket_data.get("needs_escalation", False),
                "escalation_message": ticket_data.get("escalation_message", "")
            }
            
            # Write ticket data
            writer.writerow(row_data)
            logger.info("Logged ticket to CSV successfully")
            
    except Exception as e:
        error_msg = f"Error logging ticket to CSV: {str(e)}"
        logger.error(error_msg)
        st.error(error_msg)

def get_ticket_statistics() -> Dict[str, Any]:
    """
    Get statistics about processed tickets from logs
    
    Returns:
        dict: Statistics about tickets
    """
    if not os.path.exists(LOGS_FILE):
        return {
            "total_tickets": 0,
            "category_breakdown": {},
            "average_confidence": 0.0,
            "escalation_rate": 0.0,
            "recent_tickets": []
        }
    
    try:
        # Read CSV file
        df = pd.read_csv(LOGS_FILE)
        
        if df.empty:
            return {
                "total_tickets": 0,
                "category_breakdown": {},
                "average_confidence": 0.0,
                "escalation_rate": 0.0,
                "recent_tickets": []
            }
        
        # Calculate statistics
        total_tickets = len(df)
        category_breakdown = df['category'].value_counts().to_dict()
        average_confidence = df['confidence_score'].mean() if 'confidence_score' in df.columns else 0.0
        escalation_rate = (df['needs_escalation'].sum() / total_tickets * 100) if 'needs_escalation' in df.columns else 0.0
        
        # Get recent tickets (last 5)
        recent_tickets = df.tail(5)[['timestamp', 'ticket_text', 'category']].to_dict('records')
        
        return {
            "total_tickets": total_tickets,
            "category_breakdown": category_breakdown,
            "average_confidence": round(average_confidence, 2),
            "escalation_rate": round(escalation_rate, 1),
            "recent_tickets": recent_tickets
        }
        
    except Exception as e:
        logger.error(f"Error calculating ticket statistics: {str(e)}")
        return {
            "total_tickets": 0,
            "category_breakdown": {},
            "average_confidence": 0.0,
            "escalation_rate": 0.0,
            "recent_tickets": []
        }

def validate_ticket_input(ticket_text: str) -> tuple[bool, str]:
    """
    Validate ticket input for proper format and content
    
    Args:
        ticket_text (str): The ticket text to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not ticket_text or not ticket_text.strip():
        return False, "Please enter a ticket description."
    
    cleaned_text = ticket_text.strip()
    
    if len(cleaned_text) < 10:
        return False, "Ticket description must be at least 10 characters long."
    
    if len(cleaned_text) > 2000:
        return False, "Ticket description must be less than 2000 characters."
    
    # Check for spam-like content
    if cleaned_text.lower().count(cleaned_text.split()[0].lower()) > 5:
        return False, "Ticket appears to contain repetitive content."
    
    return True, ""

def get_example_tickets() -> List[str]:
    """
    Get list of example tickets for testing
    
    Returns:
        list: Example ticket texts
    """
    return [
        "I can't access the VPN from home.",
        "How many sick leaves am I allowed per year?",
        "My salary came late this month.",
        "Where can I see the holiday calendar?",
        "I'm having issues with the finance portal.",
        "How do I apply for reimbursement?",
        "My laptop keyboard is not working properly.",
        "I need to request a new mouse and monitor.",
        "Can you help me with expense claim procedures?",
        "When will the next bonus payment be processed?"
    ]

def format_confidence_display(confidence: float) -> tuple[str, str]:
    """
    Format confidence score for display with color coding
    
    Args:
        confidence (float): Confidence score between 0.0 and 1.0
        
    Returns:
        tuple: (formatted_text, color)
    """
    percentage = int(confidence * 100)
    
    if confidence >= 0.8:
        return f"{percentage}% (High)", "green"
    elif confidence >= 0.6:
        return f"{percentage}% (Medium)", "orange"
    else:
        return f"{percentage}% (Low)", "red"

def format_category_badge(category: str) -> str:
    """
    Format category with appropriate emoji and styling
    
    Args:
        category (str): The ticket category
        
    Returns:
        str: Formatted category with emoji
    """
    category_emojis = {
        "IT": "💻",
        "HR": "👥",
        "Finance": "💰",
        "Admin": "📋",
        "Other": "❓"
    }
    
    emoji = category_emojis.get(category, "❓")
    return f"{emoji} {category}"

def create_sample_logs_if_empty() -> None:
    """
    Create sample log entries if logs.csv is empty (for demo purposes)
    """
    if not os.path.exists(LOGS_FILE) or os.path.getsize(LOGS_FILE) == 0:
        sample_tickets = [
            {
                "original_ticket": "Can't connect to VPN from home office",
                "category": "IT",
                "reply": "Please use vpn.company.com with your employee ID to connect...",
                "confidence_score": 0.85,
                "needs_escalation": False,
                "escalation_message": ""
            },
            {
                "original_ticket": "How many vacation days do I have?",
                "category": "HR", 
                "reply": "According to our leave policy, you have 25 vacation days...",
                "confidence_score": 0.92,
                "needs_escalation": False,
                "escalation_message": ""
            },
            {
                "original_ticket": "My salary was processed incorrectly",
                "category": "Finance",
                "reply": "Thank you for reporting this issue. I'll connect you with payroll...",
                "confidence_score": 0.45,
                "needs_escalation": True,
                "escalation_message": "We are forwarding this to a human support agent for further review."
            }
        ]
        
        for ticket in sample_tickets:
            log_ticket_to_csv(ticket)
        
        logger.info("Created sample log entries for demo")

def clean_markdown_text(text: str) -> str:
    """
    Clean text for proper markdown display in Streamlit
    
    Args:
        text (str): Input text
        
    Returns:
        str: Cleaned text safe for markdown
    """
    if not text:
        return ""
    
    # Remove any problematic characters that might break markdown
    cleaned = text.replace("*", "\\*").replace("_", "\\_").replace("`", "\\`")
    
    # Ensure proper line breaks
    cleaned = cleaned.replace("\n\n\n", "\n\n")
    
    return cleaned.strip() 