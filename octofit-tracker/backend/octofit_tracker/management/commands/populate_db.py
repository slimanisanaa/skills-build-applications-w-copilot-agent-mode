from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
from djongo import models

from bson.objectid import ObjectId

from django.conf import settings

import pymongo

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connexion MongoDB
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['octofit_db']

        # Nettoyage collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Données de test
        marvel_team = {'_id': ObjectId(), 'name': 'Team Marvel'}
        dc_team = {'_id': ObjectId(), 'name': 'Team DC'}
        db.teams.insert_many([marvel_team, dc_team])

        users = [
            {'_id': ObjectId(), 'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team_id': marvel_team['_id']},
            {'_id': ObjectId(), 'name': 'Captain America', 'email': 'cap@marvel.com', 'team_id': marvel_team['_id']},
            {'_id': ObjectId(), 'name': 'Batman', 'email': 'batman@dc.com', 'team_id': dc_team['_id']},
            {'_id': ObjectId(), 'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team_id': dc_team['_id']},
        ]
        db.users.insert_many(users)

        db.users.create_index([('email', pymongo.ASCENDING)], unique=True)

        activities = [
            {'_id': ObjectId(), 'user_id': users[0]['_id'], 'type': 'run', 'distance': 5},
            {'_id': ObjectId(), 'user_id': users[1]['_id'], 'type': 'cycle', 'distance': 20},
            {'_id': ObjectId(), 'user_id': users[2]['_id'], 'type': 'swim', 'distance': 2},
            {'_id': ObjectId(), 'user_id': users[3]['_id'], 'type': 'run', 'distance': 10},
        ]
        db.activities.insert_many(activities)

        leaderboard = [
            {'_id': ObjectId(), 'user_id': users[0]['_id'], 'points': 100},
            {'_id': ObjectId(), 'user_id': users[1]['_id'], 'points': 80},
            {'_id': ObjectId(), 'user_id': users[2]['_id'], 'points': 90},
            {'_id': ObjectId(), 'user_id': users[3]['_id'], 'points': 95},
        ]
        db.leaderboard.insert_many(leaderboard)

        workouts = [
            {'_id': ObjectId(), 'user_id': users[0]['_id'], 'workout': 'Pushups', 'reps': 50},
            {'_id': ObjectId(), 'user_id': users[1]['_id'], 'workout': 'Situps', 'reps': 60},
            {'_id': ObjectId(), 'user_id': users[2]['_id'], 'workout': 'Squats', 'reps': 70},
            {'_id': ObjectId(), 'user_id': users[3]['_id'], 'workout': 'Lunges', 'reps': 80},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data!'))
