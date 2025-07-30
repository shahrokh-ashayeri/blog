from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from post.models import Post


@csrf_exempt
def posts_index(request):
    if request.method == 'GET':
        # Here you would typically fetch posts from the database
        # For demonstration, we return a static response
        posts = Post.objects.all().values()
        print(posts)
        return JsonResponse(list(posts), safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)