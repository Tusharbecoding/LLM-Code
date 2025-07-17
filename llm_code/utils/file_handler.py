import os 
from pathlib import Path
from typing import List, Tuple, Optional
import mimetypes
import re

SUPPORTED_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.h', '.hpp',
    '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.r',
    '.m', '.sh', '.bash', '.zsh', '.fish', '.ps1', '.md', '.txt', '.json',
    '.xml', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.html',
    '.css', '.scss', '.sass', '.less', '.sql', '.dockerfile', '.docker',
    '.gitignore', '.env', '.makefile'
}

IGNORE_DIRS = {
    '.git', '__pycache__', 'node_modules', '.venv', 'venv', 'env',
    '.idea', '.vscode', 'dist', 'build', '.next', '.nuxt', 'target',
    'bin', 'obj', '.pytest_cache', '.mypy_cache', '.tox', 'coverage'
}

class FileHandler:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path).resolve()

    def read_file(self, filepath: str) -> Tuple[str, str]:
        try:
            path = self.base_path / filepath
            if not path.exists():
                return None, f"File {filepath} does not exist"
            
            mime_type, _ = mimetypes.guess_type(str(path))
            if mime_type and not mime_type.startswith("text"):
                try:
                    content = path.read_text(encoding="utf-8")
                except:
                    return f"Error: Connot read binary file {filepath}"
            
            else:
                content = path.read_text(encoding="utf-8")
            
            return content, filepath
            
        except Exception as e:
            return f"Error reading file {filepath}: {str(e)}"

    def read_directory(self, max_files: int = 50) -> List[Tuple[str, str]]:
        files_content = []
        file_count = 0
        
        for root, dirs, files in os.walk(self.base_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                if file_count >= max_files:
                    files_content.append((
                        f"... truncated (max {max_files} files)",
                        "truncation_notice"
                    ))
                    return files_content
                
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.base_path)
            
                if file_path.suffix.lower() in SUPPORTED_EXTENSIONS or file in SUPPORTED_EXTENSIONS:
                    content, _ = self.read_file(str(relative_path))
                    if not content.startswith("Error:"):
                        files_content.append((content, str(relative_path)))
                        file_count += 1
        
        return files_content
    
    def parse_file_references(self, text: str) -> Tuple[List[str], str]:
        pattern = r'@(\S+)'
        matches = re.findall(pattern, text)
        
        cleaned_text = re.sub(pattern, '', text).strip()
        
        valid_files = []
        for match in matches:
            if (self.base_path / match).exists():
                valid_files.append(match)
        
        return valid_files, cleaned_text
    
    def get_files_content(self, files: Optional[List[str]] = None) -> List[Tuple[str, str]]:
        if files:
            contents = []
            for file in files:
                content, filename = self.read_file(file)
                contents.append((content, filename))
            return contents
        else:
            return self.read_directory()