from django.contrib.auth.decorators import login_required
from django.views.decorators.http import (
    require_safe,
    require_http_methods,
)
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from snippets.models import Snippet, Comment
from snippets.forms import SnippetForm, CommentForm


@require_safe
def top(request):
    snippets = Snippet.objects.select_related("created_by").all()
    return render(request, "snippets/top.html", {"snippets": snippets})


@login_required
@require_http_methods(["GET", "POST", "HEAD"])
def snippet_new(request):
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.created_by = request.user
            snippet.save()
            return redirect("snippets:detail", snippet_id=snippet.pk)
    else:
        form = SnippetForm()

    return render(request, "snippets/new.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST", "HEAD"])
def snippet_edit(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if snippet.created_by_id != request.user.id:
        return HttpResponseForbidden("このスニペットの編集は許可されていません")

    if request.method == "POST":
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect("snippets:detail", snippet_id=snippet.id)
    else:
        form = SnippetForm(instance=snippet)

    return render(request, "snippets/edit.html", {"form": form})


@require_http_methods(["GET", "POST", "HEAD"])
def snippet_detail(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    comments = Comment.objects.select_related("commented_by").filter(
        commented_to=snippet
    )
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.commented_to = snippet
            comment.commented_by = request.user
            comment.save()
            return redirect("snippets:detail", snippet_id=snippet_id)
    else:
        form = CommentForm()
    context = {"snippet": snippet, "comments": comments, "form": form}
    return render(request, "snippets/detail.html", context)


@require_safe
def snippet_delete(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if snippet.created_by_id != request.user.id:
        return HttpResponseForbidden("このスニペットの削除は許可されていません")
    snippet.delete()
    return redirect("top")
