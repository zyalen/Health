#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode

from util import utils
from util import GB
from db import db

class Regist_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    user_id = db.add_account(params)
    resp = {}
    if user_id > 0:
      resp[GB.STATUS] = GB.OK
      resp[GB.ACCOUNT] = params[GB.ACCOUNT]
      resp[GB.ID] = user_id
      resp[GB.SALT] = db.get_salt(params)
    else:
      resp[GB.STATUS] = GB.ERROR

    self.write(json_encode(resp))