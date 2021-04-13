import os


if os.environ.get('PROJECT_ENV') == 'Development':
    try:
        from .dev import *
    except:
        pass

else:
    try:
        from .prod import *
    except:
        pass
