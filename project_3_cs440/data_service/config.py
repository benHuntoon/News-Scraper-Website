
class Config(object):
    HOST = '142.11.219.155'      
    DATABASE = 'news_scraper'  # fill with database name
    USER = 'dbguy'      
    PASSWORD = 'P@ssword69'  
    PORT = 3306

    CHARSET = 'utf8'
    UNICODE = True
    WARNINGS = True

    @classmethod
    def dbinfo(cls):
        return {
            'host': cls.HOST,
            'database': cls.DATABASE,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'port': cls.PORT,
        }
