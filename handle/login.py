#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode

from util import utils
from util import GB
from db import db

class Login_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    
    resp = {}
    if GB.SALT not in params:
      salt = db.get_salt(params)
      if salt is None:
        resp[GB.STATUS] = GB.ERROR
      else:
        resp[GB.ACCOUNT] = params[GB.ACCOUNT]
        resp[GB.STATUS] = GB.OK
        resp[GB.SALT] = salt
    
    else:
      user_id = db.validate_password(params)
      if user_id > 0:
        resp[GB.STATUS] = GB.OK
        resp[GB.ACCOUNT] = params[GB.ACCOUNT]
        resp[GB.ID] = user_id
      else:
        resp[GB.STATUS] = GB.ERROR
    
    self.write(json_encode(resp))