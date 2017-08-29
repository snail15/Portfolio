# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..users.models import User

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=255)
    followers = models.ManyToManyField(User, related_name='topics_followed', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

class Pin(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField('jpg', upload_to='pins', blank=True)
    topic = models.ManyToManyField(Topic, related_name='pins', blank=True)
    created_by = models.ForeignKey(User, related_name='pins_created')
    liked_by = models.ManyToManyField(User, related_name='pins_liked', blank=True)
    saved_by = models.ManyToManyField(User, related_name='pins_saved', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

class BoardManager(models.Manager):
    def add_pin(self, id):
        errors = []
        try:
            pin_to_add = Pin.objects.get(id=id)
            self.pins.add(pin_to_add)
            self.save()
            return (True, pin_to_add)
        except Exception as problem:
            errors.append(problem)
            return (False, errors)
    def remove_pin(self, id):
        errors = []
        try:
            pin_to_remove = Pin.objects.get(id=id)
            self.pins.remove(pin_to_remove)
            self.save()
            return (True, pin_to_remove)
        except Exception as problem:
            errors.append(problem)
            return (False, errors)

class Board(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    topic = models.ManyToManyField(Topic, related_name="boards")
    pins = models.ManyToManyField(Pin, related_name='boards')
    created_by = models.ForeignKey(User, related_name='boards_created')
    liked_by = models.ManyToManyField(User,related_name='boards_liked', blank=True)
    saved_by = models.ManyToManyField(User, related_name='boards_saved',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BoardManager()

    def __unicode__(self):
        return self.title

class BaseComment(models.Model):
    author = models.ForeignKey(User, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PinComment(BaseComment):
    pin = models.ForeignKey(Pin, related_name='comments')

class BoardComment(BaseComment):
    board = models.ForeignKey(Board, related_name='comments')
