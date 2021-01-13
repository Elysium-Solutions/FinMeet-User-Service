from User_Service import app
import os, json

if __name__ == "__main__":
   path = os.path.join(os.getcwd(), os.path.join('configs', 'app_settings.Config'))
   app_config = None
   with open(path) as config_file:
      app_config = json.load(config_file)
   app.run(debug=app_config.get('DEBUG'), port=app_config.get('PORT'))
