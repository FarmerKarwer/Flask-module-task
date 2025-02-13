from flask import Flask
from flask_pymongo import PyMongo
import os

#repositories
from app.repositories.advice_repository import AdviceRepository
from app.repositories.challenge_repository import ChallengeRepository
from app.repositories.icebracker_repository import IcebreakerRepository
from app.repositories.theme_repository import ThemeRepisitory
from app.repositories.user_repository import UserRepository

#services
from app.services.advice_service import AdviceService
from app.services.challenge_service import ChallengeService
from app.services.icebreaker_service import IcebreakerService
from app.services.theme_service import ThemeService
from app.services.user_service import UserService

from flasgger import Swagger

def create_app():
	app = Flask(__name__)
	Swagger(app, template_file='swagger/swagger.yml')
	print(os.environ.get('MONGO_HOST'))
	app.config['MONGO_URI'] = f'mongodb://{os.environ.get("MONGO_HOST")}:{os.environ.get("MONGO_PORT")}/{os.environ.get("MONGO_DB")}'
	print(app.config['MONGO_URI'])
	mongo = PyMongo(app)
	app.mongo = mongo

	#repositories
	adviceRepository = AdviceRepository(app)
	challengeRepository = ChallengeRepository(app)
	icebreakerRepository = IcebreakerRepository(app)
	themeRepository = ThemeRepisitory(app)
	userRepository = UserRepository(app)

	#services
	adviceService = AdviceService(adviceRepository)
	challengeService = ChallengeService(challengeRepository)
	icebreakerService = IcebreakerService(icebreakerRepository)
	themeService = ThemeService(themeRepository)
	userService = UserService(userRepository, challengeRepository)

	app.adviceService = adviceService
	app.challengeService = challengeService
	app.icebreakerService = icebreakerService
	app.themeService = themeService
	app.userService = userService
	return app