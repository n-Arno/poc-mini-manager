#!/usr/bin/python3

from bottle import route, run, request, redirect, auth_basic
import os

host = "0.0.0.0"
port = 8000


def auth_user(user, passw):
    return (user == os.environ['USER'] and passw == os.environ['PASS'])

def format(s):
    f = """<html>
<head>
<title>Node Status</title>
<meta http-equiv="refresh" content="10; url=/">
</head>
<body style="font-family: monospace;">
<p>Node Status (refresh every 10 seconds)</p>
%s
<button onclick="window.location='/stop';">Stop All</button> <button onclick="window.location='/start';">Start All</button>
</body>
</html>""" % s.replace(" ", "&nbsp;").replace("\n", "</br>\n")
    return f


@route("/", method="GET")
@auth_basic(auth_user)
def list():
    result = os.popen("scw instance server list name=render-node -o human=Name,State,Type,PublicIP,ImageName | sed 's/archived/stopped/g'").read() + '\n'
    param = dict(request.query.decode())
    if "status" in param:
        result += f"{param['status']}\n\n"
    return format(result)


@route("/stop", method="GET")
@auth_basic(auth_user)
def stop():
    try:
        os.popen('for i in $(scw instance server list name=render-node -o template="{{ .ID }}"); do scw instance server stop $i 2>/dev/null; done')
    except:
        pass
    redirect("/?status=Stopping nodes...")


@route("/start", method="GET")
@auth_basic(auth_user)
def start():
    try:
        os.popen('for i in $(scw instance server list name=render-node -o template="{{ .ID }}"); do scw instance server start $i 2>/dev/null; done')
    except:
        pass
    redirect("/?status=Starting nodes...")


def main():
    run(
        host=host,
        port=port,
        quiet=True,
        server="paste",
        use_threadpool=True,
        threadpool_workers=15,
        request_queue_size=5,
    )


if __name__ == "__main__":
    main()
