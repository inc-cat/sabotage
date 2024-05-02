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
                choices=[
                    "Bowling Ball",
                    "Double",
                    "Magnet",
                    "Midas Touch",
                    "Oil Spill",
                    "Steam Roller",
                ],
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

    # If stun is applied to a player through items, this will be triggered
    # used to skip turn of current player
    def apply_stun(self, player):
        print("Player is stunned, turn skipped.")
        del player["Status"][player["Status"].index("Stun")]

    def apply_steamroller(self, player):
        # Goes through the range of the area affected by the steam roller item
        for radius in range(player["Location"], player["Location"] + 15):
            # Removes all items from the players current spot to 15 spots ahead
            if self.item_locations[radius]:
                self.item_locations[radius] = ""

        for player_hit in self.game_data["player_data"]:
            # Does not progress if it is selecting the current player
            if player_hit["Name"] == player["Name"]:
                continue
            # Will not progress if player is outside the range
            if (
                player_hit["Location"] < player["Location"]
                or player["Location"] + 15 >= player_hit["Location"]
            ):
                continue

            if (
                random.randrange(1, 5) == 4
                and "Steam Roller" not in player_hit["Status"]
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

    def apply_slow(self, player):
        affected_players = []
        for slow_select in self.game_data["player_data"]:
            if slow_select["Name"] == player["Name"]:
                continue
            else:
                affected_players.append(slow_select)

        affected_player.sort(key=lambda location: location["Place"], reverse=True)
        slow_given = 1
        for supply_slow in affected_players:
            for slow_count in range(slow_given):
                affected_players["Status"].append("Slow")
            slow_given += 1

        item_updater = player["Item(s)"].index("Slow")
        del player["Item(s)"][item_updater]

    def apply_midastouch(self, player):
        getpass.getpass(prompt="Press Enter to roll again")
        midastouch_updater = player["Status"].index("Midas Touch")
        del player["Status"][midastouch_updater]
        midas_roll = random.randrange(1, 4)
        print(f"You rolled {midas_roll}")
        return midas_roll

    def apply_oilspill(self, player):
        oil_question = [
            inquirer.List(
                "oil_spill",
                message="How will you throw?",
                choices=["Forwards", "Backwards"],
            ),
        ]

        oil = inquirer.prompt(oil_question)["oil_spill"]

        player_location = int(player["Location"])
        if oil == "Forwards":
            self.item_location[player_location + 8] = "Oil Spill"
        elif oil == "backwards":
            self.item_location[player_location - 1] = "Oil Spill"

    def apply_magnet(self, player):
        affected_players = [
            p
            for p in self.game_data["player_data"]
            if player["Location"] < p["Location"] <= player["Location"] + 14
        ]

        if affected_players:
            affected_players.sort(key=lambda location: location["Location"])

            hit_chance = random.randrange(0, 4)
            if (
                hit_chance == 0
                or "Midas Touch" in affected_players[0]["Status"]
                or "Steam Roller" in affected_players[0]["Status"]
            ):
                print(
                    f"The magnet fails to hit {affected_players[0]['Name']} and crashes!"
                )
            else:
                print(
                    f"The magnet hits {affected_players[0]['Name']} and inflicts stun!"
                )

                affected_players[0]["Status"].append("Stun")
        else:
            magnet_throw = player["Location"] + 14
            self.item_locations[magnet_throw] = "Magnet"

        magnet_updater = player["Item(s)"].index("Magnet")
        del player["Item(s)"][magnet_updater]

    def apply_bowlingball(self, player):
        affected_players = [
            p
            for p in self.game_data["player_data"]
            if player["Location"] < p["Location"]
        ]

        if affected_players:
            affected_players.sort(
                key=lambda location: location["Location"], reverse=True
            )

        outcome_strings = []
        chance = 4
        first_player = True

        for bowling_hit in affected_players:
            if first_player:
                chance_first = random.randrange(1, 5)
                if chance_first < 4:
                    bowling_hit["Status"] = ["Stun"]
                    outcome_strings.append(
                        f"{bowling_hit['Name']} was hit and is now stunned!"
                    )
                else:
                    outcome_strings.append(f"{bowling_hit['Name']} dodged!")
                first_player = False
            else:
                chance_after = random.randrange(0, chance)
                if chance == 0:
                    outcome_strings.append(
                        f"{bowling_hit['Name']} was hit and is now stunned!"
                    )
                else:
                    outcome_strings.append(f"{bowling_hit['Name']} dodged!")

                chance *= 2

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
                    self.apply_stun(current_player)
                    continue

                # steam roller pushes the player 15 players forward and destroys all items in its way
                # has a 25% chance of hitting a player if a player is in the movement range
                elif "Steam Roller" in current_player["Status"]:
                    self.apply_steamroller(current_player)

                getpass.getpass(prompt="Press Enter to roll")

                roll_amount = self.dice_roll(current_player)

                if "Midas Touch" in current_player["Status"]:
                    midas_roller = self.apply_midastouch(current_player)
                    roll_amount += midas_roller

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
                    elif item_answer["option"] == "Midas Touch":
                        current_player["Status"] = [
                            "Midas Touch",
                            "Midas Touch",
                            "Midas Touch",
                        ]
                    elif item_answer["option"] == "Oil Spill":
                        self.apply_oilspill(current_player)

                else:
                    pass

                current_player["Location"] += roll_amount

            # print(self.game_data)
            break


run = Sabotage()
plus = run.options_screen()
if plus["option"] == "Start":
    run.game_details()
    run.game_time()
elif plus["option"] == "About":
    run.about()
