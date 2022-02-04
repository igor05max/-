def spn_(json_response):
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    t = list(map(float, toponym["boundedBy"]["Envelope"]["lowerCorner"].split()))
    t2 = list(map(float, toponym["boundedBy"]["Envelope"]["upperCorner"].split()))
    return t, t2
