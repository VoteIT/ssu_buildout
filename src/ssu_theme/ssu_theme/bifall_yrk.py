""" A button to express that someone has spoken for this proposal. ("Yrkat bifall")
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from betahaus.viewcomponent import view_action
from pyramid.renderers import render
from pyramid.response import Response
from pyramid.view import view_config
from voteit.core.models.interfaces import IProposal


ATTR_NAME = '_bifall_yrk_enabled'


@view_action('metadata_listing', 'bifall_yrk',
             interface=IProposal,
             priority=1)
def bifall_yrk_action(context, request, va, **kw):
    return render_btn(context, request)


def render_btn(context, request):
    values = {'context': context, 'enabled': getattr(context, ATTR_NAME, False)}
    return render('ssu_theme:templates/bifall_yrk_btn.pt', value=values, request=request)


@view_config(context=IProposal, name='_bifall_yrk')
def bifall_yrk_btn(context, request):
    # See the template
    enable = bool(request.GET.get('e', None))
    setattr(context, ATTR_NAME, enable)
    return Response(render_btn(context, request))


def includeme(config):
    config.scan(__name__)
