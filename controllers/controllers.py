# -*- coding: utf-8 -*-
from odoo import http

# class SiswaTabOcb11(http.Controller):
#     @http.route('/siswa_tab_ocb11/siswa_tab_ocb11/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/siswa_tab_ocb11/siswa_tab_ocb11/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('siswa_tab_ocb11.listing', {
#             'root': '/siswa_tab_ocb11/siswa_tab_ocb11',
#             'objects': http.request.env['siswa_tab_ocb11.siswa_tab_ocb11'].search([]),
#         })

#     @http.route('/siswa_tab_ocb11/siswa_tab_ocb11/objects/<model("siswa_tab_ocb11.siswa_tab_ocb11"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('siswa_tab_ocb11.object', {
#             'object': obj
#         })