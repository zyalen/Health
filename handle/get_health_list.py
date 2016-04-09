#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode

from util import utils
from util import GB
from db import db

class Get_Health_List_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    resp = {}
    resp[GB.HEALTH_LIST] = db.get_health_list(params)
    resp[GB.STATUS] = GB.OK

    self.write(json_encode(resp))