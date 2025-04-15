'''
File: views.py
Description: Define views for the Voter Analytics application.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-04-03
'''

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter
import plotly.graph_objs as go
from plotly.offline import plot


import plotly
import plotly.graph_objs as go
from plotly.offline import plot

# Create your views here.

class VotersListView(ListView):
    '''View to display voters in Newton.'''

    model = Voter
    template_name = 'voter_analytics/voters.html'
    context_object_name = 'voters'
    paginate_by = 100 # how many voters per page

    def get_queryset(self):
        '''Filtering function.'''

        voters = Voter.objects.all()

        # party
        if 'party' in self.request.GET:
            p = self.request.GET['party']
            if p:
                voters = voters.filter(party=p)
        
        # min date of birth
        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            if min_dob: # avoid checking blank str
                voters = voters.filter(dob__year__gte=int(min_dob))

        # max date of birth
        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob: # avoid checking blank str
                voters = voters.filter(dob__year__lte=int(max_dob))

        # voter score
        if 'voter_score' in self.request.GET:
            score = self.request.GET['voter_score']
            if score: # avoid checking blank str
                voters = voters.filter(voter_score=int(score))

        # elections
        for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
            if field in self.request.GET:
                if field == 'v20state':
                    voters = voters.filter(v20state=True)
                elif field == 'v21town':
                    voters = voters.filter(v21town=True)
                elif field == 'v21primary':
                    voters = voters.filter(v21primary=True)
                elif field == 'v22general':
                    voters = voters.filter(v22general=True)
                elif field == 'v23town':
                    voters = voters.filter(v23town=True)

        return voters

    def get_context_data(self, **kwargs):
        '''Return a dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)

        # find all possible parties
        parties = Voter.objects.values_list('party', flat=True).distinct()

        res = []
        for p in parties:
            res.append(p)

        context['parties'] = res

        # find max and min years for dob
        first = Voter.objects.order_by('dob')[0]
        last = Voter.objects.order_by('-dob')[0]

        min_year = first.dob.year
        max_year = last.dob.year
        context["years"] = [str(y) for y in range(min_year, max_year + 1)] # list of years from min to max

        return context

class VoterDetailView(DetailView):
    '''View to display a single voter. '''
    model = Voter
    template_name = 'voter_analytics/voter.html'
    context_object_name = 'voter'


class VoterGraphView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        '''Filtering function.'''

        voters = Voter.objects.all()

        # party
        if 'party' in self.request.GET:
            p = self.request.GET['party']
            if p:
                voters = voters.filter(party=p)
        
        # min date of birth
        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            if min_dob: # avoid checking blank str
                voters = voters.filter(dob__year__gte=int(min_dob))

        # max date of birth
        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob: # avoid checking blank str
                voters = voters.filter(dob__year__lte=int(max_dob))

        # voter score
        if 'voter_score' in self.request.GET:
            score = self.request.GET['voter_score']
            if score: # avoid checking blank str
                voters = voters.filter(voter_score=int(score))

        # elections
        for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
            if field in self.request.GET:
                if field == 'v20state':
                    voters = voters.filter(v20state=True)
                elif field == 'v21town':
                    voters = voters.filter(v21town=True)
                elif field == 'v21primary':
                    voters = voters.filter(v21primary=True)
                elif field == 'v22general':
                    voters = voters.filter(v22general=True)
                elif field == 'v23town':
                    voters = voters.filter(v23town=True)

        return voters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # find all possible parties
        parties = Voter.objects.values_list('party', flat=True).distinct()

        res = []
        for p in parties:
            res.append(p)

        context['parties'] = res

        # find max and min years for dob
        first = Voter.objects.order_by('dob')[0]
        last = Voter.objects.order_by('-dob')[0]

        min_year = first.dob.year
        max_year = last.dob.year
        context["years"] = [str(y) for y in range(min_year, max_year + 1)] # list of years from min to max

        voters = self.get_queryset()

        # Graphs

        # bar of birth years
        year_counts = {}
        for v in voters:
            y = v.dob.year
            year_counts[y] = year_counts.get(y, 0) + 1

        years = sorted(year_counts.keys())
        counts = [year_counts[y] for y in years]
        fig = go.Bar(x=years, y=counts)
        title_text1 = f'Voter distribution by Year of Birth (n={len(voters)})'
        context['birth_year_chart'] = plotly.offline.plot({'data':[fig],
                                "layout_title_text": title_text1},
                                auto_open=False,
                                output_type='div')


        # pie chart of party affiliation

        party_counts = {}
        for v in voters:
            p = v.party.strip()
            party_counts[p] = party_counts.get(p, 0) + 1

        fig2 = go.Pie(labels=list(party_counts.keys()), values=list(party_counts.values()))
        title_text2 = f'Voter distribution by Party Affiliation (n={len(voters)})'
        context['party_pie_chart'] = plotly.offline.plot({'data':[fig2],
                                        "layout_title_text": title_text2}, 
                                        auto_open=False,
                                        output_type='div')


        # bar chart for election participation
        election_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = {}
        for e in election_fields:
            election_counts[e] = 0

        # for each voter, check if they voted in each election, inc if they did
        for v in voters:
            if v.v20state:
                election_counts['v20state'] += 1
            if v.v21town:
                election_counts['v21town'] += 1
            if v.v21primary:
                election_counts['v21primary'] += 1
            if v.v22general:
                election_counts['v22general'] += 1
            if v.v23town:
                election_counts['v23town'] += 1


        fig3 = go.Bar(
            x=list(election_counts.keys()),
            y=list(election_counts.values())
        )
        title_text3 = f'Vote Count by Election (n={len(voters)})'
        context['elections_chart'] = plotly.offline.plot({'data': [fig3],
                                                        "layout_title_text": title_text3}, 
                                                         auto_open=False,
                                                         output_type='div')
        # keep form selections in the context
        context['request'] = self.request

        return context