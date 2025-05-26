from BaseClasses import World, Item
from .Items import item_name_to_id
from .Locations import location_name_to_id
from .Options import ColdSteelOptions
from .coldsteel_item_data import CHEST_ITEM_TABLE
from .craft_item_table import CRAFT_ITEM_TABLE
from .chest_patch_table import CHEST_PATCH_TABLE
from pathlib import Path
import pandas as pd
import struct

class ColdSteelWorld(World):
    game = "Cold Steel"
    option_definitions = ColdSteelOptions

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    def create_items(self):
        if self.options.randomize_chests:
            for name, item_id in CHEST_ITEM_TABLE.items():
                self.itempool.append(Item(name, self.player, item_id))

        if self.options.randomize_crafts:
            for name, item_id in CRAFT_ITEM_TABLE.items():
                self.itempool.append(Item(name, self.player, item_id))

    def create_regions(self):
        from BaseClasses import Region, Location
        start_region = Region("Cold Steel World", self.player, self.multiworld)
        for name, loc_id in self.location_name_to_id.items():
            location = Location(self.player, name, loc_id, self)
            start_region.locations.append(location)
        self.multiworld.regions.append(start_region)

    def set_rules(self):
        from Rules import set_rule
        victory_location = self.multiworld.get_location("Old Schoolhouse - Chest 1000", self.player)
        set_rule(victory_location, lambda state: True)
        self.multiworld.completion_condition[self.player] = lambda state: state.can_reach(victory_location)

    def generate_output(self, output_directory: str):
        if self.options.randomize_chests:
            output_path = Path(output_directory) / f"AP_{self.player}_coldsteel_chests.txt"
            with open(output_path, "w", encoding="utf-8") as log:
                for location_name, (map_id, offsets) in CHEST_PATCH_TABLE.items():
                    location = self.multiworld.get_location(location_name, self.player)
                    if not location or not location.item:
                        continue
                    item_id = location.item.code
                    log.write(f"{location_name}: item ID {item_id}\n")
                    map_file_path = Path("data/scripts/scena/dat_us") / f"{map_id}.dat"
                    if not map_file_path.exists():
                        continue
                    with open(map_file_path, "r+b") as map_file:
                        for offset in offsets:
                            map_file.seek(offset)
                            map_file.write(item_id.to_bytes(2, 'little'))

        if self.options.randomize_crafts:
            magic_path = Path("input/Files/Magic.csv")
            magic_df = pd.read_csv(magic_path)
            received_craft_ids = []
            for location in self.multiworld.get_locations(self.player):
                if location.name.startswith("Rean") or location.name.startswith("Emma") or "Craft Slot" in location.name:
                    if location.item and location.item.name in CRAFT_ITEM_TABLE:
                        received_craft_ids.append(CRAFT_ITEM_TABLE[location.item.name])

            patched_rows = magic_df[magic_df["id"].isin(received_craft_ids)]
            output_tbl_path = Path(output_directory) / f"AP_{self.player}_t_magic.tbl"
            with open(output_tbl_path, "wb") as f:
                f.write(struct.pack("<H", len(patched_rows)))
                for _, row in patched_rows.iterrows():
                    f.write(struct.pack(
                        "<HH4s18B32s64s",
                        int(row["id"]),
                        int(row["char_restriction"]),
                        bytes(row["flags"], encoding="utf-8").ljust(4, b'\x00'),
                        int(row["category"]), int(row["type"]), int(row["element"]),
                        int(row["targetting_type"]), int(row["targetting_range"]), int(row["targetting_size"]),
                        int(row["effect1_id"]), int(row["effect1_data1"]), int(row["effect1_data2"]),
                        int(row["effect2_id"]), int(row["effect2_data1"]), int(row["effect2_data2"]),
                        int(row["cast_delay"]), int(row["recovery_delay"]), int(row["cost"]),
                        int(row["unbalance_bonus"]), int(row["level"]), int(row["sort_id"]),
                        bytes(row["animation"], encoding="utf-8").ljust(32, b'\x00'),
                        bytes(row["name"], encoding="utf-8").ljust(64, b'\x00')
                    ))

    def fill_slot_data(self):
        return {
            "options": {opt_name: getattr(self.options, opt_name).value for opt_name in ColdSteelOptions.options}
        }
