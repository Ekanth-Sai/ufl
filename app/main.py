from fastapi import FastAPI, UploadFile, Form, Query
from app.file_handler import extract_file_data
from app.prompt_engine_local_llm import call_local_llm
from io import StringIO
import pandas as pd
import os
import time

app = FastAPI()

def validate_schema(df: pd.DataFrame):
    issues = {}
    for col in df.columns:
        dtype = df[col].dtype
        if df[col].isnull().all():
            issues[col] = "All values are null"
        elif dtype == "object":
            mixed_types = df[col].apply(lambda x: type(x)).nunique()
            if mixed_types > 1:
                issues[col] = "Mixed data types"
    return issues

@app.post("/transform/")
async def transform(file: UploadFile, prompt: str = Form(...), output_format: str = Query("csv", enum = ["csv", "json", "xlsx"])):
    file_bytes = await file.read()
    df = extract_file_data(file.filename, file_bytes)

    schema_issues = validate_schema(df)

    preview = df.head(10).to_csv(index = False)
    llm_output = call_local_llm(prompt, preview)

    new_df = pd.read_csv(StringIO(llm_output))
    ts = int(time.time())
    output_dir = "output"
    os.makedirs(output_dir, exist_ok = True)

    filename_base = f"{output_dir}/result_{ts}"

    if output_format == "json":
        output_path = f"{filename_base}.json"
        new_df.to_json(output_path, orient = "records", indent = 2)
    elif output_format == "xlsx":
        output_path = f"{filename_base}.xlsx"
        new_df.to_excel(output_path, index = False)
    else:
        output_path = f"{filename_base}.csv"
        new_df.to_csv(output_path, index = False)

    with open(f"{output_dir}/prompt_log.txt", "a") as f:
        f.write(f"\n---\nPrompt: {prompt}\nTimestamp: {ts}\nSample Input:\n{preview}\nOutput Head:\n{new_df.head().to_csv(index = False)}\n")

    return {
        "status": "Success",
        "output_path": output_path,
        "issues": schema_issues,
        "preview": new_df.head().to_dict()
    }

@app.get("/")
def home():
    return {"message": "Universal File Loader running. Use /docs to test."}
