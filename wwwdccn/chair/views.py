import csv
import math
from datetime import datetime

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from chair.forms import FilterSubmissionsForm, FilterUsersForm
from conferences.decorators import chair_required
from conferences.helpers import is_author
from conferences.models import Conference


ITEMS_PER_PAGE = 10


User = get_user_model()


@chair_required
@require_GET
def dashboard(request, pk):
    conference = get_object_or_404(Conference, pk=pk)
    return render(request, 'chair/dashboard.html', context={
        'conference': conference,
    })


@chair_required
@require_GET
def submissions_list(request, pk):
    conference = get_object_or_404(Conference, pk=pk)
    form = FilterSubmissionsForm(request.GET, instance=conference)
    submissions = list(conference.submission_set.all())

    if form.is_valid():
        submissions = form.apply(submissions)

    return render(request, 'chair/submissions_list.html', context={
        'conference': conference,
        'submissions': submissions,
        'filter_form': form,
    })


@chair_required
@require_GET
def users_list(request, pk):
    conference = get_object_or_404(Conference, pk=pk)
    users = User.objects.all()
    form = FilterUsersForm(request.GET, instance=conference)

    if form.is_valid():
        users = form.apply(users, conference)

    return render(request, 'chair/users_list.html', context={
        'conference': conference,
        'users': users,
        'filter_form': form,
    })


@chair_required
@require_GET
def user_details(request, pk, user_pk):
    conference = get_object_or_404(Conference, pk=pk)
    user = get_object_or_404(User, pk=user_pk)
    return render(request, 'chair/user_details.html', context={
        'conference': conference,
        'member': user,
    })


#############################################################################
# CSV EXPORTS
#############################################################################
@chair_required
@require_GET
def get_submissions_csv(request, pk):
    conference = get_object_or_404(Conference, pk=pk)
    submissions = list(conference.submission_set.all().order_by('pk'))

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    response['Content-Disposition'] = \
        f'attachment; filename="submissions-{timestamp}.csv"'

    writer = csv.writer(response)
    number = 1
    writer.writerow([
        '#', 'ID', 'TITLE', 'AUTHORS', 'COUNTRY', 'CORR_AUTHOR', 'CORR_EMAIL',
        'LANGUAGE', 'LINK',
    ])
    for sub in submissions:
        authors = ', '.join(a.user.profile.get_full_name()
                           for a in sub.authors.all())
        countries = ', '.join(set(a.user.profile.get_country_display()
                             for a in sub.authors.all()))
        owner = sub.created_by
        corr_author = owner.profile.get_full_name() if owner else ''
        corr_email = owner.email if owner else ''
        link = sub.review_manuscript.url if sub.review_manuscript else ''
        stype = sub.stype.get_language_display() if sub.stype else ''

        row = [
            number, sub.pk, sub.title, authors, countries, corr_author,
            corr_email, stype, link
        ]
        writer.writerow(row)
        number += 1

    return response


@chair_required
@require_GET
def get_authors_csv(request, pk):
    conference = get_object_or_404(Conference, pk=pk)
    users = [u for u in User.objects.all().order_by('pk')
             if is_author(conference, u)]

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    response['Content-Disposition'] = \
        f'attachment; filename="authors-{timestamp}.csv"'

    writer = csv.writer(response)
    number = 1
    writer.writerow([
        '#', 'ID', 'FULL_NAME', 'FULL_NAME_RUS', 'DEGREE', 'COUNTRY', 'CITY',
        'AFFILIATION', 'ROLE', 'EMAIL'
    ])
    for user in users:
        prof = user.profile
        row = [
            number, user.pk, prof.get_full_name(), prof.get_full_name_rus(),
            prof.degree, prof.get_country_display(), prof.city, prof.affiliation,
            prof.role, user.email,
        ]
        writer.writerow(row)
        number += 1

    return response
