# Datheon Internship - Task 1: Structured LLM Prompt Pipeline

## Overview
This project implements a structured data extraction pipeline using Google's Gemini API and Pydantic for strict JSON validation. It reads unstructured text (like resumes or invoices) and outputs validated, structured JSON data.

## Features
- Reads unstructured text from local `.txt` files.
- Uses Google Gemini (`gemini-flash-latest`) for intelligent extraction.
- Enforces strict data schemas using `pydantic` to guarantee valid JSON output.

## Setup
1. Clone the repository.
2. Create a virtual environment: `python3 -m venv .venv`
3. Activate it: `source .venv/bin/activate` (Mac/Linux) or `.\venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install google-generativeai pydantic`
5. Add your Gemini API key to `task1.py`.

## Usage
Run the script:
```bash
python3 task1.py