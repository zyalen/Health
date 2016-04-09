#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode

from util import utils
from util import GB
from db import db

class Get_Health_Report_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    resp = {}
    event_info = db.get_health_information(params)
    if event_info is None:
      resp[GB.STATUS] = GB.ERROR
    else:
      resp.update(event_info)
      resp[GB.STATUS] = GB.OK

    self.write(json_encode(resp))