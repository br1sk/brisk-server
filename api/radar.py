import cookielib
import json
import mechanize
import sys
import time
import urllib
import urllib2

from copy import copy
from BeautifulSoup import BeautifulSoup
from MultipartPostHandler import MultipartPostHandler

IOS_ID = 1
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) " +\
             "Gecko/20100101 Firefox/47.0"
ITUNES_CONNECT_ID = 12
APPID_KEY = "77e2a60d4bdfa6b7311c854a56505800be3c24e3a27a670098ff61b69fc5214b"

URLS = {
    "main": "https://bugreport.apple.com/problem/viewproblem",
    "login": "https://idmsa.apple.com/IDMSWebAuth/login.html" +
             "?appIdKey={appid_key}&sslEnabled=true&rv=3",
    "keepalive": "/developer/problem/keepAliveSession?_={ts}",
    "draft": "/developer/problem/fetchDraftInfo?_={ts}",
    "list": "/developer/problem/getProductFullList?_={ts}",
    "counts": "/developer/problem/getAllCounts?_={ts}",
    "sections": "/developer/problem/getSectionProblems",
    "create": "/developer/problem/createNewDevUIProblem"
}


class LoginError(Exception):
    pass


class SessionError(Exception):
    pass


class Radar:

    def __init__(self, classification, product, reproducibility, title,
                 description, steps, expected, actual, configuration, version,
                 notes, area=None, application_id=None, user_id=None):
        self.classification = classification
        self.product = product
        self.reproducibility = reproducibility
        self.title = title
        self.description = description
        self.steps = steps
        self.expected = expected
        self.actual = actual
        self.configuration = configuration
        self.version = version
        self.notes = notes
        self.area = area
        self.application_id = application_id
        self.user_id = user_id

    @property
    def json(self):
        templates = {
            ITUNES_CONNECT_ID: [
                ("Apple ID of the App", self.application_id),
                ("Apple ID of the User", self.user_id)
            ],
            IOS_ID: [
                ("Area", self.area.name if self.area else ""),
            ],
            None: [
                ("Summary", self.description),
                ("Steps to Reproduce", self.steps),
                ("Expected Results", self.expected),
                ("Actual Results", self.actual),
                ("Version", self.version),
                ("Notes", self.notes),
            ]
        }

        values = templates[None] + templates.get(self.product.pk, [])
        description = "\r\n\r\n".join("%s:\r\n%s" % kv for kv in values)

        return {
            "problemTitle": self.title,
            "configIDPop": "",
            "configTitlePop": "",
            "configDescriptionPop": "",
            "configurationText": self.configuration,
            "notes": self.notes,
            "configurationSplit": "Configuration:\r\n",
            "configurationSplitValue": self.configuration,
            "workAroundText": "",
            "descriptionText": description,
            "problemAreaTypeCode": self.area.apple_id if self.area else "",
            "classificationCode": self.classification.apple_id,
            "reproducibilityCode": self.reproducibility.apple_id,
            "component": {
                "ID": self.product.apple_id,
                "compName": self.product.name,
            },
            "draftID": "",
            "draftFlag": "0",
            "versionBuild": self.version,
            "desctextvalidate": description,
            "stepstoreprvalidate": self.steps,
            "experesultsvalidate": self.expected,
            "actresultsvalidate": self.actual,
            "addnotesvalidate": self.notes,
            "hiddenFileSizeNew": "",  # v2
            "attachmentsValue": "\r\n\r\nAttachments:\r\n",
            "configurationFileCheck": "",  # v2
            "configurationFileFinal": "",  # v2
        }


class BugReporter:

    def __init__(self):
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        self.browser.addheaders = [('User-Agent', USER_AGENT)]

    @property
    def cookies(self):
        """
        Returns all the cookies matching the domain of the main radar's page.
        """
        jar = self.browser._ua_handlers['_cookies'].cookiejar
        request = urllib2.Request(URLS['main'])
        cookies = jar._cookies_for_request(request)
        items = map(lambda x: "%s=%s" % (x.name, x.value), cookies)
        return "; ".join(items)

    def login_cookie(self, cookie):
        """
        Login into radar by using a full cookie string.

        - parameter cookie: A set of cookies joined by `;`.
        """
        cookies = cookielib.parse_ns_headers(cookie.split("; "))
        jar = self.browser._ua_handlers['_cookies'].cookiejar

        parts = urllib2.urlparse.urlparse(URLS['main'])
        request = urllib2.Request("https://%s" % parts.hostname)

        jar._policy._now = jar._now = int(time.time())
        for cookie in jar._cookies_from_attrs_set(cookies, request):
            jar.set_cookie(cookie)

    def login(self, username, password):
        """
        Login into radar by an apple_id and password.

        - parameter username: Username to be used on `bugreport.apple.com`
                              authentication.
        - parameter password: Password to be used on `bugreport.apple.com`
                              authentication.

        - returns: The cookies generated by the server for the
                   authenticated user
        """
        self.browser.open(URLS["login"].format(appid_key=APPID_KEY))
        self.browser.select_form(name="form2")
        self.browser["appleId"] = username
        self.browser["accountPassword"] = password

        result = self.browser.submit()
        soup = BeautifulSoup(result.read())
        span = soup.find("span", {"class": "dserror"})
        if span:
            raise LoginError(span.text)

        self._add_offset_cookie()
        return self.cookies

    def create_radar(self, radar):
        """
        Creates a new ticket into apple's radar. `BugTracker` should be
        authenticated before calling this method.o

        - parameter radar: The radar model with the information for the ticket.

        - returns: The radar ID from apple's radar.
        """
        if not self.browser._response or URLS["main"] != self.browser.geturl():
            self.browser.open(URLS["main"])

        # Remove floating OPTIONs from HTML
        soup = BeautifulSoup(self.browser.response().read())
        csrf_input = soup.find("input", {"id": "csrftokenPage"})
        if not csrf_input:
            raise SessionError("Session timed out")

        # Get CSRF token from HTML
        data = radar.json
        data["csrftokencheck"] = csrf_input["value"]

        self._send_keep_alive(data["csrftokencheck"])

        # MIME encode the POST payload
        url = urllib2.urlparse.urljoin(self.browser.geturl(), URLS["create"])
        boundary, data = MultipartPostHandler.multipart_encode(
            [("hJsonScreenVal", json.dumps(data))], [])

        headers = self.browser.addheaders + [
            ("Referer", URLS["main"]),
            ("Cookie", self.cookies),
            ("Content-Type", "multipart/form-data; boundary=%s" % boundary),
        ]

        request = urllib2.Request(url, data.strip(), headers=dict(headers))

        try:
            response = urllib2.urlopen(request)
            return int(response.read())
        except ValueError:
            raise SessionError("Invalid Radar ID")

        except urllib2.URLError, e:
            raise SessionError(str(e))

    def _add_offset_cookie(self):
        jar = self.browser._ua_handlers['_cookies'].cookiejar
        offset_cookie = copy(jar[0])
        offset_cookie.name = "clientTimeOffsetCookie"
        offset_cookie.value = "-25200000"
        jar.set_cookie(offset_cookie)

    def _send_keep_alive(self, csrf):
        ts = int(time.time() * 100)

        headers = self.browser.addheaders + [
            ("X-Requested-With", "XMLHttpRequest"),
            ("Cookie", self.cookies),
            ("Accept", "application/json, text/javascript, */*; q=0.01"),
            ("csrftokencheck", csrf),
        ]

        url = urllib2.urlparse.urljoin(self.browser.geturl(),
                                       URLS["list"].format(ts=ts))
        request = urllib2.Request(url, headers=dict(headers))
        urllib2.urlopen(request)
