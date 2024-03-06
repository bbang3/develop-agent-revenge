from tavily import TavilyClient
from dotenv import load_dotenv

import os


class WebSurfer:
    def __init__(self) -> None:
        load_dotenv()
        self.tavily_client = TavilyClient(os.environ.get("TAVILY_API_KEY"))
        self.func_name = "websurfer"
        self.description = "Search the web for information"
        self.parameters = {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query",
                },
            },
            "required": ["query"],
        }

    def __call__(self, query: str) -> str:
        """
        Search the web for information using tavily.
        Returns the relevant information as a single string.
        """
        response = self.tavily_client.get_search_context(query, search_depth="advanced")
        return response

    def as_dict(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.func_name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }
