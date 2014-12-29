import time
import math
from plugins.baseplugin import BasePlugin


class Plugin(BasePlugin):
    """
    Countdown tools for any scheduled, limited time event.
    """
    name = 'CountdownPlugin'

    def configure(self, configuration):
        self.config = configuration.event

    def createDefaultSettings(self):
        self.settings.setMulti({
            'event_name': self.config and self.config.event_name or '',
            'event_start': self.config and self.config.event_start or 0,
            'event_stages': self.config and self.config.event_stages or []
        }, initial=True)

    def command_remaining(self, user, nick, channel, rest):
        self.command_countdown(user, nick, channel, rest)

    def command_timeleft(self, user, nick, channel, rest):
        self.command_countdown(user, nick, channel, rest)

    def command_countdown(self, user, nick, channel, rest):
        """
        Get the time until the start/end of the event.
        Aliases: {command_prefix}remaining, {command_prefix}timeleft
        """

        # get and validate event start time
        event_start = self.settings.get('event_start', 0)
        if event_start == 0:
            self.reply(
                channel,
                nick,
                self.formatDoc('Event start time not set. Find a {nick} admin')
            )
            return

        # get current time
        now = time.time()

        # get stages
        event_stages = self.settings.get('event_stages', [])

        if len(event_stages) == 0:
            self.reply(
                channel,
                nick,
                self.formatDoc(
                    'Event stages are not defined. Find a {nick} admin.'
                )
            )
            return

        # get event name
        event_name = self.settings.get('event_name', '')

        # find the current stage
        for stage in event_stages:
            stage_start = event_start + stage['delay']
            if now < stage_start:
                message = self.getCountdown(stage_start)
                if event_name != '':
                    message = (stage['name'] + ' in: ' + message).format(
                            nick=self.nick,
                            event_name=event_name
                        )
                self.reply(channel, nick, message)
                return

        # no current stage found
        message = "No current event info. Get the " + \
                "unix timestamp for the next event and send it to an admin."
        self.reply(channel, nick, message)

    def admin_set_event_name(self, user, nick, channel, rest):
        """Sets the name of the next event."""
        self.settings.set('event_name', rest)
        self.reply(channel, nick, 'Setting event name to %s' % rest)

    def admin_set_event_start(self, user, nick, channel, rest):
        """Sets the event start time (unix timestamp)."""
        try:
            start = int(rest)
        except ValueError, TypeError:
            self.reply(
                    channel,
                    nick,
                    "Invalid event start time: %s" % rest
                )
            return
        self.settings.set('event_start', start)
        self.reply(
                channel, nick, 'Setting event start time to %d' % start
            )

    def admin_get_event_info(self, user, nick, channel, rest):
        """Prints the current event information."""
        event_name = self.settings.get('event_name')
        event_start = self.settings.get('event_start')
        message = "Event Name: %s   Event Start: %d" % (event_name, event_start)

        stages = self.settings.get('event_stages', [])
        for stage in stages:
            message += "   %s: %d" % (
                    stage['name'], event_start + stage['duration']
                )

        self.reply(channel, nick, message)

    def getCountdown(self, target_time):
        try:
            target_time = int(target_time)
        except ValueError, TypeError:
            return False

        seconds = target_time - time.time()
        if seconds < 0:
            return False

        output = ''
        if seconds > 86400:
            days = math.floor(seconds / 86400)
            seconds = seconds % 86400
            output = '%dd ' % days

        if seconds > 3600:
            hours = math.floor(seconds / 3600)
            seconds = seconds % 3600
            output += '%dh ' % hours

        if seconds > 60:
            minutes = math.floor(seconds / 60)
            seconds = seconds % 60
            output += '%dm ' % minutes

        if seconds > 0:
            if output == '':
                if seconds > 1:
                    output = '%d seconds' % seconds
                else:
                    output = '1 second'
##            else:
##                if seconds > 1:
##                    output += 'and %2d seconds' % seconds
##                else:
##                    output += 'and 1 second'

        return output
