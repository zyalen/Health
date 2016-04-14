#!/usr/python

import tornado
import tornado.httpserver
import tornado.options
import tornado.web
import tornado.ioloop
import os
import sys


from handle import add_health
from handle import get_health_report
from handle import get_health_list
from handle import get_item_list
from handle import get_recommand
from handle import get_user_info
from handle import login
from handle import modify_password
from handle import modify_user_info
from handle import regist
from handle import remove_health

os.chdir(os.path.join(os.getcwd(), os.path.dirname(sys.argv[0])))

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

def main():
  port = 1501
  application = tornado.web.Application(
    handlers=[
      (r"/", IndexHandler),
      (r"/add_health", add_health.Add_Health_Handler),
      (r"/get_health_report", get_health_report.Get_Health_Report_Handler),
      (r"/get_health_list", get_health_list.Get_Health_List_Handler),
      (r"/get_item_list", get_item_list.Get_Item_List_Handler),
      (r"/get_recommand", get_recommand.Get_Recommand_Handler),
      (r"/get_user_info", get_user_info.Get_User_Information_Handler),
      (r"/login", login.Login_Handler),
      (r"/modify_password", modify_password.Modify_Password_Handler),
      (r"/modify_user_info", modify_user_info.Modify_User_Information_Handler),
      (r"/regist", regist.Regist_Handler),
      (r"/remove_health", remove_health.Remove_Health_Handler),
      (r"/(.*)", tornado.web.StaticFileHandler, {"path": "static"})
    ], debug=True)
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(port)

  tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()