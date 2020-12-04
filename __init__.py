# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import party


def register():
    Pool.register(
        party.Iae,
        party.Party,
        party.PartyIae,
        module='party_iae', type_='model')
