from typing import Any, Dict, List


def get_object_info(data: Dict[str, Any], object_to_search: str) -> List[str]:
    """
    Recursively searches for an object in the catalog and returns its name, category, and location path.

    Parameters:
        node (dict): The current node (container) in the catalog.
        target_object (str): The name of the object to search for.

    Returns:
        list: A list containing [object_name, category, container names from inner to outer].
              Returns an empty list if the object is not found.
    """
    
    for object in data.get("objects", []):
        
        if object_to_search == object.get("name"):
            
            return [object["name"], object["category"], data["name"]]
        
    for container in data.get("containers", []):
        
        result = get_object_info(container, object_to_search)
        
        if result:
            
            return result + [data["name"]]

    return []



def delete_object(data: Dict[str, Any], object_name: str) -> bool:
    """
    Delete an object from the nested catalog structure.

    This function performs a recursive search through all containers
    to find and remove the specified object.

    Parameters:
        data: The catalog data (nested dictionary).
        object_name: The name of the object to delete.

    Returns:
        True if the object was deleted, False otherwise.
    """
    
    objects_list = data.get("objects", [])
    
    for object in objects_list:
        
        if object.get("name") == object_name:
            
            objects_list.remove(object)
            
            return True

    for container in data.get("containers", []):
        
        if delete_object(container, object_name):
            
            return True

    return False



def get_object(data: Dict[str, Any], object_name: str) -> Dict[str, str] | None:
    """
    Recursively searches for an object by name in the catalog.

    Parameters:
        data (Dict[str, Any]): The catalog data structure.
        object_name (str): The name of the object to find.

    Returns:
        Dict[str, str] | None: The object dictionary if found, otherwise None.
    """
    for object in data.get("objects", []):
        
        if object.get("name") == object_name:
            
            return object
    
    for container in data.get("containers", []):
        
        result = get_object(container, object_name)
        
        if result:
            
            return result
    
    return None



def modify_object(data: Dict[str, Any], object_name: str, new_object_name: str = "", new_category_name: str = "") -> bool:
    """
    Modifies the name and/or category of an existing object in the catalog.

    Parameters:
        data (Dict[str, Any]): The catalog data.
        object_name (str): The current name of the object to modify.
        new_object_name (str, optional): The new name to assign (leave blank to skip).
        new_category_name (str, optional): The new category to assign (leave blank to skip).

    Returns:
        bool: True if the object was found and modified, False otherwise.
    """
    object: Dict[str, Any] = get_object(data, object_name)
    
    if object is None:
        
        return False
    
    if new_object_name:
        
        object["name"] = new_object_name
        
    if new_category_name: 
        
        object["category"] = new_category_name
        
    return True



def get_container_by_name(data: Dict[str, Any], container_name: str) -> Dict[str, Any] | None:
    """
    Recursively searches for a container by name within the catalog structure.
    Searches the current node and all nested containers until a match is found.

    Parameters:
        data (Dict[str, Any]): The catalog data structure to search in.
        container_name (str): The name of the container to locate.

    Returns:
        Dict[str, Any] | None: The container dictionary if found, otherwise None.
    """
    if data.get("name") == container_name:
        return data

    for container in data.get("containers", []):
        result = get_container_by_name(container, container_name)
        if result:
            return result

    return None
