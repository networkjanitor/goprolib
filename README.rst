========
goprolib
========

This is a python3 library to interact with wifi-connected gopro cameras.

Currently supported are the following camera models:

    - HERO4 Silver
    - HERO4 Black
    - HERO4 Session

READ ALL ABOUT THE API HERE: https://github.com/KonradIT/goprowifihack

Project Setup
=============

======================================= ============================================
                File                                    Description
======================================= ============================================
.
├── gopro-control.py                    empty
├── goprolib
│   ├── api_dump                        dump of all available API calls/values
│   └── HERO4                           HERO4 specifc API implementation
│       ├── commands.py                 ENUM: commands (non-setting api)
│       ├── exceptions.py               custom exception/errors
│       ├── fisheye.py                  ENUM: lens correction values
│       ├── HERO4.py                    class to interact with a HERO4 camera
│       ├── __init__.py                 empty
│       ├── scripts
│       │   ├── __init__.py             empty
│       │   └── stream-udp-keepalive.py script to keep livestream alive
│       ├── settings.py                 ENUM: settings api (key/values/names)
│       └── status.py                   ENUM: status api (key/values/names)
├── research
│   └── undocumented settings values
├── scripts
│   ├── infinitetimelapse.py            run timelapse forever (or util battery dies)
│   └── stop_capture.py                 stop capturing
├── setup.py                            pypi setup
└── tests                               empty
======================================= ============================================