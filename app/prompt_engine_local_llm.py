import ollama

def call_local_llm(prompt: str, data_preview: str) -> str:
    full_prompt = f"""You are a data assistant.
You are given this tabular data (in CSV format):

{data_preview}

User wants to do this:
{prompt}

Return the transformed table in CSV format (with headers). Return ONLY the transformed table as raw CSV. Do not add any explanation or markdown."""

    response = ollama.chat(
        model="phi",
        messages=[{"role": "user", "content": full_prompt}]
    )
    return response['message']['content']
