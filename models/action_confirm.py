# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pprint import pprint
from datetime import datetime, date


class action_confirm(models.Model):
    _name = 'siswa_tab_ocb11.action_confirm'

    name = fields.Char(string='Action Name', requred=True)
    tabungan_id = fields.Many2one('siswa_tab_ocb11.tabungan', required=True, ondelete="restrict")


    