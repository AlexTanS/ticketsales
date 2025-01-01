from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Route, Ticket


# TODO для паспорта сделать проверку в форме занесения данных чтобы минимум и максимум символов совпадали

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
        empty = all_place -len(tickets)  # сколько свободных мест
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


def passenger_registration(request: HttpRequest):
    """Страница для регистрации пассажира"""
    pass


def ticket_buy(request: HttpRequest):
    """Страница с формой покупки билета"""
    pass


def about(request: HttpRequest):
    """Информация о фирме"""
    content = {
        "title": "О нас"
    }
    return render(request=request, template_name="index.html", context=content)
