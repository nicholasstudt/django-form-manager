from django.db import models
from django.utils.translation import ugettext_lazy as _

#/* This is the postgresql schema for FormBuilder >= 0.65 */
#
#create sequence "form_validate_seq";
#create table "form_validate" (
#	"id" integer primary key not null default nextval( 'form_validate_seq' ),
#	"name" 	varchar not null,
#	"regex" varchar,
#	"func" 	varchar
#);
#
#create sequence "form_types_seq";
#create table "form_types" (
#	"id" 	integer primary key not null default nextval( 'form_types_seq' ),
#	"type" 		varchar,
#	"name" 		varchar default '0',
#	"value" 	varchar default '0',
#	"row" 		varchar default '0',
#	"col" 		varchar default '0',
#	"size" 		varchar default '0',
#	"max" 		varchar default '0',
#	"checkd" 	varchar default '0',
#	"read" 		varchar default '0',
#	"mult" 		varchar default '0',
#	"tab" 		varchar default '0',
#	"css" 		varchar default '0',
#	"src" 		varchar default '0',
#	"alt" 		varchar default '0' 
#);
#
#create sequence "form_data_seq";
#create table "form_data" (
#	"id" integer primary key not null default nextval( 'form_data_seq' ),
#	"active" 				boolean,
#	"send_email"			boolean,
#	"page_count" 			integer,
#	"number_of_elements" 	integer default '0',
#	"created" 				timestamp with time zone,
#	"modified" 				timestamp with time zone,
#	"start_date" 			timestamp with time zone,
#	"stop_date" 			timestamp with time zone,
#	"ident" 				varchar not null, -- name of form and uri 
#	"name" 					varchar, -- display name of form (pretty)
#	"email_address" 		varchar not null, -- to send results to
#	"email_subject" 		varchar,
#	"redirect_cancel" 		varchar not null, -- for cancel and conclusion
#	"redirect_confirm" 		varchar,
#	"confirm_page"			varchar,
#	"frame" 				varchar,
#	"store_as" 				varchar,
#	"send_as" 				varchar,
#	"filename"				varchar,
#	"description" 			text,
#);
#
#create sequence "form_element_seq";
#create table "form_element" (
#	"id" integer primary key not null default nextval( 'form_element_seq' ),
#	"isdefault"				boolean default 'false',
#	"required" 				boolean default 'false',
#	"checked" 				boolean default 'false',
#	"readonly" 				boolean default 'false',
#	"multiple" 				boolean default 'false',
#	"form_data_id" 			integer, -- form_data.id
#	"form_types_id" 		integer, -- form_types.id
#	"form_validate_id" 		integer, -- form_validate.id
#	"max_length" 			integer,
#	"tab_index" 			integer,
#	"row_count" 			integer, 
#	"col_count" 			integer,
#	"size_count" 			integer,
#	"page_number" 			integer,
#	"created" 				timestamp with time zone,
#	"modified" 				timestamp with time zone,
#	"question_number" 		real,
#	"name" 					varchar not null,
#	"value" 				varchar,
#	"css_class" 			varchar,
#	"src"				 	varchar,
#	"addition_params" 		text,
#	"alt"				 	text,
#	"pre_text" 				text,
#	"post_text" 			text,
#	"error_msg" 			text
#);

class Form(models.Model):
    """
    Form 
    """

    STORE_CHOICES = (
        (1, _('Do not save')),
        (2, _('CSV File')),
        (3, _('HTML File')),
        (4, _('Text File')),
    )

    SEND_CHOICES = (
        (1, _('Inline Text Only')),
        (2, _('Attached CSV')),
        (3, _('Attached HTML')),
        (4, _('Attached Text')),
    )

    name = models.CharField(max_length=250) 
    owner = models.EmailField(_('E-mail'))
    abstract = models.TextField()
    active = models.BooleanField(_('active'), default=True)
    start_date = models.DateTimeField(_('start date'))
    stop_date = models.DateTimeField(_('stop date'))

    created = models.DateTimeField(_('created'), auto_now=True, editable=False)
    modified = models.DateTimeField(_('last modified'), auto_now=True, editable=False)

    redirect = models.URLField(_('Completed Page'),)

    slug = models.SlugField(_('slug'),unique=True)

    store = models.IntegerField(_('Store Locally As'), choices=STORE_CHOICES, default=1)
    send = models.IntegerField(_('Send Data As'), choices=SEND_CHOICES, default=1)


class Element(models.Model):
    """
    Elements 
    """

    TYPE_CHOICES = (
        ('raw', _('raw')),
        ('button', _('button')),
        ('checkbox', _('checkbox')),
        ('file', _('file')),
        ('hidden', _('hidden')),
        ('image', _('image')),
        ('password', _('password')),
        ('radio', _('radio')),
        ('reset', _('reset')),
        ('select', _('select')),
        ('submit', _('submit')),
        ('text', _('text')),
    )

    REQUIRE_CHOICES = (
        ('none', _('None')),
        ('date', _('Date')),
        ('email', _('E-mail')),
        ('not empty', _('Not Empty')),
        ('number', _('Number')),
        ('text', _('Text')),
        ('time', _('Time')),
        ('url', _('URL')),
    )

    form = models.ForeignKey(Form)

    page = models.IntegerField(default=1)
    order = models.IntegerField()

    label = models.CharField(max_length=250) 
    slug = models.SlugField()

    type = models.CharField(_('Type'), max_length=20, choices=TYPE_CHOICES)
    require = models.CharField(_('Requirements'), max_length=20, 
                               choices=REQUIRE_CHOICES, default='none')

    value = models.TextField()
