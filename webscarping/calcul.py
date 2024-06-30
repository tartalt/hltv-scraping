import csv
import json

# Fichiers CSV d'entrée
team_info_csv = 'top_20_teams.csv'
team_stats_csv = 'team_stats_filtered.csv'

# Lecture du fichier CSV des informations des équipes
teams_info = {}
with open(team_info_csv, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        team_id = row['Team ID']
        teams_info[team_id] = {
            'team_name': row['Team Name'],
            'team_id': team_id,
            'logo_url': row['Logo URL'],
            'hltv_score': int(row['HLTV Score']),
            'players': row['Players'].split(', '),
            'map_scores': {}
        }

# Lecture du fichier CSV des statistiques des équipes
team_stats = {}
with open(team_stats_csv, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        team_id = row['Team ID']
        if team_id not in teams_info:
            continue  # Ignorer les équipes non présentes dans le top 20
        map_name = row['Map']
        win_percentage = float(row['Win Percentage'])
        rounds_won = int(row['Rounds Won'])
        rounds_lost = int(row['Rounds Lost'])
        total_rounds = rounds_won + rounds_lost
        
        if total_rounds > 0:
            map_score = teams_info[team_id]['hltv_score'] * win_percentage * (1 + (rounds_won - rounds_lost) / total_rounds)
        else:
            map_score = teams_info[team_id]['hltv_score'] * win_percentage  # Cas où il n'y a pas de rounds joués
        
        teams_info[team_id]['map_scores'][map_name] = map_score

# Vérifier et ajuster les scores pour les équipes n'ayant pas de statistiques sur certaines cartes
maps = ['Mirage', 'Dust2', 'Nuke', 'Ancient', 'Inferno', 'Vertigo', 'Anubis']
for team_id, team in teams_info.items():
    for map_name in maps:
        if map_name not in team['map_scores']:
            team['map_scores'][map_name] = team['hltv_score'] * 0.9 * 40

# Normalisation des scores
def normalize_scores(scores):
    min_score = min(scores)
    max_score = max(scores)
    return [(score - min_score) / (max_score - min_score) * 100 for score in scores]

# Normaliser les scores de chaque carte pour chaque équipe
for map_name in maps:
    scores = [team['map_scores'][map_name] for team in teams_info.values()]
    normalized_scores = normalize_scores(scores)
    for i, team_id in enumerate(teams_info.keys()):
        teams_info[team_id]['map_scores'][map_name] = normalized_scores[i]

# Générer le fichier JSON final
output_data = list(teams_info.values())
with open('team_scores.json', 'w') as json_file:
    json.dump(output_data, json_file, indent=4)

print("Les scores des équipes ont été sauvegardés dans team_scores.json")

# import csv

# # Fichier CSV d'entrée et de sortie
# input_csv = 'teams_map_stats.csv'
# output_csv = 'team_stats_filtered.csv'

# # Lire le fichier CSV et filtrer les lignes
# filtered_rows = []
# with open(input_csv, 'r') as infile:
#     reader = csv.DictReader(infile)
#     fieldnames = reader.fieldnames  # Obtenir les noms des colonnes
#     for row in reader:
#         if row['Map'] != 'Overpass':
#             filtered_rows.append(row)

# # Écrire les lignes filtrées dans un nouveau fichier CSV
# with open(output_csv, 'w', newline='') as outfile:
#     writer = csv.DictWriter(outfile, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(filtered_rows)

# print(f"Toutes les lignes contenant 'Overpass' ont été supprimées et le fichier résultant a été sauvegardé sous le nom '{output_csv}'")
