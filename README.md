Yaib Countdown Plugin
=================

~~~
!timeleft
Event stage starts in: 14h 42m
~~~

A countdown plugin for [yaib](https://github.com/collingreen/yaib) to support
any scheduled, limited time event. Originally created to manage the time left
between various stages of the Ludum Dare game development competition. See
below.

To use, add an `event` key to your configuration with a list `event_stages`
that contains objects with properties `name` and `delay`. The delay should
be the number of seconds after the start of the event. You can also set the
`event_name` and `event_start` fields in config, or set them from the admin
`set_event_name` and `set_event_start` commands. All times are in unix timestamp
format (seconds from the epoch).

Originally, this plugin was used to count down to the start of the
LudumDare game development competition, then count down until the end of
the various stages (compo start, compo end, jam end, judging end, next
compo). The configuration for this setup looks like this:

~~~
"event": {
    "event_stages": [
        {"name": "{event_name} competition starts", "delay": 0},
        {"name": "{event_name} competition ends", "delay": 172800},
        {"name": "{event_name} jam ends", "delay": 259200},
        {"name": "{event_name} judging ends", "delay": 1468800}
    ]
}
~~~
