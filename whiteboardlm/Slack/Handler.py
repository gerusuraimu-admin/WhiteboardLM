from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from whiteboardlm.Common import respond
from whiteboardlm.Slack import SlackEventObject


def slack_start(slack_token: str, app_token: str, uid: str):
    app = App(token=slack_token)

    @app.event('app_mention')
    def response(event, say):
        obj = SlackEventObject(**event)
        result = respond(obj.message, uid)
        say(result)

    handler = SocketModeHandler(app, app_token)
    handler.start()
