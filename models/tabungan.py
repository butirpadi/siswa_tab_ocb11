# -*- coding: utf-8 -*-

from flectra import models, fields, api, exceptions, _
from pprint import pprint
from datetime import datetime, date


class tabungan(models.Model):
    _name = 'siswa_tab_ocb11.tabungan'

    name = fields.Char(string='Kode Pembayaran', requred=True, default='New')
    state = fields.Selection([('draft', 'Draft'), ('post', 'Posted')], string='State', required=True, default='draft')
    siswa_id = fields.Many2one('res.partner',string="Siswa", required=True)
    induk = fields.Char(string='Induk', related='siswa_id.induk')
    saldo_tabungan = fields.Float('Saldo Tabungan', compute="_compute_get_saldo", store=True)
    active_rombel_id = fields.Many2one('siswa_ocb11.rombel', related='siswa_id.active_rombel_id', string='Rombongan Belajar')
    tanggal = fields.Date(string='Tanggal', required=True, default=datetime.today())
    jumlah = fields.Float(string='Jumlah', required=True, default=0)
    jumlah_temp = fields.Float(string='Jumlah', required=True, default=0)
    jenis = fields.Selection([('setor', 'Setoran'), ('tarik', 'Tarik Tunai')], string='Jenis', required=True, default='setor')
    confirm_ids = fields.One2many('siswa_tab_ocb11.action_confirm', inverse_name="tabungan_id")
    desc = fields.Char('Keterangan')

    @api.depends('siswa_id')
    def _compute_get_saldo(self):
        for rec in self:
            rec.saldo_tabungan = rec.siswa_id.saldo_tabungan

    @api.model
    def create(self, vals):
        # # cek saldo siswa
        siswa = self.env['res.partner'].search([('id','=',vals['siswa_id'])])

        can_draw = True
        if siswa.saldo_tabungan == 0:
            vals['jenis'] = 'setor'
        else:
            if vals['jenis'] == 'tarik':
                if siswa.saldo_tabungan < vals['jumlah_temp']:
                    can_draw = False

        if can_draw:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = 'DRAFT/TAB/'+str(datetime.today().strftime('%d%m%y/%H%M%S'))

            if vals['jenis'] == 'tarik' :
                vals['jumlah_temp'] = -vals['jumlah_temp']
            result = super(tabungan, self).create(vals)
            return result

        else:
            print('Gagal Simpan Tabungan')
            # return {'warning': {
            #             'title': _('Warning'),
            #             'message': _('Saldo tabungan tidak mencukupi.')
            #             }}
            raise exceptions.except_orm(_('Warning'), _('Saldo tabungan tidak mencukupi.'))
    
    @api.multi
    def write(self, values):
        self.ensure_one()
        if 'jumlah_temp' in values:
            if 'jenis' in values:
                if values['jenis'] == 'tarik':
                    values['jumlah_temp'] = -values['jumlah_temp']
            else:
                if self.jenis == 'tarik':
                    values['jumlah_temp'] = -values['jumlah_temp']
        else:
            if self.jenis == 'tarik':
                values['jumlah_temp'] = -self.jumlah_temp

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
            'jumlah' : self.jumlah_temp,
            'state' : 'post'
        })
        self.confirm_ids = (0,0,{
            'name' : name_seq
        })
        self.update_saldo_siswa()

        # update compute tabungan
        self.update_saldo_tabungan_dashboard()
    
    def update_saldo_tabungan_dashboard(self):
        # dash_tab_id = self.env['ir.model.data'].search([('name','=','default_dashboard_tabungan')]).res_id
        # dash_tab = self.env['siswa_tab_ocb11.dashboard_tabungan'].search([('id','=',dash_tab_id)])
        
        dash_tab = self.env['siswa_tab_ocb11.dashboard_tabungan'].search([('id','ilike','%')])
        for dash in dash_tab:
            dash.compute_saldo_tabungan()  
    
    def action_cancel(self):
        self.ensure_one()
        # delete confirm_ids
        self.confirm_ids.unlink()
        # update name to database
        self.write({
            'name' : 'DRAFT/'+self.name,
            'state' : 'draft',
            'jumlah' : 0
        })
        # update saldo siswa
        self.update_saldo_siswa()

        # update compute tabungan
        self.update_saldo_tabungan_dashboard()

     