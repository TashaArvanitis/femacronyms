from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# from .forms import CurrentPassForm
from .forms import AcronymSearchForm
from .models import load_data, search


def query_view(request):
    # Unpopulated form - serve the blank/default form!
    if len(request.GET.keys()) == 0:
        form = AcronymSearchForm()
    else:
        # Process the form if the GET request is real
        form = AcronymSearchForm(request.GET)
        if form.is_valid():
            df = load_data()
            search_string = form.cleaned_data['search_term']
            (acronym_match, fulltext_match) = search(
                df, search_string=search_string)
            params = {'search_string': search_string,
                      'acronym_matches': len(acronym_match) > 0,
                      'acronym_html': acronym_match.to_html(index=False, na_rep=''),
                      'fulltext_matches': len(fulltext_match) > 0,
                      'fulltext_html': fulltext_match.to_html(index=False, na_rep=''),
                      }
            print(params)
            return render(request, 'femacronyms/query.html', params)

    # If we're just serving the form or if there was an error in a
    # submitted one, show the form!
    return render(request, 'femacronyms/query.html', {'form': form})



def index_view(request):
    template_name = 'femacronyms/index.html'
    return render(request, template_name, {})
