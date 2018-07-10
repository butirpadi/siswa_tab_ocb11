# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pprint import pprint

class tahunajaran(models.Model):
    _inherit = 'siswa_ocb11.tahunajaran'
    
    @api.model
    def create(self, vals):
        result = super(tahunajaran, self).create(vals)

        # generate dashboard tabungan
        rombels = self.env['siswa_ocb11.rombel'].search([('name','ilike','%')])
        for rb in rombels:
            new_dash = self.env['siswa_tab_ocb11.dashboard_tabungan'].create({
                        'rombel_id' : rb.id,
                        'tahunajaran_id' : result.id,
                        'active' : False,
                        'name' : rb.name,
                        'subtitle' : result.name,
                        })
            new_dash.compute_saldo_tabungan()

        return result
    
    @api.multi
    def write(self, values):
        for rec in self:
            if 'active' in values:
                if values['active']:
                    # get default tabungan dashboard id
                    def_dash_tab_id = self.env['ir.model.data'].search([('name','=','default_dashboard_tabungan')]).res_id
                    
                    # update active tabungan rombels
                    query_disabel = 'update siswa_tab_ocb11_dashboard_tabungan set active = False where id != ' + str(def_dash_tab_id)
                    print(query_disabel)
                    self.env.cr.execute(query_disabel)
                    print('------------------------------------')
                    query_active = 'update siswa_tab_ocb11_dashboard_tabungan set active = True where tahunajaran_id = ' + str(rec.id) + ' or id = ' + str(def_dash_tab_id) 
                    print(query_active)
                    self.env.cr.execute(query_active)

        result = super(tahunajaran, self).write(values)
        return result
