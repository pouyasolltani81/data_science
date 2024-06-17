from django.shortcuts import render

import requests
from django.conf import settings

def index(request):
    # Fetch all posts
    query = """
    query {
    allPosts {
        id
        title
        content
        author {
            username
        }
        comments {
            content
            author {
                username
            }
        }
    }
}

    """
    response = requests.post(settings.GRAPHQL_URL, json={'query': query})
    posts = response.json().get('data', {}).get('allPosts', [])

    # Render template with posts
    return render(request, 'myapp/index.html', {'posts': posts})

