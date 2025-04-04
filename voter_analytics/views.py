from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter

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
        for election_field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
            if election_field in self.request.GET:
                voters = voters.filter(**{election_field: True})

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