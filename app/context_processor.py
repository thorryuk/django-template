def media_url(request):
    cms_url = "http://cms-pln"
    return {'media_url':cms_url}

def frontend_url(request):
    fe = "http://frontend-pln/"
    return {'frontend_url': fe}

def backend_url(request):
    cms = "http://cms-pln/"
    return {'backend_url': cms}