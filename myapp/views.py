from django.shortcuts import render,reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from myapp.models import Post,Comment
from django.views.generic.edit import CreateView
from myapp.forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
	p=Post.objects.all()
	context={'posts':p}
	return render(request,'index.html',context)

def detail(request,pk):
	p=Post.objects.get(pk=pk)
	context={'posts':p}
	return render(request,'detail.html',context)
class PostCreate(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','description','image']
    template_name='create.html'
    success_url='/'

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)

@login_required
def detail(request,pk):
    p=Post.objects.get(pk=pk)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            comment=form.cleaned_data['comment']
            print(comment)
            c=Comment(post=p,comment=comment,user=request.user)
            c.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('myapp:detail',args=(pk,)))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm()
    comments = Comment.objects.filter(post=p)

    return render(request, 'detail.html', {'form': form,'post':p,'comments':comments})
	
def like(request):
    if request.is_ajax():
        i=request.GET.get('i')
        p=Post.objects.get(pk=i)
        p.likes+=1
        p.save()
        data={'i':p.likes}
        return JsonResponse(data)
