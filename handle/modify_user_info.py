#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode

from util import utils
from util import GB
from db import db

class Modify_User_Information_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    result = db.update_user(params)
    resp = {}
    if result:
      resp[GB.STATUS] = GB.OK
      resp[GB.ID] = params[GB.ID]
    else:
      resp[GB.STATUS] = GB.ERROR

    self.write(json_encode(resp))