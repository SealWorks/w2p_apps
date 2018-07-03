# -*- coding: utf-8 -*-
from gluon import CAT, DIV, SPAN, LABEL, P, INPUT, A

class Form_render():
    def __init__(self, form, fields, *args):
        self.form = form
        self.fields = fields
        self.args = args
        self.holder = DIV(_class='row')

    def render(self):
        for id, label, controls, help in self.fields:
            self.holder.append(self.render_field(label, controls, help))
        return self.holder

    def render_field(self, label, controls, help):
        if isinstance(controls, basestring):
            return self._render_not_form(label, controls, help)
        tag = getattr(controls, 'tag', None)
        if tag == 'input/':
            return self._render_tag_input(label, controls, help)
        elif tag == 'textarea':
            return self._render_tag_textarea(label, controls, help)
        elif tag == 'span':
            return self._render_tag_span(label, controls, help)
        elif tag == 'div':
            return self._render_tag_div(label, controls, help)
        return self._render_tag_default(label, controls, help)

    def _render_tag_default(self, label, controls, help):
        row = DIV(_class="input-field col s12")
        self._append_basic_field(row, label, controls, help)
        return row

    def _render_tag_input(self, label, controls, help):
        type = controls['_class'] or controls['_type']
        if type == 'submit':
            return self._render_tag_input_submit(label, controls, help)
        elif type == 'date':
            return self._render_tag_input_date(label, controls, help)
        elif type == 'time':
            return self._render_tag_input_time(label, controls, help)
        elif type == 'upload':
            return self._render_tag_input_upload(label, controls, help)
        if any(x in type for x in ('boolean', 'delete', 'checkbox')):
            return self._render_tag_input_boolean(label, controls, help)
        return self._render_tag_default(label, controls, help)

    def _render_tag_input_boolean(self, label, controls, help):
        row = DIV(_class='input-field col s12')
        row.append(P(LABEL(controls, SPAN(label[0]))))
        return row

    def _render_tag_input_date(self, label, controls, help):
        row = DIV(_class='input-field col s12')
        controls.add_class('datepicker')
        self._append_basic_field(row, label, controls, help)
        return row

    def _render_tag_input_time(self, label, controls, help):
        row = DIV(_class='input-field col s12')
        controls.add_class('timepicker')
        self._append_basic_field(row, label, controls, help)
        return row

    def _render_tag_input_submit(self, label, controls, help):
        row = DIV(_class='col s12')
        controls.add_class('btn')
        self._append_basic_field(row, label, controls, help)
        return row

    def _render_tag_input_upload(self, label, controls, help):
        row = DIV(_class='file-field input-field col s12')
        btn = DIV(_class='btn')
        label.tag = 'SPAN'
        self._append_basic_field(btn, controls, label, help) # reverse label and controls
        row.append(btn)
        row.append(DIV(INPUT(_class='file-path validate', _type='text'), _class='file-path-wrapper'))
        return row

    def _render_tag_span(self, label, controls, help):
        row = DIV(_class='col s12')
        self._append_basic_field(row, controls, label, help)  # reverse label and controls
        return row

    def _render_tag_textarea(self, label, controls, help):
        row = DIV(_class='input-field col s12')
        controls.add_class('materialize-textarea')
        self._append_basic_field(row, label, controls, help)
        return row

    def _render_tag_div(self, label, controls, help):
        row = DIV(_class='col s12')
        label.tag = 'SPAN'
        row.append(DIV(
            DIV(label, controls[0], _class='btn'),
            DIV(INPUT(_class='file-path validate', _type='text'), _class='file-path-wrapper'),
            _class='file-field input-field'
        ))
        row.append(A(controls[3], _href=controls[1][1]['_href']))
        row.append(DIV(
            P(LABEL(controls[1][3], SPAN(controls[1][4][0])))
        ))
        return row

    def _append_basic_field(self, row, label, controls, help=None):
        row.append(controls)
        row.append(label)
        if help: row.append(help)

    def _render_not_form(self, label, controls, help):
        row = DIV(_class='col s12')
        label.tag = 'SPAN'
        self._append_basic_field(row, controls, label, help) #reverse label and controls
        return row


def formstyle_materialize(form, fields, *args, **kwargs):
    # debug prints
    # print('--'*20)
    # print(form)
    # for i in fields:
    #     print(i)
    # print('args - ', args)
    # print('kwargs - ', kwargs)
    return Form_render(form, fields, args).render()

