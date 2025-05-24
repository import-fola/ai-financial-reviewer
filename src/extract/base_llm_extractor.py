"""
Abstract base class for LLM/OCR extractors (Claude, GPT-4, Gemini, etc.).
"""

from abc import ABC, abstractmethod

class BaseLLMExtractor(ABC):
    """Abstract base class for LLM/OCR extractors."""

    @abstractmethod
    def extract_from_pdf(self, file_path):
        """Extract structured data from a PDF file."""
        pass

    @abstractmethod
    def extract_from_image(self, file_path):
        """Extract structured data from an image file (PNG/JPG)."""
        pass 