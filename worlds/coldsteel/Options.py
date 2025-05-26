from Options import Toggle, OptionSet

class RandomizeChests(Toggle):
    """Randomize chests across the game."""
    display_name = "Randomize Chests"
    default = True

class RandomizeCrafts(Toggle):
    """Randomize crafts per character."""
    display_name = "Randomize Crafts"
    default = False

class RandomizeMasterQuartz(Toggle):
    """Randomize Master Quartz abilities and properties."""
    display_name = "Randomize Master Quartz"
    default = False

class RandomizeNoteCook(Toggle):
    """Randomize NoteCook notebook unlocks (recipes, books, info)."""
    display_name = "Randomize NoteCook"
    default = False

class RandomizeStats(Toggle):
    """Randomize character stat growth or base stats."""
    display_name = "Randomize Stats"
    default = False

class RandomizeMonsters(Toggle):
    """Randomize monsters and enemy data."""
    display_name = "Randomize Monsters"
    default = False

class RandomizeQoL(Toggle):
    """Randomize or modify QoL features (e.g., money, XP rates)."""
    display_name = "Randomize QoL"
    default = False

class RandomizeOrbmentSlots(Toggle):
    """Randomize orbment line structure and slots."""
    display_name = "Randomize Orbment Slots"
    default = False

class ColdSteelOptions(OptionSet):
    options = {
        "randomize_chests": RandomizeChests,
        "randomize_crafts": RandomizeCrafts,
        "randomize_master_quartz": RandomizeMasterQuartz,
        "randomize_notecook": RandomizeNoteCook,
        "randomize_stats": RandomizeStats,
        "randomize_monsters": RandomizeMonsters,
        "randomize_qol": RandomizeQoL,
        "randomize_orbment_slots": RandomizeOrbmentSlots,
    }
