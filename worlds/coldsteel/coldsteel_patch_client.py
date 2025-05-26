import asyncio
from NetUtils import NetworkItem
from CommonClient import CommonContext, server_loop
from .craft_item_table import CRAFT_ITEM_TABLE
import pandas as pd
import struct
from pathlib import Path

class ColdSteelContext(CommonContext):
    game = "Cold Steel"
    async def on_received_items(self):
        received = [item.item for item in self.items_received if item.player == self.slot]
        await apply_crafts(received)

async def apply_crafts(received_ids):
    print("[PatchClient] Received items:", received_ids)
    magic_path = Path("input/Files/Magic.csv")
    magic_df = pd.read_csv(magic_path)
    matched_rows = magic_df[magic_df["id"].isin(received_ids)]

    if not matched_rows.empty:
        output_path = Path("data/t_magic.tbl")
        with open(output_path, "wb") as f:
            f.write(struct.pack("<H", len(matched_rows)))
            for _, row in matched_rows.iterrows():
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
        print("[PatchClient] Patched t_magic.tbl. Please restart your game to apply changes.")

async def main():
    ctx = ColdSteelContext("Cold Steel Client")
    ctx.auth = {
        "password": None
    }
    ctx.server_address = input("Enter Archipelago server address (e.g. localhost:38281): ")
    await server_loop(ctx, lambda: True)

if __name__ == "__main__":
    asyncio.run(main())
