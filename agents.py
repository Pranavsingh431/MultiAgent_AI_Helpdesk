"""
Multi-Agent System for AI Helpdesk
Contains 4 specialized agents: Classifier, Retriever, Responder, Confidence
"""

import os
import re
from granite_client import get_granite_response
import logging

logger = logging.getLogger(__name__)

def classify_ticket(ticket_text: str) -> str:
    """
    Classifier Agent: Classifies tickets into categories
    
    Args:
        ticket_text (str): The ticket text to classify
        
    Returns:
        str: Category - "IT", "HR", "Finance", "Admin", or "Other"
    """
    prompt = f"""You are a ticket classifier. Read the following message and classify it into one of the categories:
- IT
- HR
- Finance
- Admin
- Other

Only return the category name.

Message:
"{ticket_text}" """
    
    try:
        response = get_granite_response(prompt)
        
        # Clean the response and ensure it's a valid category
        category = response.strip().upper()
        
        valid_categories = ["IT", "HR", "FINANCE", "ADMIN", "OTHER"]
        
        if category in valid_categories:
            return category.title()  # Return with proper capitalization
        else:
            # Fallback keyword-based classification if AI response is unclear
            return _fallback_classification(ticket_text)
            
    except Exception as e:
        logger.error(f"Error in classify_ticket: {str(e)}")
        return _fallback_classification(ticket_text)

def _fallback_classification(ticket_text: str) -> str:
    """
    Fallback keyword-based classification if AI fails
    """
    text_lower = ticket_text.lower()
    
    # IT keywords
    it_keywords = ['vpn', 'password', 'login', 'computer', 'laptop', 'software', 
                   'network', 'email', 'internet', 'wifi', 'system', 'technical',
                   'hardware', 'mouse', 'keyboard', 'monitor']
    
    # HR keywords  
    hr_keywords = ['leave', 'vacation', 'sick', 'holiday', 'hr', 'human resources',
                   'employment', 'manager', 'policy', 'maternity', 'paternity']
    
    # Finance keywords
    finance_keywords = ['salary', 'payroll', 'reimbursement', 'expense', 'payment',
                       'finance', 'money', 'tax', 'bonus', 'overtime', 'receipt']
    
    # Admin keywords
    admin_keywords = ['admin', 'administration', 'office', 'supplies', 'calendar',
                     'meeting', 'room', 'booking', 'facility']
    
    # Count keyword matches
    it_score = sum(1 for keyword in it_keywords if keyword in text_lower)
    hr_score = sum(1 for keyword in hr_keywords if keyword in text_lower)
    finance_score = sum(1 for keyword in finance_keywords if keyword in text_lower)
    admin_score = sum(1 for keyword in admin_keywords if keyword in text_lower)
    
    # Find category with highest score
    scores = {
        "IT": it_score,
        "HR": hr_score, 
        "Finance": finance_score,
        "Admin": admin_score
    }
    
    max_category = max(scores, key=scores.get)
    
    # If no clear winner, return Other
    if scores[max_category] == 0:
        return "Other"
    
    return max_category

def retrieve_context(category: str) -> str:
    """
    Retriever Agent: Loads relevant .txt file from knowledge_base
    
    Args:
        category (str): The classified ticket type
        
    Returns:
        str: Relevant context from knowledge base or fallback message
    """
    knowledge_base_path = "knowledge_base"
    
    # Map categories to file names
    category_files = {
        "IT": "vpn_policy.txt",
        "HR": "leave_policy.txt", 
        "Finance": "reimbursement_policy.txt",
        "Admin": "hardware_issuance.txt"
    }
    
    try:
        if category in category_files:
            file_path = os.path.join(knowledge_base_path, category_files[category])
            
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    logger.info(f"Retrieved context for {category} from {file_path}")
                    return content
            else:
                logger.warning(f"Knowledge base file not found: {file_path}")
                return "No policy found."
        
        # For Finance tickets, also check salary policy
        elif category == "Finance":
            # Try both reimbursement and salary policies
            contexts = []
            for filename in ["reimbursement_policy.txt", "salary_policy.txt"]:
                file_path = os.path.join(knowledge_base_path, filename)
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        contexts.append(f.read().strip())
            
            if contexts:
                return "\n\n".join(contexts)
            else:
                return "No policy found."
        
        # For Admin tickets, try holiday calendar too
        elif category == "Admin":
            contexts = []
            for filename in ["hardware_issuance.txt", "holiday_calendar.txt"]:
                file_path = os.path.join(knowledge_base_path, filename)
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        contexts.append(f.read().strip())
            
            if contexts:
                return "\n\n".join(contexts)
            else:
                return "No policy found."
        
        else:
            return "No policy found."
            
    except Exception as e:
        logger.error(f"Error in retrieve_context: {str(e)}")
        return "No policy found."

def generate_reply(ticket_text: str, context: str) -> str:
    """
    Responder Agent: Generates professional reply using context
    
    Args:
        ticket_text (str): The original ticket text
        context (str): Relevant context from knowledge base
        
    Returns:
        str: Generated professional reply
    """
    prompt = f"""You are a company helpdesk AI assistant.

Employee ticket: {ticket_text}

Company policy: {context}

Write a concise, helpful response in 2-3 sentences. Be direct and skip formal greetings. Focus on the solution."""
    
    try:
        response = get_granite_response(prompt)
        logger.info("Generated reply using Responder Agent")
        return response
        
    except Exception as e:
        logger.error(f"Error in generate_reply: {str(e)}")
        return "Thank you for your inquiry. I'm currently experiencing technical difficulties. Please contact our support team directly for immediate assistance."

def rate_confidence(ticket_text: str, response: str) -> float:
    """
    Confidence Agent: Rates confidence in the AI response
    
    Args:
        ticket_text (str): The original ticket text
        response (str): The AI-generated response
        
    Returns:
        float: Confidence score between 0.0 and 1.0
    """
    prompt = f"""You are evaluating how confident the AI helpdesk is in the reply below.

Ticket: {ticket_text}
Reply: {response}

Respond with a number between 0.0 and 1.0 representing confidence.
Only return the number."""
    
    try:
        confidence_response = get_granite_response(prompt)
        
        # Extract number from response
        numbers = re.findall(r'0\.\d+|1\.0|0|1', confidence_response)
        
        if numbers:
            confidence = float(numbers[0])
            # Ensure it's within valid range
            confidence = max(0.0, min(1.0, confidence))
            logger.info(f"Confidence rating: {confidence}")
            return confidence
        else:
            # Fallback confidence calculation based on response quality
            return _calculate_fallback_confidence(ticket_text, response)
            
    except Exception as e:
        logger.error(f"Error in rate_confidence: {str(e)}")
        return _calculate_fallback_confidence(ticket_text, response)

def _calculate_fallback_confidence(ticket_text: str, response: str) -> float:
    """
    Fallback confidence calculation based on response characteristics
    """
    confidence = 0.5  # Base confidence
    
    # Increase confidence if response is detailed
    if len(response) > 100:
        confidence += 0.1
    
    # Increase confidence if response contains specific information
    specific_terms = ['contact', 'portal', 'policy', 'procedure', 'email', 'phone']
    for term in specific_terms:
        if term.lower() in response.lower():
            confidence += 0.05
    
    # Decrease confidence if response contains error messages
    error_terms = ['error', 'unable', 'technical issue', 'try again']
    for term in error_terms:
        if term.lower() in response.lower():
            confidence -= 0.2
    
    # Ensure within bounds
    return max(0.0, min(1.0, confidence))

def should_escalate(confidence_score: float) -> tuple[bool, str]:
    """
    Determines if ticket should be escalated based on confidence
    
    Args:
        confidence_score (float): The confidence rating
        
    Returns:
        tuple: (should_escalate: bool, escalation_message: str)
    """
    if confidence_score < 0.6:
        escalation_message = "We are forwarding this to a human support agent for further review."
        return True, escalation_message
    else:
        return False, ""

def process_ticket_pipeline(ticket_text: str) -> dict:
    """
    Complete ticket processing pipeline using all four agents
    
    Args:
        ticket_text (str): The input ticket text
        
    Returns:
        dict: Complete processing results
    """
    logger.info("Starting ticket processing pipeline")
    
    # Step 1: Classify the ticket
    category = classify_ticket(ticket_text)
    logger.info(f"Ticket classified as: {category}")
    
    # Step 2: Retrieve relevant context
    context = retrieve_context(category)
    logger.info(f"Retrieved context length: {len(context)} characters")
    
    # Step 3: Generate reply
    reply = generate_reply(ticket_text, context)
    logger.info("Generated AI reply")
    
    # Step 4: Rate confidence
    confidence = rate_confidence(ticket_text, reply)
    logger.info(f"Confidence score: {confidence}")
    
    # Step 5: Check if escalation needed
    needs_escalation, escalation_msg = should_escalate(confidence)
    
    return {
        "original_ticket": ticket_text,
        "category": category,
        "context": context,
        "reply": reply,
        "confidence_score": confidence,
        "needs_escalation": needs_escalation,
        "escalation_message": escalation_msg
    } 