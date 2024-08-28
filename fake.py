import csv
import random
from faker import Faker
import numpy as np
from datetime import datetime, timedelta

fake = Faker()

class FantasyNameGenerator:
    def __init__(self):
        self.name_parts = {
            'Human': {
                'first': ['Anduin', 'Jaina', 'Varian', 'Arthas', 'Uther', 'Tirion', 'Bolvar', 'Lorna', 'Mathias', 'Vanessa'],
                'last': ['Wrynn', 'Proudmoore', 'Menethil', 'Fordragon', 'Mograine', 'Fordring', 'Shaw', 'Crowley', 'VanCleef', 'Prestor']
            },
            'Orc': {
                'first': ['Thrall', 'Garrosh', 'Grom', 'Durotan', 'Orgrim', 'Blackhand', 'Eitrigg', 'Nazgrel', 'Rehgar', 'Garona'],
                'last': ['Hellscream', 'Doomhammer', 'Saurfang', 'Bladefist', 'Blackrock', 'Frostwolf', 'Warsong', 'Dragonmaw', 'Thunderlord', 'Bleeding Hollow']
            },
            'Dwarf': {
                'first': ['Magni', 'Muradin', 'Brann', 'Moira', 'Falstad', 'Kurdran', 'Thargas', 'Fendrig', 'Gavan', 'Bael'],
                'last': ['Bronzebeard', 'Wildhammer', 'Thaurissan', 'Anvilmar', 'Thunderbrew', 'Stormpike', 'Ironforge', 'Flintlocke', 'Hammerfall', 'Deepforge']
            },
            'Night Elf': {
                'first': ['Tyrande', 'Malfurion', 'Illidan', 'Shandris', 'Fandral', 'Jarod', 'Maiev', 'Cordana', 'Naisha', 'Broll'],
                'last': ['Whisperwind', 'Stormrage', 'Shadowsong', 'Feathermoon', 'Staghelm', 'Ravencrest', 'Moonwhisper', 'Starseeker', 'Nightsong', 'Bearmantle']
            },
            'Undead': {
                'first': ['Sylvanas', 'Nathanos', 'Putress', 'Lilian', 'Alonsus', 'Meryl', 'Calia', 'Leonid', 'Gunther', 'Amelia'],
                'last': ['Windrunner', 'Blightcaller', 'Voss', 'Faol', 'Felstorm', 'Menethil', 'Barthalomew', 'Zelling', 'Mograine', 'Crowley']
            },
            'Tauren': {
                'first': ['Cairne', 'Baine', 'Magatha', 'Hamuul', 'Trag', 'Aponi', 'Sunwalker', 'Muln', 'Jevan', 'Tagar'],
                'last': ['Bloodhoof', 'Grimtotem', 'Runetotem', 'Thunderhorn', 'Dawnstrider', 'Wildmane', 'Skychaser', 'Stormhoof', 'Ragetotem', 'Earthfury']
            },
            'Gnome': {
                'first': ['Gelbin', 'Sicco', 'Millhouse', 'Chromie', 'Kelsey', 'Toshley', 'Tinkmaster', 'Fizzlebang', 'Nimzy', 'Razlo'],
                'last': ['Mekkatorque', 'Thermaplugg', 'Manastorm', 'Steelspark', 'Steelspring', 'Gearloose', 'Overspark', 'Cogspinner', 'Quickwrench', 'Boltbucket']
            },
            'Troll': {
                'first': ['Vol\'jin', 'Zul\'jin', 'Rokhan', 'Sen\'jin', 'Zanzil', 'Zalazane', 'Jeklik', 'Zandalar', 'Rastakhan', 'Talanji'],
                'last': ['Shadowhunter', 'Hexer', 'Spiritchaser', 'Voodoomaster', 'Bonecrusher', 'Blooddrinker', 'Soulflayer', 'Zandalari', 'Darkspear', 'Gurubashi']
            },
            'Blood Elf': {
                'first': ['Kael\'thas', 'Lor\'themar', 'Halduron', 'Rommath', 'Liadrin', 'Valeera', 'Aethas', 'Tae\'thelan', 'Pathaleon', 'Astalor'],
                'last': ['Sunstrider', 'Theron', 'Brightwing', 'Sanguinar', 'Sunfury', 'Bloodsworn', 'Sunreaver', 'Dawnsinger', 'Flamestrike', 'Dawnblade']
            },
            'Draenei': {
                'first': ['Velen', 'Maraad', 'Yrel', 'Nobundo', 'Akama', 'Ishanah', 'Iridi', 'Talador', 'Naielle', 'Restalaan'],
                'last': ['Lightforged', 'Soulbinder', 'Lightwarden', 'Truthseeker', 'Stormcaller', 'Dawnchaser', 'Starweaver', 'Crystalheart', 'Lightbringer', 'Soulpriest']
            },
            'Goblin': {
                'first': ['Gazlowe', 'Gallywix', 'Sassy', 'Hobart', 'Druz', 'Megs', 'Grizzle', 'Nubsy', 'Krix', 'Zazzle'],
                'last': ['Gearspanner', 'Goldgrubber', 'Sparkbolt', 'Boomfizzle', 'Blastfuse', 'Kaboombox', 'Rocketfuel', 'Zapnozzle', 'Greasebot', 'Bangshift']
            },
            'Worgen': {
                'first': ['Genn', 'Darius', 'Ivar', 'Belysra', 'Halford', 'Celestine', 'Tobias', 'Lorna', 'Vincent', 'Adalyn'],
                'last': ['Greymane', 'Crowley', 'Bloodfang', 'Starseeker', 'Wyrmbane', 'Springvale', 'Mistmantle', 'Shadowbane', 'Godfrey', 'Darkfang']
            }
        }

    def generate_name(self, race):
        first = random.choice(self.name_parts[race]['first'])
        last = random.choice(self.name_parts[race]['last'])
        return f"{first} {last}"


class FantasyWorld:
    def __init__(self):
        self.base_population = np.random.randint(5000, 20000)
        self.regions = ['Elwynn Forest', 'Durotar', 'Mulgore', 'Dun Morogh', 'Teldrassil', 
                        'Tirisfal Glades', 'Eversong Woods', 'Azuremyst Isle', 'Gilneas', 'Kezan']
        self.races = ['Human', 'Orc', 'Dwarf', 'Night Elf', 'Undead', 'Tauren', 'Gnome', 'Troll', 
                      'Blood Elf', 'Draenei', 'Goblin', 'Worgen']
        self.classes = ['Warrior', 'Paladin', 'Hunter', 'Rogue', 'Priest', 'Shaman', 'Mage', 
                        'Warlock', 'Monk', 'Druid', 'Demon Hunter', 'Death Knight']
        self.professions = ['Mining', 'Herbalism', 'Skinning', 'Alchemy', 'Blacksmithing', 
                            'Enchanting', 'Engineering', 'Leatherworking', 'Tailoring', 'Jewelcrafting']
        
        self.name_generator = FantasyNameGenerator()
        
        self.characters = self.generate_characters()
        self.households = self.generate_households()
        self.guilds = self.generate_guilds()
        self.economic_data = self.generate_economic_data()
        self.quests = self.generate_quests()
        self.character_activities = self.generate_character_activities()

    def generate_characters(self):
        characters = []
        for i in range(self.base_population):
            race = np.random.choice(self.races, p=[0.2, 0.15, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
            name = self.name_generator.generate_name(race)
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=1000)  # Some races live very long
            character = {
                'character_id': i + 1,
                'name': name,
                'race': race,
                'class': np.random.choice(self.classes, p=[0.15, 0.1, 0.1, 0.1, 0.1, 0.08, 0.08, 0.08, 0.07, 0.07, 0.04, 0.03]),
                'level': np.random.choice(range(1, 121), p=np.array([1/(1+i**1.5) for i in range(120)])/sum([1/(1+i**1.5) for i in range(120)])),
                'region_id': np.random.randint(1, len(self.regions) + 1),
                'profession_primary': np.random.choice(self.professions),
                'profession_secondary': np.random.choice(self.professions),
                'gold': np.random.lognormal(mean=8, sigma=2),
                'achievement_points': np.random.randint(0, 25000),
                'household_id': None,
                'guild_id': None,
                'gender': np.random.choice(['Male', 'Female'], p=[0.51, 0.49]),
                'age': (datetime.now().date() - birth_date).days // 365,
                'birth_date': birth_date.strftime('%Y-%m-%d'),
                'education_level': np.random.choice(['None', 'Basic', 'Advanced', 'Master'], p=[0.1, 0.5, 0.3, 0.1]),
                'relationship_status': np.random.choice(['Single', 'Married', 'Divorced', 'Widowed'], p=[0.4, 0.4, 0.1, 0.1]),
                'num_children': np.random.choice([0, 1, 2, 3, 4, 5], p=[0.3, 0.25, 0.2, 0.15, 0.07, 0.03])
            }
            characters.append(character)
        return characters

    def generate_households(self):
        households = []
        household_id = 1
        for character in self.characters:
            if random.random() < 0.7:  # 70% chance of being in a household
                household_size = np.random.choice([1, 2, 3, 4, 5], p=[0.2, 0.4, 0.25, 0.1, 0.05])
                household = {
                    'household_id': household_id,
                    'region_id': character['region_id'],
                    'size': household_size,
                    'total_income': np.random.lognormal(mean=10, sigma=1)
                }
                character['household_id'] = household_id
                for _ in range(household_size - 1):
                    if len(self.characters) > 0:
                        additional_character = self.characters[np.random.randint(0, len(self.characters))]
                        if additional_character['household_id'] is None:
                            additional_character['household_id'] = household_id
                            additional_character['region_id'] = household['region_id']
                households.append(household)
                household_id += 1
        return households 

    def generate_guilds(self):
        num_guilds = self.base_population // 100  # Assuming average guild size of 100
        guilds = []
        for i in range(num_guilds):
            guild = {
                'guild_id': i + 1,
                'name': fake.company(),
                'region_id': np.random.randint(1, len(self.regions) + 1),
                'level': np.random.choice(range(1, 26), p=np.array([1/(1+i**1.2) for i in range(25)])/sum([1/(1+i**1.2) for i in range(25)])),
                'member_count': np.random.randint(5, 500),
                'bank_gold': np.random.lognormal(mean=12, sigma=2),
                'achievement_points': np.random.randint(0, 50000)
            }
            guilds.append(guild)
        
        # Assign characters to guilds
        for character in self.characters:
            if random.random() < 0.8:  # 80% chance of being in a guild
                guild = random.choice(guilds)
                character['guild_id'] = guild['guild_id']
        
        return guilds

    def generate_economic_data(self):
        economic_data = []
        for i, region in enumerate(self.regions, 1):
            data = {
                'region_id': i,
                'region_name': region,
                'avg_item_price': np.random.lognormal(mean=4, sigma=0.5),
                'inflation_rate': max(0, np.random.normal(2, 1)),
                'unemployment_rate': max(0, min(100, np.random.normal(5, 2))),
                'gdp_growth': np.random.normal(3, 1.5),
                'trade_volume': np.random.lognormal(mean=15, sigma=1)
            }
            economic_data.append(data)
        return economic_data

    def generate_quests(self):
        num_quests = self.base_population // 20  # Assuming 1 quest per 20 characters on average
        quests = []
        for i in range(num_quests):
            quest = {
                'quest_id': i + 1,
                'name': fake.catch_phrase(),
                'region_id': np.random.randint(1, len(self.regions) + 1),
                'min_level': np.random.randint(1, 120),
                'difficulty': np.random.choice(['Easy', 'Medium', 'Hard', 'Elite', 'Legendary'], p=[0.3, 0.3, 0.2, 0.15, 0.05]),
                'reward_gold': np.random.lognormal(mean=4, sigma=1),
                'reward_xp': np.random.lognormal(mean=6, sigma=1),
                'required_participants': np.random.choice([1, 2, 3, 5, 10, 25], p=[0.5, 0.2, 0.1, 0.1, 0.07, 0.03])
            }
            quests.append(quest)
        return quests

    def generate_character_activities(self):
        activities = []
        for character in self.characters:
            num_activities = np.random.randint(1, 6)
            for _ in range(num_activities):
                activity = {
                    'character_id': character['character_id'],
                    'activity_type': np.random.choice(['Questing', 'Combat', 'Crafting', 'Trading', 'Exploration'], p=[0.4, 0.3, 0.1, 0.1, 0.1]),
                    'duration_hours': np.random.lognormal(mean=1, sigma=0.5),
                    'gold_earned': np.random.lognormal(mean=3, sigma=1) if random.random() < 0.8 else 0,
                    'xp_earned': np.random.lognormal(mean=5, sigma=1) if character['level'] < 120 else 0
                }
                activities.append(activity)
        return activities

def write_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def write_data_dictionary(filename):
    with open(filename, 'w') as f:
        f.write("# Fantasy World Data Dictionary\n\n")
        
        # Characters
        f.write("## Characters\n\n")
        f.write("| Field | Description |\n")
        f.write("|-------|-------------|\n")
        f.write("| character_id | Unique identifier for each character |\n")
        f.write("| name | Character's full name |\n")
        f.write("| race | Character's race |\n")
        f.write("| class | Character's class |\n")
        f.write("| level | Character's current level (1-120) |\n")
        f.write("| region_id | ID of the region where the character resides |\n")
        f.write("| profession_primary | Character's primary profession |\n")
        f.write("| profession_secondary | Character's secondary profession |\n")
        f.write("| gold | Amount of gold the character possesses |\n")
        f.write("| achievement_points | Character's total achievement points |\n")
        f.write("| household_id | ID of the household the character belongs to |\n")
        f.write("| guild_id | ID of the guild the character belongs to |\n")
        f.write("| gender | Character's gender |\n")
        f.write("| age | Character's age in years |\n")
        f.write("| birth_date | Character's date of birth |\n")
        f.write("| education_level | Character's level of education |\n")
        f.write("| relationship_status | Character's relationship status |\n")
        f.write("| num_children | Number of children the character has |\n\n")

        # Households
        f.write("## Households\n\n")
        f.write("| Field | Description |\n")
        f.write("|-------|-------------|\n")
        f.write("| household_id | Unique identifier for each household |\n")
        f.write("| region_id | ID of the region where the household is located |\n")
        f.write("| size | Number of characters in the household |\n")
        f.write("| total_income | Total income of the household |\n\n")

        # Guilds
        f.write("## Guilds\n\n")
        f.write("| Field | Description |\n")
        f.write("|-------|-------------|\n")
        f.write("| guild_id | Unique identifier for each guild |\n")
        f.write("| name | Name of the guild |\n")
        f.write("| region_id | ID of the region where the guild is based |\n")
        f.write("| level | Guild's current level (1-25) |\n")
        f.write("| member_count | Number of members in the guild |\n")
        f.write("| bank_gold | Amount of gold in the guild bank |\n")
        f.write("| achievement_points | Guild's total achievement points |\n\n")

        # Economic Data
        f.write("## Economic Data\n\n")
        f.write("| Field | Description |\n")
        f.write("|-------|-------------|\n")
        f.write("| region_id | Unique identifier for each region |\n")
        f.write("| region_name | Name of the region |\n")
        f.write("| avg_item_price | Average price of items in the region |\n")
        f.write("| inflation_rate | Current inflation rate in the region |\n")
        f.write("| unemployment_rate | Current unemployment rate in the region |\n")
        f.write("| gdp_growth | GDP growth rate of the region |\n")
        f.write("| trade_volume | Total trade volume in the region |\n\n")

        # Quests
        f.write("## Quests\n\n")
        f.write("| Field | Description |\n")
        f.write("|-------|-------------|\n")
        f.write("| quest_id | Unique identifier for each quest |\n")
        f.write("| name | Name of the quest |\n")
        f.write("| region_id | ID of the region where the quest is available |\n")
        f.write("| min_level | Minimum level required to start the quest |\n")
        f.write("| difficulty | Difficulty level of the quest |\n")
        f.write("| reward_gold | Amount of gold rewarded for completing the quest |\n")
        f.write("| reward_xp | Amount of experience points rewarded for completing the quest |\n")
        f.write("| required_participants | Number of participants required for the quest |\n\n")

        # Character Activities
        f.write("## Character Activities\n\n")
        f.write("| Field | Description |\n")
        f.write("|-------|-------------|\n")
        f.write("| character_id | ID of the character performing the activity |\n")
        f.write("| activity_type | Type of activity performed |\n")
        f.write("| duration_hours | Duration of the activity in hours |\n")
        f.write("| gold_earned | Amount of gold earned from the activity |\n")
        f.write("| xp_earned | Amount of experience points earned from the activity |\n")

def main():
    world = FantasyWorld()
    
    write_csv(world.characters, 'characters.csv')
    write_csv(world.households, 'households.csv')
    write_csv(world.guilds, 'guilds.csv')
    write_csv(world.economic_data, 'economic_data.csv')
    write_csv(world.quests, 'quests.csv')
    write_csv(world.character_activities, 'character_activities.csv')

    write_data_dictionary('fantasy_world_data_dictionary.md')

    print(f"Generated {len(world.characters)} characters in characters.csv")
    print(f"Generated {len(world.households)} households in households.csv")
    print(f"Generated {len(world.guilds)} guilds in guilds.csv")
    print(f"Generated economic data for {len(world.economic_data)} regions in economic_data.csv")
    print(f"Generated {len(world.quests)} quests in quests.csv")
    print(f"Generated {len(world.character_activities)} character activities in character_activities.csv")
    print("Generated data dictionary in fantasy_world_data_dictionary.md")

if __name__ == "__main__":
    main()