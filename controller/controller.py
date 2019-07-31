from controller import create_app

controllerApp = app = create_app()

if __name__ == '__main__':
	controllerApp.run(threaded=True)