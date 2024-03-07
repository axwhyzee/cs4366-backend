from datetime import datetime


def logger(f):
    """Decorator for logging function calls. Displays time, function name, params"""
    def wrapper(*args, **kwargs):
        print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] ({f.__name__})',
          *args,
          **kwargs
        )
        return f(*args, **kwargs)

    return wrapper


@logger
def name_to_dir(text: str):
    """Extracts NORTH / SOUTH / EAST / WEST / LOOP from route text"""
    return text.split(' ')[0].upper()


@logger
def stem_route(route_id: str):
    """Stemming of route ID, e.g., S2*3 => S2"""
    return route_id.split('*')[0].split('/')[0]