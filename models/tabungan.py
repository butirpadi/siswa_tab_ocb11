# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pprint import pprint
from datetime import datetime, date


class tabungan(models.Model):
    _name = 'siswa_tab_ocb11.tabungan'

    name = fields.Char(string='Kode Pembayaran', requred=True, default='New')
    siswa_id = fields.Many2one('res.partner',string="Siswa", required=True)
    induk = fields.Char(string='Induk', related='siswa_id.induk')
    active_rombel_id = fields.Many2one('siswa_ocb11.rombel', related='siswa_id.active_rombel_id', string='Rombongan Belajar')
    tanggal = fields.Datetime(string='Tanggal', required=True, default=datetime.today())
    jumlah = fields.Float(string='Jumlah', required=True)
    jenis = fields.Selection([('setor', 'Setoran'), ('tarik', 'Tarik Tunai')], string='Jenis', required=True, default='setor')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('tabungan.siswa.tab.ocb11') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('tabungan.siswa.tab.ocb11') or _('New')

        result = super(tabungan, self).create(vals)
        return result

    