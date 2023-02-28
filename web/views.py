from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models.functions import Lower, TruncDate
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, ListView, UpdateView, DeleteView

from web.forms import RegistrationForm, LoginForm, TranslatedPasswordChangeForm
from web.models import User, Note, Tag, PageVisitCount


class RegistrationFormView(FormView):
    template_name = 'web/form.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = User(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
        )
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)


class LoginFormView(FormView):
    template_name = 'web/form.html'
    form_class = LoginForm
    success_url = reverse_lazy('main')

    def get_form_kwargs(self):
        kwargs = super(LoginFormView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = TranslatedPasswordChangeForm(request.user)
    return render(request, 'web/password_change_form.html', {
        'form': form
    })

    # def form_valid(self, form):
    #    return super().form_valid(form)


@login_required
def logout_view(request):
    logout(request)
    return redirect("main")


def website_analytics_view(request):
    object_list = PageVisitCount.objects.order_by('-visit_count')
    return render(request, 'web/website_analytics.html', {'object_list': object_list})


@login_required
def notes_analytics_view(request):
    notes = Note.objects.filter(user=request.user)  # .prefetch_related('tags')
    context = {}
    context['notes_count'] = notes.count()
    context['notes_count_by_date_created'] = notes.annotate(date_created=TruncDate("time_created")) \
        .values('date_created').annotate(count=Count('id')) \
        .order_by('date_created')
    context['notes_count_by_date_edited'] = notes.annotate(date_edited=TruncDate("time_edited")) \
        .values('date_edited').annotate(count=Count('id')) \
        .order_by('date_edited')
    return render(request, 'web/notes_analytics.html', context)


class NoteListView(LoginRequiredMixin, ListView):
    template_name = 'web/note_list_view.html'
    model = Note
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['sort_column'] = self.request.GET.get('sort_column', 'title')
        context['sort_direction'] = self.request.GET.get('sort_direction', 'asc')
        context['search_text'] = self.request.GET.get('search_text', '')

        get_copy = self.request.GET.copy()
        get_copy.pop('page', True)
        parameters = get_copy.urlencode()
        context['parameters'] = parameters

        return context

    def get_queryset(self):
        # TODO orderby date, name, ...
        sort_column = self.request.GET.get('sort_column', 'title')
        sort_direction = self.request.GET.get('sort_direction', 'asc')
        search_text = self.request.GET.get('search_text', '')
        if sort_direction == 'desc':
            sort_column = '-' + sort_column

        queryset = Note.objects.filter(user=self.request.user).order_by(sort_column).prefetch_related('tags')

        if search_text != '':
            queryset = queryset.filter(title__icontains=search_text)
        return queryset


class NoteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'web/new_note_form.html'
    success_url = reverse_lazy('main')
    model = Note
    fields = ['title', 'text', 'tags']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_class(self):
        form = super().get_form_class()
        form.base_fields['tags'].queryset = Tag.objects.filter(user=self.request.user)
        form.base_fields['tags'].required = False
        return form


class NoteEditView(LoginRequiredMixin, UpdateView):
    template_name = 'web/edit_delete_form.html'
    success_url = reverse_lazy('main')
    model = Note
    fields = ['title', 'text', 'tags']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_url_name'] = 'delete_note'
        context['display_tag_hint'] = True
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_form_class(self):
        form = super().get_form_class()
        form.base_fields['tags'].queryset = Tag.objects.filter(user=self.request.user)
        form.base_fields['tags'].required = False
        return form


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'web/note_delete_form.html'
    success_url = reverse_lazy('main')
    model = Note

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.user == self.request.user:
            raise Http404
        return obj


class TagCreateView(LoginRequiredMixin, CreateView):
    template_name = 'web/tags.html'
    success_url = reverse_lazy('tags')
    model = Tag
    fields = ['text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Tag.objects.filter(user=self.request.user).order_by(Lower('text'))
        return context


class TagEditView(LoginRequiredMixin, UpdateView):
    template_name = 'web/edit_delete_form.html'
    success_url = reverse_lazy('tags')
    model = Tag
    fields = ['text']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_url_name'] = 'delete_tag'
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.user == self.request.user:
            raise Http404
        return obj


class TagDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'web/tag_delete_form.html'
    success_url = reverse_lazy('tags')
    model = Tag

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.user == self.request.user:
            raise Http404
        return obj
