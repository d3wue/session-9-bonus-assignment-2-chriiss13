import requests
from bs4 import BeautifulSoup

# Function to fetch HTML content from a URL with a specified user-agent
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch the webpage.")
        return None

# Function to extract and collect team names from Bundesliga
def get_bundesliga_teams():
    url = "https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1"
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, "html.parser")
        team_elements = soup.find_all("td", class_="hauptlink no-border-links")
        teams = [team.text.strip() for team in team_elements]
        return teams
    else:
        return []

# Function to get high level information of a team
def get_team_info(team_name, team_id):
    url = f"https://www.transfermarkt.com/{team_name}/startseite/verein/{team_id}/saison_id/2023"
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, "html.parser")

        stadion = {"href": f"/{team_name}/stadion/verein/{team_id}"}
        stadium_tag = soup.find("a", stadion)
        stadium = stadium_tag.get_text() if stadium_tag else "Information not available"

        trainer = {"class": "name svelte-1vf4nm9"}
        coach_tag = soup.find("div", trainer)
        coach = coach_tag.find_next("a").text.strip() if coach_tag else "Information not available"

        wert = {"class": "data-header__market-value-wrapper"}
        value_tag = soup.find("a", wert)
        value = value_tag.find_next("#text").get_text() if value_tag else "Information not available"

        print()
        print(f"Team: {team_name}")
        print(f"Stadium: {stadium}")
        print(f"Coach: {coach}")
        print(f"Total Market Value: {value}")
        print()
    else:
        print("Failed to fetch team information.")

# Function to extract team IDs from Bundesliga page
def get_bundesliga_team_ids():
    url = "https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1"
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, "html.parser")
        team_elements = soup.find_all("td", class_="hauptlink no-border-links")
        team_ids = {}
        for team in team_elements:
            team_name = team.text.strip()
            team_link = team.find("a")["href"]
            team_id = team_link.split("/")[2]  # Extract team ID from URL
            team_ids[team_name] = team_id
        return team_ids
    else:
        return {}

# Main function
def main():
    while True:
        print("\nOptions:")
        print("1. Show available teams")
        print("2. Select team and show high level information")
        print("3. Stop the program")
        choice = input("Enter your choice: ")

        if choice == "1":
            teams = get_bundesliga_teams()
            print("\nAvailable Teams:")
            for index, team in enumerate(teams, start=1):
                print(f"{index}. {team}")
        elif choice == "2":
            teams = get_bundesliga_teams()
            team_ids = get_bundesliga_team_ids()
            print("\nAvailable Teams:")
            for index, team in enumerate(teams, start=1):
                print(f"{index}. {team}")
            team_index = int(input("Enter the team number: ")) - 1
            if 0 <= team_index < len(teams):
                team_name = teams[team_index]
                team_id = team_ids.get(team_name)
                get_team_info(team_name, team_id)
            else:
                print("Invalid team number.")
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
