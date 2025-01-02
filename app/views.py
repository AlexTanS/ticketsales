from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Route, Ticket, Client
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
    routers = Route.objects.all()[:5]  # первые пять маршрутов
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


@login_required
def ticket_buy(request: HttpRequest):
    """Страница с формой покупки билета"""
    content = {
        "title": "Покупка"
    }
    return render(request=request, template_name="", context=content)


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
    tickets = Ticket.objects.filter(owner=request.user.pk)
    list_tickets = []
    for t in tickets:
        list_tickets.append(
            {
                "id_ticket": t.id_ticket,
                "fio_f": t.client.fio_f,
                "fio_i": t.client.fio_i,
                "fio_o": t.client.fio_o,
                "route_number": t.route.id_route,
                "route_start": t.route.city_start,
                "route_finish": t.route.city_finish,
                "price": t.route.price,
                "bus": t.route.bus.get_brand_display(),
                "state_number": t.route.bus.state_number,
                "passport": t.client.passport,
            }
        )
    content = {
        "title": "Профиль",
        "list_tickets": list_tickets,
    }
    return render(request=request, template_name="profile.html", context=content)
