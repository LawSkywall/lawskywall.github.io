#import time

ILEVEL_CAP = 895
CRAFTED_ILEVEL_CAP = 855

DUNGEON_ILEVELS = list(range(825,ILEVEL_CAP+5,5))
RAID_ILEVELS = list(range(850,ILEVEL_CAP+5,5))
RAID_ILEVELS.append(835)
CRAFTED_ILEVELS = list(range(815,CRAFTED_ILEVEL_CAP+5,5))
MYTHIC_ONLY_ILEVELS = list(range(840,ILEVEL_CAP+5,5))
WQ_REWARD_ILEVELS = list(range(810,ILEVEL_CAP,5)) #max 890

SOURCES = {
    'Dungeon': {'ilevels': DUNGEON_ILEVELS, 'id': '0'},
    'Raid': {'ilevels': RAID_ILEVELS, 'id': '1'},
    'Crafted': {'ilevels': CRAFTED_ILEVELS, 'id': '2'},
    'Mythic Only Dungeon': {'ilevels': MYTHIC_ONLY_ILEVELS, 'id': '3'},
    'WQ Reward': {'ilevels': WQ_REWARD_ILEVELS, 'id': '4'},
    'Stat Stick': {'ilevels': WQ_REWARD_ILEVELS, 'id': '5'},
}

TRINKETS = [
    ("Nature's Call", '139334', SOURCES['Raid']),
    ('Ravaged Seed Pod', '139320', SOURCES['Raid']),
    ('Spontaneous Appendages', '139325', SOURCES['Raid']),
    ("Ursoc's Rending Paw", '139328', SOURCES['Raid']),
    ('Chaos Talisman', '137459', SOURCES['Dungeon']),
    ('Faulty Countermeasure', '137539', SOURCES['Dungeon']),
    ('Giant Ornamental Pearl', '137369', SOURCES['Dungeon']),
    ('Hunger of the Pack', '136975', SOURCES['Dungeon']),
    ('Impact Tremor', '140034', SOURCES['Dungeon']),
    ('Mark of Dargrul', '137357', SOURCES['Dungeon']),
    ('Memento of Angerboda', '133644', SOURCES['Dungeon']),
    ('Spiked Counterweight', '136715', SOURCES['Dungeon']),
    ('Terrorbound Nexus', '137406', SOURCES['Dungeon']),
    ('Tiny Oozeling in a Jar', '137439', SOURCES['Dungeon']),
    ('Windscar Whetstone', '137486', SOURCES['Dungeon']),
    ('Chrono Shard', '137419', SOURCES['Mythic Only Dungeon']),
    ('Gift of Radiance', '133647', SOURCES['Dungeon']),
    ('Infernal Alchemist Stone', '127842', SOURCES['Crafted']),
    ('Strand of the Stars', '137487', SOURCES['Mythic Only Dungeon']),
    ('Darkmoon Deck: Dominion', '128705', SOURCES['Crafted']),
    ('Horn of Valor', '133642', SOURCES['Dungeon']),
    ("Marfisi's Giant Censer", '141586', SOURCES['WQ Reward']),
]

trinket_string_format = "trinket1=,id={},bonus_id={}"
trinket_string_format_no_bonus = "trinket1=,id={}"

def calculate_bonus_id(trinket_source, ilevel):
    modifier_bonus_id = None
    base_bonus_id = '0'

    if trinket_source['id'] in [
        SOURCES['Dungeon']['id'],
        SOURCES['Mythic Only Dungeon']['id'],
    ]:
        if ilevel not in [825, 840]:
            modifier_bonus_id = str(1477 + (ilevel - 825))

        if ilevel < 840:
            base_bonus_id = '1726'
        else:
            base_bonus_id = '1727'

    elif trinket_source['id'] == SOURCES['Raid']['id']:
        if ilevel == 835:
            base_bonus_id='3379'
        elif ilevel > 850 and ilevel < 865:
            base_bonus_id = str(1472 + (ilevel - 850))
        elif ilevel >= 865:
            base_bonus_id='1805'

            if ilevel > 865:
                modifier_bonus_id = str(1472 + (ilevel - 850))

    elif trinket_source['id'] == SOURCES['Crafted']['id']:
        if ilevel <= 830:
            base_bonus_id = int(596 + ((ilevel - 815) / 5))
        else:
            base_bonus_id = int(665 + ((ilevel - 830) / 5))
    elif trinket_source['id'] == SOURCES['WQ Reward']['id']:
        if ilevel > 810:
            base_bonus_id = str(1472 + (ilevel - 810))

    if modifier_bonus_id:
        return '{}/{}'.format(modifier_bonus_id, base_bonus_id)
    else:
        return base_bonus_id

trinket_iterations = []

for trinket in TRINKETS:
    trinket_name = trinket[0]
    trinket_id = trinket[1]
    trinket_source = trinket[2]

    for ilevel in trinket_source['ilevels']:
        bonus_id = calculate_bonus_id(trinket_source, ilevel)
        if bonus_id != '0':
            stringline = trinket_string_format.format(trinket_id, bonus_id)
        else:
            stringline = trinket_string_format_no_bonus.format(trinket_id)

        trinket_iterations.append((stringline, trinket_name, ilevel))

print("Total combinations: {}".format(len(trinket_iterations)))

BASE_PROFILE = """
warrior="Law_845_{}"
level=110
race=gnome
region=us
server=skywall
role=attack
professions=blacksmithing=761/engineering=724
talents=1332311
spec=arms
artifact=36:0:0:0:0:1136:1:1137:1:1139:1:1141:1:1142:1:1145:3:1146:3:1148:3:1149:3:1150:3:1356:1

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask,type=countless_armies
actions.precombat+=/food,type=nightborne_delicacy_platter
actions.precombat+=/augmentation,type=defiled
# Snapshot raid buffed stats before combat begins and pre-potting is done.
actions.precombat+=/snapshot_stats
actions.precombat+=/potion,name=deadly_grace

# Executed every time the actor is available.
actions=charge
actions+=/auto_attack
actions+=/potion,name=deadly_grace,if=(target.health.pct<20&buff.battle_cry.up)|target.time_to_die<=26
actions+=/battle_cry,if=(buff.bloodlust.up|time>=1)&!gcd.remains
actions+=/avatar,if=(buff.bloodlust.up|time>=1)&!gcd.remains
actions+=/blood_fury,if=buff.battle_cry.up|target.time_to_die<=16
actions+=/berserking,if=buff.battle_cry.up|target.time_to_die<=11
actions+=/arcane_torrent,if=buff.battle_cry_deadly_calm.down&rage.deficit>40
actions+=/use_item,name=gift_of_radiance
actions+=/hamstring,if=buff.battle_cry_deadly_calm.remains>cooldown.hamstring.remains
actions+=/heroic_leap,if=debuff.colossus_smash.up
actions+=/rend,if=remains<gcd
actions+=/focused_rage,if=buff.battle_cry_deadly_calm.remains>cooldown.focused_rage.remains&(buff.focused_rage.stack<3|cooldown.mortal_strike.remains)
actions+=/colossus_smash,if=debuff.colossus_smash.down
actions+=/warbreaker,if=debuff.colossus_smash.down
actions+=/ravager
actions+=/overpower
actions+=/run_action_list,name=cleave,if=spell_targets.whirlwind>=2&talent.sweeping_strikes.enabled
actions+=/run_action_list,name=aoe,if=spell_targets.whirlwind>=2&!talent.sweeping_strikes.enabled
actions+=/run_action_list,name=execute,if=target.health.pct<=20
actions+=/run_action_list,name=single

actions.single=mortal_strike,if=buff.battle_cry.up&buff.focused_rage.stack>=1&buff.battle_cry.remains<gcd
actions.single+=/colossus_smash,if=buff.shattered_defenses.down
actions.single+=/warbreaker,if=buff.shattered_defenses.down&cooldown.mortal_strike.remains<gcd
actions.single+=/focused_rage,if=buff.focused_rage.stack<3&(buff.shattered_defenses.up|cooldown.colossus_smash.remains)
actions.single+=/mortal_strike
actions.single+=/slam,if=buff.battle_cry_deadly_calm.up|buff.focused_rage.stack=3|rage.deficit<=30
actions.single+=/execute,if=equipped.137060
actions.single+=/slam,if=equipped.137060
actions.single+=/focused_rage,if=equipped.137060
actions.single+=/heroic_charge,if=rage.deficit>=40&(!cooldown.heroic_leap.remains|swing.mh.remains>1.2)
#Remove the # above to run out of melee and charge back in for rage.
actions.single+=/bladestorm,interrupt=1,if=raid_event.adds.in>90|!raid_event.adds.exists|spell_targets.bladestorm_mh>desired_targets

actions.cleave=mortal_strike
actions.cleave+=/execute,if=buff.stone_heart.react
actions.cleave+=/colossus_smash,if=buff.shattered_defenses.down&buff.precise_strikes.down
actions.cleave+=/warbreaker,if=buff.shattered_defenses.down
actions.cleave+=/focused_rage,if=buff.shattered_defenses.down
actions.cleave+=/whirlwind,if=talent.fervor_of_battle.enabled&(debuff.colossus_smash.up|rage.deficit<50)&(!talent.focused_rage.enabled|buff.battle_cry_deadly_calm.up|buff.cleave.up)
actions.cleave+=/rend,if=remains<=duration*0.3
actions.cleave+=/bladestorm
actions.cleave+=/cleave
actions.cleave+=/whirlwind,if=rage>=100|buff.focused_rage.stack=3
actions.cleave+=/shockwave
actions.cleave+=/storm_bolt

actions.aoe=mortal_strike
actions.aoe+=/execute,if=buff.stone_heart.react
actions.aoe+=/colossus_smash,if=buff.shattered_defenses.down&buff.precise_strikes.down
actions.aoe+=/warbreaker,if=buff.shattered_defenses.down
actions.aoe+=/whirlwind,if=talent.fervor_of_battle.enabled&(debuff.colossus_smash.up|rage.deficit<50)&(!talent.focused_rage.enabled|buff.battle_cry_deadly_calm.up|buff.cleave.up)
actions.aoe+=/rend,if=remains<=duration*0.3
actions.aoe+=/bladestorm
actions.aoe+=/cleave
actions.aoe+=/whirlwind,if=rage>=60
actions.aoe+=/shockwave
actions.aoe+=/storm_bolt

actions.execute=focused_rage,if=buff.focused_rage.stack<3&debuff.colossus_smash.down
actions.execute+=/mortal_strike,if=buff.battle_cry.up&(buff.focused_rage.stack=3|buff.focused_rage.stack=2&buff.battle_cry.remains<gcd)
actions.execute+=/execute,if=buff.battle_cry_deadly_calm.up
actions.execute+=/colossus_smash,if=buff.shattered_defenses.down
actions.execute+=/warbreaker,if=buff.shattered_defenses.down&rage<=30
actions.execute+=/execute,if=buff.shattered_defenses.up
actions.execute+=/mortal_strike,if=buff.focused_rage.stack=3
actions.execute+=/execute,if=debuff.colossus_smash.up
#Remove the # above to run out of melee and charge back in for rage.
actions.execute+=/bladestorm,interrupt=1,if=raid_event.adds.in>90|!raid_event.adds.exists|spell_targets.bladestorm_mh>desired_targets

head=,id=139684,bonus_id=3385/3384
neck=,id=130243,enchant_id=5438,bonus_id=1782/689/600/669,gem_id=130222
shoulder=,id=134228,bonus_id=1727/42/1502/1813
back=,id=134404,enchant_id=5431,bonus_id=1727/1492/1813
chest=,id=134223,bonus_id=1727/1507/3336
wrist=,id=134230,bonus_id=3397/1492/1675
hands=,id=137525,bonus_id=1727/1492/1813
waist=,id=134225,bonus_id=1726/1502/3337
legs=,id=134271,bonus_id=3396/1808/1492/3339,gem_id=130222
feet=,id=134523,bonus_id=1727/1808/1497/3336,gem_id=130222
finger1=,id=134487,bonus_id=1727/1497/3336
finger2=,id=136713,enchant_id=5425,bonus_id=3358/689/600/669,gem_id=130222
{}
trinket2=,id=139102,bonus_id=3432/605/1502/3336
main_hand=,id=128910,bonus_id=750,relic_id=1727:1497:3336/1726:1482:3339/1727:1492:1813,gem_id=133763/137363/137317/0
"""

profiles = []

for combination in trinket_iterations:
    stringline = combination[0]
    trinket_name = combination[1]
    ilevel = combination[2]

    profile_name = '{}_{}'.format(trinket_name, ilevel)

    profiles.append(BASE_PROFILE.format(profile_name, stringline))

with open("trinkets_profile.simc", 'w+') as trink_profile_file:
    for profile in profiles:
        trink_profile_file.write(profile)
        trink_profile_file.write('\n\n')
