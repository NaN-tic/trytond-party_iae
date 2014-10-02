# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta

__all__ = ['Iae', 'Party', 'PartyIae']
__metaclass__ = PoolMeta


class Iae(ModelSQL, ModelView):
    '''IAE'''
    __name__ = 'party.iae'
    _order = 'section, division, grouping, group, epigraph'

    section = fields.Char('Section', required=True)
    division = fields.Char('Division')
    grouping = fields.Char('Grouping')
    group = fields.Char('Group')
    epigraph = fields.Char('Epigraph')
    name = fields.Char('Name', required=True)
    parent = fields.Many2One('party.iae', 'Parent', select=True)
    childs = fields.One2Many('party.iae', 'parent', string='Children')
    full_name = fields.Function(fields.Char('Full Name'),
        'get_full_name')

    @classmethod
    def validate(cls, iaes):
        super(Iae, cls).validate(iaes)
        cls.check_recursion(iaes, rec_name='name')

    def get_rec_name(self, name):
        code = self.section
        if self.division not in (None, ""):
            code += "-" + self.division
        if self.epigraph:
            code += "-" + self.epigraph
        elif self.group:
            code += "-" + self.group
        elif self.grouping:
            code += "-" + self.grouping
        if code:
            return u"[%s] %s" % (code, self.name)
        return self.name

    @classmethod
    def search_rec_name(cls, name, clause):
        return ['OR',
            ('epigraph',) + tuple(clause[1:]),
            ('group',) + tuple(clause[1:]),
            ('name',) + tuple(clause[1:]),
            ]

    def get_full_name(self, name):
        res = self.rec_name
        parent = self.parent
        while parent:
            res = u'%s / %s' % (parent.name, res)
            parent = parent.parent
        return res


class Party:
    __name__ = 'party.party'

    main_iae = fields.Many2One('party.iae', 'Main IAE')  # , domain=[
            # ('childs', '=', None),
            # ])
    secondary_iaes = fields.Many2Many('party.party-party.iae', 'party', 'iae',
        'Secondary IAEs')  # , domain=[
            # ('childs', '=', None),
            # ])


class PartyIae(ModelSQL):
    'Party - IAE'
    __name__ = 'party.party-party.iae'
    party = fields.Many2One('party.party', 'Party', ondelete='CASCADE',
        required=True, select=True)
    iae = fields.Many2One('party.iae', 'IAE', ondelete='CASCADE',
        required=True, select=True)
