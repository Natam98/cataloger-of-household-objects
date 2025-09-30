import json
from typing import Any, Dict

    
def load_json_file(file_name: str) -> Dict[str, Any]:
    
    """
    Loads and parses a JSON file into a Python dictionary.

    Args:
        file_name (str): The path to the JSON file to be loaded.

    Returns:
        Dict[str, Any]: The parsed JSON content as a dictionary.
                        Returns an empty dictionary if the file is not found
                        or if the content is not valid JSON.
    """
    try:
        with open(file_name, mode="r") as input_file:
            return json.load(input_file)
        
    except FileNotFoundError:
        print(f"Errore: il file '{file_name}' non è stato trovato.")
        return {}
    
    except json.JSONDecodeError as error:
        print(f"Errore di decodifica JSON nel file '{file_name}': {error}")
        return {}
        
    
def save_json_file(data: Dict[str, Any], file_name: str) -> None:
    """
    Saves a Python dictionary to a JSON file.

    Args:
        data (Dict[str, Any]): The data to be written to the JSON file.
        file_name (str): The path to the destination JSON file.

    Returns:
        None
    """
    try:
        with open(file_name, mode="w") as output_file:
            
            json.dump(data, output_file, indent = 4)
            
    except (OSError, TypeError) as error:
        
        print(f"Errore durante il salvataggio del file JSON: {error}")