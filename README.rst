***********************
BridgeDB |Build Status|
***********************

BridgeDB is a collection of backend servers used to distribute `Tor Bridges
<https://www.torproject.org/docs/bridges>`__. Currently, it mainly consists of
a webserver with `an HTTPS interface <https://bridges.torproject.org>`__,
`an email responder <mailto:bridges@torproject.org>`__, and an SQLite database.

.. |Build Status| image:: https://travis-ci.org/NullHypothesis/bridgedb.svg?branch=master
   :target: https://travis-ci.org/github/NullHypothesis/bridgedb

.. image:: doc/sphinx/source/_static/bay-bridge.jpg
   :scale: 80%
   :align: center


.. contents::
   :backlinks: entry


=====================
What are Tor Bridges?
=====================

`Tor Bridges <https://www.torproject.org/docs/bridges>`__ are special
Tor relays which are not listed in the public relay directory. They are
used to help circumvent `censorship <https://ooni.torproject.org>`__ by
providing users with connections to the public relays in the Tor
network.

Tor Bridges are different from normal relays in another important way:
they can run what are called *Pluggable* *Transports*.

-----------------------------
What's a Pluggable Transport?
-----------------------------

A `Pluggable
Transport <https://www.torproject.org/docs/pluggable-transports.html.en>`__
is a program which is *pluggable* — meaning that it is meant to work
with lots of other anonymity and censorship circumvention software, not
just Tor — and is a *transport* — meaning that it transports your
internet traffic, usually in a way which makes it look different. For
example,
`Obfsproxy <https://www.torproject.org/projects/obfsproxy.html.en>`__ is
a Pluggable Transport which disguises your traffic by adding an
obfuscating layer of encryption.

---------------------
So how do I use this?
---------------------

Well, probably, you don't. But if you're looking for bridges, you can
use `the web interface <https://bridges.torproject.org>`__ of the
BridgeDB instance deployed by the Tor Project, which has instructions on
getting the Pluggable Transports-capable Tor Browser Bundle, as well as
instructions for getting extra Bridges.


================
Maintainer Setup
================

If you'd like to hack on BridgeDB, you might wish to read BridgeDB's
`developer documentation <https://pythonhosted.org/bridgedb/>`__.  The rest of
this document mainly concerns mainenance and installation instructions.

-----------------------------
Dependencies and installation
-----------------------------

BridgeDB requires the following OS-level dependencies:

-  python>=3
-  python3-dev
-  `python3-dkim <https://pypi.org/project/dkimpy/>`__ (it contains the ``dkimverify`` binary)
-  build-essential
-  OpenSSL>=1.0.1g
-  `SQLite3 <http://www.maxmind.com/app/python>`__
-  `MaxMind GeoIP <https://www.maxmind.com/en/geolocation_landing>`__
-  libgeoip-dev
-  geoip-database
-  `python-setuptools <https://pypi.python.org/pypi/setuptools>`__
-  libjpeg-dev
-  `flog <https://packages.debian.org/jessie/flog>`__ (only required if bridgedb
   is invocated with the ``run-bridgedb`` `script
   <https://gitweb.torproject.org/project/bridges/bridgedb-admin.git/tree/bin/run-bridgedb>`__)

As well as any Python dependencies in the ``requirements.txt`` file.

.. note: There are additional dependencies for things like running the test
    suites, building BridgeDB's developer documentation, etc. Read on for more
    info if you wish to enable addition features.


------------------
Deploying BridgeDB
------------------

BridgeDB should work with or without a Python virtualenv.

-  Install Python 3, and other OS-level dependencies. On Debian, you
   can do::

         sudo apt-get install build-essential openssl python3 python3-dev \
           python3-setuptools sqlite3 gnupg2 libgeoip-dev geoip-database


-  Install Pip 1.3.1 or later. Debian has this version, but if for some
   reason that or a newer version isn't available, the easiest way to
   install a newer Pip is to use the Pip development teams's `getpip
   script <https://raw.github.com/pypa/pip/master/contrib/get-pip.py>`__::

         wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
         sudo python get-pip.py


-  **(virtualenv installs only)** Use Pip to install virtualenv and
   `virtualenvwrapper <https://virtualenvwrapper.readthedocs.org>`__::

         sudo pip install --upgrade virtualenv virtualenvwrapper


-  **(virtualenv installs only)** Configure virtualenvwrapper and create a
   virtualenv for BridgeDB::

         WORKON_HOME=${HOME}/.virtualenvs
         export WORKON_HOME
         mkdir -p $WORKON_HOME
         source $(which virtualenvwrapper.sh)
         git clone https://git.torproject.org/bridgedb.git && cd bridgedb
         mkvirtualenv -a $PWD -r requirements.txt --unzip-setuptools --setuptools bridgedb

   From now on, to use BridgeDB's virtualenv, just do ``$ workon bridgedb``
   (after sourcing virtualenvwrapper.sh, as before). To exit the virtualenv
   without exiting the shell, do ``$ deactivate``.


-  **(virtualenv installs only)** To install, set PYTHONPATH to include the
   root directory of the virtualenv::

         export PYTHONPATH=$PYTHONPATH:${VIRTUAL_ENV}/lib/python3.7/site-packages


-  Then, proceed as usual::

         python setup.py install --record installed-files.txt


============================
Enabling additional features
============================

------------
Translations
------------

For general information on the translation process, take a look at
`our translation guidelines for developers
<https://trac.torproject.org/projects/tor/wiki/doc/translation/developers>`__.

**Using New Translations**:

This should be done when newly completed translations are available in
Transifex.

Piece of cake. Running ``maint/get-completed-translations`` will take
care of cloning *only* the ``bridgedb_completed`` branch of Tor's
`translations repo <https://gitweb.torproject.org/translation.git>`__
and placing all the updated files in their correct locations.

-------

**Requesting Translations for Altered/Added Source Code**:

This should be done whenever any of the strings requiring translation --
``_("the ones inside the weird underscore function, like this")`` -- are
changed, or new ones are added. See ``lib/bridgedb/strings.py``.

Translations for Tor Project repos are kept `in a separate repo
<https://gitweb.torproject.org/translation.git>`__. To request new or updated
translations, you'll need to extract the strings from BridgeDB's source code
into our ./i18n/templates/bridgedb.pot template, and then commit it to our
``develop`` branch.  From there, the translation system takes over and
eventually, new translations will be available.  To extract all strings from
BridgeDB's source, run::

         python setup.py extract_messages

Transifex uses the resulting file ./i18n/templates/bridgedb.pot (and this file
only) as input and fetches it from BridgeDB's ``develop`` branch, so we don't
need to release a new BridgeDB version (which we only do in the ``master``
branch) to request translations.

-------

--------------
Enabling HTTPS
--------------

Create a self-signed certificate with::

         scripts/make-ssl-cert

Or, place an existing certificate in the path specified in bridgedb.conf
by the ``HTTPS_CERT_FILE`` option, and a private key where
``HTTPS_KEY_FILE`` points to. The defaults are 'cert' and 'privkey.pem',
respectively.


------------------------
Enabling CAPTCHA Support
------------------------

BridgeDB has two ways to use CAPTCHAs on webpages. The first uses reCaptcha_,
an external Google service (this requires an account with them), which
BridgeDB fetches the CAPTCHAs images from for each incoming request from a
client. The second method uses a local cache of pre-made CAPTCHAs, created by
scripting Gimp using gimp-captcha_. The latter cannot easily be run on
headless server, unfortunately, because Gimp requires an X server to be
installed.

.. _reCaptcha: https://www.google.com/recaptcha
.. _gimp-captcha: https://github.com/isislovecruft/gimp-captcha


**reCaptcha**

To enable fetching CAPTCHAs from the reCaptcha API server, set these
options in bridgedb.conf::

      RECAPTCHA_ENABLED
      RECAPTCHA_PUB_KEY
      RECAPTCHA_SEC_KEY

-------

**gimp-captcha**

To enable using a local cache of CAPTCHAs, set the following options::

      GIMP_CAPTCHA_ENABLED
      GIMP_CAPTCHA_DIR
      GIMP_CAPTCHA_HMAC_KEYFILE
      GIMP_CAPTCHA_RSA_KEYFILE

-------


----------------------------------------------------------
Preventing already-blocked bridges from being distributed:
----------------------------------------------------------

Uncomment or add ``COUNTRY_BLOCK_FILE`` to your bridgedb.conf. This file
should contain one bridge entry per line, in the format::

      fingerprint <bridge fingerprint> country-code <country code>

If the ``COUNTRY_BLOCK_FILE`` file is present, bridgedb will filter
blocked bridges from the responses it gives to clients requesting
bridges.


================
Testing BridgeDB
================

Before running to any of BridgeDB's test suites, make sure you have the
additional dependencies in the Pip requirements file,
``.test.requirements.txt`` installed::

      pip install -r .test.requirements.txt

To create a bunch of fake bridge descriptors to test BridgeDB, do::

      bridgedb mock [-n NUMBER_OF_DESCRIPTORS]

To run the test suites, do::

      make coverage

If you just want to run the tests, and don't care about code coverage
statistics, see the ``bridgedb trial`` and ``bridgedb test`` commands.


================
Running BridgeDB
================

To run BridgeDB, simply make any necessary changes to bridgedb.conf, and do::

      bridgedb

And remember that all files/directories in ``bridgedb.conf`` are assumed
relative to the runtime directory. By default, BridgeDB uses the current
working directory; you can, however specify an a different runtime
directory::

      bridgedb -r /srv/bridges.torproject.org/run

Make sure that the files and directories referred to in bridgedb.conf
exist. However, many of them, if not found, will be touched on disk so
that attempts to read/write from/to them will not raise excessive
errors.


----------------------------------------------
Reloading Bridges From Their Descriptor Files:
----------------------------------------------

When you have new lists of bridges from the Bridge Authority, replace
the old files and do::

      kill -s SIGHUP `cat .../run/bridgedb.pid`


=========================
Using a BridgeDB Instance
=========================

Obviously, you'll have to feed it bridge descriptor files from a
BridgeAuthority. There's currently only one BridgeAuthority in the entire
world, but Tor Project is, of course, very interested in adding support for
multiple BridgeAuthorities so that we can scale our own network, and make it
easier for individual and organisations who wish to run a lot of Tor bridge
relays have an easier time distributing those bridges themselves (if they wish
to do so). If you'd like to fund our work on this, please contact
tor-dev@lists.torproject.org!

----------------------------------
Accessing the HTTPS User Interface
----------------------------------

Just connect to the appropriate port. (See the ``HTTPS_PORT`` and
``HTTP_UNENCRYPTED_PORT`` options in the ``bridgedb.conf`` file.)

The HTTPS interface for our BridgeDB instance can be found `here
<https://bridges.torproject.org>`__.


----------------------------------
Accessing the Email User Interface
----------------------------------

Any mail sent to the ``EMAIL_PORT`` with a destination username as defined by
the ``EMAIL_USERNAME`` configuration option (the default is ``'bridge'``, e.g.
bridges@...) and sent from an ``@riseup.net`` or ``@gmail.com`` address (by
default, but configurable with the ``EMAIL_DOMAINS`` option).

You can email our BridgeDB instance `here <mailto:bridges@torproject.org>`__.


----------------------------
Accessing the Moat Interface
----------------------------

Moat is a bridge distributor for requesting bridges through `Tor Launcher's
<https://gitweb.torproject.org/tor-launcher.git/>`__ user interface.

The following describes the Moat API, version 0.1.0.

The client and server both MUST conform to `JSON-API <http://jsonapi.org/>`__.

The client SHOULD direct all requests via the Meek reflector at ``MEEK_REFECTOR``.
..
   XXX meek reflector URL

Requesting Bridges
""""""""""""""""""

The client MUST send a ``POST /moat/fetch`` containing the following JSON::

    {
      "data": [{
        "version": "0.1.0",
        "type": "client-transports",
        "supported": [ "TRANSPORT", "TRANSPORT", ... ],
      }]
    }

where:

* ``TRANSPORT`` is a string identifying a transport, e.g. ``"obfs3"`` or
  ``"obfs4"``.  Currently supported transport identifiers are:
  - ``"vanilla"``
  - ``"fte"``
  - ``"obfs3"``
  - ``"obfs4"``
  - ``"scramblesuit"``


Receiving a CAPTCHA challenge
"""""""""""""""""""""""""""""

The moat server will respond with ``200 OK``.

If there is an overlap with what BridgeDB supports, the moat server will select
the "best" transport from the list of supported transports, and respond with the
following JSON containing a CAPTCHA challenge::

    {
      "data": [{
        "id": "1",
        "type": "moat-challenge",
        "version": "0.1.0",
        "transport": "TRANSPORT",
        "image": "CAPTCHA",
        "challenge": "CHALLENGE",
      }]
    }

where:

* ``TRANSPORT`` is the agreed upon transport which will be distributed,
* ``CAPTCHA`` is a base64-encoded, jpeg image that is 400 pixels in
  length and 125 pixels in height,
* ``CHALLENGE`` is a base64-encoded CAPTCHA challenge which MUST be
  later passed back to the server along with the proposed solution.

The challenge contains an encrypted-then-HMACed timestamp, and
solutions submitted more than 30 minutes after requesting the CAPTCHA
are considered invalid.

If there is no overlap with the transports which BridgeDB supports, the moat
server will respond with the list of transports which is *does* support::

    {
      "data": [{
        "id": "1",
        "type": "moat-challenge",
        "version": "0.1.0",
        "transport": [ "TRANSPORT", "TRANSPORT", ... ],
        "image": "CAPTCHA",
        "challenge": "CHALLENGE",
      }]
    }


Responding to a CAPTCHA challenge
"""""""""""""""""""""""""""""""""

To propose a solution to a CAPTCHA, the client MUST send a request for ``POST
/moat/check``, where the body of the request contains the following JSON::

    {
      "data": [{
        "id": "2",
        "type": "moat-solution",
        "version": "0.1.0",
        "transport": "TRANSPORT",
        "challenge": "CHALLENGE",
        "solution": "SOLUTION",
        "qrcode": "BOOLEAN",
      }]
    }


where:

* ``TRANSPORT`` is the agreed upon transport which will be distributed,
* ``CHALLENGE`` is a base64-encoded CAPTCHA challenge which MUST be
  later passed back to the server along with the proposed solution.
* ``SOLUTION`` is a valid unicode string, up to 20 bytes in length,
  containing the client's answer (i.e. what characters the CAPTCHA
  image displayed).  The solution is *not* case-sensitive.
* ``BOOLEAN`` is ``"true"`` if the client wants a qrcode containing the bridge
  lines to be generated and returned; ``"false"`` otherwise.


Receiving Bridges
"""""""""""""""""

If the ``CHALLENGE`` has already timed out, or if the ``SOLUTION`` was
incorrect, the server SHOULD respond with ``419 No You're A Teapot``.

If the ``SOLUTION`` was successful for the supplied ``CHALLENGE``, the
server responds ``200 OK`` with the following JSON::

    {
      "data": [{
        "id": "3",
        "type": "moat-bridges",
        "version": "0.1.0",
        "bridges": [ "BRIDGE_LINE", ... ],
        "qrcode": "QRCODE",
      }]
    }

where:

* ``BRIDGE_LINE`` is a bridge line suitable for configuration in a torrc,
* ``QRCODE`` is a base64-encoded jpeg image of a QRCode containing all the
  ``BRIDGE_LINE``, if one was requested, otherwise this field will be ``NaN``.

..
    XXX do we care to differentiate the errors for "unable to distribute
        bridges"? are any of these useful to Tor Launcher?

If the ``SOLUTION`` was successful for the supplied ``CHALLENGE``, but the
server is unable to distribute the requested Bridges, the server responds ``200
OK`` with the following JSON::

    {
      "errors": [{
        "id": "6",
        "type": "moat-bridges",
        "version": "0.1.0",
        "code": "404",
        "status": "Not Found",
        "detail": "DETAILS",
      }]
    }

where:

* ``DETAILS`` is some string describing the detailed nature of the issue.


Other Responses
"""""""""""""""

If the client requested some page other than ``/moat/fetch``, or
``/moat/check``, the server MUST respond with ``501 Not Implemented``.

If the client attempts any other HTTP method, other than ``POST``, the server
MUST respond ``403 FORBIDDEN``.


=================
Contact & Support
=================

Send your questions, patches, and suggestions to
`the tor-dev mailing list <mailto:tor-dev@lists.torproject.org>`__, or to
`Philipp Winter <mailto:phw@torproject.org>`__.
