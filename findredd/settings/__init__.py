import os


if os.environ.get('PROJECT_ENV') == 'development':
    try:
        from .dev import *
    except:
        pass

else:
    try:
        from .prod import *
    except:
        pass
