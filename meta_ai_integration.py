"""
Meta AI Integration Script
This script provides a Python interface for the Meta AI API
Make sure to install the required package: pip install meta_ai_api
"""

from meta_ai_api import MetaAI
import json
import sys

class MetaAIIntegration:
    def __init__(self):
        """Initialize the Meta AI client"""
        try:
            self.ai = MetaAI()
            self.is_initialized = True
        except Exception as e:
            print(f"Error initializing Meta AI: {e}")
            self.is_initialized = False
    
    def get_response(self, message):
        """Get response from Meta AI"""
        if not self.is_initialized:
            return {"success": False, "error": "Meta AI not initialized"}
        
        try:
            response = self.ai.prompt(message=message)
            
            # Clean and format the response
            if isinstance(response, dict):
                cleaned_response = str(response.get('message', ''))
            else:
                cleaned_response = str(response).replace("\n", " ")
            
            # Remove unwanted prefixes
            cleaned_response = cleaned_response.replace("source:", "").replace("media:", "").strip()
            
            return {
                "success": True,
                "response": cleaned_response,
                "original_response": response
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error getting AI response: {str(e)}"
            }

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python meta_ai_integration.py 'your message here'")
        return
    
    message = sys.argv[1]
    ai_integration = MetaAIIntegration()
    result = ai_integration.get_response(message)
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()