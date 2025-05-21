from smolagents import CodeAgent, InferenceClientModel, Tool, HfApiModel
import requests
import json

model_id ='Qwen/Qwen2.5-Coder-32B-Instruct'

class HadithRequest(Tool):
    name = "query_islamic_hadith"
    description = """This tool gets Islamic hadiths from the API based on one or more of these parameters:
    - hadithEnglish: English word(s) to search
    - hadithUrdu: Urdu word(s) to search
    - hadithArabic: Arabic word(s) to search
    - hadithNumber: Number of the hadith
    - book: Slug of the book (e.g., 'sahih-bukhari')
    - chapter: Chapter number of any book
    - status: 'Sahih' / 'Hasan' / 'Da`eef'
    - paginate: Number of hadiths per page (default: 25)
    """

    output_type = "object"

    inputs = {
        "hadithEnglish": {
            "type": "string",
            "description": "English word(s) to search in hadiths collection",
            "required": False,
            "nullable": True
        },
        "hadithUrdu": {
            "type": "string",
            "description": "Urdu word(s) to search in hadiths collection",
            "required": False,
            "nullable": True
        },
        "hadithArabic": {
            "type": "string",
            "description": "Arabic word(s) to search in hadiths collection",
            "required": False,
            "nullable": True
        },
        "hadithNumber": {
            "type": "integer",
            "description": "Number of the hadith",
            "required": False,
            "nullable": True
        },
        "book": {
            "type": "string",
            "description": "Slug of the book (e.g., 'sahih-bukhari')",
            "required": False,
            "nullable": True
        },
        "chapter": {
            "type": "integer",
            "description": "Chapter number of any book",
            "required": False,
            "nullable": True
        },
        "status": {
            "type": "string",
            "description": "Sahih / Hasan / Da`eef",
            "required": False,
            "nullable": True
        },
        "paginate": {
            "type": "integer",
            "description": "Number of hadiths to paginate (default: 25)",
            "required": False,
            "nullable": True
        }
    }

    def __init__(self, api_key=None):
        """Initialize the HadithRequest tool."""
        super().__init__()  # Call the parent class's __init__ method
        self.api_key = api_key
        self.base_url = "https://hadithapi.com/api/hadiths/"
        self.is_initialized = True  # Set is_initialized to True

    def forward(self, hadithEnglish=None, hadithUrdu=None, hadithArabic=None, 
                hadithNumber=None, book=None, chapter=None, status=None, paginate=None):
        """
        Query the Hadith API with the given parameters.
        
        Parameters match the keys defined in the inputs dictionary.
        
        Returns:
        - Dictionary: JSON response from the API
        """
        # Add API key to params
        query_params = {"apiKey": self.api_key}
        
        # Add parameters that are not None
        if hadithEnglish is not None:
            query_params["hadithEnglish"] = hadithEnglish
        if hadithUrdu is not None:
            query_params["hadithUrdu"] = hadithUrdu
        if hadithArabic is not None:
            query_params["hadithArabic"] = hadithArabic
        if hadithNumber is not None:
            query_params["hadithNumber"] = hadithNumber
        if book is not None:
            query_params["book"] = book
        if chapter is not None:
            query_params["chapter"] = chapter
        if status is not None:
            query_params["status"] = status
        if paginate is not None:
            query_params["paginate"] = paginate
        
        # Make the request
        response = requests.get(self.base_url, params=query_params)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise ValueError("Unauthorized - API key is invalid")
        elif response.status_code == 403:
            raise ValueError("Forbidden - API key is required")
        elif response.status_code == 404:
            raise ValueError("Not found - Books not found")
        else:
            raise ValueError("Request failed with status code: {}".format(response.status_code))


# Create an instance of the tool with your API key
hadith_tool = HadithRequest(api_key="$2y$10$glbbDYYMsqT6kxssWdCeDr9h9ywTLnOFIAuqzY99dAIqMcG")

model = HfApiModel(
max_tokens=2096,
temperature=0.5,
model_id=model_id,# it is possible that this model may be overloaded
custom_role_conversions=None,
)
# Create the agent with the tool instance
agent = CodeAgent(
    model=model,
    tools=[hadith_tool],  # Pass the instance, not the class
    max_steps=3,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None
)

# Run the agent
result = agent.run(
    "My lover left me im really sad please give me a hadith to cheer me up"
)

print(result)