#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode

from util import utils
from util import GB
from db import db

class Get_Recommand_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    items = db.get_recommand_items(params)
    resp = {}
    if items is not None:
      resp[GB.STATUS] = GB.OK
      resp[GB.ITEM_LIST] = items
    else:
      resp[GB.STATUS] = GB.ERROR

    self.write(json_encode(resp))