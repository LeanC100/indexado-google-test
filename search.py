from googlesearch import search


def google(name):
    # realiza una busqueda especial en google 
    google_query = str(f"site:www.clarin.com \" {name} \"")
    search_google = search(google_query, start=0,pause=2)

    return results_check(search_google)

def results_check(result):
    try:
        print('site indexed correctly')
        return True
    except StopIteration:
        print('Google indexed in process ...')
        return False
