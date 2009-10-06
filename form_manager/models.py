from django.db import models
from django.utils.translation import ugettext_lazy as _

class ActiveManager(models.Manager):
    """Returns published posts that are not in the future.""" 
    
    def active(self, **kwargs):
        return self.get_query_set().filter(active=True, **kwargs)


class Form(models.Model):
    """
    Forms
    """

    STORE_CHOICES = (
        (0, _('Do not save')),
        (1, _('CSV File')),
#        (2, _('HTML File')),
#        (3, _('Text File')),
    )

    SEND_CHOICES = (
        (0, _('Do Not Send')),
        (1, _('Inline Text Only')),
#        (2, _('Attached CSV')),
#        (3, _('Attached HTML')),
#        (4, _('Attached Text')),
    )

    name = models.CharField(max_length=250) 
    owner = models.EmailField(_('E-mail'))
    abstract = models.TextField()
    active = models.BooleanField(_('active'), default=True)

    # I don't recall this ever really being used. 
    #start_date = models.DateTimeField(_('start date'))
    #stop_date = models.DateTimeField(_('stop date'))

    redirect = models.URLField(_('Completed Page'),)

    slug = models.SlugField(_('slug'),unique=True)

    store = models.IntegerField(_('Store Locally As'), choices=STORE_CHOICES, default=0)
    send = models.IntegerField(_('Send Data As'), choices=SEND_CHOICES, default=1)
    
    objects = ActiveManager()

    def __unicode__(self):
        return( u'%s' % self.name )

    def get_absolute_url(self):
        return ('form_manager_form', (), { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)

class Element(models.Model):
    """
    Form Elements 
    """

    TYPE_CHOICES = (
        ('raw', _('raw')), 
        #('button', _('button')), # Use <button>
        ('checkbox', _('checkbox')),
        ('file', _('file')),
        ('hidden', _('hidden')),
        ('honeypot', _('honeypot')),
        ('image', _('image')),  # Use <button>
        ('password', _('password')),
        ('radio', _('radio')),
        ('reset', _('reset')), # Use <button>
        ('select', _('select')), 
        ('submit', _('submit')), # Use <button>
        ('text', _('text')),
        ('textarea', _('textarea')),
    )

    REQUIRE_CHOICES = (
        ('none', _('None')),
        ('date', _('Date')),
        ('email', _('E-mail')),
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

    value = models.TextField(blank=True)

    class Meta:
        ordering = ['page', 'order']


    def __unicode__(self):
        return( u'%s.%s: %s' % (self.page, self.order, self.label) )


