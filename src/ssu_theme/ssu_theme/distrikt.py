# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import deform
import colander
from arche.interfaces import ISchemaCreatedEvent
from arche.schemas import UserSchema


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


def includeme(config):
    config.add_subscriber(add_distrikt, [UserSchema, ISchemaCreatedEvent])
    from voteit.core.models.user import User
    User.add_field('ssu_distrikt')
