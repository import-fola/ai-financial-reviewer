"""
Gemini Vision extractor implementation for AI Financial Reviewer.
"""

from .base_llm_extractor import BaseLLMExtractor

class GeminiExtractor(BaseLLMExtractor):
    """LLM extractor using Gemini Vision API."""

    def extract_from_pdf(self, file_path):
        """Extract structured data from a PDF file using Gemini Vision."""
        pass

    def extract_from_image(self, file_path):
        """Extract structured data from an image file using Gemini Vision."""
        pass 