from django.db import models
from django.conf import settings

from thing.models import Thing

import hashlib

#
FEATURES = ((0, 'Strength'), (1, 'Dexterity'), (2, 'Intuition'), 
            (3, 'Health'), (4, 'Swords'), (5, 'Axes'),
            (6, 'Knives'), (7, 'Knives'), (8, 'Shields'), 
            (9, 'Protection head'), (10, 'Protection breast'), 
            (11, 'Protection zone'), (12, 'Protection leg'), (13, 'Damage min'), 
            (14, 'Damage max'), (15, 'Accuracy'), (16, 'Dodge'), 
            (17, 'Devastate'), (18, 'Durability'), (19, 'Block break'), 
            (20, 'Armor break'), (21, 'Hp'),)

class HeroImage(models.Model):
    image = models.ImageField(upload_to='upload/heroimages')
    is_art = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'HeroImage'
        
    def __unicode__(self):
        return str(self.image).split('/')[-1]
        
    def thumbnail(self):
        url = '%s%s' % (settings.MEDIA_URL, self.image)
        return '<img src="%s" width="%s" height="%s" />' % (url, '', '')
    thumbnail.short_description = 'Image'
    thumbnail.allow_tags = True

class HeroSkill(models.Model):
    name = models.CharField(max_length=32, unique=True)
    
    class Meta:
        db_table = 'HeroSkill'
        
    def __unicode__(self):
        return self.name

class SkillFeature(models.Model):
    heroskill = models.ForeignKey(HeroSkill)
    feature = models.IntegerField(default=0, choices=FEATURES)
    plus = models.IntegerField()
    
    class Meta:
        db_table = 'SkillFeature'
        unique_together = (('heroskill', 'feature'),)
        
    def __unicode__(self):
        return '%s %s' % (FEATURES[self.feature][1], self.plus)
            
class Hero(models.Model):
    login = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    email = models.EmailField(max_length=64, unique=True)
    experience = models.IntegerField(default=0)
    money = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    money_art = models.DecimalField(max_digits=10, decimal_places=2, 
                                    default=0.0)
    location = models.CharField(max_length=32, blank=True)
    level = models.IntegerField(default=0)
    image = models.ForeignKey(HeroImage, null=True, blank=True)
    
    number_of_wins = models.IntegerField(default=0)
    number_of_losses = models.IntegerField(default=0)
    number_of_draws = models.IntegerField(default=0)
    
    hp = models.IntegerField(default=20)
    
    strength = models.IntegerField(default=3)
    dexterity = models.IntegerField(default=3)
    intuition = models.IntegerField(default=3)
    health = models.IntegerField(default=3)
    swords = models.IntegerField(default=0)
    axes = models.IntegerField(default=0)
    knives = models.IntegerField(default=0)
    clubs = models.IntegerField(default=0)
    shields = models.IntegerField(default=0)
    
    date_of_birthday = models.DateField()
#
    SEXS = ((0, 'Male'), (1, 'Female'))
    sex = models.SmallIntegerField(default=0, choices=SEXS)
    country = models.CharField(max_length=32, blank=True)
    city = models.CharField(max_length=32, blank=True)
    name = models.CharField(max_length=64, blank=True)
    about = models.TextField(blank=True)
    
    skills = models.ManyToManyField(HeroSkill, through='HeroHeroSkill')
    things = models.ManyToManyField(Thing, through='HeroThing')
    
    class Meta:
        db_table = 'Hero'
        verbose_name_plural = 'Heroes'
    
    def __unicode__(self):
        return u'%s [%s]' % (self.login, self.level)
    
    def save(self):
        if not self.id:
            self.password = hashlib.sha1(self.password).hexdigest()
        else:
            if self.password != Hero.objects.get(id=self.id).password:
                self.password = hashlib.sha1(self.password).hexdigest()
        super(Hero, self).save()

class HeroFeature(models.Model):

    hero = models.ForeignKey(Hero)
       
    strength = models.CharField(max_length=32, null=True)
    dexterity = models.CharField(max_length=32, null=True)
    intuition = models.CharField(max_length=32, null=True)
    health = models.CharField(max_length=32, null=True)
    
    swords = models.CharField(max_length=32, null=True)
    axes = models.CharField(max_length=32, null=True)
    knives = models.CharField(max_length=32, null=True)
    clubs = models.CharField(max_length=32, null=True)
    shields = models.CharField(max_length=32, null=True)
    
    protection_head = models.CharField(max_length=32, null=True)
    protection_breast = models.CharField(max_length=32, null=True)
    protection_zone = models.CharField(max_length=32, null=True)
    protection_leg = models.CharField(max_length=32, null=True)
    
    damage_min = models.CharField(max_length=32, null=True)
    damage_max = models.CharField(max_length=32, null=True)
    
    accuracy = models.CharField(max_length=32, null=True)
    dodge = models.CharField(max_length=32, null=True)
    devastate = models.CharField(max_length=32, null=True)
    durability = models.CharField(max_length=32, null=True)
    block_break = models.CharField(max_length=32, null=True)
    armor_break = models.CharField(max_length=32, null=True)
    
    hp = models.CharField(max_length=32, null=True)

    class Meta:
        db_table = 'HeroFeature'
        
class HeroHeroSkill(models.Model):
    hero = models.ForeignKey(Hero)
    skill = models.ForeignKey(HeroSkill)
    level = models.IntegerField()
    
    def __unicode__(self):
        return '%s %s' % (self.skill, self.level)
    
    class Meta:
        db_table = 'HeroHeroSkill'
        unique_together = (('hero', 'skill'),)

class HeroThing(models.Model):
    hero = models.ForeignKey(Hero)
    thing = models.ForeignKey(Thing)
    stability_all = models.IntegerField()
    stability_left = models.IntegerField()
    dressed = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s %s' % (self.hero, self.thing)
    
    class Meta:
        db_table = 'HeroThing'

class HeroThingFeature(models.Model):
    herothing = models.ForeignKey(HeroThing)
    feature = models.IntegerField(default=0, choices=FEATURES)
    plus = models.IntegerField()
    
    def __unicode__(self):
        return self.herothing.hero
    
    def hero(self):
        return self.herothing.hero
    
    def thing(self):
        return self.herothing.thing
    
    class Meta:
        db_table = 'HeroThingFeature'
        unique_together = (('herothing', 'feature'),)