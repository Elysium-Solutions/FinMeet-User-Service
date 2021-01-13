import os, json
from sshtunnel import SSHTunnelForwarder



class Config:
    __instance__ = None


    def __init__(self):
        """Build out config object from requested config"""
        if Config.__instance__ is None:
            print(os.getcwd())
            path = os.path.join(os.getcwd(), os.path.join('configs', 'service.Config'))
            with open(path) as config_file:
	            config = json.load(config_file)
            local_port=""
            server = SSHTunnelForwarder(
                ('45.79.171.221', 22),
                ssh_username="root",
                ssh_password="Fold2706metro39ted",
                remote_bind_address=('127.0.0.1', 5432)
                )

            server.start()
            local_port = str(server.local_bind_port)

            self.SECRET_KEY = config.get('SECRET_KEY')
            self.SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI').replace("port", local_port)
            self.PLAID_REDIRECT_URI = config.get('PLAID_REDIRECT_URI')
            self.PLAID_COUNTRY_CODES = config.get('PLAID_COUNTRY_CODES')
            self.PLAID_PRODUCTS = config.get('PLAID_PRODUCTS')
            self.PLAID_CLIENT_ID = config.get('PLAID_CLIENT_ID')
            self.PLAID_SECRET = config.get('PLAID_SECRET')
            self.PLAID_ENVIRONMENT= config.get('PLAID_ENVIRONMENT')
            self.ADDRESS= config.get('ADDRESS')
            self.BALANCE_WEBHOOK_URL= config.get('BALANCE_WEBHOOK_URL')


            Config.__instance__ = self
        else:
            raise Exception("You cannot create another Config class")

    @staticmethod
    def get_instance():
        """ Static method to fetch the current instance."""
        if not Config.__instance__:
            Config()
        return Config.__instance__
    