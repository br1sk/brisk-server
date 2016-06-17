Login
=====

Request
-------

```json
POST /token HTTP/1.1
Host: api.radar.com
Content-Type: application/json

{
    "appleid": "fz",
    "password": "app1e"
}
```

Response
--------

```json
{
    "authentication_token": "cacacacacacacacaca",
    "expiration": "2016-06-21T00:00:00+00:00",
    "error": "",
    "status": "success|failure"
}
```

New radar
=========

Request
-------

```json
POST /radar HTTP/1.1
Host: api.radar.com
Authorize: "authentication_token=cacacacacacacacaca"
Content-Type: application/json

{
    "product": "ios",
    "classification": "seriousbug",
    "reproducibility": "always",
    "area": "uikit",
    "title": "UIKit is broken",
    "description": "Everything is broken when using iOS",
    "steps": "1. Hold your phone\n2. Unlock it",
    "expected": "Everything should not be broken",
    "actual": "Stuff is broken",
    "configuration": "Every version of iOS",
    "version": "iPhone 2+",
    "notes": "Did I mention everything is broken?"
}
```

 - *product*: Select a product from the list below.
 - *classification*: The type of problem (see below for available options).
 - *reproducibility*: How often the problem occurs (see below for available 
   options).
 - *title*: A short but descriptive sentence that summarizes the issue.
 - *description*: A detailed description about the issue and include specific 
   details to help the engineering team understand the problem.
 - *steps*: The step by step process to reproduce the issue.
 - *expected*: What you expected to see.
 - *actual*: What you actually saw.
 - *configuration*: The circumstances where this does or does not occur.
 - *version*: Product version and build number.
 - *notes*: Any other relevant notes not previously mentioned.

Types
=====

Request
-------

```json
GET /types HTTP/1.1
Host: api.radar.com
```

Response
--------

```json
{
    "products": [{"id": "ios"}],
    "classification": [],
    "reproducibility": [],
    "area": []
}
```

## Products

### OS and development

 - ios
 - iossdk
 - macos
 - macossdk
 - macosserver
 - tvos
 - tvossdk
 - watchos
 - watchossdk
 - tools
 - documentation
 - itunesconnect
 - parallaxpreviewer
 - samplecode
 - technote

### Applications and software

 - ibooks
 - icloud
 - ilife
 - itunes
 - iwork
 - mail
 - proapps
 - quicktime
 - safari
 - safaripreview
 - siri
 - swiftplaygrounds

### Hardware

 - appletv
 - ipad
 - iphone
 - ipod
 - mac
 - printing
 - otherhardware
 - carplayaccessory
 - homekitaccessory

### Other

 - accessibility
 - appstore
 - macappstore
 - bugreporter
 - iad
 - iadproducer
 - java
 - other

## Classification

 - security
 - crash
 - power
 - peformance
 - uiux
 - seriousbug
 - otherbug
 - newfeature
 - enhancement

## Reproducibility

 - always
 - sometimes
 - rarely
 - unable
 - didnttry
 - notapplicable

## Area

 - accessibility
 - apns
 - appswitcher
 - avfoundation
 - battery
 - bluetooth
 - calendar
 - carplay
 - cellular
 - cloudkit
 - contacts
 - controlcenter
 - corelocation
 - devicemanagement
 - facetime
 - gamekit
 - healthkit
 - homekit
 - ipodaccessory
 - itunesconnect
 - itunesstore
 - keyboard
 - lockscreen
 - mail
 - mapkit
 - messages
 - metal
 - music
 - nightshift
 - notes
 - notificationcenter
 - nsurl
 - phoneapp
 - photos
 - reminders
 - safariservices
 - scenekit
 - setupassistant
 - softwareupdate
 - spotlight
 - springboard
 - spritekit
 - storekit
 - systemunresposive
 - touchid
 - uikit
 - vpn
 - webkit
 - wifi
 - xcode
 - other

Response
--------

```json
{
    "radar_id": "123447",
    "error": "",
    "status": "success|failure"
}
```
