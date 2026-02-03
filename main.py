import argparse
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Ensure the files are available for import
try:
    from pdf_reader import PDFReader
    from resume_tailor import ResumeTailor
except ImportError as e:
    print(f"Import Error: Could not find required modules (pdf_reader or resume_tailor). Ensure all three files are in the same directory.")
    sys.exit(1)

# Load environment variables from a .env file if present
load_dotenv(override=True)

def main():
    parser = argparse.ArgumentParser(description="AI Resume Tailor & Analyzer: Compares a resume against a JD and generates a tailored summary and gap analysis.")
    
    # Required positional arguments
    parser.add_argument("resume_path", help="Path to the candidate's PDF resume")
    parser.add_argument("jd_path", help="Path to the PDF or TXT job description")
    
    # Optional arguments
    parser.add_argument("-o", "--output", help="Output file path (optional). Writes the full report.")
    parser.add_argument("--api-key", help="OpenAI API Key (overrides OPENAI_API_KEY environment variable)")

    args = parser.parse_args()

    # --- 1. Validation and Initialization ---
    if not Path(args.resume_path).exists():
        print(f"Error: Resume file '{args.resume_path}' does not exist.")
        sys.exit(1)
    if not Path(args.jd_path).exists():
        print(f"Error: Job Description file '{args.jd_path}' does not exist.")
        sys.exit(1)

    try:
        # Initialize the PDF Reader, which validates the API key
        pdf_processor = PDFReader(api_key=args.api_key)
        # Initialize the Tailor, reusing the validated API key
        tailor = ResumeTailor(api_key=pdf_processor.api_key)

    except ValueError as ve:
        print(f"\nConfiguration Error: {ve}")
        print("Please ensure your OPENAI_API_KEY is set correctly in your .env file.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Initialization Error: {e}")
        sys.exit(1)

    # --- 2. Extract Text from Resume and Job Description (JD) ---
    try:
        print("\n" + "="*50)
        print("STEP 1: EXTRACTING RESUME CONTENT...")
        print("="*50)
        resume_text = pdf_processor.extract_text(args.resume_path)
        print(f"Successfully extracted {len(resume_text)} characters from the resume.")
        
        print("\n" + "="*50)
        print("STEP 2: EXTRACTING JOB DESCRIPTION...")
        print("="*50)
        jd_text = pdf_processor.extract_text(args.jd_path)
        print(f"Successfully extracted {len(jd_text)} characters from the JD.")
        
    except Exception as e:
        print(f"Extraction Error: {e}")
        sys.exit(1)
    
    if not resume_text or not jd_text:
        print("Critical Error: Could not extract necessary text from one or both documents.")
        sys.exit(1)

    # --- 3. Core Tailoring Logic (Calling the LLM) ---
    print("\n" + "="*50)
    print("STEP 3: ANALYZING SKILL GAPS (ATS OPTIMIZATION)")
    print("="*50)
    skill_gap_analysis = tailor.analyze_gap(resume_text, jd_text)
    
    print("\n" + "="*50)
    print("STEP 4: GENERATING TAILORED SUMMARY")
    print("="*50)
    new_summary = tailor.generate_summary(resume_text, jd_text)

    # --- 4. Display and Save Final Report ---
    print("\n" + "#"*60)
    print("#" + " "*10 + "FINAL AI RESUME TAILORING REPORT" + " "*10 + "#")
    print("#"*60)
    
    print("\n--- NEW PROFESSIONAL SUMMARY (4 Sentences Max) ---\n")
    print(new_summary)
    
    print("\n--- SKILL GAP ANALYSIS (Keywords to add/emphasize) ---\n")
    print(skill_gap_analysis)
    print("\n" + "#"*60 + "\n")
    
    # Prepare the output string for saving
    final_report = (
        "--- AI RESUME TAILORING REPORT ---\n\n"
        f"JOB DESCRIPTION PATH: {args.jd_path}\n"
        f"RESUME PATH: {args.resume_path}\n\n"
        "=======================================\n\n"
        "1. NEW PROFESSIONAL SUMMARY (Optimized for JD):\n"
        "---------------------------------------\n"
        f"{new_summary}\n\n"
        "=======================================\n\n"
        "2. SKILL GAP ANALYSIS (Keywords to add/emphasize):\n"
        "---------------------------------------\n"
        f"{skill_gap_analysis}\n"
    )

    if args.output:
        output_file = args.output or "resume_tailoring_report.md"  # Default filename
        try:
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(final_report)
            print(f"Full report successfully saved to {output_file}")
        except Exception as e:
            print(f"Error saving file: {e}")

if __name__ == "__main__":
    main()
