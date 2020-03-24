import json

from tornado.web import RequestHandler

from get_path import get_path
from progress import Progress
from database import Database


class IndexHandler(RequestHandler):

    def get(self):
        self.render(get_path("resources/index.html"))


class DataHandler(RequestHandler):

    def get(self):
        db = Database()

        # 获取请求的省份
        request_province = self.get_argument("province", None)
        # 获取所有省份
        provinces = db.select("SELECT `province` FROM `data` GROUP BY `province`")
        # 获取所有日期
        dates = db.select("SELECT `date` FROM `data` GROUP BY `date` ORDER BY `date` DESC")
        # 检查请求的省份是否存在
        province_exists = db.select(
            "SELECT COUNT(*) FROM `data` WHERE `province` = ?",
            [request_province]
        )[0][0] > 0
        if province_exists:
            # 若存在，选择所有日期数据，否则可以任意选择
            request_date = None
        else:
            request_province = None
            # 获取请求的日期
            request_date = self.get_argument("date", None)
            # 检查请求的日期是否存在
            date_exists = db.select(
                "SELECT COUNT(*) FROM `data` WHERE `date` = ?",
                [request_date]
            )[0][0] > 0
            # 若不存在选择最近一天
            if not date_exists:
                request_date = dates[0][0]

        if request_province is None:
            sql = "SELECT * FROM `data` WHERE `date` = ?"
            arguments = [request_date]
            nav = "date"
        else:
            sql = "SELECT * FROM `data` WHERE `province` = ?"
            arguments = [request_province]
            nav = "province"
        result = {
            "data": db.select(sql, arguments),
            "date": request_date,
            "dates": dates,
            "province": request_province,
            "provinces": provinces,
            "nav": nav,
            "navCol": nav + "s"
        }

        # 以 JSON 返回
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(result))


class ProgressHandler(RequestHandler):

    def get(self):
        self.set_header("Content-Type", "text/plain")
        self.set_header("Cache-control", "no-cache")
        self.set_status(200)
        self.write(str(Progress().get()))
