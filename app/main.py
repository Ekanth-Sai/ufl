from fastapi import FastAPI, UploadFile, Form
from app.file_handler import extract_file_data
from app.prompt_engine_local_llm import call_local_llm
from io import StringIO
import pandas as pd
import os

app = FastAPI()

@app.post("/transform/")
async def transform(file: UploadFile, prompt: str = Form(...)):
    file_bytes = await file.read()
    df = extract_file_data(file.filename, file_bytes)

    preview = df.head(10).to_csv(index = False)
    llm_output = call_local_llm(prompt, preview)

    new_df = pd.read_csv(StringIO(llm_output))
    output_path = f"output/result.csv"
    new_df.to_csv(output_path, index = False)

    return {
        "status": "Success",
        "output_path": output_path,
        "preview": new_df.head().to_dict()
    }

@app.get("/")
def home():
    return {"message": "Universal File Loader running. Use /docs to test."}
