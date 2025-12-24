import os
from openai import OpenAI

class ResumeTailor:
    """
    Handles the intelligent tailoring of resume content based on a Job Description (JD).
    """
    def __init__(self, api_key: str):
        """Initializes the OpenAI client."""
        self.client = OpenAI(api_key=api_key)
        # Using gpt-3.5-turbo for maximum compatibility across all API account tiers
        self.model = "gpt-3.5-turbo" 

    def analyze_gap(self, resume_text: str, jd_text: str) -> str:
        """
        Compares the resume against the job description to find skill gaps.
        """
        system_prompt = (
            "You are a professional HR analyst specializing in ATS optimization. "
            "Compare the candidate's resume against the job description. "
            "Identify 5 to 8 specific keywords or skills missing from the resume. "
            "Output only a bulleted list."
        )

        user_prompt = (
            f"JOB DESCRIPTION:\n{jd_text}\n\n"
            f"RESUME CONTENT:\n{resume_text}"
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.4
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[Error analyzing gap: {e}]"

    def generate_summary(self, resume_text: str, jd_text: str) -> str:
        """
        Rewrites the professional summary to be relevant to the JD.
        """
        system_prompt = (
            "You are a professional resume writer. Rewrite the candidate's professional "
            "summary to target the job description. Keep it under 4 sentences. "
            "Integrate key technical keywords from the JD while staying factual."
        )
        
        user_prompt = (
            f"JOB DESCRIPTION:\n{jd_text}\n\n"
            f"RESUME CONTENT:\n{resume_text}"
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[Error generating summary: {e}]"