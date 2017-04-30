# coding: utf-8
from __future__ import unicode_literals

from .constructors import Relation


__all__ = [
    'gender_relation',
    'number_relation',
    'case_relation',
    'gnc_relation'
]


class gender_relation(Relation):
    def __call__(self, form, other):
        if form.number.plural and other.number.plural:
            return True

        (form_male, form_female, form_neutral,
         form_bi, form_general) = form.gender
        (other_male, other_female, other_neutral,
         other_bi, other_general) = other.gender
        return (
            (form_male and other_male)
            or (form_female and other_female)
            or (form_neutral and other_neutral)
            or (form_bi and (other_male or other_female))
            or (other_bi and (form_male or form_female))
            or form_general
            or other_general
        )


class number_relation(Relation):
    def __call__(self, form, other):
        (form_single, form_plural,
         form_only_single, form_only_plural) = form.number
        (other_single, other_plural,
         other_only_single, other_only_plural) = other.number

        return (
            (form_single and other_single)
            or (form_plural and other_plural)
            or (form_only_single and other_single)
            or (form_only_plural and other_plural)
            or (other_only_single and form_single)
            or (other_only_plural and form_plural)
        )


class case_relation(Relation):
    def __call__(self, form, other):
        form_mask, form_fixed = form.case
        other_mask, other_fixed = other.case
        return (
            form_mask == other_mask
            or form_fixed
            or other_fixed
        )


class gnc_relation(gender_relation, number_relation, case_relation):
    def __call__(self, form, other):
        return (
            gender_relation.__call__(self, form, other)
            and number_relation.__call__(self, form, other)
            and case_relation.__call__(self, form, other)
        )
