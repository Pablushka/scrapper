import xml.etree.ElementTree as ET
from  xml.etree.ElementTree import Element
from typing import Dict, Any


def xml_to_dict(data: bytes ) -> Dict[str, Any]:
    """Convert XML to dictionary recursively."""
    result = {}

    if type(data) != Element:
        element = ET.fromstring(data)
    else:
        element = data

    # Handle attributes
    if element.attrib:
        result.update(element.attrib)
    
    # Handle children
    for child in element:
        # Remove namespace prefix from tags
        tag = child.tag.split('}')[-1]
        
        child_data = xml_to_dict(child)
        
        if tag in result:
            if not isinstance(result[tag], list):
                result[tag] = [result[tag]]
            result[tag].append(child_data)
        else:
            result[tag] = child_data
    
    # Handle text content
    if element.text and element.text.strip():
        if result:
            result['value'] = element.text.strip()
        else:
            result = element.text.strip()
    
    return result
