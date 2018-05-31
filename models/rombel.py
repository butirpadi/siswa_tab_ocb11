# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions 
from pprint import pprint

class rombel(models.Model):
    _inherit = 'siswa_ocb11.rombel'

    @api.multi
    def write(self, vals):
        print('Inside Write on Siswa_Tab_ocb11')
        if 'is_show_on_dashboard' in vals:
            # Generate Dashboard Tabungan Per Rombel
            print('inside create dashboard tabungan')
            active_id = self.id

            if vals['is_show_on_dashboard']:
                # insert to dashboard_tabungan
                tahunajaran = self.env['siswa_ocb11.tahunajaran'].search([('name','ilike','%'),('active','ilike','%')])
                for ta in tahunajaran:
                    new_dash = self.env['siswa_tab_ocb11.dashboard_tabungan'].create({
                        'rombel_id' : active_id,
                        'tahunajaran_id' : ta.id,
                        'active' : ta.active,
                        'name' : self.name,
                        'subtitle' : ta.name,
                    })
                    new_dash.compute_saldo_tabungan()
            else:
                query = "delete from siswa_tab_ocb11_dashboard_tabungan where rombel_id =" + str(active_id)
                self.env.cr.execute(query)

        result = super(rombel, self).write(vals)        
        
        return result