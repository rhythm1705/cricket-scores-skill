from mycroft import MycroftSkill, intent_file_handler


class CricketScores(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('scores.cricket.intent')
    def handle_scores_cricket(self, message):
        self.speak_dialog('scores.cricket')


def create_skill():
    return CricketScores()

