from flask.ext import wtf
from libs import markup
from libs.markup import oneliner as e


class MultiCheckboxField(wtf.SelectMultipleField):

    def __init__(self, *args, **kwargs):
        self.pre_validate_option = kwargs.pop('pre_validate', False)
        super(MultiCheckboxField, self).__init__(*args, **kwargs)

    def pre_validate(self, form):
        if self.pre_validate_option:
            return super(MultiCheckboxField, self).pre_validate(self, form)
        return True

    widget = wtf.widgets.ListWidget(prefix_label=False)

    option_widget = wtf.widgets.CheckboxInput()


class CustomFileField(wtf.FileField):

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            filestorage = valuelist[0]
            filestorage.filename = filestorage.filename.lower()
            self.data = filestorage
        else:
            self.data = ''


class CustomRadioField(wtf.RadioField):

    def process_formdata(self, valuelist):
        if not valuelist:
            self.data = None
        else:
            self.data = valuelist[0]


class CustomBoolean(wtf.BooleanField):

    def process_formdata(self, valuelist):
        if bool(valuelist[0]):
            self.data = '1'
        else:
            self.data = ''


# class TagitWidget(wtf.widgets.TextInput):

#     def __call__(self, field, **kwargs):
#         # import pdb; pdb.set_trace()
#         kwargs.setdefault('id', field.id)
#         kwargs.setdefault('type', self.input_type)
#         if 'value' not in kwargs:
#             kwargs['value'] = field._value()
#         return HTMLString('<input %s>' % self.html_params(name=field.name, **kwargs))


class Tagit(wtf.TextField):

    # widget = TagitWidget()

    def process_data(self, value):
        self.data = ""


def expand_choices(field):
    choices = list(field.choices)
    if field.data:
        for i in field.data:
            if i not in [c[0] for c in choices]: choices.append((i, i))
        field.choices = tuple(choices)
    return field


class MatrixBaseWidget():

    def update_data(self, form_field, data):
        for value in form_field.data.values():
            if not value: continue
            for item in value:
                if item not in [i[0] for i in data]: data.append((item, item))
        return data

    def update_keys(self, form_field, data_keys):
        for value in form_field.data.values():
            if not value: continue
            for item in value:
                if item not in data_keys: data_keys.append(item)
        return data_keys


class MatrixCheckboxWidget(MatrixBaseWidget):

    def __init__(self, data, *args, **kwargs):
        self.data = data
        self.id = kwargs.pop('id', '')

    def __call__(self, form_field, **kwargs):
        fields = [f for f in form_field if 'csrf_token' not in f.id ]
        data_keys = [i[0] for i in self.data]
        data_keys = self.update_keys(form_field, data_keys)
        self.data = self.update_data(form_field, self.data)

        page = markup.page()
        page.table(id=self.id, class_='matrix')

        page.thead()
        page.tr()
        page.th('', class_='category-left')
        for i, f in enumerate(fields):
            page.th(f.label.text, class_=i%2 and 'odd' or 'even')
        page.tr.close()
        page.thead.close()

        page.tbody()
        page.tr()
        page.td(e.div(data_keys), class_='category-left')
        for i, field in enumerate(fields):
            field.choices = [(k, v) for k, v in self.data]
            odd_even = i%2 and 'odd' or 'even'
            page.td(field(**kwargs), class_=('check-column %s' % odd_even))
        page.tr.close()

        page.tbody.close()
        page.table.close()

        return page
