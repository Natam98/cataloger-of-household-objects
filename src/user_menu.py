from typing import Any, Dict
from src.data_storage import load_json_file
from src.catalog_interface import add_object_in_catalog, delete_object_from_catalog, explore_catalog, isInteger, modify_object_in_catalog, search_object_in_catalog

file_name: str = "data/house_catalog.json"

data: Dict[str, Any] = load_json_file(file_name)

menu_options: Dict[int, str] = {
    "1": "view all objects in the catalog.",
    "2": "search for an object by name.",
    "3": "add a new object to the catalog.",
    "4": "edit an existing object.",
    "5": "delete an object from the catalog.",
}


def display_menu_options(menu_options: Dict[int, str]) -> None:
    
    print("Welcome to the Cataloger of Household Objects!\n")

    for key, option in menu_options.items():
        
        print(f"Press [{key}] to {option}")



def main() -> None:

    display_menu_options(menu_options)

    while not (isInteger(user_choice := input("\nChoose an option: ").strip())
                and user_choice in menu_options):
        print("Invalid input. Please try again!")

    match user_choice: 
        case "1":
            explore_catalog(data)
        
        case "2":
            search_object_in_catalog(data)
            
        case "3":
            add_object_in_catalog(data, file_name)
            
        case "4":
            modify_object_in_catalog(data, file_name)
            
        case "5":
            delete_object_from_catalog(data, file_name)
