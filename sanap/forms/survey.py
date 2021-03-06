from datetime import datetime
from flask import g
from flask.ext import wtf
from flask.ext.mongoengine.wtf import model_form
from flask.ext.uploads import UploadSet, AllExcept, SCRIPTS, EXECUTABLES

from sanap.models import Survey
from sanap.forms.fields import *
from sanap.model_data import *


files = UploadSet('files', AllExcept(SCRIPTS + EXECUTABLES))
_SurveyForm = model_form(Survey)
FILE_FIELDS = ('assessment_subnational_files', 'action_plan_files',
               'part4_files', 'part2_files', 'part1_files', 'part3_files',)


class SectorsForm(wtf.Form):

    adaptation_national = MultiTextField('Adaptation at national level')

    adaptation_sub_national = MultiTextField('Adaptation at sub-national level (e.g. provinces, regions)')

    adaptation_local = MultiTextField('Adaptation at local or city-level')

    priority_sectors = MultiCheckboxField('Priority sectors/areas for implementation')

    examples = MultiTextAreaField('Please provide some examples if you have indicated that the adaptation state is 4, 5 or 6')


class MainInstrumentsForm(wtf.Form):

    agriculture = MultiCheckboxField()

    forestry = MultiCheckboxField()

    biodiversity = MultiCheckboxField()

    human_health = MultiCheckboxField()

    water = MultiCheckboxField()

    marine_fisheries = MultiCheckboxField()

    coastal_areas = MultiCheckboxField()

    mountain_areas = MultiCheckboxField()

    tourism = MultiCheckboxField()

    transport = MultiCheckboxField()

    energy = MultiCheckboxField()

    built_environment = MultiCheckboxField()

    spatial_planning = MultiCheckboxField()

    disaster_risk_reduction  = MultiCheckboxField()

    civil_protection = MultiCheckboxField()

    industry = MultiCheckboxField()

    business_services = MultiCheckboxField()

    financial_insurance = MultiCheckboxField()

    cultural_heritage = MultiCheckboxField()


class InvolmentForm(wtf.Form):

    information_given =  MultiCheckboxField()

    information_gathered = MultiCheckboxField()

    consultation = MultiCheckboxField()

    active_involvement = MultiCheckboxField()

    partnerships = MultiCheckboxField()

    empowerment = MultiCheckboxField()


class SectorsAssessmentsForm(wtf.Form):

    national = MultiCheckboxField('covered in the national assessment')

    public_sector = MultiCheckboxField('covered in sector-based assessment led by ministries in charge  of this sector')

    private_sector = MultiCheckboxField('covered in sector-based assessment led by private sector or industry groups')


class SurveyForm(_SurveyForm):

    draft = CustomBoolean(default=True)

    lead_organisation = wtf.TextAreaField(Q['lead_organisation'])

    organisations = Tagit(Q['organisations'])

    country = wtf.TextField()

    public_awareness = CustomRadioField(Q['1'], choices=AGREEMENT,
        validators=[wtf.validators.optional()])

    adaptation_need = CustomRadioField(Q['2'], choices=AGREEMENT,
        validators=[wtf.validators.optional()])

    triggers = MultiCheckboxField(Q['3'], choices=TRIGGERS,
        validators=[wtf.validators.optional()])

    willingness = CustomRadioField(Q['4'], choices=LEVEL,
        validators=[wtf.validators.optional()])

    knowledge = CustomRadioField(Q['5'], choices=AGREEMENT,
        validators=[wtf.validators.optional()])

    uncertainties = CustomRadioField(Q['6'], choices=AGREEMENT,
        validators=[wtf.validators.optional()])

    objectives = CustomRadioField(Q['7'], choices=AGREEMENT,
        validators=[wtf.validators.optional()])

    integration = CustomRadioField(Q['8'], choices=AGREEMENT,
        validators=[wtf.validators.optional()])

    integration_examples = wtf.TextAreaField(Q['provide_examples'])

    mitigation = CustomRadioField(Q['9'], choices=AGREEMENT,
        validators=[wtf.validators.optional()])

    mitigation_examples = wtf.TextAreaField(Q['provide_examples'])

    transnational_cooperation = CustomRadioField(Q['10'], choices=AGREEMENT,
        validators=[wtf.validators.optional()])

    transnational_cooperation_examples = wtf.TextAreaField(Q['provide_examples'])

    barriers = MultiCheckboxField(Q['11'], choices=BARRIERS,
        validators=[wtf.validators.optional()])

    part1_comments = wtf.TextAreaField(Q['p1comments'])

    part1_files =  CustomFileField(Q['files'],
       validators=[wtf.file_allowed(files, 'Document is not valid')])

    ## part2

    process_stage = CustomRadioField(Q['12'], choices=PROCESS_STAGE,
        validators=[wtf.validators.optional()])

    horizontal_integration = CustomRadioField(Q['13'], choices=EFFECTIVENESS,
        validators=[wtf.validators.optional()])

    vertical_integration = CustomRadioField(Q['14'], choices=EFFECTIVENESS,
        validators=[wtf.validators.optional()])

    horizontal_coordination = wtf.TextAreaField(Q['h_coordination'])

    vertical_coordination = wtf.TextAreaField(Q['v_coordination'])

    crucial_in_coordination = wtf.TextAreaField(Q['c_coordination'])

    challenging_in_coordination = wtf.TextAreaField(Q['m_coordination'])

    assessment = CustomRadioField(Q['16'], choices=STATUS,
        validators=[wtf.validators.optional()])

    assessment_scale = MultiCheckboxField(Q['if_yes'], choices=ASSESSMENT_SCALE,
        validators=[wtf.validators.optional()])

    assessment_subnational_info = wtf.TextAreaField(Q['text'])

    assessment_subnational_files = CustomFileField(Q['files'],
       validators=[wtf.file_allowed(files, 'Document is not valid')])

    sectors_assessments = wtf.FormField(SectorsAssessmentsForm,label=Q['17'],
        widget=MatrixCheckboxWidget(data=SECTORS_EXTENDED, label=Q['17'],
                     title='Coverage /<br />Sectors', id='sectors-assessments'))

    assessment_coordination = wtf.TextAreaField(Q['coordination'])

    assessment_methodological_approach = wtf.TextAreaField(Q['meth_approach'])

    change_adaptation_costs = wtf.TextAreaField(Q['19'])

    needed_info = MultiCheckboxField(Q['20'], choices=NEEDED_INFO,
        validators=[wtf.validators.optional()])

    assessment_update = CustomRadioField(Q['21'], choices=PLANNING,
        validators=[wtf.validators.optional()])

    assessment_update_info = wtf.TextAreaField(Q['req_regular'])

    adaptation_options = CustomRadioField(Q['22'], choices=STATUS,
        validators=[wtf.validators.optional()])

    adaptation_scale = MultiCheckboxField(Q['if_yes'], choices=ADAPTATION_SCALE,
        validators=[wtf.validators.optional()])

    identified_options = MultiCheckboxField(Q['23'], choices=IDENTIFIED_OPTIONS,
        validators=[wtf.validators.optional()])

    adaptation_actions = MultiCheckboxField(Q['24'], choices=ADAPTATION_ACTIONS,
        validators=[wtf.validators.optional()])

    prioritised_options = CustomRadioField(Q['25'], choices=STATUS,
        validators=[wtf.validators.optional()])

    options_methodological = wtf.TextAreaField(Q['26'])

    action_plan_info = wtf.TextAreaField(Q['27'])

    action_plan_files = CustomFileField(Q['files'],
       validators=[wtf.file_allowed(files, 'Document is not valid')])

    practice_example = wtf.TextAreaField(Q['28'])

    integrating_plans = wtf.TextAreaField(Q['29'])

    monitoring_state = CustomRadioField(Q['30a'], choices=STATE_OF_WORK,
                                        validators=[wtf.validators.optional()])

    reporting_state = CustomRadioField(Q['30b'], choices=STATE_OF_WORK,
                                        validators=[wtf.validators.optional()])

    evaluation_state = CustomRadioField(Q['30c'], choices=STATE_OF_WORK,
                                        validators=[wtf.validators.optional()])

    part2_comments = wtf.TextAreaField(Q['p2comments'])

    part2_files = CustomFileField(Q['files'],
       validators=[wtf.file_allowed(files, 'Document is not valid')])

    ## part3

    sectors = wtf.FormField(SectorsForm, widget=MatrixCheckboxWidget(
        data=SECTORS, id='sectors', title='Levels /<br />Sectors'))

    instruments = CustomRadioField(Q['32'], choices=INSTRUMENTS,
        validators=[wtf.validators.optional()])

    main_instruments = wtf.FormField(MainInstrumentsForm,
        label=Q['33'],
        widget=MatrixCheckboxWidget(data=MAIN_INSTRUMENTS, id='main-instruments',
                                    title="Sectors / Instruments",
                                    label=Q['33']))

    main_instruments_considered = wtf.TextAreaField(Q['34'])

    financing_mechanisms = wtf.FormField(MainInstrumentsForm,
        label=Q['35'],
        widget=MatrixCheckboxWidget(data=FINANCING_MECHANISMS, label=Q['35'],
                                    id='financing-mechanisms',
                                    title="Financing mechanisms / Sectors"))

    part3_comments = wtf.TextAreaField(Q['p3comments'])

    part3_files = CustomFileField(Q['files'],
       validators=[wtf.file_allowed(files, 'Document is not valid')])

    transboundary_issues = wtf.TextAreaField(Q['36'])

    regions_coordination = wtf.TextAreaField(Q['37'])

    ## part 4

    stakeholders_involved = CustomRadioField(Q['38'], choices=YES_NO,
        validators=[wtf.validators.optional()])

    stakeholders_contribution = CustomRadioField(Q['39'],
                                         choices=STAKEHOLDERS_CONTRIBUTION,
                                         validators=[wtf.validators.optional()])

    development_involvement = wtf.FormField(InvolmentForm,
        label=Q['development_phase'],
        widget=MatrixCheckboxWidget(data=INVOLVEMENT, id='development-involvement',
                                    label=Q['development_phase'],
                                    title='Stakeholders / Format of involvement'))

    implementation_involvement = wtf.FormField(InvolmentForm,
        label=Q['implementation_phase'],
        widget=MatrixCheckboxWidget(data=INVOLVEMENT, id='implementation-involvement',
                                    label=Q['implementation_phase'],
                                    title='Stakeholders / Format of involvement'))

    monitoring_involvement = wtf.FormField(InvolmentForm,
        label=Q['monitor_evaluate_phase'],
        widget=MatrixCheckboxWidget(data=INVOLVEMENT, id='monitoring-involvement',
                                    label=Q['monitor_evaluate_phase'],
                                    title='Stakeholders / Format of involvement'))

    stakeholders_success = wtf.TextAreaField(Q['41'])

    part4_comments = wtf.TextAreaField(Q['p4comments'])

    part4_files = CustomFileField(Q['files'],
       validators=[wtf.file_allowed(files, 'Document is not valid')])

    ## part 5

    next_step_vulnerability = wtf.TextAreaField(Q['risk_assessments'])

    next_step_legislation = wtf.TextAreaField(Q['legislation'])

    next_step_implementation = wtf.TextAreaField(Q['implementation'])

    next_step_monitoring = wtf.TextAreaField(Q['monitoring'])

    next_step_strategy = wtf.TextAreaField(Q['updating'])

    next_step_others = wtf.TextAreaField(Q['others'])

    adaptation_key_issues = wtf.TextAreaField(Q['43'])

    adaptation_support_eu_level = wtf.TextAreaField(Q['44'])

    feedback = wtf.TextAreaField(Q['feedback'])

    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        expand_choices(self.triggers)
        expand_choices(self.barriers)
        expand_choices(self.assessment_scale)
        expand_choices(self.needed_info)
        expand_choices(self.adaptation_scale)
        expand_choices(self.identified_options)
        expand_choices(self.adaptation_actions)

    def get_fields(self, exclude=[]):
        for field in self:
            if field.name not in exclude:
                yield field

    def save(self, survey):
        user = g.user._get_current_object()

        survey = survey or Survey()
        survey.user = user
        survey.country = user.country
        survey.for_eea = False if user.invitee else True
        survey.draft = True if self.data['draft'] else False

        for key, value in self.data.items():
            if key in ('organisations',
                       'country', 'for_eea', 'user', 'draft') + FILE_FIELDS:
                continue
            if value:
                setattr(survey, key, value)
            else:
                setattr(survey, key, None)

        organisations = self.data['organisations'].strip()
        if organisations:
            survey.organisations = list(set(organisations.split(',')))
        else:
            survey.organisations = None

        for field_name in FILE_FIELDS:
            uploaded = self.data[field_name]
            if uploaded:
                value = getattr(survey, field_name, False) or []
                new_values = [files.save(upfile) for upfile in uploaded]
                value.extend(new_values)
                setattr(survey, field_name, value)

        if not survey.date_created:
            survey.date_created = datetime.now()
        survey.date_saved = datetime.now()

        survey.save()
        return survey
