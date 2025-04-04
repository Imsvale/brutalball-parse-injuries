import re
import argparse
import textwrap

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
        """
        Copy from injuries page on Brutalball website.
        https://dozerverse.com/brutalball/injury.php
        Paste into injuries.txt and run parser.
        """))

    parser.add_argument("-f", "--file", type=str, help="Path to input file", default="injuries.txt")
    parser.add_argument("-o", "--out", type=str, help="Path to output file", default="injuries parsed.txt")
    parser.add_argument("-s", "--season", type=str ,help="Season number to use", default="4")
    parser.add_argument("-t", "--teams", type=str ,help="Path to teams file", default="teams.txt")

    try:
        args = parser.parse_args()
    except ValueError as e:
        print(e)
        print(parser.help())
        exit()

    if args.file:
        print(f"Taking input from {args.file}")

    try:
        with open(args.file) as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Input file {args.file} not found.\n")
        exit()

    content = content.strip()

    teams_hardcoded = [
        "Urrgmelonflex", "Volcamoose Saints", "Blood Pit Bouncers", "Bulldozer Power", 
        "Failurewood Hills", "Vuvu Boys", "Grunt Auto Gruppe", "Sunshine Funbus",
        "Port Miggins Pirates", "Sweaty Marsupials", "Kernal Space Agency", "Picks Creek Miners",
        "Sportsball Union", "Peninsula Transport", "Red Star Pathfinders", "Fire Chefs", 
        "Ov City Axemen", "Eduslum Marching Band", "Budget Roadies", "Nomads", "Grazer Ridge",
        "Bongolia Sea Raiders", "Bumson Medics", "Cheerio Inc", "Steggonauts", "Shady Palms",
        "Toymasters", "Stardozer HR", "Wizard Hole Wizards", "Beekeepers", "Wretched Minstrels",
        "LingoBlend Allstars"
    ]

    try:
        with open(args.teams) as f:
            teams = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        teams = teams_hardcoded

    print("Parsing...")

    # Week number
    week_pattern = re.compile("W([\\d+])")
    content = re.sub(week_pattern, f"{args.season},\\1", content)

    # # INJURY
    # content = re.sub(

    #     # Input: [DUR xx] [Blah] [BRU xx] SR Drops from [SR0] to [SR1] [Bounty]
    #     " DUR.(\\d+) (.+) BRU (\\d+) SR Drops from (\\d+) to (\\d+) *",

    #     # Output: SR0,SR1,DUR,Blah,Bounty
    #     ",\\4,\\5,\\1,\\2,\\3,", content)
    
    # INJURY regex example
    injury_pattern = re.compile(
        " DUR.(\\d+) (.+) BRU (\\d+) SR Drops from (\\d+) to (\\d+) *"
    )
    content = injury_pattern.sub(",\\4,\\5,\\1,\\2,\\3,", content)

    # # KILL
    # content = re.sub(
    #     # Input: [SR] DUR xx [Blah] [BRU xx] [Bounty]
    #     " SR (\\d+) DUR (\\d+) (.+) BRU (\\d+) *",
    #     # Output: SR,,DUR,Blah,BRU,Bounty
    #     ",\\1,,\\2,\\3,\\4,", content)
    
    # KILL regex example
    kill_pattern = re.compile(
        " SR (\\d+) DUR (\\d+) (.+) BRU (\\d+) *"
    )
    content = kill_pattern.sub(",\\1,,\\2,\\3,\\4,", content)

    # Wrap team names in commas
    for team in teams:
        content = re.sub(f" *({team}) *", f",{team},", content)

    # Split at injury type
    content = re.sub(" *(INJURED|KILLED|SEASON ENDING INJURY)( by)+", "\\1", content)

    headers = "Season,Week,Victim Team,Victim,SR0,SR1,DUR,Type,Offender Team,Offender,BRU,Bounty\n"

    print("Writing to file...")
    with open(args.out, "w+") as f:
        f.write(headers)
        f.write(content)
    print("All done!")

if __name__ == "__main__":
    main()