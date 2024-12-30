from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# TODO для паспорта и госномера сделать проверку в форме занесения данных чтобы минимум и максимум символов совпадали

class Cities(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="название города",
                            help_text="здесь указывается название города")

    class Meta:
        verbose_name = "город"
        verbose_name_plural = "города"

    def __str__(self):
        return self.name


class Client(models.Model):
    fio_f = models.CharField(max_length=100, verbose_name="фамилия", help_text="фамилия пассажира")
    fio_i = models.CharField(max_length=100, verbose_name="имя", help_text="имя пассажира")
    fio_o = models.CharField(max_length=100, verbose_name="отчество", help_text="отчество пассажира")
    passport = models.CharField(max_length=10, unique=True, verbose_name="паспорт",
                                help_text="паспортные данные пассажира: 10 цифр", db_index=True)
    money = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="деньги", help_text="сумма денег на счете")

    class Meta:
        ordering = ["fio_f", "fio_i", "fio_o", ]
        verbose_name = "пассажир"
        verbose_name_plural = "пассажиры"

    def __str__(self):
        return self.passport


class ListOfServices(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="услуга", help_text="наименование услуги")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="цена", help_text="стоимость услуги")

    class Meta:
        ordering = ["name", ]
        verbose_name = "услуга"
        verbose_name_plural = "услуги"

    def __str__(self):
        return self.name


class Bus(models.Model):
    BRAND_CHOICES = (
        ("NF", "NEFAZ"),
        ("MS", "MERCEDES"),
        ("IK", "IKARUS"),
        ("MN", "MEN"),
    )
    state_number = models.CharField(max_length=10, unique=True, verbose_name="госномер",
                                    help_text="государственный регистрационный номер")
    brand = models.CharField(max_length=2, choices=BRAND_CHOICES, verbose_name="марка", help_text="марка автобуса")
    count_place = models.PositiveSmallIntegerField(validators=[MinValueValidator(20), MaxValueValidator(120)],
                                                   verbose_name="места", help_text="количество посадочных мест")


class BusDriver(models.Model):
    first_name = models.CharField(max_length=70, unique=True, verbose_name="фамилия", help_text="фамилия водителя")
    last_name = models.CharField(max_length=35, verbose_name="имя", help_text="имя водителя")
    use_bus = models.OneToOneField(Bus, null=True, on_delete=models.SET_NULL, verbose_name="автобус",
                                   help_text="используемый автобус")

    class Meta:
        verbose_name = "водитель"
        verbose_name_plural = "водители"

    def __str__(self):
        return self.first_name


class Services(models.Model):
    service = models.ManyToManyField(ListOfServices, verbose_name="услуги", help_text="заказанные услуги")

    class Meta:
        verbose_name = "допуслуга"
        verbose_name_plural = "допуслуги"

    def __str__(self):
        return self.service


class StartCity(models.Model):
    city_start = models.ForeignKey(Cities, on_delete=models.CASCADE, verbose_name="старт",
                                   help_text="город отправления")

    class Meta:
        verbose_name = "город"
        verbose_name_plural = "города"

    def __str__(self):
        return self.city_start


class FinishCity(models.Model):
    city_finish = models.ForeignKey(Cities, on_delete=models.CASCADE, verbose_name="финиш",
                                    help_text="город назначения")

    class Meta:
        verbose_name = "город"
        verbose_name_plural = "города"

    def __str__(self):
        return self.city_finish


class Route(models.Model):
    id_route = models.IntegerField(primary_key=True)
    city_start = models.ForeignKey(StartCity, on_delete=models.CASCADE, verbose_name="откуда",
                                   help_text="город отправления")
    city_finish = models.ForeignKey(FinishCity, on_delete=models.CASCADE, verbose_name="куда",
                                    help_text="город назначения")
    bus = models.ForeignKey(Bus, null=True, on_delete=models.SET_NULL, verbose_name="автобус",
                            help_text="назначенный автобус")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="цена",
                                help_text="стоимость проезда по маршруту")

    class Meta:
        verbose_name = "маршрут"
        verbose_name_plural = "маршруты"

    def __str__(self):
        return self.id_route


class Ticket(models.Model):
    id_ticket = models.IntegerField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="пассажир", help_text="пассажир")
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name="маршрут", help_text="маршрут поездки")
    services = models.OneToOneField(Services, null=True, on_delete=models.SET_NULL, verbose_name="услуги",
                                    help_text="дополнительные услуги")

    class Meta:
        verbose_name = "билет"
        verbose_name_plural = "билеты"

    def __str__(self):
        return self.id_ticket
