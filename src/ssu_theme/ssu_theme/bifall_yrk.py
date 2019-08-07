# -*- coding: utf-8 -*-
""" A button to express that someone has spoken for this proposal. ("Yrkat bifall")
"""
from __future__ import unicode_literals

from arche.views.base import BaseView
from betahaus.viewcomponent import view_action
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render
from pyramid.response import Response
from pyramid.view import view_config
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IProposal
from voteit.core.security import MODERATE_MEETING
from voteit.core.security import unrestricted_wf_transition_to


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


@view_action('proposal_extras', 'start_decisions',
             interface=IAgendaItem,
             priority=1)
def start_decisions_action(context, request, va, **kw):
    return """<li><a href="{}">{}</a></li>""".format(
        request.resource_path(context, '_start_decisions'),
        "Preparera för beslut"
    )


@view_config(context=IAgendaItem, name='_start_decisions', permission=MODERATE_MEETING)
class StartDecisionsView(BaseView):

    def __call__(self):
        """ Start the decision process.
            * Block proposals
            * Make all proposals that aren't marked with 'bifall yrkat' unhandled.
        """
        # context is the agenda item - block proposals
        self.context.proposal_block = True
        # Change all proposals that are published to unhandled, if they aren't marked as 'bifall yrkat'
        count = 0
        for obj in self.context.values():
            if IProposal.providedBy(obj) and obj.get_workflow_state() == 'published' and not getattr(obj, ATTR_NAME, False):
                unrestricted_wf_transition_to(obj, 'unhandled')
                count += 1
        self.flash_messages.add("{} förslag justerade".format(count))
        return HTTPFound(location=self.request.resource_url(self.context))


def includeme(config):
    config.scan(__name__)
