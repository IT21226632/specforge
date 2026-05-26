from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_plan(spec_text: str):

    with open("pipeline/prompts/planner.txt", "r") as file:
        planner_prompt = file.read()

    prompt = f"""
    {planner_prompt}

    FEATURE SPEC:
    {spec_text}
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    )

    return response.text


    