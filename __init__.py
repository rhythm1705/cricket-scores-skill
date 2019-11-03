from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler, intent_handler
import requests
from bs4 import BeautifulSoup


class CricketScoresSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('scores.cricket.intent')
    def handle_scores_cricket(self, message):
        self.speak_dialog('scores.cricket')
        list_of_live_matches = live_matches_extractor(
            "https://sports.ndtv.com/cricket/live-scores")
        for live_match in list_of_live_matches:
            self.speak(str(live_match))


def create_skill():
    return CricketScoresSkill()


def live_matches_extractor(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    matches = soup.select('.live-score-listing .live-score-item')
    # for match in matches:
    #     print(match.text.strip())
    matchesList = []
    for match in matches:
        matchSoup = BeautifulSoup(str(match), 'html.parser')
        location = matchSoup.select('.live-score-item .location')
        summary = matchSoup.select('.live-score-item .summary')
        game = matchSoup.select(
            '.live-score-item .match-venue-livescrore > span')
        teamA = matchSoup.select('.live-score-item .team-a .team-name')
        teamA_inn = matchSoup.select('.live-score-item .team-a .team-inns')
        teamB = matchSoup.select('.live-score-item .team-b .team-name')
        teamB_inn = matchSoup.select('.live-score-item .team-b .team-inns')
        if((len(teamA_inn) != 0) and (len(teamB_inn) != 0)):
            matchDetails = [location[0].text.strip(), summary[0].text.strip(), game[0].text.strip(
            ), teamA[0].text.strip(), teamA_inn[0].text.strip(), teamB[0].text.strip(), teamB_inn[0].text.strip()]
        else:
            matchDetails = [location[0].text.strip(), summary[0].text.strip(
            ), game[0].text.strip(), teamA[0].text.strip(), -1, teamB[0].text.strip(), -1]
        matchesList.append(matchDetails)
    new_matchesList = []
    for elem in matchesList:
        if elem not in new_matchesList:
            new_matchesList.append(elem)
    matchesList = new_matchesList
    return matchesList
