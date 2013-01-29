from django.shortcuts import redirect, render
from django.http import HttpResponse
from tapiriik.services import Service
from tapiriik.auth import User
def authreturn(req, service):
    svc = Service.FromID(service)
    uid, authData = svc.RetrieveAuthenticationToken(req)
    serviceRecord = Service.EnsureServiceRecordWithAuth(svc, uid, authData)

    # auth by this service connection
    existingUser = User.AuthByService(serviceRecord)
    # only log us in as this different user in the case that we don't already have an account
    if req.user is None and existingUser is not None:
        User.Login(existingUser, req)
    else:
        User.Ensure(req)
    # link service to user account, possible merge happens behind the scenes (but doesn't effect active user)
    User.ConnectService(req.user, serviceRecord)
    
    return render(req, "oauth-return.html")