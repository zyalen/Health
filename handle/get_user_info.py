#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode

from util import utils
from util import GB
from db import db

class Get_User_Information_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    resp = {}
    user_info = db.get_user_information(params)
    if user_info is None:
      resp[GB.STATUS] = GB.ERROR
    resp[GB.STATUS] = GB.OK
    
    self.write(json_encode(resp))