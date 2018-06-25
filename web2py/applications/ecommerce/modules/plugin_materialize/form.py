# -*- coding: utf-8 -*-
from gluon import CAT, DIV, SPAN, INPUT, I, LABEL, P

def formstyle_materialize(form, fields, *args, **kwargs):
    form.add_class('row')
    parent = CAT(_class='col s12')
    for id, label, controls, help in fields:
        type = controls['_type']
        _input_field = type == 'checkbox' and P(_class="col s12") or DIV(_class='input-field col s12')
        if type == 'checkbox':
            if controls['_value'] == 'on': controls['_checked'] = "checked"
            _input_field.append(LABEL(
                controls,
                SPAN(label.components[0])
            ))
        elif type == 'submit':
            controls.add_class('btn')
        if len(_input_field) < 1:
            _input_field.append(controls)
            _input_field.append(label)
        parent.append(_input_field)
    return parent

