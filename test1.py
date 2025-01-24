import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List
from db.models import Well

def load_xml_content(file_path: str) -> str:
    """Load XML file content into string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"XML file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading XML file: {str(e)}")


def parse_datetime(date_str: str) -> datetime:
    """Convert OData datetime string to Python datetime"""
    if date_str:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    return None

def get_well_models(xml_file: str) -> List[Well]:
    # Define namespaces
    namespaces = {
        'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices',
        'm': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata'
    }
    
    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    wells = []
    # Find all entries
    for entry in root.findall('.//m:properties', namespaces):
        well_data = {}
        
        # Map all properties to Well model fields
        for field in Well._meta.fields:
            field_name = field
            if field_name == 'id':
                field_name = '_id'  # Handle special case for id field
                
            elem = entry.find(f'd:{field_name}', namespaces)
            if elem is not None:
                value = elem.text
                field_type = elem.get(f'{{{namespaces["m"]}}}type', 'Edm.String')
                
                # Convert types based on Edm type
                if field_type == 'Edm.Double':
                    value = float(value) if value else None
                elif field_type == 'Edm.DateTime':
                    value = parse_datetime(value)
                elif field_type == 'Edm.Int32':
                    value = int(value) if value else None
                
                well_data[field_name] = value
        
        # Create Well instance
        well = Well(**well_data)
        wells.append(well)
    
    return wells

# Usage example
if __name__ == "__main__":
    # xml_content = load_xml_content('example.xml')
    wells = get_well_models('example.xml')
    for well in wells:
        print(f"Well {well.sigla}: {well.empresa}")