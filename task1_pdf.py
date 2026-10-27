import google.generativeai as genai
from pydantic import BaseModel, ValidationError, Field
from typing import Optional
import json
import os
from dotenv import load_dotenv
from pypdf import PdfReader

# Load environment variables
load_dotenv()

# --- 1. CONFIGURE API SECURELY ---
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("API key not found. Please check your .env file.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

# --- 2. DEFINE PYDANTIC SCHEMA (With Optional fallbacks) ---
class InvoiceData(BaseModel):
    vendor_name: Optional[str] = Field(default="Unknown", description="Name of the vendor")
    invoice_number: Optional[str] = Field(default="Unknown", description="Invoice number")
    invoice_date: Optional[str] = Field(default="Unknown", description="Date of invoice")
    total_amount: Optional[float] = Field(default=0.0, description="Total amount")
    line_items: Optional[list[str]] = Field(default_factory=list, description="List of items")

# --- 3. READ REAL DATA FROM PDF ---
pdf_filename = "document.pdf"
print(f"📂 Reading from {pdf_filename}...")

if not os.path.exists(pdf_filename):
    print(f"❌ Error: {pdf_filename} not found. Please add a PDF to this folder!")
    exit()

try:
    reader = PdfReader(pdf_filename)
    pdf_text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            pdf_text += extracted + "\n"
    
    # Debug: Show how much text we actually got
    print(f"🔍 Extracted {len(pdf_text)} characters from PDF.")
    
    if len(pdf_text) < 50:
        print("⚠️ Warning: Very little text extracted. This PDF might be a scanned image.")
        print("Please use a text-based PDF (where you can highlight the text with your mouse).")
        # Don't exit, let's see what the LLM does with it anyway
        
except Exception as e:
    print(f"❌ Error reading PDF: {e}")
    exit()

# --- 4. BUILD THE PROMPT ---
prompt = f"""
Extract the invoice information from the document text below. 
You MUST return ONLY a valid JSON object matching this structure. 
If a field is not found, use "Unknown" for strings or 0.0 for numbers.

{{
  "vendor_name": "string",
  "invoice_number": "string",
  "invoice_date": "string",
  "total_amount": float,
  "line_items": ["list", "of", "strings"]
}}

Document text to analyze:
{pdf_text[:2000]}  # Limiting to first 2000 chars to save tokens and avoid confusion
"""

# --- 5. RUN AND VALIDATE ---
print("🚀 Sending prompt to Gemini...")
response = model.generate_content(prompt)

try:
    raw_json = response.text.strip().replace("```json", "").replace("```", "")
    extracted_data = json.loads(raw_json)
    
    validated_invoice = InvoiceData(**extracted_data)
    
    print("\n✅ SUCCESS! Validated Invoice Data:")
    print(validated_invoice.model_dump_json(indent=2))

except json.JSONDecodeError:
    print("❌ Error: The LLM did not return valid JSON.")
    print("🔍 Raw LLM Response:")
    print(response.text)
except ValidationError as e:
    print("❌ Error: The JSON didn't match our Pydantic schema.")
    print("🔍 Raw LLM Response (to see what it tried to return):")
    print(response.text)
    print("\n🔍 Pydantic Errors:")
    print(e)