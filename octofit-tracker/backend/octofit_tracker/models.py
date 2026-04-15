from djongo import models


class Team(models.Model):
	_id = models.ObjectIdField(primary_key=True, editable=False, db_column='_id')
	name = models.CharField(max_length=100)
	class Meta:
		db_table = 'teams'
		managed = False


class User(models.Model):
	_id = models.ObjectIdField(primary_key=True, editable=False, db_column='_id')
	name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	team_id = models.ObjectIdField(db_column='team_id')
	class Meta:
		db_table = 'users'
		managed = False


class Activity(models.Model):
	_id = models.ObjectIdField(primary_key=True, editable=False, db_column='_id')
	user_id = models.ObjectIdField(db_column='user_id')
	type = models.CharField(max_length=50)
	distance = models.FloatField()
	class Meta:
		db_table = 'activities'
		managed = False


class Leaderboard(models.Model):
	_id = models.ObjectIdField(primary_key=True, editable=False, db_column='_id')
	user_id = models.ObjectIdField(db_column='user_id')
	points = models.IntegerField()
	class Meta:
		db_table = 'leaderboard'
		managed = False


class Workout(models.Model):
	_id = models.ObjectIdField(primary_key=True, editable=False, db_column='_id')
	user_id = models.ObjectIdField(db_column='user_id')
	workout = models.CharField(max_length=100)
	reps = models.IntegerField()
	class Meta:
		db_table = 'workouts'
		managed = False
