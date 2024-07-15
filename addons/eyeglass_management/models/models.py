from odoo import models, fields, api

class EyeglassManagement(models.Model):
    _name = 'eyeglass.management'
    _description = 'Patient Eye Profile'

    fullname = fields.Char(string="Full Name", required=True)
    email = fields.Char(string="Email", required=True)
    birthday = fields.Date(string="Birthday")
    address = fields.Text(string="Address")
    cellphone = fields.Char(string="Cell Phone")
    homephone = fields.Char(string="Home Phone")
    occupation = fields.Char(string="Occupation")
    
    eyeglass_ids = fields.One2many(
        'eyeglass.detail', 'management_id', string="Eyeglass Details", 
        default=lambda self: self._default_eyeglass_details()
    )
    
    # History tracking
    history_ids = fields.One2many('eyeglass.history', 'management_id', string="History")

    @api.model
    def create(self, vals):
        record = super(EyeglassManagement, self).create(vals)
        return record
    
    def write(self, vals):
        self._create_history(self, vals)
        return super(EyeglassManagement, self).write(vals)
    
    def _create_history(self, record, vals=None):

        for detail in self.eyeglass_ids:
         self.env['eyeglass.history'].create({
            'management_id': record.id,
            'changes':  'Updated fields: ' + ', '.join(vals.keys()),
            'eye': detail.eye,
            'sph': detail.sph,
            'cyl': detail.cyl,
            'add': detail.add,
            'axis': detail.axis,
            'prism': detail.prism,
            'cd': detail.cd,
            'pd': detail.pd,
        })

       
    def action_submit(self):
        self.ensure_one()
        return True
    

    @api.model
    def _default_eyeglass_details(self):
        return [
            (0, 0, {'eye': 'right'}),
            (0, 0, {'eye': 'left'})
        ]

  

class EyeglassDetail(models.Model):
    _name = 'eyeglass.detail'
    _description = 'Eyeglass Detail'

    management_id = fields.Many2one('eyeglass.management', string="Management", ondelete="cascade")
    eye = fields.Selection([('right', 'Right Eye (OD)'), ('left', 'Left Eye (OS)')], required=True)
    
    # Fields with select options
    sph = fields.Selection([(str(x / 100), '{:.2f}'.format(x / 100)) for x in range(-2500, 2501, 25)], string="SPH")
    cyl = fields.Selection([(str(x / 100), '{:.2f}'.format(x / 100)) for x in range(-1000, 1, 25)], string="CYL")
    add = fields.Selection([(str(x / 100), '{:.2f}'.format(x / 100)) for x in range(25, 401, 25)], string="ADD")

    # Fields with input
    axis = fields.Float(string="AXIS")
    prism = fields.Float(string="PRISM")
    cd = fields.Float(string="CD")
    pd = fields.Float(string="PD")
    
    
class EyeglassHistory(models.Model):
    _name = 'eyeglass.history'
    _description = 'Eyeglass History'
    
    management_id = fields.Many2one('eyeglass.management', string="Patient Eye Profile", readonly=True)
    change_date = fields.Datetime(string="Change Date", default=fields.Datetime.now, readonly=True)
    changes = fields.Text(string="Changes", readonly=True)
    eye = fields.Selection([('right', 'Right Eye (OD)'), ('left', 'Left Eye (OS)')],  readonly=True)
    sph = fields.Selection([(str(x / 100), '{:.2f}'.format(x / 100)) for x in range(-2500, 2501, 25)], string="SPH",  readonly=True)
    cyl = fields.Selection([(str(x / 100), '{:.2f}'.format(x / 100)) for x in range(-1000, 1, 25)], string="CYL",  readonly=True)
    add = fields.Selection([(str(x / 100), '{:.2f}'.format(x / 100)) for x in range(25, 401, 25)], string="ADD",  readonly=True)
    axis = fields.Float(string="AXIS",  readonly=True )
    prism = fields.Float(string="PRISM",  readonly=True)
    cd = fields.Float(string="CD",  readonly=True)
    pd = fields.Float(string="PD",  readonly=True)


