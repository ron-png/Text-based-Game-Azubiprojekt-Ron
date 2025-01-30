import random
from dataclasses import dataclass

@dataclass
class Item:
    name: str
    description: str
    price: int
    effect: str

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.stamina = 10
        self.max_stamina = 10
        self.gold = 50
        self.attack_power = 15
        self.inventory = {
            "Health Potion": 2,
            "Stamina Potion": 1,
            "Weapon": "Rusty Sword",
            "Keys": 0
        }
        self.location = "village"
        self.moves = 0

    def show_status(self):
        print(f"\n{self.name}'s Status:")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Stamina: {self.stamina}/{self.max_stamina}")
        print(f"Gold: {self.gold}")
        print(f"Weapon: {self.inventory['Weapon']} (+{self.attack_power} damage)")

class Enemy:
    def __init__(self, name, health, attack, gold_drop):
        self.name = name
        self.health = health
        self.attack = attack
        self.gold_drop = gold_drop

class Location:
    def __init__(self, name, description, exits, safe=False):
        self.name = name
        self.description = description
        self.exits = exits
        self.safe = safe

class Vendor:
    def __init__(self, name, wares):
        self.name = name
        self.wares = wares

# Game Items
ITEMS = {
    "Health Potion": Item("Health Potion", "Restores 20 HP", 15, "health"),
    "Stamina Potion": Item("Stamina Potion", "Restores 5 Stamina", 10, "stamina"),
    "Iron Sword": Item("Iron Sword", "+5 Attack Power", 50, "weapon"),
    "Mystery Key": Item("Myst ery Key", "Unlocks special areas", 25, "key")
}

class Game:
    def __init__(self):
        self.player = None
        self.locations = {
            "village": Location("Village", "A bustling village with shops and friendly NPCs.", ["forest", "home"]),
            "forest": Location("Enchanted Forest", "A mystical forest filled with magical creatures.", ["village", "dark cave"]),
            "dark cave": Location("Dark Cave", "A dark and eerie cave with hidden treasures.", ["forest", "mountain pass"]),
            "mountain pass": Location("Mountain Pass", "A treacherous path leading to the mountains.", ["dark cave", "abandoned temple"]),
            "abandoned temple": Location("Abandoned Temple", "An ancient temple filled with secrets.", ["mountain pass"])
        }
        self.vendors = {
            "village": Vendor("Potion Master", [ITEMS["Health Potion"], ITEMS["Stamina Potion"], ITEMS["Iron Sword"]])
        }
        self.current_location = self.locations["village"]

    def start(self):
        player_name = input("Enter your name: ")
        self.player = Player(player_name)
        print(f"Welcome, {self.player.name}! Your adventure begins now.")
        self.game_loop()

    def game_loop(self):
        while True:
            self.player.show_status()
            print(f"\nYou are at the {self.current_location.name}. {self.current_location.description}")
            print(f"Available exits: {', '.join(self.current_location.exits)}")
            print("Available commands: help, rest, inventory, move <location>, shop, quit")
            command = input("What do you want to do? ").strip().lower()
            if command == 'quit':
                print("Thanks for playing!")
                break
            elif command == 'help':
                self.show_help()
            elif command == 'rest':
                self.rest()
            elif command == 'inventory':
                self.show_inventory()
            elif command == 'shop':
                self.visit_shop()
            elif command.startswith('move '):
                direction = command.split(' ')[1]
                self.move(direction)
            else:
                print("Invalid command.")

    def show_help(self):
        print("Available commands:")
        print(" - help: Show this help message")
        print(" - rest: Rest to recover stamina")
        print(" - inventory: Show your inventory")
        print(" - move <direction>: Move to a different location")
        print(" - shop: Visit the shop to buy items")
        print(" - quit: Exit the game")

    def move(self, direction):
        if direction in self.current_location.exits:
            if direction == "home" and self.current_location.name != "village":
                print("You can only access your home base from the village.")
            else:
                self.current_location = self.locations[direction]
                print(f"You move to the {self.current_location.name}.")
        else:
            print("You can't go that way.")

    def visit_shop(self):
        vendor = self.vendors["village"]
        print(f"\nWelcome to {vendor.name}'s shop!")
        print("Items for sale:")
        for item in vendor.wares:
            print(f"{item.name}: {item.price} gold - {item.description}")
        item_to_buy = input("Which item do you want to buy? (type 'exit' to leave) ").strip()
        if item_to_buy in [item.name for item in vendor.wares]:
            item = next(item for item in vendor.wares if item.name == item_to_buy)
            if self.player.gold >= item.price:
                self.player.gold -= item.price
                self.player.inventory[item.name] = self.player.inventory.get(item.name, 0) + 1
                print(f"You bought a {item.name}.")
            else:
                print("You don't have enough gold.")
        elif item_to_buy == 'exit':
            print("Leaving the shop.")
        else:
            print("Invalid item.")

    def rest(self):
        if self.current_location.name == "village":
            print("You rest at your home base to recover stamina.")
            self.player.stamina = min(self.player.max_stamina, self.player.stamina + 5)
        else:
            print("You rest to recover stamina.")
            self.player.stamina = min(self.player.max_stamina, self.player.stamina + 2)
            if random.random() < 0.5:  # 50% chance of being attacked while resting
                self.encounter()

    def show_inventory(self):
        print("Your inventory:")
        for item, count in self.player.inventory.items():
            print(f"{item}: {count}")
        print(f"Gold: {self.player.gold}")

    def encounter(self):
        enemy = Enemy("Goblin", 30, 10, 10)
        print(f"A wild {enemy.name} appears!")
        self.battle(enemy)

    def battle(self, enemy):
        while enemy.health > 0 and self .player.health > 0:
            action = input("Do you want to 'attack', 'use item', or 'flee'? ").strip().lower()
            if action == 'attack':
                enemy.health -= self.player.attack_power
                print(f"You attack the {enemy.name} for {self.player.attack_power} damage.")
                if enemy.health > 0:
                    self.player.health -= enemy.attack
                    print(f"The {enemy.name} attacks you for {enemy.attack} damage.")
            elif action == 'use item':
                self.use_item()
            elif action == 'flee':
                if random.random() < 0.5:  # 50% chance to flee
                    print("You successfully fled!")
                    break
                else:
                    print("You failed to flee!")
                    self.player.health -= enemy.attack
            else:
                print("Invalid action.")
            if self.player.health <= 0:
                print("You have been defeated! Game over.")
                break
        if enemy.health <= 0:
            print(f"You defeated the {enemy.name} and collected {enemy.gold_drop} gold!")
            self.player.gold += enemy.gold_drop

    def use_item(self):
        item = input("Which item do you want to use? ").strip()
        if item in self.player.inventory and self.player.inventory[item] > 0:
            if item == "Health Potion":
                self.player.health = min(self.player.max_health, self.player.health + 20)
                self.player.inventory[item] -= 1
                print("You used a Health Potion.")
            elif item == "Stamina Potion":
                self.player.stamina = min(self.player.max_stamina, self.player.stamina + 5)
                self.player.inventory[item] -= 1
                print("You used a Stamina Potion.")
        else:
            print("You don't have that item.")

if __name__ == "__main__":
    game = Game()
    game.start()