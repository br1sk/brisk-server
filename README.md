Login
=====

Authenticates apple_id and password at `bugreport.apple.com`, apple IDs
or passwords will not be stored.

Request
-------

```json
POST /login HTTP/1.1
Host: radar.fzed.io
Content-Type: application/json

{
    "apple_id": "fz",
    "password": "app1e"
}
```

 - **apple_id**: Username to be used on `bugreport.apple.com`
   authentication.
 - **password**: Password to be used on `bugreport.apple.com`
   authentication.

Response
--------

```json
{
    "token": "cacacacacacacacaca",
    "error": "",
    "status": "success|failure"
}
```

New radar
=========

Creates a new ticket into apple's radar. Authentication is done via the
`Authorization` header.

Request
-------

```json
POST /radar HTTP/1.1
Host: radar.fzed.io
Authorization: cacacacacacacacaca
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

 - **product**: Select a product from the list below.
 - **classification**: The type of problem (see below for available options).
 - **reproducibility**: How often the problem occurs (see below for available
   options).
 - **title**: A short but descriptive sentence that summarizes the issue.
 - **description**: A detailed description about the issue and include
   specific details to help the engineering team understand the problem.
 - **steps**: The step by step process to reproduce the issue.
 - **expected**: What you expected to see.
 - **actual**: What you actually saw.
 - **configuration**: The circumstances where this does or does not occur.
 - **version**: Product version and build number.
 - **notes**: Any other relevant notes not previously mentioned.


Response
--------

```json
{
    "radar_id": "123447",
    "error": "",
    "status": "success|failure"
}
```

Types
=====

Returns all the type display names along with identifier to be used when
creating a radar.

Request
-------

```json
GET /types HTTP/1.1
Host: radar.fzed.io
```

Response
--------

```json
{
    "products": [{"id": "ios", "name": "iOS", "category": "OS and Development"}],
    "classifications": [],
    "reproducibilities": [],
    "areas": []
}
```
