from django.db import models


class Criteria(models.Model):
    criteria = models.TextField(null=False, blank=False)


class Disease(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название болезни', null=False, blank=False)
    description = models.CharField(max_length=256, verbose_name='Описание болезни', null=False,
                                   blank=False)
    criteria = models.ManyToManyField(Criteria, related_name='diseases', verbose_name='Критерии')


class Code(models.Model):
    code = models.CharField(max_length=20, verbose_name='Код МКБ-10', null=False, blank=False)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='codes',
                                verbose_name='Болезнь', null=False, blank=False)



