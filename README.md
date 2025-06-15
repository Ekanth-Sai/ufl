# Universal File Loader

A smart tool to ingest, extract, transform, and structure data from various file formats using a local LLM (used Phi via Ollama). Designed for data analysts to automate repetitive transformations and work with structured output like CSV/JSON.

---

## Features

- Upload and parse files: CSV, Excel, PDF, DOCX.
- Prompt-based data transformation using local LLMs
- Output structured results in CSV/JSON/XLSX
- Detect and fix data issues (e.g., nulls, duplicates) (yet to be tested)
- Save transformation history and results

---

##  Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Ekanth-Sai/ufl.git
cd universal-file-loader
```

### 2. Create and Activate Virtual Environment (Optional but Recommended)

```bash
python3 -m venv ufl
source ufl/bin/activate  # On Windows: .\ufl\Scripts\activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Setup Ollama and Pull the Local Model (I used phi because of local system restrictions. If system persists, you can go with mistral)
```bash
ollama run phi #use mistral if system persists
```

### 5. Running the application
```bash
uvicorn app.main:app --reload
```
- Visit the interactive API at: http://localhost:8000/docs
- Upload files and provide prompts to test the full pipeline.

### 6. Testing the Application
- File test cases have been provided in the `uploads/` directory. Prompt can be chosen as per the user requirement.