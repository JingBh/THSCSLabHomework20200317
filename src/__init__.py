import webbrowser
from threading import Thread

import tornado.ioloop
import tornado.web

from database import Database
from get_path import get_path
from handler import IndexHandler, ProgressHandler, DataHandler
from progress import Progress


def load_data():
    db = Database()
    db.truncate()
    db.load_data_source(progress=Progress())
    db.close()


def start_server():
    application = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/progress", ProgressHandler),
        (r"/data", DataHandler),
        (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": get_path("resources/js")}),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {"path": get_path("resources/css")})
    ], debug=True)
    application.listen(10317)


def start_browser():
    url = "http://localhost:10317/"
    webbrowser.open(url)
    print("若浏览器没有自动打开，请手动打开此网页：", url, sep="\n")


def run():
    Progress().clear()
    start_server()
    start_browser()
    Thread(target=load_data).start()
    tornado.ioloop.IOLoop.current().start()  # Mainloop
