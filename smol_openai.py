from smolagents import CodeAgent, ToolCallingAgent, DuckDuckGoSearchTool, PythonInterpreterTool, tool
from typing import Optional
import os

from dotenv import load_dotenv
load_dotenv()
from smolagents import OpenAIServerModel
# Replace LiteLLMModel with OpenAI model
model = OpenAIServerModel(
    model_id="gpt-4o-mini",
    api_base="https://api.openai.com/v1",
    api_key=os.environ["OPENAI_API_KEY"],
)

import re
import requests
from markdownify import markdownify
from requests.exceptions import RequestException


@tool
def visit_webpage(url: str) -> str:
    """Visits a webpage at the given URL and returns its content as a markdown string.

    Args:
        url: The URL of the webpage to visit.

    Returns:
        The content of the webpage converted to Markdown, or an error message if the request fails.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Convert the HTML content to Markdown
        markdown_content = markdownify(response.text).strip()

        # Remove multiple line breaks
        markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

        return markdown_content

    except RequestException as e:
        return f"Error fetching the webpage: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

@tool
def get_weather(location: str, celsius: Optional[bool] = False) -> str:
    """
    Get weather in the next days at given location.
    Args:
        location: the location
        celsius: whether to use Celsius for temperature
    """
    return f"The weather in {location} is sunny with temperatures around 7°C."

#agent = ToolCallingAgent(tools=[get_weather], model=model)


agent = CodeAgent(tools=[DuckDuckGoSearchTool(), visit_webpage], model=model)
answer = agent.run("What is the weather in Copenhagen? Is it good weather for cycling?")
print(answer)