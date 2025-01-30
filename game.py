import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.stamina = 10
        self.max_stamina = 10
        self.inventory = {"Health Potion": 2, "Stamina Potion": 1}
        self.moves = 0
        self.location = "home"
    
    def show_status(self):
        print(f"\n{self.name}'s Status:")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Stamina: {self.stamina}/{self.max_stamina}")
        print(f"Moves since last rest: {self.moves}")

class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Game:
    def __init__(self):
        self.player = None
        self.home_base = Room("Home Base", "This is your safe place to rest and recover.")
        self.current_room = self.home_base

    def start(self):
        player_name = input("Enter your name: ")
        self.player = Player(player_name)
        print(f"Welcome, {self.player.name}! Your adventure begins now.")
        self.game_loop()

    def game_loop(self):
        while True:
            self.player.show_status()
            command = input("What do you want to do? ").strip().lower()
            if command in ['quit', 'exit']:
                print("Thanks for playing!")
                break
            elif command in ['rest']:
                self.rest()
            elif command in ['inventory']:
                self.show_inventory()
            else:
                self.move(command)

    def move(self, direction):
        if self.player.stamina > 0:
            self.player.moves += 1
            self.player.stamina -= 1
            print(f"You move {direction}.")
            if random.random() < 0.3:  # 30% chance of encounter
                self.encounter()
            if self.player.moves >= 5:
                print("You are feeling tired. You need to rest.")
                self.player.stamina = 0
        else:
            print("You are too tired to move. You need to rest.")

    def encounter(self):
        enemy = Enemy("Goblin", 30, 10)
        print(f"A wild {enemy.name} appears!")
        self.battle(enemy)

    def battle(self, enemy):
        while enemy.health > 0 and self.player.health > 0:
            action = input("Do you want to 'attack', 'use item', or 'flee'? ").strip().lower()
            if action == 'attack':
                enemy.health -= 20
                print(f"You attack the {enemy.name} for 20 damage.")
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

    def rest(self):
        if self.player.location == "home":
            print("You rest at your home base to recover stamina.")
            self.player.stamina = min(self.player.max_stamina, self.player.stamina + 5)
            self.player.moves = 0
        else:
            print("You rest to recover stamina.")
            self.player.stamina = min(self.player.max_stamina, self.player.stamina + 2)
            if random.random() < 0.5:  # 50% chance of being attacked while resting
                self.encounter()

    def show_inventory(self):
        print("Your inventory:")
        for item, count in self.player.inventory.items():
            print(f"{item}: {count}")

if __name__ == "__main__":
    game = Game()
    game.start()