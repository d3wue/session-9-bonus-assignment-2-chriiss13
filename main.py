import requests
from bs4 import BeautifulSoup

def fetch_league_data(league_url, user_agent):
    headers = {'User-Agent': user_agent}
    response = requests.get(league_url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print("Fehler beim Abrufen der Daten von Transfermarkt.com")
        return None

#Hier nach Fehler suchen
def extract_teams(html_content):
    teams = []
    soup = BeautifulSoup(html_content, 'html.parser')
    team_table = soup.find('div', class_='responsive-table')
    rows = team_table.find_all('tr', class_='odd') + team_table.find_all('tr', class_='even')
    for row in rows:
        team_link = row.find('a', class_='vereinprofil_tooltip')
        if team_link:
            team_name = team_link.text.strip()
            team_url = team_link['href']
            teams.append({'name': team_name, 'url': team_url})
    return teams

def extract_players(team_url, user_agent):
    headers = {'User-Agent': user_agent}
    players = []
    response = requests.get(team_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        player_table = soup.find('table', class_='items')
        if player_table:
            rows = player_table.find_all('tr', class_='odd') + player_table.find_all('tr', class_='even')
            for row in rows:
                player_name = row.find('a', class_='spielprofil_tooltip').text.strip()
                players.append({'name': player_name})
    return players

def show_available_teams(teams):
    print("Verfügbare Mannschaften:")
    for index, team in enumerate(teams, start=1):
        print(f"{index}. {team['name']}")

def show_team_players(players):
    print("Spieler:")
    for player in players:
        print(player['name'])

if __name__ == "__main__":
    league_url = "https://www.transfermarkt.com/1-bundesliga/startseite/wettbewerb/L1"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    
    league_data = fetch_league_data(league_url, user_agent)
    if league_data:
        teams = extract_teams(league_data)
        show_available_teams(teams)
        
        while True:
            choice = input("Wählen Sie eine Mannschaft (geben Sie die entsprechende Nummer ein) oder geben Sie 'exit' ein, um zu beenden: ")
            if choice.lower() == 'exit':
                break
            try:
                choice_index = int(choice) - 1
                selected_team = teams[choice_index]
                team_url = "https://www.transfermarkt.com" + selected_team['url']
                team_players = extract_players(team_url, user_agent)
                show_team_players(team_players)
            except (ValueError, IndexError):
                print("Ungültige Eingabe. Bitte geben Sie eine gültige Nummer ein.")

