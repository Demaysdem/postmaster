from django.db import models


class MessageStatusChoices(models.TextChoices):
    WAITING = "WAITING", "В ожидании"
    SUCCESSFUL = "SUCCESSFUL", "Успешно"
    FAILED = "FAILED", "Провалено"
    DELETED = "DELETED", "Удаленно"


class MessageTypeChoices(models.TextChoices):
    REGULAR = "REGULAR", "Стандарт"
    ADS = "ADS", "Реклама"
    MARKED = "MARKED", "Маркер"
