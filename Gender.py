from enum import Enum


class Gender(Enum):
    FEMININE = 'fem'
    MASCULINE = 'masc'
    UNISEX = 'uni'


def get_gender(feminine, masculine):
    if feminine is not None and masculine is not None:
        return Gender.UNISEX.value
    if feminine is not None:
        return Gender.FEMININE.value
    if masculine is not None:
        return Gender.MASCULINE.value
