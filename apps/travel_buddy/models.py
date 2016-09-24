from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.
class UserManager(models.Manager):
	def login(self, username, password):
		error_msg = []
		if len(username) < 1 or len(password) < 1:
			error_msg.append('empty fields')
			return (False, error_msg)
		else:
			user = User.objects.filter(username = username)
			if user:
				check_pass = user[0].password
				if password == check_pass :
					return (True,'success')
				else:
					error_msg.append('invalid password')
					return (False, error_msg)
			else:
				error_msg.append('invalid username')
				return(False, error_msg)

	def register(self, name, username, password, con_password):
		errors = False
		error_msg = []
		if len(name) < 2:
			errors = True
			error_msg.append("Name is too short")
		if len(username) < 2:
			errors = True
			error_msg.append("Username is too short")
		if len(password) < 8:
			errors = True
			error_msg.append('password need to be at least 8 characters')
		if not password == con_password:
			errors = True
			error_msg.append('password does not match')
		if User.objects.filter(username = username):
			errors = True
			error_msg.append('Existing username')
		if errors:
			return (False, error_msg)
		else:
			User.objects.create(name = name, password = password, username = username)
			return (True, 'success')

class TripManager(models.Manager):
	def add_trip(self, destination, description, date_from, date_to, user):
		error_msg = []
		if len(destination) < 1 or len(description) < 1 or len(date_from) < 1 or len(date_to) < 1:
			error_msg.append('empty fields')
			return (False, error_msg)
		else:
			date_from = datetime.strptime(date_from, '%Y-%m-%d')
			date_to = datetime.strptime(date_to, '%Y-%m-%d')
			if date_from < datetime.now() or date_to < datetime.now():
				error_msg.append('need to be future dates')
				return (False, error_msg)
			elif date_from > date_to :
				error_msg.append('Travel date To should be after Travel date From')
				return (False, error_msg)
			else:
				Trip.objects.create(destination = destination, description = description, date_from = date_from, date_to = date_to, user = user)
				return (True, 'success')

class JoinTripManager(models.Manager):
	def join_trip(self, trip, user):
		JoinTrip.objects.create(trip = trip, user = user)
		return

class User(models.Model):
	name = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Trip(models.Model):
	destination = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	date_from = models.DateField(auto_now=False)
	date_to = models.DateField(auto_now=False)
	user = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = TripManager()

class JoinTrip(models.Model):
	user = models.ForeignKey(User, related_name='jointouser')
	trip = models.ForeignKey(Trip, related_name='jointotrip')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = JoinTripManager()