from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.http import HttpResponseNotFound
from django.db.models import Max
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from .serializers import ListOfServicesSerializer
from .forms import RegisterUserForm, BuyTicketClient
from .models import Route, Ticket, Client, ListOfServices, Services


def index(request: HttpRequest):
    """Главная страница"""
    content = {
        "title": "Главная страница"
    }
    return render(request=request, template_name="index.html", context=content)


def route_info(request: HttpRequest):
    """Информация о маршрутах"""
    routers = Route.objects.all()
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
    paginator = Paginator(list_routers, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    content = {
        "title": "Маршруты",
        "page_obj": page_obj,
    }
    return render(request=request, template_name="route_info.html", context=content)


@login_required
def ticket_buy(request: HttpRequest):
    """Страница с формой покупки билета"""
    content = {
        "title": "Покупка"
    }

    try:
        number_route = int(request.GET.get("number_route"))  # номер маршрута
    except ValueError:
        return HttpResponseNotFound("Ошибка, данного маршрута не существует")

    if not number_route:  # если номера нет
        return HttpResponseNotFound("Ошибка, данного маршрута не существует")
    else:
        if request.method == "POST":
            form = BuyTicketClient(data=request.POST)
            if form.is_valid():

                # данные из формы
                fio_f = form.cleaned_data["fio_f"]
                fio_i = form.cleaned_data["fio_i"]
                fio_o = form.cleaned_data["fio_o"]
                passport = form.cleaned_data["passport"]
                money = form.cleaned_data["money"]

                # обработка данных
                if Client.objects.filter(passport=passport):  # если уже есть такой пассажир
                    # изменяю старую запись
                    client = Client.objects.get(passport=passport)
                    client.fio_f = fio_f
                    client.fio_i = fio_i
                    client.fio_o = fio_o
                    client.passport = passport
                    client.money = money
                    client.save()
                else:  # если пассажира в БД нет
                    client = Client(fio_f=fio_f, fio_i=fio_i, fio_o=fio_o, passport=passport, money=money)
                    client.save()

                # формирую новый id_ticket
                new_id_ticket = Ticket.objects.aggregate(max_value=Max("id_ticket"))["max_value"] + 1
                new_owner = request.user
                new_client = client
                new_route = Route.objects.get(id_route=number_route)
                new_ticket = Ticket(id_ticket=new_id_ticket, owner=new_owner, client=new_client, route=new_route)
                new_ticket.save()

                content["form"] = form
                return redirect("profile")
            else:
                content["error"] = "Форма заполнена неправильно"
                content["form"] = BuyTicketClient()
        else:
            content["form"] = BuyTicketClient()
    return render(request=request, template_name="ticket_buy.html", context=content)


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
    paginator = Paginator(list_tickets, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    content = {
        "title": "Профиль",
        "page_obj": page_obj,
    }
    return render(request=request, template_name="profile.html", context=content)


def api_list_of_services(request: Request):
    """Данные обо всех дополнительных услугах"""
    if request.method == "GET":
        services = ListOfServices.objects.all()
        serializer = ListOfServicesSerializer(services, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(["GET", "POST"])
def api_service(request: Request):
    """Доп услуги"""
    data = request.data
    # проверка номера билета
    if not Ticket.objects.filter(id_ticket=data["id_ticket"]):
        return Response({"response": "Такого билета не существует"}, status=status.HTTP_200_OK)
    # проверка пароля
    user_password = Ticket.objects.filter(id_ticket=data["id_ticket"])[0].owner.password
    if not check_password(data["password"], user_password):
        return Response({"response": "Неверный пароль"}, status=status.HTTP_200_OK)
    # проверка наличия данной услуги в билете
    instance_list_of_service = ListOfServices.objects.get(name=data["service"])  # нужный сервис
    instance_ticket = Ticket.objects.get(id_ticket=data["id_ticket"])  # билет
    try:
        # ошибка выдается если нет записи, если все норм - взять существующую запись
        list_services = Services.objects.filter(ticket=instance_ticket)[0].service.all()  # список полученных услуг
        new_service = Services.objects.get(ticket=instance_ticket)  # запись с услугами
    except IndexError:
        # новая запись об услуге
        new_service = Services.objects.create(ticket=instance_ticket)
        list_services = []
    services_buy = []
    for s in list_services:
        services_buy.append(str(s))
    if data["service"] in services_buy:
        return Response({"response": "Данная услуга уже включена в билет"}, status=status.HTTP_200_OK)

    new_service.service.add(instance_list_of_service)
    # расчет средств на  счету с учетом услуги
    client_passport = Ticket.objects.get(id_ticket=data["id_ticket"]).client.passport
    client = Client.objects.get(passport=client_passport)
    price = ListOfServices.objects.get(name=data["service"]).price  # стоимость услуги
    new_money = client.money - price
    client.money = new_money
    client.save()
    # отправка ответа об успехе
    d = {"response": f"Услуга успешно включена в стоимость вашего билета, у вас на счету осталось {new_money}"}
    return Response(d, status=status.HTTP_200_OK)
