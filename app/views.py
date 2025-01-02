from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Route, Ticket
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from .forms import RegisterUserForm


# TODO для паспорта сделать проверку в форме занесения данных чтобы минимум и максимум символов совпадали

def index(request: HttpRequest):
    """Главная страница"""
    content = {
        "title": "Главная страница"
    }
    return render(request=request, template_name="index.html", context=content)


def route_info(request: HttpRequest):
    """Информация о маршрутах"""
    routers = Route.objects.all()[:5]
    list_routers = []
    for r in routers:
        # получаю список всех билетов связанных с данным маршрутом
        tickets = Ticket.objects.filter(route__id_route=r.id_route)
        all_place = r.bus.count_place  # всего мест в автобусе
        empty = all_place - len(tickets)  # сколько свободных мест
        list_routers.append({"number_route": r.id_route,
                             "empty_place": empty,
                             "all_place": all_place,
                             "start": r.city_start,
                             "finish": r.city_finish,
                             "bus": r.bus.get_brand_display(),
                             "price": r.price})
    content = {
        "title": "Маршруты",
        "list_routers": list_routers,
    }
    return render(request=request, template_name="route_info.html", context=content)


def ticket_buy(request: HttpRequest):
    """Страница с формой покупки билета"""
    pass


def about(request: HttpRequest):
    """Информация о фирме"""
    content = {
        "title": "О нас"
    }
    return render(request=request, template_name="index.html", context=content)


class AppLoginView(LoginView):
    """Авторизация на сайте"""
    template_name = "registration/login.html"

    # передача параметров в шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Вход"
        return context


class AppLogoutView(LoginRequiredMixin, LogoutView):
    """Выход из авторизации"""
    template_name = "registration/logout.html"


class RegisterUserView(CreateView):
    """Регистрация"""
    form_class = RegisterUserForm
    template_name = "registration/register.html"
    extra_context = {"title": "Регистрация"}
    success_url = "register_done"


class RegisterDoneView(TemplateView):
    """Успешная регистрация"""
    template_name = "registration/register_done.html"
    extra_context = {"title": "Успешная регистрация"}


@login_required
def profile(request: HttpRequest):
    """Страница профиля зарегистрированного пользователя"""
    content = {
        "title": "Профиль"
    }
    return render(request=request, template_name="profile.html", context=content)

# def signup_view(request: HttpRequest):
#     """Регистрация"""
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()  # Сохраняем нового пользователя
#             login(request, user)  # Выполняем вход
#             return redirect('index')  # Перенаправляем на главную страницу
#     else:
#         form = SignUpForm()
#     return render(request=request, template_name='signup.html', context={'form': form})
#
#
# def login_view(request: HttpRequest):
#     """Вход пользователя"""
#     form = LoginForm(data=request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(username=username, password=password)  # Проверяем учетные данные
#             if user is not None:
#                 login(request, user)  # Выполняем вход
#                 return redirect('route_info')  # Перенаправляем на страницу маршрутов
#     return render(request=request, template_name='registration/login.html', context={'form': form})
