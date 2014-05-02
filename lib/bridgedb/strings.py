# -*- coding: utf-8 -*-

from __future__ import unicode_literals


def _(text):
    """This is necessary because strings are translated when they're imported.
    Otherwise this would make it impossible to switch languages more than
    once.

    :returns: The **text**.
    """
    return text


# TRANSLATORS: Please do not translate the word "TYPE".
EMAIL_MISC_TEXT = {
    0: _("""\
[This is an automated message; please do not reply.]"""),
    1: _("""\
Here are your bridges:"""),
    2: _("""\
You have exceeded the rate limit. Please slow down! The minimum time between
emails is %s hours. All further emails during this time period will be ignored."""),
    3: _("""\
COMMANDs: (combine COMMANDs to specify multiple options simultaneously)"""),
    4: _("Welcome to BridgeDB!"),
    # TRANLATORS: Please DO NOT tranlate the words "transport" or "TYPE".
    5: _("Currently supported tranport TYPEs:"),
}

WELCOME = {
    0: _("""\
BridgeDB can provide bridges with several %stypes of Pluggable Transports%s,
which can help obfuscate your connections to the Tor Network, making it more
difficult for anyone watching your internet traffic to determine that you are
using Tor.\n\n"""),

    1: _("""\
Some bridges with IPv6 addresses are also available, though some Pluggable
Transports aren't IPv6 compatible.\n\n"""),

    2: _("""\
Additionally, BridgeDB has plenty of plain-ol'-vanilla bridges %s without any
Pluggable Transports %s which maybe doesn't sound as cool, but they can still
help to circumvent internet censorship in many cases.\n\n"""),
}
"""These strings should go on the first "Welcome" email sent by the
:mod:`~bridgedb.EmailServer`, as well as on the ``index.html`` template used
by the :mod:`~bridgedb.HTTPServer`. They are used as an introduction to
explain what Tor bridges are, what bridges do, and why someone might want to
use bridges.
"""

FAQ = {
    0: _("What are bridges?"),
    1: _("""\
%s Bridges %s are Tor relays that help you circumvent censorship."""),
}

OTHER_DISTRIBUTORS = {
    0: _("I need an alternative way of getting bridges!"),
    1: _("""\
Another way to get bridges is to send an email to %s. Please note that you must
send the email using an address from one of the following email providers:
%s or %s."""),
}

HELP = {
    0: _("My bridges don't work! I need help!"),
    1: _("""If your Tor doesn't work, you should email %s."""),
    2: _("""\
Try including as much info about your case as you can, including the list of
bridges and Pluggable Transports you tried to use, your Tor Browser version,
and any messages which Tor gave out, etc."""),
}

BRIDGES = {
    0: _("Bridges"),
    1: _("Get Bridges!"),
}

OPTIONS = {
    0: _("Please select options for bridge type:"),
    1: _("Do you need IPv6 addresses?"),
    2: _("Do you need a %s?"),
}

CAPTCHA = {
    0: _('Your browser is not displaying images properly.'),
    1: _('Enter the characters from the image above...'),
}

HOWTO_TBB = {
    0: _("""How to start using your bridges"""),
    1: _("""\
To enter bridges into Tor Browser, follow the instructions on the %s Tor
Browser download page %s to start Tor Browser."""),
    2: _("""\
When the 'Tor Network Settings' dialogue pops up, click 'Configure' and follow
the wizard until it asks:"""),
    3: _("""\
Does your Internet Service Provider (ISP) block or otherwise censor connections
to the Tor network?"""),
    4: _("""\
Select 'Yes' and then click 'Next'. To configure your new bridges, copy and
paste the bridge lines (shown above) into the text input box. Finally, click
'Connect', and you should be good to go! If you experience trouble, try
clicking the 'Help' button in the 'Tor Network Settings' wizard for further
assistance."""),
}

EMAIL_COMMANDS = {
    "get help":             _("Displays this message."),
    "get bridges":          _("Request vanilla bridges."),
    "get ipv6":             _("Request IPv6 bridges."),
    # TRANLATORS: Please DO NOT tranlate the word the word "TYPE".
    "get transport [TYPE]": _("Request a Pluggable Transport by TYPE."),
    #"subscribe":            _("Subscribe to receive new bridges once per week")
    #"unsubscribe":          _("Cancel a subscription to new bridges")
}

#-----------------------------------------------------------------------------
#           All of the following containers are untranslated!
#-----------------------------------------------------------------------------

#: A list of all currently available pluggable transports. By "currently
#: available" we mean:
#:
#:   1. The PT is in a widely accepted, usable state for most Tor users.
#:   2. The PT is currently publicly deployed *en masse*".
#:
CURRENT_TRANSPORTS = [
    "obfs2",
    "obfs3",
    "scramblesuit",
]

EMAIL_SPRINTF = {
    # Goes into the "%s types of Pluggable Transports %s" part of ``WELCOME[0]``
    "WELCOME0": ("", "[0]"),
    # Goes into the "%s without Pluggable Transport %s" part of ``WELCOME[2]``
    "WELCOME2": ("-", "-"),
    # For the "%s Tor Browser download page %s" part of ``HOWTO_TBB[1]``
    "HOWTO_TBB1": ("", "[0]"),
    # For the "you should email %s" in ``HELP[0]``
    "HELP0": ("help@rt.torproject.org"),
}
"""``EMAIL_SPRINTF`` is a dictionary that maps translated strings which
contain format specifiers (i.e. ``%s``) to what those format specifiers should
be replaced with in a given template system.

For example, a string which needs a pair of HTML ``("<a href=''">, "</a>")``
tags (for the templates used by :mod:`bridgedb.HTTPServer`) would need some
alternative replacements for the :mod:`EmailServer`, because the latter uses
templates with a ``text/plain`` mimetype instead of HTML. For the
``EmailServer``, the format strings specifiers are replaced with an empty
string where the opening ``<a>`` tags would go, and a numbered Markdown link
specifier where the closing ``</a>`` tags would go.

The keys in this dictionary are the Python variable names of the corresponding
strings which are being formatted, i.e. ``WELCOME0`` would be the string
replacements for ``strings.WELCOME.get(0)``.


For example, the ``0`` string in :data:`WELCOME` above has the substring::

    "%s without Pluggable Transport %s"

and so to replace the two ``%s`` format specifiers, you would use this mapping
like so::

>>> from bridgedb import strings
>>> welcome = strings.WELCOME.get(0)
>>> emailWelcome = welcome.format(strings.EMAIL_SPRINTF.get("WELCOME0"))
>>> emailWelcome
"""

EMAIL_REFERENCE_LINKS = {
    "WELCOME0": "[0]: https://www.torproject.org/docs/pluggable-transports.html",
    "HOWTO_TBB1": "[0]: https://www.torproject.org/projects/torbrowser.html.en#downloads-beta",
}