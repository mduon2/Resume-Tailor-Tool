import os
from pathlib import Path
from typing import Optional
import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv(override=True)

class PDFReader:
    """
    Handles file extraction from PDF or TXT files.
    """
    def __init__(self, api_key: Optional[str] = None):
        """Initializes the API client and checks for API key."""
        # Check for API key from arguments or environment variable
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OpenAI API Key is missing. Please set OPENAI_API_KEY in .env or pass it as an argument.")

        # Initialize the OpenAI client
        self.client = OpenAI(api_key=self.api_key)

    def extract_text(self, file_path: str) -> str:
        """
        Extracts raw text from a PDF file or reads a simple text file.
        This allows the JD to be provided as either format.
        """
        file = Path(file_path)
        if not file.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Handle simple text files (for job descriptions)
        if file.suffix.lower() == '.txt':
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                return content

        # Handle PDF files (for resumes or JDs)
        try:
            with open(file, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                return text.strip()
        
        except Exception as e:
            raise Exception(f"Error reading PDF file '{file_path}': {e}")