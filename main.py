import inquirer
import random
import pandas as pd
import getpass
import data


class Sabotage:
    def __init__(self):

        # all instances of the below string are to clear the screen for use experience
        print("\033c")

        # for loop to work on multi line ascii text and initial credit
        for ascii_line in data.TITLE_TEXT:
            print(ascii_line)
        input("by Anwar Louis\nPress enter to continue. . . ")

    # main options screen for user to pick what they want to do.
    def options_screen(self):
        print("\033c")
        for ascii_line in data.TITLE_TEXT:
            print(ascii_line)
        option_question = [
            inquirer.List(
                "option",
                message="Where do we go from here?",
                choices=["Start", "About", "Credits", "Added options", "Quit"],
            ),
        ]

        return inquirer.prompt(option_question)

    # Game rules and mechanics are explained from here, text is from data.json as data
    def about(self):
        print("\033c")
        for ascii_line in data.TITLE_TEXT:
            print(ascii_line)
        print("\n", data.INTRO_TEXT)
        for item_scroll in data.ITEM_RUNDOWN:
            print(item_scroll)
        print("\n---")
        print(data.NOTES)

    # If a player choses to start the game
    def game_details(self):
        print("\033c")
        numbers_question = [
            inquirer.List(
                "players",
                message="How many players?",
                choices=[2, 3, 4, 5],
            ),
        ]
        numbers = inquirer.prompt(numbers_question)

        self.player_data = []
        player_names = []
        for player_numbers in range(numbers["players"]):
            while True:
                current_player = input(f"Player {player_numbers + 1} name: ")
                if current_player == "":
                    print("\rPlease type a name!")
                elif current_player in player_names:
                    print("\r Name already taken!")
                else:
                    break
            player_names.append(current_player)
            self.player_data.append(
                {
                    "Name": current_player,
                    "Location": 0,
                    "Item(s)": [],
                    "Status": [],
                    "Place": None,
                }
            )

        print("\033c")
        items_question = [
            inquirer.Checkbox(
                "items",
                message="Which items are allowed to be used?",
                choices=["Brown", "Blue", "Yellow"],
            ),
        ]
        items = inquirer.prompt(items_question)

        print("\033c")
        duration_question = [
            inquirer.List(
                "duration",
                message="How much to win?",
                choices=[50, 100, 200, 400],
            ),
        ]

        space = inquirer.prompt(duration_question)

        # game data is stored in this dictionary and will be referenced when gameplay has started
        self.game_data = {
            "player_data": self.player_data,
            "items": items["items"],
            "duration": space["duration"],
        }

    def apply_stun(self, player):
        print("Player is stunned, turn skipped.")
        del player["Status"][player["Status"].index("Stun")]

    def apply_steamroller(self, player):
        for radius in range(player["Location"], player["Location"] + 15):
            if self.item_locations[radius]:
                self.item_locations[radius] = ""

        for player_hit in self.game_data["player_data"]:
            if player_hit["Name"] == player["Name"]:
                continue
            if (
                player_hit["Location"] < player["Location"]
                or player["Location"] + 15 >= player_hit["Location"]
            ):
                continue


            if (
                random.randrange(1, 5) == 4 and 
                "Steam Roller" not in player_hit["Status"]
                and "Midas Touch" not in player_hit["Status"]
            ):
                print(
                    player["Name"],
                    "hits",
                    player_hit["Name"] + "!",
                )
                player_hit["Status"].append("Stun")
                
            else:
                print(
                    player["Name"],
                    "misses",
                    player_hit["Name"],
                    ".",
                )
                

        player["Location"] += 15
        status_updater = player["Status"].index("Steam Roller")
        del player["Status"][status_updater]

    def dice_roll(self, player):
        if "Slow" in player["Status"]:
            roll = random.randrange(1, 4)
        else:
            roll = random.randrange(1, 7)

        print(f"You rolled {roll}!")
        return roll

    def game_time(self):
        print("\033c")
        # when items are placed on the board
        self.item_locations = {}
        for construct_items in range(1, self.game_data["duration"] + 1):
            self.item_locations[construct_items] = ""

        # shuffles player order for game
        random.shuffle(self.game_data["player_data"])

        # while game is in progress, this will loop continually until all players are finished
        while True:
            # stunned players will have to skip a turn
            # if stun is found in the status list, it will be removed.
            for current_player in self.game_data["player_data"]:
                current_player["Item(s)"] = ["Double"]
                if "Stun" in current_player["Status"]:
                    self.apply_stun(current_player)
                    continue

                # steam roller pushes the player 15 players forward and destroys all items in its way
                # has a 25% chance of hitting a player if a player is in the movement range
                elif "Steam Roller" in current_player["Status"]:
                    self.apply_steamroller(current_player)

                getpass.getpass(prompt="Press Enter to roll")

                roll_amount = self.dice_roll(current_player)

                if current_player["Item(s)"]:
                    item_options = list(current_player["Item(s)"])
                    questions = [
                        inquirer.List(
                            "option",
                            message="What size do you need?",
                            choices=item_options + ["Pass"],
                        ),
                    ]

                    item_answer = inquirer.prompt(questions)
                    if item_answer["option"] == "Pass":
                        continue
                    elif item_answer["option"] == "Double":
                        double_roll = self.dice_roll(current_player)
                        print(f"Which brings your total to {double_roll + roll_amount}")
                        roll_amount += double_roll
                    elif item_answer["option"] == "Steam Roller":
                        current_player["Status"] = ["Steam Roller", "Steam Roller"]

                else:
                    pass

                current_player["Location"] += roll_amount

            break


run = Sabotage()
plus = run.options_screen()
if plus["option"] == "Start":
    run.game_details()
    run.game_time()
elif plus["option"] == "About":
    run.about()
