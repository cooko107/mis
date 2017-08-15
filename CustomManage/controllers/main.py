# -*- coding: utf-8 -*-
import logging
import werkzeug

from openerp import SUPERUSER_ID
from openerp import http
from openerp import tools
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug

PPG = 20 # Products Per Page
PPR = 4  # Products Per Row

_logger = logging.getLogger(__name__)



class website_news(http.Controller):

	@http.route(['/page/test'],type='http', auth="public", website=True)
	def send_info(self, **post):
		values={'tt':'xx'}
		return request.website.render("website.test", values)