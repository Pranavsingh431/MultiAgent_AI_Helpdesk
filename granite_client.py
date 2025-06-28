"""
IBM Granite API Client for Multi-Agent Helpdesk System
Handles all communication with IBM Watsonx Granite models
"""

from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from ibm_watsonx_ai import Credentials
import logging

# IBM Watsonx Configuration
IBM_URL = "https://us-south.ml.cloud.ibm.com"
IBM_API_KEY = "6v18auqypEP0CcKKmeFWLYCBsBVHjtrl9LV3x1YoTz8C"
PROJECT_ID = "dab1c6ed-9b03-4362-87c6-b5f854a6fb34"
MODEL_ID = "ibm/granite-3-3-8b-instruct"

# Model Configuration
MODEL_PARAMS = {
    GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
    GenParams.TEMPERATURE: 0.6,
    GenParams.MAX_NEW_TOKENS: 300,
}

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_granite_response(prompt: str) -> str:
    """
    Sends prompt to IBM Granite and returns clean, trimmed response
    
    Args:
        prompt (str): The input prompt for the model
        
    Returns:
        str: Clean, trimmed response from Granite model
    """
    try:
        # Set up credentials
        credentials = Credentials(
            url=IBM_URL,
            api_key=IBM_API_KEY
        )
        
        # Initialize the model
        model = Model(
            model_id=MODEL_ID,
            params=MODEL_PARAMS,
            credentials=credentials,
            project_id=PROJECT_ID
        )
        
        # Generate response
        logger.info(f"Sending prompt to Granite model: {MODEL_ID}")
        response = model.generate_text(prompt=prompt)
        
        # Clean and trim response
        cleaned_response = response.strip()
        
        # Remove any unwanted prefixes or suffixes that the model might add
        if cleaned_response.startswith('"') and cleaned_response.endswith('"'):
            cleaned_response = cleaned_response[1:-1]
        
        logger.info("Successfully received response from Granite")
        return cleaned_response
        
    except Exception as e:
        error_msg = f"Error calling Granite API: {str(e)}"
        logger.error(error_msg)
        return f"I apologize, but I'm currently unable to process your request due to a technical issue. Please try again later or contact IT support. Error: {str(e)}"

def test_granite_connection() -> bool:
    """
    Test connection to IBM Granite API
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        test_prompt = "Hello, please confirm you are working by saying 'System operational'"
        response = get_granite_response(test_prompt)
        
        # Check if we got a meaningful response
        if response and len(response) > 5 and "Error" not in response:
            logger.info("Granite connection test successful")
            return True
        else:
            logger.warning("Granite connection test failed - no valid response")
            return False
            
    except Exception as e:
        logger.error(f"Granite connection test failed: {str(e)}")
        return False

def get_model_info() -> dict:
    """
    Returns information about the current model configuration
    
    Returns:
        dict: Model configuration details
    """
    return {
        "model_id": MODEL_ID,
        "url": IBM_URL,
        "temperature": MODEL_PARAMS[GenParams.TEMPERATURE],
        "max_tokens": MODEL_PARAMS[GenParams.MAX_NEW_TOKENS],
        "decoding_method": "greedy",
        "status": "connected" if test_granite_connection() else "disconnected"
    } 