# Fantasy World Data Dictionary

## Characters

| Field | Description |
|-------|-------------|
| character_id | Unique identifier for each character |
| name | Character's full name |
| race | Character's race |
| class | Character's class |
| level | Character's current level (1-120) |
| region_id | ID of the region where the character resides |
| profession_primary | Character's primary profession |
| profession_secondary | Character's secondary profession |
| gold | Amount of gold the character possesses |
| achievement_points | Character's total achievement points |
| household_id | ID of the household the character belongs to |
| guild_id | ID of the guild the character belongs to |
| gender | Character's gender |
| age | Character's age in years |
| birth_date | Character's date of birth |
| education_level | Character's level of education |
| relationship_status | Character's relationship status |
| num_children | Number of children the character has |

## Households

| Field | Description |
|-------|-------------|
| household_id | Unique identifier for each household |
| region_id | ID of the region where the household is located |
| size | Number of characters in the household |
| total_income | Total income of the household |

## Guilds

| Field | Description |
|-------|-------------|
| guild_id | Unique identifier for each guild |
| name | Name of the guild |
| region_id | ID of the region where the guild is based |
| level | Guild's current level (1-25) |
| member_count | Number of members in the guild |
| bank_gold | Amount of gold in the guild bank |
| achievement_points | Guild's total achievement points |

## Economic Data

| Field | Description |
|-------|-------------|
| region_id | Unique identifier for each region |
| region_name | Name of the region |
| avg_item_price | Average price of items in the region |
| inflation_rate | Current inflation rate in the region |
| unemployment_rate | Current unemployment rate in the region |
| gdp_growth | GDP growth rate of the region |
| trade_volume | Total trade volume in the region |

## Quests

| Field | Description |
|-------|-------------|
| quest_id | Unique identifier for each quest |
| name | Name of the quest |
| region_id | ID of the region where the quest is available |
| min_level | Minimum level required to start the quest |
| difficulty | Difficulty level of the quest |
| reward_gold | Amount of gold rewarded for completing the quest |
| reward_xp | Amount of experience points rewarded for completing the quest |
| required_participants | Number of participants required for the quest |

## Character Activities

| Field | Description |
|-------|-------------|
| character_id | ID of the character performing the activity |
| activity_type | Type of activity performed |
| duration_hours | Duration of the activity in hours |
| gold_earned | Amount of gold earned from the activity |
| xp_earned | Amount of experience points earned from the activity |
