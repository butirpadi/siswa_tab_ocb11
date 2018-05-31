# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pprint import pprint
from datetime import datetime, date


class siswa(models.Model):
    _inherit = 'res.partner'

    tabungan_ids = fields.One2many('siswa_tab_ocb11.tabungan',inverse_name='siswa_id', string="Tabungan")
    saldo_tabungan = fields.Float('Saldo Tabungan', default=0)

    