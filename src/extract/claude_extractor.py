"""
Claude Vision extractor implementation for AI Financial Reviewer.
"""

from .base_llm_extractor import BaseLLMExtractor

class ClaudeExtractor(BaseLLMExtractor):
    """LLM extractor using Claude Vision API."""

    def extract_from_pdf(self, file_path):
        """Extract structured data from a PDF file using Claude Vision."""
        pass

    def extract_from_image(self, file_path):
        """Extract structured data from an image file using Claude Vision."""
        pass 