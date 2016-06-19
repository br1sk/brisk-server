import urllib2

from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from authentication import token_auth, authenticate
from models import Product, Classification, Reproducibility, Area
from radar import Radar, BugReporter

FAILURE_STATUS = "failure"
SUCCESS_STATUS = "success"


@cache_page(60 * 60 * 1)
def types(request):
    """
    Returns all the type display names along with identifier to be used when
    creating a radar.
    """
    data = {
        "products": list(
            Product.objects.values("identifier", "name", "category")
        ),
        "classifications": list(
            Classification.objects.values("identifier", "name")
        ),
        "reproducibilities": list(
            Reproducibility.objects.values("identifier", "name")
        ),
        "areas": list(Area.objects.values("identifier", "name")),
    }

    return JsonResponse(data)


def login(request):
    """
    Authenticates apple_id and password at `bugreport.apple.com`, Apple IDs
    or passwords will not be persisted.

    POST parameters
    ---------------

    - apple_id: Username to be used on `bugreport.apple.com` authentication
    - password: Password to be used on `bugreport.apple.com` authentication
    """
    reporter = BugReporter()
    try:
        cookie = reporter.login(request.POST["apple_id"],
                                request.POST["password"])
    except Exception, e:
        return JsonResponse({"status": FAILURE_STATUS, "error": str(e)})

    auth = authenticate(cookie)
    return JsonResponse({"status": SUCCESS_STATUS, "token": auth.token})


@token_auth
def create(request):
    """
    Creates a new ticket into apple's radar. Authentication is done via the
    `Authorization` header.

    POST parameters
    ---------------

    - product: Select a product from the list below.
    - classification: The type of problem (see below for available options).
    - reproducibility: How often the problem occurs (see below for available
      options).
    - title: A short but descriptive sentence that summarizes the issue.
    - description: A detailed description about the issue and include
      pecific details to help the engineering team understand the problem.
    - steps: The step by step process to reproduce the issue.
    - expected: What you expected to see.
    - actual: What you actually saw.
    - configuration: The circumstances where this does or does not occur.
    - version: Product version and build number.
    - notes: Any other relevant notes not previously mentioned.
    """
    post = request.POST

    try:
        product = Product.objects.get(identifier=post['product'])
    except (KeyError, Product.DoesNotExist):
        return JsonResponse({
            "status": FAILURE_STATUS,
            "error": "Invalid product id"
        })

    try:
        reproducibility = Reproducibility.objects.get(
            identifier=post['reproducibility'])
    except (KeyError, Reproducibility.DoesNotExist):
        return JsonResponse({
            "status": FAILURE_STATUS,
            "error": "Invalid reproducibility id"
        })

    try:
        classification = Classification.objects.get(
            identifier=post['classification'])
    except (KeyError, Classification.DoesNotExist):
        return JsonResponse({
            "status": FAILURE_STATUS,
            "error": "Invalid classification id"
        })

    try:
        area = Area.objects.get(identifier=post['area'])
    except KeyError:
        area = None

    except Area.DoesNotExist:
        return JsonResponse({
            "status": FAILURE_STATUS,
            "error": "Invalid area id"
        })

    try:
        radar = Radar(classification=classification, product=product,
                      reproducibility=reproducibility, title=post['title'],
                      description=post['description'], steps=post['steps'],
                      expected=post['expected'], actual=post['actual'],
                      configuration=post['configuration'],
                      version=post['version'], notes=post['notes'], area=area)
    except KeyError, key:
        return JsonResponse({
            "status": FAILURE_STATUS,
            "error": "Invalid %s field" % str(key)
        })

    reporter = BugReporter()
    reporter.login_cookie(request.authorization.cookie)
    try:
        radar_id = reporter.create_radar(radar)
    except SessionError, e:
        return JsonResponse({"status": FAILURE_STATUS, "error": str(e)})

    except urllib2.HTTPError, e:
        return JsonResponse({
            "status": FAILURE_STATUS,
            "error": "Unhandled error while connecting with Radar"
        })

    return JsonResponse({"radar_id": radar_id, "status": SUCCESS_STATUS})
