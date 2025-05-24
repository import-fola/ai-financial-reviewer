"""
GPT-4 Vision extractor implementation for AI Financial Reviewer.
"""

from .base_llm_extractor import BaseLLMExtractor

class GPT4Extractor(BaseLLMExtractor):
    """LLM extractor using OpenAI GPT-4 Vision API."""

    def extract_from_pdf(self, file_path):
        """Extract structured data from a PDF file using GPT-4 Vision."""
        pass

    def extract_from_image(self, file_path):
        """Extract structured data from an image file using GPT-4 Vision."""
        pass 