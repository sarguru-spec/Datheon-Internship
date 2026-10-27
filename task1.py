import google.generativeai as genai
from pydantic import BaseModel, ValidationError
import json
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# --- 1. CONFIGURE API SECURELY ---
# This correctly looks for the variable named "GEMINI_API_KEY" inside your .env file
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Please check your .env file.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

# --- 2. DEFINE PYDANTIC SCHEMA ---
class ResumeData(BaseModel):
    full_name: str
    email: str
    skills: list[str]
    years_of_experience: int

# --- 3. READ REAL DATA FROM FILE ---
print("📂 Reading from sample_resume.txt...")
try:
    with open("sample_resume.txt", "r", encoding="utf-8") as file:
        sample_text = file.read()
except FileNotFoundError:
    print("❌ Error: sample_resume.txt not found. Please create it in the same folder!")
    exit()

# --- 4. BUILD THE PROMPT ---
prompt = f"""
Extract the candidate's information from the resume text below. 
You MUST return ONLY a valid JSON object matching this structure:
{{
  "full_name": "string",
  "email": "string",
  "skills": ["list", "of", "strings"],
  "years_of_experience": integer
}}

Resume text to analyze:
{sample_text}
"""

# --- 5. RUN AND VALIDATE ---
print("🚀 Sending prompt to Gemini...")
response = model.generate_content(prompt)

try:
    # Clean up markdown code blocks if the LLM adds them
    raw_json = response.text.strip().replace("```json", "").replace("```", "")
    extracted_data = json.loads(raw_json)
    
    # Validate it against our Pydantic schema
    validated_resume = ResumeData(**extracted_data)
    
    print("\n✅ SUCCESS! Validated Data from File:")
    print(validated_resume.model_dump_json(indent=2))

except json.JSONDecodeError:
    print("❌ Error: The LLM did not return valid JSON.")
    print("Raw response:", response.text)
except ValidationError as e:
    print("❌ Error: The JSON didn't match our Pydantic schema.")
    print(e)