import os
import PyPDF2
from docx import Document
import re
from typing import List, Dict, Any
from config import Config

class FileProcessor:
    """Handles processing of various file formats for text extraction"""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error processing DOCX: {str(e)}")
    
    @staticmethod
    def extract_text_from_txt(file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            raise Exception(f"Error processing TXT: {str(e)}")
    
    @staticmethod
    def process_file(file_path: str) -> Dict[str, Any]:
        """Process any supported file and return extracted text with metadata"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension not in Config.SUPPORTED_TEXT_FILES:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        # Extract text based on file type
        if file_extension == '.pdf':
            text = FileProcessor.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            text = FileProcessor.extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            text = FileProcessor.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        # Get file metadata
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        
        # Analyze text
        word_count = len(text.split())
        char_count = len(text)
        paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
        
        return {
            'text': text,
            'file_name': file_name,
            'file_size': file_size,
            'file_type': file_extension,
            'word_count': word_count,
            'char_count': char_count,
            'paragraph_count': paragraph_count,
            'estimated_reading_time': word_count // 200  # Average reading speed
        }
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}]', '', text)
        return text.strip()
    
    @staticmethod
    def split_text_into_chunks(text: str, max_chunk_size: int = 1000) -> List[str]:
        """Split text into manageable chunks for processing"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            if current_size + len(word) + 1 > max_chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_size = len(word)
            else:
                current_chunk.append(word)
                current_size += len(word) + 1
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
