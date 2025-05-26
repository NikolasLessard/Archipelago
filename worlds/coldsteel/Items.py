from typing import Dict
from BaseClasses import Item
from ItemList import item_name_groups
from .coldsteel_item_data import CHEST_ITEM_TABLE

item_name_to_id: Dict[str, int] = {}
id_to_item_name: Dict[int, str] = {}

for i, (name, item_id) in enumerate(CHEST_ITEM_TABLE.items()):
    item_name_to_id[name] = item_id
    id_to_item_name[item_id] = name

