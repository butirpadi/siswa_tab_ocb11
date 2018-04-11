# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pprint import pprint
from datetime import datetime, date


class tabungan(models.Model):
    _name = 'siswa_tab_ocb11.tabungan'

    name = fields.Char(string='Kode Pembayaran', requred=True, default='New')
    state = fields.Selection([('draft', 'Draft'), ('post', 'Posted')], string='State', required=True, default='draft')
    siswa_id = fields.Many2one('res.partner',string="Siswa", required=True)
    induk = fields.Char(string='Induk', related='siswa_id.induk')
    active_rombel_id = fields.Many2one('siswa_ocb11.rombel', related='siswa_id.active_rombel_id', string='Rombongan Belajar')
    tanggal = fields.Date(string='Tanggal', required=True, default=datetime.today())
    jumlah = fields.Float(string='Jumlah', required=True)
    jenis = fields.Selection([('setor', 'Setoran'), ('tarik', 'Tarik Tunai')], string='Jenis', required=True, default='setor')
    confirm_ids = fields.One2many('siswa_tab_ocb11.action_confirm', inverse_name="tabungan_id")

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = 'DRAFT/TAB/'+str(datetime.today().strftime('%d%m%y/%H%M%S'))
            # if 'company_id' in vals:
            #     vals['name'] = 'DRAFT-' + self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('tabungan.siswa.tab.ocb11') or _('New')
            # else:
            #     vals['name'] = 'DRAFT-' self.env['ir.sequence'].next_by_code('tabungan.siswa.tab.ocb11') or _('New')
        if vals['jenis'] == 'tarik' :
            vals['jumlah'] = -vals['jumlah']
        result = super(tabungan, self).create(vals)
        return result
    
    @api.multi
    def write(self, values):
        self.ensure_one()
        if 'jumlah' in values:
            if 'jenis' in values:
                if values['jenis'] == 'tarik':
                    values['jumlah'] = -values['jumlah']
            else:
                if self.jenis == 'tarik':
                    values['jumlah'] = -values['jumlah']
        else:
            if self.jenis == 'tarik':
                values['jumlah'] = -self.jumlah

        result = super(tabungan, self).write(values)
        self.update_saldo_siswa()
        return result
    
    def update_saldo_siswa(self):
        self.ensure_one()
        # update saldo siswa
        tabs = self.env['siswa_tab_ocb11.tabungan'].search([('siswa_id','=',self.siswa_id.id), ('state','=','post')])
        self.env['res.partner'].search([('id','=',self.siswa_id.id)]).write({
            'saldo_tabungan' : sum(x.jumlah for x in tabs )
        })

    def action_confirm(self):
        self.ensure_one()
        # generate code
        name_seq = self.env['ir.sequence'].next_by_code('tabungan.siswa.tab.ocb11') or _('New')        
        # update name to database
        self.write({
            'name' : name_seq,
            'state' : 'post'
        })
        self.confirm_ids = (0,0,{
            'name' : name_seq
        })
        self.update_saldo_siswa()
    
    def action_cancel(self):
        self.ensure_one()
        # delete confirm_ids
        self.confirm_ids.unlink()
        # update name to database
        self.write({
            'name' : 'DRAFT/'+self.name,
            'state' : 'draft'
        })

    