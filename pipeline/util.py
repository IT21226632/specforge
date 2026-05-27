def clean_code_block(text: str) -> str:

    text = text.replace("```python", "")
    text = text.replace("```", "")

    return text.strip()