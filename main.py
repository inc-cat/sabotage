import inquirer
import json
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
                    "Item(s)": "",
                    "Status": [],
                    "Place": "",
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
                if "Stun" in current_player["Status"]:
                    print("Player is stunned, turn skipped.")
                    del current_player["Status"][current_player["Status"].index("Stun")]
                    continue

                # steam roller pushes the player 15 players forward and destroys all items in its way
                # has a 25% chance of hitting a player if a player is in the movement range
                elif "Steam Roller" in current_player["Status"]:
                    radius = [
                        current_player["Location"],
                        current_player["Location"] + 15,
                    ]
                    current_player["Location"] += 15
                    for radius in range(
                        current_player["Location"], current_player["Location"] + 15
                    ):
                        if self.item_locations[radius]:
                            self.item_locations[radius] = ""
                        else:
                            continue

                    for player_hit in self.game_data["player_data"]:
                        if player_hit["Name"] == current_player["Name"]:
                            continue
                        else:
                            if random.randrange(1, 5) == 4:
                                if (
                                    "Steam Roller" in player_hit["Status"]
                                    or "Midas Touch" in player_hit["Status"]
                                ):
                                    print(
                                        current_player["Name"],
                                        "misses",
                                        player_hit["Name"],
                                        ".",
                                    )
                                    pass
                                else:
                                    player_hit["Satus"].append("Stun")

                getpass.getpass(prompt="Press Enter to roll")

                if "Slow" in current_player["Status"]:
                    roll = random.randrange(1, 4)
                else:
                    roll = random.randrange(1, 7)


            break


run = Sabotage()
plus = run.options_screen()
if plus["option"] == "Start":
    run.game_details()
    run.game_time()
elif plus["option"] == "About":
    run.about()
