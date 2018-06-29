# -*- coding: utf-8 -*-
from gluon import CAT, DIV, SPAN, LABEL, P

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
        if not isinstance(controls, DIV):
            return self.render_not_form(label, controls, help)
        if controls.tag == 'input/':
            return self.render_tag_input(label, controls, help)
        elif controls.tag == 'textarea':
            return self.render_tag_textarea(label, controls, help)
        elif controls.tag == 'span':
            return self.render_tag_span(label, controls, help)
        return CAT()

    def render_tag_input(self, label, controls, help):
        type = controls['_type']
        if type == 'text':
            return self.render_tag_input_text(label, controls, help)
        elif type == 'submit':
            return self.render_tag_input_submit(label, controls, help)
        elif type == 'checkbox':
            return self.render_tag_input_checkbox(label, controls, help)
        return self.render_tag_input_default(label, controls, help)

    def _append_basic_field(self, _row, label, controls, help=None):
        _row.append(controls)
        _row.append(label)
        if help: _row.append(help)

    def render_tag_input_checkbox(self, label, controls, help):
        _row = DIV(_class="input-field col s12")
        _row.append(P(LABEL(controls, SPAN(label.components[0]))))
        return _row

    def render_tag_input_default(self, label, controls, help):
        _row = DIV(_class="input-field col s12")
        self._append_basic_field(_row, label, controls, help)
        return _row

    def render_tag_input_submit(self, label, controls, help):
        _row = DIV(_class="col s12")
        controls.add_class('btn')
        self._append_basic_field(_row, label, controls, help)
        return _row

    def render_tag_input_text(self, label, controls, help):
        _class = controls['_class']
        if _class == "date":
            return self.render_tag_input_text_date(label, controls, help)
        if _class == "time":
            return self.render_tag_input_text_time(label, controls, help)
        return self.render_tag_input_default(label, controls, help)

    def render_tag_input_text_date(self, label, controls, help):
        _row = DIV(_class="input-field col s12")
        controls.add_class('datepicker')
        self._append_basic_field(_row, label, controls, help)
        return _row

    def render_tag_input_text_time(self, label, controls, help):
        _row = DIV(_class="input-field col s12")
        controls.add_class('timepicker')
        self._append_basic_field(_row, label, controls, help)
        return _row

    def render_tag_span(self, label, controls, help):
        _row = DIV(_class="col s12")
        self._append_basic_field(_row, controls, label, help)  # reverse label and controls
        return _row

    def render_tag_textarea(self, label, controls, help):
        _row = DIV(_class="input-field col s12")
        controls.add_class('materialize-textarea')
        self._append_basic_field(_row, label, controls, help)
        return _row

    def render_not_form(self, label, controls, help):
        _row = DIV(_class="col s12")
        label.tag = 'SPAN'
        self._append_basic_field(_row, controls, label, help) #reverse label and controls
        return _row


def formstyle_materialize(form, fields, *args):
    print('--'*20)
    f = Form_render(form, fields, args)
    return f.render()
