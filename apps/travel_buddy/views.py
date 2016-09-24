from django.shortcuts import render, redirect
from .models import User, Trip, JoinTrip
from django.contrib import messages

# Create your views here.
def index(request):
	return redirect('/main')
def main(request):
	return render(request, 'travel_buddy/main.html')
def reg_user(request):
	if request.method == 'POST':
		name = request.POST['name']
		username = request.POST['username']
		password = request.POST['password']
		con_password = request.POST['con_password']
		user = User.objects.register(name, username, password, con_password)
		if user[0]:
			request.session['username'] = username
			return redirect('/travels')
		else:
			for message in user[1]:
				messages.error(request, message)
			return redirect('/main')
def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = User.objects.login(username, password)
		if user[0]:
			request.session['username'] = username
			return redirect('/travels')
		else:
			for message in user[1]:
				messages.error(request, message)
			return redirect('/main')
def logout(request):
	request.session['username'] = ''
	return redirect('/main')
def travels(request):
	if request.session['username'] is not '':
		user = User.objects.filter(username = request.session['username'])
		your_trip = Trip.objects.filter(user = user)|Trip.objects.filter(jointotrip__user = user)
		other_trip = Trip.objects.exclude(user = user).exclude(jointotrip__user = user)
		return render(request, 'travel_buddy/travels.html', context={'user':user, 'your_trip':your_trip, 'other_trip':other_trip})
	else:
		return redirect('/main')
def add(request):
	return render(request, 'travel_buddy/add_trip.html')
def add_trip(request):
	if request.method == 'POST':
		destination = request.POST['destination']
		description = request.POST['description']
		date_from = request.POST['date_from']
		date_to = request.POST['date_to']
		user = User.objects.filter(username = request.session['username'])
		print user
		trip = Trip.objects.add_trip(destination, description, date_from, date_to, user[0])
		if trip[0]:
			return redirect('/travels')
		else:
			for message in trip[1]:
				messages.error(request, message)
			return redirect('/travels/add')
def destination(request, id):
	trip = Trip.objects.get(id = id)
	jointrip = JoinTrip.objects.filter(trip = trip)
	print jointrip
	return render(request, 'travel_buddy/destination.html', context={'trip': trip, 'jointrip':jointrip})
def join_trip(request, id):
	user = User.objects.filter(username = request.session['username'])
	trip = Trip.objects.get(id = id)
	JoinTrip.objects.join_trip(trip, user[0])
	return redirect('/travels')