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
    ('Goblet of Nightmarish Ichor', '139324', SOURCES['Raid']),
    ('Nightmare Egg Shell', '137312', SOURCES['Dungeon']),
]

MASTERY = 605
CRIT = 603
HASTE = 604
VERS = 607

STAT_STICK_ID = '139102'

STAT_STICKS = [
    ("An'she's Strength/Mastery", MASTERY),
    ("An'she's Strength/Crit", CRIT),
    ("An'she's Strength/Haste", HASTE),
    ("An'she's Strength/Vers", VERS),
]

trinket_string_format = "trinket1=,id={},bonus_id={}"
trinket_string_format_no_bonus = "trinket1=,id={}"

def calculate_stat_stick_bonus_id(stick_type, ilevel):
    base_bonus_id = 1825
    modifier_bonus_id = None

    if ilevel > 810:
        modifier_bonus_id = str(1472 + (ilevel - 810))

    if modifier_bonus_id:
        return "{}/{}/{}".format(stick_type, modifier_bonus_id, base_bonus_id)
    else:
        return "{}/{}".format(stick_type, base_bonus_id)

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

for trinket in STAT_STICKS:
    trinket_name = trinket[0]
    stick_type = trinket[1]

    for ilevel in WQ_REWARD_ILEVELS:
        bonus_id = calculate_stat_stick_bonus_id(stick_type, ilevel)
        stringline = trinket_string_format.format(STAT_STICK_ID, bonus_id)

        trinket_iterations.append((stringline, trinket_name, ilevel))

print("Total combinations: {}".format(len(trinket_iterations)))

BASE_PROFILE = """
warrior="No Trinket"
level=110
race=blood_elf
role=attack
position=back
talents=1332311
artifact=36:0:0:0:0:1136:1:1137:1:1139:1:1142:1:1145:3:1147:3:1148:3:1149:3:1150:3:1356:1
spec=arms

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
actions.precombat+=/potion,name=old_war

# Executed every time the actor is available.
actions=charge
actions+=/auto_attack
actions+=/potion,name=old_war,if=(target.health.pct<20&buff.battle_cry.up)|target.time_to_die<=26
actions+=/blood_fury,if=buff.battle_cry.up|target.time_to_die<=16
actions+=/berserking,if=buff.battle_cry.up|target.time_to_die<=11
actions+=/arcane_torrent,if=buff.battle_cry_deadly_calm.down&rage.deficit>40
actions+=/battle_cry,if=(buff.bloodlust.up|time>=1)&!gcd.remains&(buff.shattered_defenses.up|(cooldown.colossus_smash.remains&cooldown.warbreaker.remains))|target.time_to_die<=10
actions+=/avatar,if=(buff.bloodlust.up|time>=1)
actions+=/use_item,name=gift_of_radiance
actions+=/hamstring,if=buff.battle_cry_deadly_calm.remains>cooldown.hamstring.remains
actions+=/heroic_leap,if=debuff.colossus_smash.up
actions+=/rend,if=remains<gcd
# The tl;dr of this line is to spam focused rage inside battle cry, the added nonsense is to help modeling the difficulty of timing focused rage immediately after mortal strike.
# In game, if focused rage is used the same instant as mortal strike, rage will be deducted for focused rage, the buff is immediately consumed, but it does not buff the damage of mortal strike.
actions+=/focused_rage,if=buff.battle_cry_deadly_calm.remains>cooldown.focused_rage.remains&(buff.focused_rage.stack<3|!cooldown.mortal_strike.up)&((!buff.focused_rage.react&prev_gcd.mortal_strike)|!prev_gcd.mortal_strike)
actions+=/colossus_smash,if=debuff.colossus_smash.down
actions+=/warbreaker,if=debuff.colossus_smash.down
actions+=/ravager
actions+=/overpower,if=buff.overpower.react
actions+=/run_action_list,name=cleave,if=spell_targets.whirlwind>=2&talent.sweeping_strikes.enabled
actions+=/run_action_list,name=aoe,if=spell_targets.whirlwind>=2&!talent.sweeping_strikes.enabled
actions+=/run_action_list,name=execute,if=target.health.pct<=20
actions+=/run_action_list,name=single,if=target.health.pct>20

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

actions.execute=mortal_strike,if=buff.battle_cry.up&buff.focused_rage.stack=3
actions.execute+=/execute,if=buff.battle_cry_deadly_calm.up
actions.execute+=/colossus_smash,if=buff.shattered_defenses.down
actions.execute+=/warbreaker,if=buff.shattered_defenses.down&rage<=30
actions.execute+=/execute,if=buff.shattered_defenses.up&rage>22|buff.shattered_defenses.down
# actions.single+=/heroic_charge,if=rage.deficit>=40&(!cooldown.heroic_leap.remains|swing.mh.remains>1.2)
#Remove the # above to run out of melee and charge back in for rage.
actions.execute+=/bladestorm,interrupt=1,if=raid_event.adds.in>90|!raid_event.adds.exists|spell_targets.bladestorm_mh>desired_targets

actions.single=mortal_strike,if=buff.battle_cry.up&buff.focused_rage.stack>=1&buff.battle_cry.remains<gcd
actions.single+=/colossus_smash,if=buff.shattered_defenses.down
actions.single+=/warbreaker,if=buff.shattered_defenses.down&cooldown.mortal_strike.remains<gcd
actions.single+=/focused_rage,if=((!buff.focused_rage.react&prev_gcd.mortal_strike)|!prev_gcd.mortal_strike)&buff.focused_rage.stack<3&(buff.shattered_defenses.up|cooldown.colossus_smash.remains)
actions.single+=/mortal_strike
actions.single+=/execute,if=buff.stone_heart.react
actions.single+=/slam,if=buff.battle_cry_deadly_calm.up|buff.focused_rage.stack=3|rage.deficit<=30
actions.single+=/execute,if=equipped.archavons_heavy_hand
actions.single+=/slam,if=equipped.archavons_heavy_hand
actions.single+=/focused_rage,if=equipped.archavons_heavy_hand
# actions.single+=/heroic_charge,if=rage.deficit>=40&(!cooldown.heroic_leap.remains|swing.mh.remains>1.2)
#Remove the # above to run out of melee and charge back in for rage.
actions.single+=/bladestorm,interrupt=1,if=raid_event.adds.in>90|!raid_event.adds.exists|spell_targets.bladestorm_mh>desired_targets

head=vision_of_the_spider_queen,id=137451,bonus_id=1727
neck=brysngamen_torc_of_helheim,id=133636,bonus_id=1727,enchant=mark_of_the_distant_army
shoulders=mortar_guard_shoulderplates,id=137524,bonus_id=1727
back=stole_of_malefic_repose,id=134404,bonus_id=1727,enchant=binding_of_strength
chest=etheldrins_breastplate,id=136976,bonus_id=1727
wrists=exomesh_carpalform_armplates_mk._vii,id=134502,bonus_id=1727
hands=reinforced_mook_handguards,id=140596,bonus_id=1727
waist=roaring_breeze_waistguard,id=137499,bonus_id=1727
legs=legplates_of_the_swarm,id=134506,bonus_id=1727
feet=leadfoot_earthshakers,id=134507,bonus_id=1727
finger1=loop_of_eightfold_eyes,id=134527,bonus_id=1727,enchant=binding_of_mastery
finger2=archdruids_tainted_seal,id=134487,bonus_id=1727,enchant=binding_of_mastery
trinket2=terrorbound_nexus,id=137406,bonus_id=1727
main_hand=stromkar_the_warbreaker,id=128910,gem_id=137469/137363/137377,relic_id=3412/3412/3412
"""

TRINKET_COPY = """
copy="{}"
{}"""

profiles = []

for combination in trinket_iterations:
    stringline = combination[0]
    trinket_name = combination[1]
    ilevel = combination[2]

    profile_name = '{}_{}'.format(trinket_name, ilevel)

    profiles.append(TRINKET_COPY.format(profile_name, stringline))

with open("trinkets_profile.simc", 'w+') as trink_profile_file:
    trink_profile_file.write(BASE_PROFILE)

    for profile in profiles:
        trink_profile_file.write(profile)
        trink_profile_file.write('\n')
