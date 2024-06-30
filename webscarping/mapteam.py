from bs4 import BeautifulSoup
import csv
import time
import random
from zenrows import ZenRowsClient

# Fonction pour récupérer les statistiques de chaque match et carte
def get_team_match_stats(team_id, team_name, start_date, end_date, client):
    team_name_url = team_name.replace(' ', '-').lower()
    url = f"https://www.hltv.org/stats/teams/matches/{team_id}/{team_name_url}?startDate={start_date}&endDate={end_date}&matchType=Lan&rankingFilter=Top20"

    params = {"premium_proxy": "true"}  # Premium proxy enabled
    
    try:
        response = client.get(url, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = soup.select('tbody tr')
        
        map_stats = {}
        
        for match in matches:
            try:
                map_name = match.select_one('td.statsMapPlayed span').text.strip()
                result = match.select_one('td.gtSmartphone-only span.statsDetail').text.strip()
                rounds_won, rounds_lost = map(int, result.split('-'))
                
                if map_name not in map_stats:
                    map_stats[map_name] = {'wins': 0, 'losses': 0, 'rounds_won': 0, 'rounds_lost': 0}
                
                map_stats[map_name]['rounds_won'] += rounds_won
                map_stats[map_name]['rounds_lost'] += rounds_lost
                
                if rounds_won >= rounds_lost:
                    map_stats[map_name]['wins'] += 1
                else:
                    map_stats[map_name]['losses'] += 1
                    
            except Exception as e:
                print(f"Failed to parse match data: {e}")
        
        return map_stats
    
    except Exception as e:
        print(f"Failed to fetch data for team {team_name}: {e}")
        return None

# Create an instance of ZenRowsClient
client = ZenRowsClient("77f044fb8ba4432c25ca4d8756961ab8965f843a")

# Read data from the CSV file
teams = []
with open('top_20_teams 2.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        teams.append((row['Team ID'], row['Team Name']))

# Define the date range
start_date = '2024-03-26'
end_date = '2024-06-26'

# Save the new data to a CSV file
with open('teams_map_stats3.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Team ID', 'Team Name', 'Map', 'Win Percentage', 'Total Matches', 'Total Lost', 'Rounds Won', 'Rounds Lost'])
    
    for team_id, team_name in teams:
        try:
            map_stats = get_team_match_stats(team_id, team_name, start_date, end_date, client)
            if map_stats:
                for map_name, stats in map_stats.items():
                    total_matches = stats['wins'] + stats['losses']
                    total_lost = stats['losses']
                    win_percentage = (stats['wins'] / total_matches) * 100 if total_matches > 0 else 0.0  # Ensure float division
                    writer.writerow([team_id, team_name, map_name, win_percentage, total_matches, total_lost, stats['rounds_won'], stats['rounds_lost']])
                    time.sleep(random.randint(2, 5))
        except Exception as e:
            print(f"Failed to get stats for team {team_name}: {e}")

print("Team map statistics have been saved to teams_map_stats.csv")
