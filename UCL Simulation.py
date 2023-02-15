import csv
import random
import sqlite3
import pandas as pd
import time



class Team:
    def __init__(self, name, league):
        self.name = name
        self.league = league
        self.points = self.gd = self.ga = self.gf = self.losses = self.draws = self.wins = self.mp = 0
        self.qfg = 0  # For quarter final goals - so that they start from zero
        self.sfg = 0  # For semi final goals - so that they start from zero
        self.fg = 0  # For final goals - so that they start from zero
        self.penalty = 0  # For penalty shootout in the final


premier_league_teams = []
laliga_teams = []
bundesliga_teams = []
serieA_teams = []

group_a = []
group_b = []
group_c = []
group_d = []
groups = [group_a, group_b, group_c, group_d]

allocated_teams = []
qualified_quarter_finals =[]
qualified_semi_finals =[]
qualified_final =[]


quarter_final_1 = []
quarter_final_2 = []
quarter_final_3 = []
quarter_final_4 = []
quarter_finals =[quarter_final_1, quarter_final_2, quarter_final_3, quarter_final_4]

semi_final_1 = []
semi_final_2 = []
semi_finals = [semi_final_1, semi_final_2]


def group_selection(group):

    selection_1 = random.choice(premier_league_teams)
    group.append(selection_1)
    premier_league_teams.remove(selection_1)

    selection_2 = random.choice(laliga_teams)
    group.append(selection_2)
    laliga_teams.remove(selection_2)

    selection_3 = random.choice(bundesliga_teams)
    group.append(selection_3)
    bundesliga_teams.remove(selection_3)

    selection_4 = random.choice(serieA_teams)
    group.append(selection_4)
    serieA_teams.remove(selection_4)


def generateRandomScore():
    return random.randint(0, 6), random.randint(0, 5)


def simulate_league(group):
    for home_team in group:
        for away_team in group:
            if home_team == away_team:
                pass
            if home_team != away_team:
                home_score, away_score = generateRandomScore()
                home_team.gf += home_score
                away_team.gf += away_score
                home_team.ga += away_score
                away_team.ga += home_score
                home_team.gd = home_team.gf - home_team.ga
                away_team.gd = away_team.gf - away_team.ga
                home_team.mp += 1
                away_team.mp += 1
                if home_score == away_score:
                    home_team.draws += 1
                    away_team.draws += 1
                    home_team.points += 1
                    away_team.points += 1
                if home_score > away_score:
                    home_team.wins += 1
                    away_team.losses += 1
                    home_team.points += 3
                if away_score > home_score:
                    away_team.wins += 1
                    home_team.losses += 1
                    away_team.points += 3



def simulate_quarters(quarter_finals_teams):
    for home_team in quarter_finals_teams:
        print("=" * 50)
        print(home_team.name.upper() + "'S HOME GAME: ")
        print("=" * 50)
        for away_team in quarter_finals_teams:
            if home_team == away_team:
                pass
            if home_team != away_team:
                home_score, away_score = generateRandomScore()
                home_team.qfg += home_score
                away_team.qfg += away_score
                print(home_team.name, home_score, ":", away_score, away_team.name, "\nAGGREGATE:",[home_team.qfg], ":",[away_team.qfg])
                if home_team.qfg == away_team.qfg:
                    home_score, away_score = random.randint(1,5), random.randint(1,5)
                    home_team.qfg = home_score
                    away_team.qfg = away_score
                    print("Penaly Shootout: ", home_team.name,home_score,":",away_score,away_team.name)




def simulate_semis(semi_finals_teams):
    for home_team in semi_finals_teams:
        print("=" * 50)
        print(home_team.name.upper() + "'S HOME GAME: ")
        print("=" * 50)
        for away_team in semi_finals_teams:
            if home_team == away_team:
                pass
            if home_team != away_team:
                home_score, away_score = generateRandomScore()
                home_team.sfg += home_score
                away_team.sfg += away_score
                print(home_team.name, home_score, ":", away_score, away_team.name, "\nAGGREGATE: ",[home_team.sfg], " : ",[away_team.sfg])
                if home_team.sfg == away_team.sfg:
                    home_score, away_score = generateRandomScore()
                    home_team.sfg = home_score
                    away_team.sfg = away_score
                    print("Penaly Shootout: ", home_team.name,home_score,":",away_score,away_team.name)




def simulate_final(team_1, team_2):

    home_score, away_score = generateRandomScore()
    print(team_1.name, home_score, ":", away_score, team_2.name)
    team_1.fg += home_score
    team_2.fg += away_score
    if team_1.fg == team_2.fg:
        penalty_shootout(team_1, team_2)
    if team_1.fg > team_2.fg:
        team1_cheer = team_1.name + " " + "has won the UEFA Champions League"
        print("=" * 70)
        print("||", "-" * 5, team1_cheer, "-" * 5,"||")
        print("=" * 70)
        time.sleep(15)
    if team_2.fg > team_1.fg:
        team2_cheer = team_2.name + " " + "has won the UEFA Champions League"
        print("=" * 70)
        print("||", "-" * 10, team2_cheer, "-" * 10,"||")
        print("=" * 70)
        time.sleep(15)


def penalty_shootout(team_1, team_2):
    print("The game has ended with the scores level!\n")
    print("This means the game has gone to a penalty shootout!\n")
    input("Press enter to start the penalty shootout.\n")
    team_1.penalty = random.randint(1, 5)
    team_2.penalty = random.randint(1, 5)
    if team_1.penalty > team_2.penalty:
        print(team_1.name, team_1.penalty, ":", team_2.penalty, team_2.name)
        print(team_1.name, "have won the penalty shootout\n")
        print(team_1.name, "are the winners of the UEFA Champions League.")
    elif team_1.penalty < team_2.penalty:
        print(team_1.name, team_1.penalty, ":", team_2.penalty, team_2.name)
        print(team_2.name, "have won the penalty shootout\n")
        print(team_2.name, "are the winners of the UEFA Champions League.")
    if team_1.penalty == team_2.penalty:
        team_1_decider = random.randint(1, 5)
        team_2_decider = random.randint(1, 5)
        if team_1_decider > team_2_decider:
            print(team_1.name, "have won the penalty shootout\n")
            print(team_1.name, "are the winners of the UEFA Champions League.")
        if team_2_decider > team_1_decider:
            print(team_1.name, "have won the penalty shootout\n")
            print(team_1.name, "are the winners of the UEFA Champions League.")


print("--------------------COMP LEAGUES--------------------")
print("\nAre you ready to play your very own UEFA Champions League?")
while True:
    show_teams = input("Press the Enter key to begin.")
    if show_teams not in "\n":
        print("Invalid Input")
        continue
    else:
        break



all_teams = [
    Team("Manchester United", "Premier League"), Team("Liverpool", "Premier League"),
    Team("Manchester City", "Premier League"), Team("Chelsea", "Premier League"),
    Team("Real Madrid", "La Liga"), Team("Barcelona", "La Liga"), Team("Atletico Madrid", "La Liga"),
    Team("Sevilla", "La Liga"), Team("Bayern Munich", "Bundesliga"),
    Team("Borussia Dortmund", "Bundesliga"), Team("Bayer Leverkusen", "Bundesliga"), Team("RB Leipzig", "Bundesliga"),
    Team("Juventus", "Serie A"), Team("Inter Milan", "Serie A"),
    Team("AC Milan", "Serie A"), Team("Napoli", "Serie A")
]


for team in all_teams[:4]:
    premier_league_teams.append(team)
for team in premier_league_teams:
    allocated_teams.append(team)
for team in all_teams:
    if len(laliga_teams) < 4 and team not in premier_league_teams:
        laliga_teams.append(team)
        allocated_teams.append(team)
for team in all_teams:
    if len(bundesliga_teams) < 4 and team not in allocated_teams:
        bundesliga_teams.append(team)
        allocated_teams.append(team)
for team in all_teams:
    if len(serieA_teams) < 4 and team not in allocated_teams:
        serieA_teams.append(team)
        allocated_teams.append(team)

print("\nFirst, the top four teams from four leagues will be selected.")
while True:
    show_leagues = input("Press the enter key to see the teams.")
    if show_leagues not in "\n":
        print("Invalid Input")
        continue
    else:
        break

print("\nPremier League Teams:")
print("=" * 40)
for team in premier_league_teams:
    print(team.name, "|-", team.league, "-|")
print("=" * 40)

print("\nLa-Liga Teams:")
print("=" * 40)
for team in laliga_teams:
    print(team.name, "|-", team.league, "-|")
print("=" * 40)

print("\nBundesliga Teams:")
print("=" * 40)
for team in bundesliga_teams:
    print(team.name, "|-", team.league, "-|")
print("=" * 40)

print("\nSerie-A Teams:")
print("=" * 40)
for team in serieA_teams:
    print(team.name, "|-", team.league, "-|")
print("=" * 40)

group_selection(group_a)
group_selection(group_b)
group_selection(group_c)
group_selection(group_d)

print("\nIt's time to do the group stage draw.")
while True:
    group_stage = input("Press the enter key to see the groups.")
    if group_stage not in "\n":
        print("Invalid Value")
        continue
    else:
        break

print("\n")
print("=" * 20)
print("Group A:")
print("=" * 20)
a = 0
b = 0
c = 0
d = 0
for team in group_a:
    a += 1
    print(a,".",team.name)

print("\n")
print("=" * 20)
print("Group B:")
print("=" * 20)
for team in group_b:
    b += 1
    print(b,".",team.name)

print("\n")
print("=" * 20)
print("Group C:")
print("=" * 20)
for team in group_c:
    c += 1
    print(c,".",team.name)

print("\n")
print("=" * 20)
print("Group D:")
print("=" * 20)
for team in group_d:
    d += 1
    print(d,".",team.name)


print("\nNow it's time to play the group stage matches.")
while True:
    standings = input("Press the enter key to see the standings after group stage.")
    if standings not in "\n":
        print("Invalid input")
        continue
    else:
        break
print("\n")

for group in groups:
    simulate_league(group)



sorted_group_a = sorted(group_a, key=lambda t: t.points, reverse=True)
sorted_group_b = sorted(group_b, key=lambda t: t.points, reverse=True)
sorted_group_c = sorted(group_c, key=lambda t: t.points, reverse=True)
sorted_group_d = sorted(group_d, key=lambda t: t.points, reverse=True)

sorted_groups = [sorted_group_a, sorted_group_b, sorted_group_c, sorted_group_d]



for group in sorted_groups:
    print("| {:<20} | {:^4} | {:^3} | {:^3} | {:^3} | {:^4} | {:^4} | {:^4} | {:^6} |".format("CLUB", "MP", "W", "D", "L", "GF", "GA", "GD", "PTS"))

    for team in group:
        print("| {:<20} | {:^4} | {:^3} | {:^3} | {:^3} | {:^4} | {:^4} | {:^4} | {:^6} |".format(team.name, team.mp, team.wins,team.draws,team.losses,team.gf,team.ga,team.gd,team.points))
    print("\n")


while True:
    quarterteams = input("Press the enter key to see which teams have made it through to the quarter-finals of the competition.")
    if quarterteams not in "\n":
        print("Invalid Input")
        continue
    else:
        break


for group in sorted_groups:
    qualified_quarter_finals.append(group[0])
    if group[1].points > group[2].points:
        qualified_quarter_finals.append(group[1])
    elif group[1].gd > group[2].gd:
        qualified_quarter_finals.append(group[1])
    elif group[2].gd > group[1].gd:
        qualified_quarter_finals.append(group[2])
    elif group[1].gf > group[2].gf:
        qualified_quarter_finals.append(group[1])
    elif group[2].gf > group[1].gf:
        qualified_quarter_finals.append(group[2])

qualifiedTeams = []
qualifiedLeages = []

print("\n")
for team in qualified_quarter_finals:
    qualifiedTeams.append(team.name)
    qualifiedLeages.append(team.league)
    print(team.name)

quarter_teams_table = {'Names':qualifiedTeams,'Leagues':qualifiedLeages}
df = pd.DataFrame(quarter_teams_table)
df.to_csv('QualifiedTeams.csv')
conn = sqlite3.connect('Groupstagequalifiers.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS QualifiedTeams')
cur.execute("CREATE TABLE QualifiedTeams(No INT, Teams TEXT, Leagues TEXT)")
file = open("QualifiedTeams.csv")
rows = csv.reader(file)
cur.executemany("INSERT INTO QualifiedTeams(No, Teams, Leagues) VALUES(?,?,?)", rows)
conn.commit()
conn.close()


print("\n")
while True:
    quarter_result = input("Press Enter to see the result of the quarter finals")
    if quarter_result not in "\n":
        print("Invalid input!")
        continue
    else:
        break

print("\n")
for quarter_final in quarter_finals:
    selection_1 = random.choice(qualified_quarter_finals)
    quarter_final.append(selection_1)
    qualified_quarter_finals.remove(selection_1)
    selection_2 = random.choice(qualified_quarter_finals)
    quarter_final.append(selection_2)
    qualified_quarter_finals.remove(selection_2)
    simulate_quarters(quarter_final)
    print("\n")


for match in quarter_finals:
    if match[0].qfg > match[1].qfg:
        qualified_semi_finals.append(match[0])
    elif match[0].qfg < match[1].qfg:
        qualified_semi_finals.append(match[1])
    else:
        winner = random.randint(0,1)
        qualified_semi_finals.append(match[winner])


while True:
    semi_teams = input("Press the enter key to see which teams have made it through to the semi-finals of the competition.")
    if semi_teams not in "\n":
        print("Invalid input!")
        continue
    else:
        break

print("\n")
for team in qualified_semi_finals:
    print(team.name)
print("\n")

for semi_final in semi_finals:
    selection_1 = random.choice(qualified_semi_finals)
    semi_final.append(selection_1)
    qualified_semi_finals.remove(selection_1)
    selection_2 = random.choice(qualified_semi_finals)
    semi_final.append(selection_2)
    qualified_semi_finals.remove(selection_2)
print("\n")
while True:
    semi_results = input("Press the enter key to see the results of the semi-finals.")
    if semi_results not in "\n":
        print("Invalid input!")
        continue
    else:
        break

for semi_final in semi_finals:
    simulate_semis(semi_final)
    print("\n")

for match in semi_finals:
    if match[0].sfg > match[1].sfg:
        qualified_final.append(match[0])
    elif match[0].sfg < match[1].sfg:
        qualified_final.append(match[1])
    else:
        winner = random.randint(0, 1)
        qualified_final.append(match[winner])
print("\n")
while True:
    final_teams = input("Press the enter key to see which teams have made it through to the final of the competition.")
    if final_teams not in "\n":
        print("Invalid input!")
        continue
    else:
        break

for team in qualified_final:
    print(team.name)
print("\n")

print("\nPresenting the final of the UEFA Champions League.")
print("=" * 50)
print(qualified_final[0].name, "VS", qualified_final[1].name)
print("=" * 50)
print("\n")

while True:
    finalscore = input("Press the enter key to see which team has won the Champions League.")
    if finalscore not in "\n":
        print("Invalid input")
        continue
    else:
        break


simulate_final(qualified_final[0], qualified_final[1])