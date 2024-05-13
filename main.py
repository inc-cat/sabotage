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

        # holda all player data
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
                    "Finished": False
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
                    "Slow",
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
                choices=[100, 200, 400, 500],
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
        # determining how far the player will move with a rng die roll
        if "Slow" in player["Status"]:
            roll = random.randrange(1, 4)
        else:
            roll = random.randrange(1, 7)

        print(f"You rolled {roll}!")
        return roll

    def apply_slow(self, player):
        # the slow affect halves the movement speed of the player by halving what a player can roll
        affected_players = []
        for slow_select in self.game_data["player_data"]:
            if slow_select["Name"] == player["Name"]:
                continue
            else:
                affected_players.append(slow_select)

        # the further ahead of the player you are, the longer you have slow applied to you
        affected_player.sort(key=lambda location: location["Place"], reverse=True)
        slow_given = 1
        for supply_slow in affected_players:
            for slow_count in range(slow_given):
                affected_players["Status"].append("Slow")
            slow_given += 1

        item_updater = player["Item(s)"].index("Slow")
        del player["Item(s)"][item_updater]

    def apply_midastouch(self, player):
        # Makes players immune to all attacks and gives players an extra roll from 1 to 3
        getpass.getpass(prompt="Press Enter to roll again")
        midastouch_updater = player["Status"].index("Midas Touch")
        del player["Status"][midastouch_updater]
        midas_roll = random.randrange(1, 4)
        print(f"You rolled {midas_roll}")
        return midas_roll

    def apply_oilspill(self, player):
        # player can choose to throw oil forward or backwards tactically to attack other players or defend
        # forward throws 8 spaces ahead and backward puts it 1 behind.
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
            self.item_locations[player_location + 8] = "Oil Spill"
        elif oil == "backwards":
            self.item_locations[player_location - 1] = "Oil Spill"

        oil_index = player["Item(s)"].index("Oil Spill")
        del player["Item(s)"][oil_index]

    def apply_magnet(self, player):
        # this will seek out players within a 15 space scope, can be blocked by invincibility status
        affected_players = [
            p
            for p in self.game_data["player_data"]
            if player["Location"] < p["Location"] <= player["Location"] + 14
        ]
        # sorts list from bottom to top position
        if affected_players:
            affected_players.sort(key=lambda location: location["Location"])

            # decides with a 1 in 4 chance if a player is stunned
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

        # removes status after use
        magnet_updater = player["Item(s)"].index("Magnet")
        del player["Item(s)"][magnet_updater]

    def apply_bowlingball(self, player):
        # designed to hit all players in front of user to enforce stun for 1 turn
        affected_players = [
            p
            for p in self.game_data["player_data"]
            if player["Location"] < p["Location"]
        ]

        if affected_players:
            affected_players.sort(
                key=lambda location: location["Location"], reverse=True
            )

        # the chance of being hit is less with every player that is ahead.
        # starting with the player in 1st having a 3 in 4 chance of being hit
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

    def item_picker(self, player):
        # when a player lands on a space that is a multiple of 15 the player can pick an item up to affect the game
        player_position = [p for p in self.game_data["player_data"]]

        player_position.sort(key=lambda location: location["Location"], reverse=True)

        if player_position[-1]["Name"] == player["Name"]:
            if "Oil Spill" in self.game_data["items"]:
                player["Item(s)"].append("Oil Spill")
                return
            else:
                return

        first_position = player_position[-1]["Location"]
        second_position = None
        for position_difference in player_position:
            if position_difference["Name"] == player["Name"]:
                second_position = int(position_difference["Location"])
                break

        difference = abs(first_position - second_position)
        # items are distributed based on your position
        # the further away from first you are, the better the items you will receive
        item_distribution = None
        if difference < 10:
            item_distribution = {"Double": 1, "Magnet": 1, "Oil Spill": 2}
        elif difference < 20:
            item_distribution = {"Double": 1, "Magnet": 1, "Oil Spill": 1}
        elif difference < 40:
            item_distribution = {"Double": 2, "Magnet": 2, "Midas Touch": 1}
        elif difference < 60:
            item_distribution = {
                "Double": 3,
                "Magnet": 1,
                "Midas Touch": 4,
                "Bowling Ball": 1,
            }
        elif difference < 75:
            item_distribution = {
                "Double": 2,
                "Midas Touch": 4,
                "Bowling Ball": 2,
                "Steam Roller": 1,
            }
        elif difference < 100:
            item_distribution = {
                "Double": 1,
                "Midas Touch": 3,
                "Bowling Ball": 2,
                "Steam Roller": 1,
                "Slow": 1,
            }
        elif difference >= 100:
            item_distribution = {
                "Midas Touch": 1,
                "Bowling Ball": 1,
                "Steam Roller": 2,
                "Slow": 2,
            }

        item_keys = list(item_distribution.keys())


        item_push = []
        for allocate_items in item_keys:
            if allocate_items in self.game_data["items"]:
                for add_probability in range(item_distribution[allocate_items]):
                    item_push.append(allocate_items)


        if item_push:
            given_item = random.choice(item_push)
            print(f'{player["Name"]} picked up {given_item}!')
            player["Item(s)"].append(given_item)
        else:
            return

    def magnet_movement(self, player):
        # if the magnet is about to go off the board
        if board_space + 15 > self.game_data["duration"]:
            for move_forward in range(board_space, self.game_data["duration"]):
                if self.item_locations[move_forward] == "Oil Spill":
                    self.item_locations[board_space] = ""
                    print("The magnet fell into the oil spill and can not progress!")
                    return

                for player_check in player:
                    if player["Location"] == move_forward:
                        player["Staus"].append("Stun")
                        print(f"{player['Name']} was hit by the magnet and stunned")
                        self.item_locations[board_space] = ""
                        return
        else:
            for move_forward in range(board_space, board_space + 15):
                if self.item_locations[move_forward] == "Oil Spill":
                    self.item_locations[board_space] = ""
                    print("The magnet fell into the oil spill and can not progress!")
                    return

                for player_check in player:
                    if player["Location"] == move_forward:
                        player["Staus"].append("Stun")
                        print(f"{player['Name']} was hit by the magnet and stunned")
                        self.item_locations[board_space] = ""
                        return
            new_magnet = board_space + 15
            self.item_locations[board_space] = ""
            self.item_locations[new_magnet] = "Magnet"

    def item_board(self, player):
        for board_space in range(self.game_data["duration"], 0, -1):
            if not self.item_locations[board_space]:
                return

            if self.item_locations[board_space] == "Magnet":
                self.magnet_movement(player)

    def game_time(self):
        print("\033c")
        self.finished_players = []


        # when items are placed on the board
        self.item_locations = {}
        for construct_items in range(1, self.game_data["duration"] + 1):
            self.item_locations[construct_items] = ""

        # shuffles player order for game
        random.shuffle(self.game_data["player_data"])

        first_turn = True

        # while game is in progress, this will loop continually until all players are finished

        while True:
            if first_turn:
                print("Let's go!")
            elif len(self.finished_players) == len(self.game_data["player_data"]) - 1:
                print("Game over!")
                break

            else:
                print("\033c")
                names = []
                locations = []
                items = []
                status = []
                place = []
                players_location = self.game_data["player_data"]
                players_location.sort(
                    key=lambda location: location["Location"], reverse=True
                )
                place_count = 1

                for data_info in self.game_data["player_data"]:
                    names.append(data_info["Name"])
                    locations.append(data_info["Location"])
                    items.append(list(dict.fromkeys(data_info["Item(s)"])))
                    status.append(list(dict.fromkeys(data_info["Status"])))

                for plot in players_location:
                    place.append(place_count)
                    place_count += 1
                table_data = {
                    "Location": locations,
                    "Items": items,
                    "Status": status,
                    "Place": place,
                }

                df = pd.DataFrame(table_data, index=names)
                print(df)
                print("-_-_-_")

            # stunned players will have to skip a turn
            # if stun is found in the status list, it will be removed.
            for current_player in self.game_data["player_data"]:
                if current_player["Finished"]:
                    continue

                if "Stun" in current_player["Status"]:
                    self.apply_stun(current_player)
                    continue

                # steam roller pushes the player 15 players forward and destroys all items in its way
                # has a 25% chance of hitting a player if a player is in the movement range
                elif "Steam Roller" in current_player["Status"]:
                    self.apply_steamroller(current_player)

                getpass.getpass(prompt=f"{current_player['Name']}: Press Enter to roll")

                roll_amount = self.dice_roll(current_player)

                if "Midas Touch" in current_player["Status"]:
                    midas_roller = self.apply_midastouch(current_player)
                    roll_amount += midas_roller

                current_player["Location"] += roll_amount

                if (
                    current_player["Location"] % 15 == 0
                    and len(current_player["Item(s)"]) < 3
                ):
                    self.item_picker(current_player)

                if current_player["Item(s)"]:
                    item_options = list(current_player["Item(s)"])
                    questions = [
                        inquirer.List(
                            "option",
                            message="What item do you want to use?",
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
                        double_ind = current_player["Item(s)"].index("Double")
                        del current_player["Item(s)"][double_ind]
                    elif item_answer["option"] == "Steam Roller":
                        current_player["Status"] = ["Steam Roller", "Steam Roller"]
                    elif item_answer["option"] == "Midas Touch":
                        current_player["Status"] = [
                            "Midas Touch",
                            "Midas Touch",
                            "Midas Touch",
                        ]
                        midas_find = current_player["Item(s)"].index("Midas Touch")
                        del current_player["Item(s)"][midas_find]
                    elif item_answer["option"] == "Oil Spill":
                        self.apply_oilspill(current_player)
                    elif item_answer["option"] == "Magnet":
                        self.apply_magnet(current_player)
                    elif item_answer["option"] == "Bowling Ball":
                        self.apply_bowlingball(current_player)
                    elif item_answe["option"] == "Slow":
                        self.apply_slow(current_player)

                else:
                    pass

                if current_player["Location"] >= self.game_data["duration"]:
                    current_player["Finished"] = True
                    self.finished_players.append(current_player["Name"])
            self.item_board(current_player)
            getpass.getpass(prompt=". . .")
            first_turn = False
                


run = Sabotage()
plus = run.options_screen()
if plus["option"] == "Start":
    run.game_details()
    run.game_time()
elif plus["option"] == "About":
    run.about()
