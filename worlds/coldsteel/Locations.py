from typing import Dict
from .coldsteel_location_data import location_name_to_id as chest_location_name_to_id, id_to_location_name as chest_id_to_location_name
from .craft_location_data import location_name_to_id as craft_location_name_to_id, id_to_location_name as craft_id_to_location_name

# Combine both location tables
location_name_to_id: Dict[str, int] = {**chest_location_name_to_id, **craft_location_name_to_id}
id_to_location_name: Dict[int, str] = {**chest_id_to_location_name, **craft_id_to_location_name}
