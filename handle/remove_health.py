#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode

from util import utils
from util import GB
from db import db

class Remove_Health_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    
    resp = {}
    result = db.remove_health(params)
    if GB.HEALTH_ID in params:
      resp[GB.HEALTH_ID] = params[GB.HEALTH_ID]
    if result:
      resp[GB.STATUS] = GB.OK
    else:
      resp[GB.STATUS] = GB.ERROR
    
    self.write(json_encode(resp))