#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode

from util import utils
from util import GB
from db import db

class Add_Health_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    resp = {}
    health_id = db.add_health(params)
    if health_id > 0:
      event_info = {}
      event_info[GB.HEALTH_ID] = health_id
      resp = db.get_health_information(event_info)
      if resp is None:
        resp = {}
      resp[GB.STATUS] = GB.OK
    else:
      resp[GB.STATUS] = GB.ERROR

    self.write(json_encode(resp))