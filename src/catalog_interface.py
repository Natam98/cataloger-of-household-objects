from typing import Any, Dict, Literal
from src.catalog_manage import get_object_info, delete_object, get_container_by_name, modify_object
from src.data_storage import save_json_file


def explore_catalog(data: Dict[str, Any], path: list[str] | None = None) -> None:
    """
    Recursively traverses the catalog and prints details of all objects.

    Starts from the given node and explores all nested containers,
    printing each object's name, category, and its full hierarchical path.

    Parameters:
        data (Dict[str, Any]): The current node (container) in the catalog.
        path (list[str] | None): The path of container names from the root to the current node.
                                 Defaults to None, which initializes the path with the root name.

    Returns:
        None
    """    
    if path is None:
        
        path = [data.get("name", "house")]

    for object in data.get("objects", []):
        
        print(f"Name: {object.get("name", "")}")
        print(f"Category: {object.get("category", "")}")
        print(f"Location: {" > ".join(path)}")
        print("-" * 50)

    for container in data.get("containers", []):
        
        new_path = path + [container.get("name", "")]
        
        explore_catalog(container, new_path)   



def search_object_in_catalog(data: Dict[str, Any]) -> None:
    """
    Prompts the user for an object name and searches for it in the catalog.

    If the object is found, its name, category, and location path are printed.
    Otherwise, a message is shown indicating the object was not found.

    Parameters:
        data (Dict[str, Any]): The catalog data structure to search in.

    Returns:
        None
    """        
    object_name = input("Enter the name of the object to search: ").strip().lower()
    
    object_info = get_object_info(data, object_name)
    
    if object_info:
        print(f"Name: {object_info[0]}")
        print(f"Category: {object_info[1]}")
        print(f"Location: {" > ".join(object_info[2:][::-1])}")
        
    else:
        print("Object not found in the catalog!")



def delete_object_from_catalog(data: Dict[str, Any], file_name: str) -> None:
    """
    Prompts the user to delete an object from the catalog by name.

    If the object is found and deleted, the catalog is saved to file.
    Otherwise, an error message is displayed.

    Parameters:
        data (Dict[str, Any]): The catalog data structure.
        file_name (str): The file path where the updated catalog should be saved.

    Returns:
        None
    """
    object_name = input("Enter the name of the object to delete: ").strip().lower()
    
    if delete_object(data, object_name):
        
        save_json_file(data, file_name)
        
        print("Object successfully deleted from the catalog!")

    else:
        print(f"Object not found in the catalog!")



def modify_object_in_catalog(data: Dict[str, Any], file_name: str) -> None:
    """
    Allows the user to modify an object's name and/or category in the catalog.

    If the object is found, its data is updated and the catalog is saved.
    Otherwise, a message is shown indicating that the object was not found.

    Parameters:
        data (Dict[str, Any]): The catalog structure.
        file_name (str): The file path where the updated catalog should be saved.

    Returns:
        None
    """
    object_name = input("Enter the name of the object to modify: ").strip().lower()
    
    new_object_name = input("Enter the new name of the object (blank line to keep it unchanged): ").strip().lower()
    
    new_category_name = input("Enter the new category of the object (blank line to keep it unchanged): ").strip().lower()
    
    if modify_object(data, object_name, new_object_name, new_category_name):
        
        save_json_file(data, file_name)
        
        print("Object successfully modified in the catalog!")
    
    else:
        
        print(f"Object not found in the catalog!")
    


def get_container_for_adding(data: Dict[str, Any], key: Literal["objects", "containers"]) -> Dict[str, Any]:
    """
    Prompts the user to select a container by name for adding an object or a new container.

    Performs recursive search until a valid container is found.

    Parameters:
        data (Dict[str, Any]): The catalog structure.
        key (Literal["objects", "containers"]): Determines the context of addition
                                                ("objects" for adding an object,
                                                 "containers" for adding a new container).

    Returns:
        Dict[str, Any]: The container where the object or new container will be added.
    """
    prompt = {
        
        "objects": "Enter the name of the container where you want to add the object (e.g. 'house', 'kitchen'): ",
        
        "containers": "Enter the name of the container where the new container should be added (e.g. 'house', 'kitchen'): "
    }
    
    error_message = {
        
        "objects": "Container not found. Please try again!",
        
        "containers": "Container where you want to insert the new container not found. Please try again!"
    }
    
    while not (container := get_container_by_name(data, input(prompt[key]).strip().lower())):
            
        print(error_message[key])

    return container



def create_new_object() -> Dict[str, str]:
    """
    Prompts the user to enter details for a new object (name and category).

    Returns:
        Dict[str, str]: A dictionary representing the new object.
    """
    object_name = input("Enter the name of the object to add to the catalog: ").strip().lower()

    object_category = input("Enter the category of the object to add: ").strip().lower()
    
    return {"name": object_name, "category": object_category}  



def add_object(data: Dict[str, Any], file_name: str) -> None:
    """
    Creates a new object and adds it to a user-selected existing container.

    Saves the updated catalog to the specified file.

    Parameters:
        data (Dict[str, Any]): The catalog structure.
        file_name (str): The file path where the updated catalog should be saved.

    Returns:
        None
    """
    new_object = create_new_object() 
        
    container: Dict[str, Any] = get_container_for_adding(data, "objects")
    
    container.get("objects", []).append(new_object)
    
    save_json_file(data, file_name)
    
    print("Object successfully added to the catalog!")
    
    
    
def add_object_in_catalog(data: Dict[str, Any], file_name) -> None:
    """
    Handles object addition, either to an existing container or by creating a new container.

    Prompts the user to choose between adding the object to an existing container (option 1),
    or creating a new container and adding the object inside it (option 2).

    Parameters:
        data (Dict[str, Any]): The catalog structure.
        file_name (str): The file path where the updated catalog should be saved.

    Returns:
        None
    """
    print("Press [1] to add an object to an existing container.")
    print("Press [2] to create a new container and add an object to it.")

    while not (user_choice := input("\nChoose an option: ").strip()) in ["1", "2"]:
        
        print("Invalid input. Please enter 1 or 2!")
        
    match user_choice:
        
        case "1":
            
            add_object(data, file_name)
        
        case "2":
            
            new_container_name = input("Enter the name of the new container: ").strip().lower()
            
            new_container: Dict[str, Any] = {"name": new_container_name, "objects": [], "containers": []}

            container: Dict[str, Any] = get_container_for_adding(data, "containers")
    
            container.get("containers", []).append(new_container)
            
            new_object: Dict[str, str] = create_new_object()
            
            new_container.get("objects", []).append(new_object)
    
            save_json_file(data, file_name)
            
            print("New container and object successfully added to the catalog!")  
