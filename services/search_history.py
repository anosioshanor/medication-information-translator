import json
import os
from datetime import datetime


class SearchHistory:
    """Search History class for managing medication search history with file handling"""
    
    def __init__(self):
        """Initialize search history with file path"""
        self.file_path = "data/search_history.json"
        self._ensure_directory_exists()
        self._ensure_file_exists()
    
    def _ensure_directory_exists(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
    
    def _ensure_file_exists(self):
        """Ensure history file exists"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump([], file, indent=4)
    
    def save_search(self, medicine):
        """
        Save a medication search to history using file handling
        
        Args:
            medicine (str): Medication name to save
        """
        try:
            history = self.get_history()
            
            # Add timestamp to each search
            entry = {
                "medicine": medicine.strip(),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            history.append(entry)
            
            # Keep only last 50 entries to avoid large files
            if len(history) > 50:
                history = history[-50:]
            
            # Write to file
            with open(self.file_path, 'w') as file:
                json.dump(history, file, indent=4)
                
        except Exception as e:
            raise IOError(f"Failed to save search history: {str(e)}")
    
    def get_history(self):
        """
        Get search history from file
        
        Returns:
            list: List of search entries
        """
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                
                # Handle both old format (strings) and new format (dicts)
                if data and isinstance(data[0], str):
                    # Convert old format to new format
                    entries = [{"medicine": item, "timestamp": "Unknown"} for item in data]
                    return [entry["medicine"] for entry in entries]
                else:
                    return [entry["medicine"] for entry in data]
                
        except json.JSONDecodeError:
            return []
        except FileNotFoundError:
            self._ensure_file_exists()
            return []
        except Exception as e:
            return []
    
    def clear_history(self):
        """Clear all search history"""
        try:
            with open(self.file_path, 'w') as file:
                json.dump([], file, indent=4)
        except Exception as e:
            raise IOError(f"Failed to clear history: {str(e)}")
