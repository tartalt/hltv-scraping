import cloudscraper
from bs4 import BeautifulSoup
import csv

# Créer une instance de cloudscraper
scraper = cloudscraper.create_scraper()

# URL de la page du classement des équipes
url = "https://www.hltv.org/ranking/teams"

# Faire une requête GET pour récupérer la page
response = scraper.get(url)
response.raise_for_status()  # S'assurer que la requête a réussi

# Parser le contenu de la page avec BeautifulSoup
soup = BeautifulSoup(response.text, 'lxml')

# Trouver les éléments contenant les informations des équipes
teams = soup.select('div.ranking-header')

# Extraire et afficher le top 20 des équipes
top_20_teams = []
for team in teams[:20]:
    # Extraire le nom de l'équipe en format spécifié
    team_name = team.select_one('div.teamLine span.name').text.strip().lower().replace(' ', '-').replace('.', '')
    
    # Extraire le score HLTV
    hltv_score = team.select_one('div.teamLine span.points').text.strip().replace('(', '').replace(')', '').replace(' points', '')
    
    # Initialiser l'ID de l'équipe
    team_id = None
    
    # Trouver l'élément avec l'ID de l'équipe
    more_info = team.find_next_sibling('div', class_='lineup-con')
    if more_info:
        team_profile_link = more_info.find('a', class_='moreLink')['href']
        team_id = team_profile_link.split('/')[2]  # Extraire l'ID de l'URL
    
    # Extraire le lien du logo de l'équipe
    logo_img = team.select_one('span.team-logo img')
    logo_url = logo_img['src'] if logo_img else 'N/A'
    
    # Extraire les joueurs et leurs IDs
    players_info = more_info.select('td.player-holder a.pointer')
    players = []
    for player in players_info:
        player_id = player['href'].split('/')[2]
        player_name = player.select_one('div.nick').text.strip()
        players.append(f"{player_name} (ID: {player_id})")
    
    top_20_teams.append((hltv_score, team_name, team_id, logo_url, ', '.join(players)))

# Enregistrer les données dans un fichier CSV
with open('top_20_teams.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['HLTV Score', 'Team Name', 'Team ID', 'Logo URL', 'Players'])
    writer.writerows(top_20_teams)

print("Top 20 teams have been saved to top_20_teams.csv")
