# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import deform
import colander
from arche.interfaces import ISchemaCreatedEvent
from arche.schemas import UserSchema
from betahaus.viewcomponent import view_action
from pyramid.events import subscriber
from voteit.core.models.interfaces import IUser


SSU_DISTRIKT = (
    "SSU Blekinge",
    "SSU Dalarna",
    "SSU Fyrbodal",
    "SSU Gotland",
    "SSU Gävleborg",
    "SSU Göteborg",
    "SSU Göteborgsområdet",
    "SSU Halland",
    "SSU Jämtlands län",
    "SSU Jönköpings län",
    "SSU Kalmar län",
    "SSU Kronoberg",
    "SSU Norrbotten",
    "SSU Skaraborg",
    "SSU Skåne",
    "SSU Stockholms län",
    "SSU Stockholms stad",
    "SSU Södra Älvsborg",
    "SSU Sörmland",
    "SSU Uppland",
    "SSU Värmland",
    "SSU Västerbotten",
    "SSU Västernorrland",
    "SSU Västmanland",
    "SSU Örebro län",
    "SSU Östergötland",
)


SELECTABLE_DISTRIKT = [("", "(Inget)")]
SELECTABLE_DISTRIKT.extend([(x, x) for x in SSU_DISTRIKT])


@subscriber([UserSchema, ISchemaCreatedEvent])
def add_distrikt(schema, event):
    schema.add(
        colander.SchemaNode(
            colander.String(),
            name="ssu_distrikt",
            title = "SSU-distrikt",
            missing="",
            validator=colander.OneOf(SSU_DISTRIKT),
            widget=deform.widget.Select2Widget(values=SELECTABLE_DISTRIKT)
        )
    )


@view_action('user_info', 'profile_distrikt', interface = IUser, priority = 20)
def profile_distrikt(context, request, va, **kw):
    distrikt = getattr(context, 'ssu_distrikt', '')
    if distrikt:
        return """<h5>SSU-distrikt</h5>
            <p>{}</p>
        """.format(distrikt)


def includeme(config):
    from voteit.core.models.user import User
    User.add_field('ssu_distrikt')
    config.scan(__name__)
