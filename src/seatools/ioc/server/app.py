from seatools.ioc import Autowired
from fastapi import FastAPI


def app():
    """server app factory."""
    # Get FastAPI instance from ioc_bean()
    return Autowired(cls=FastAPI).ioc_bean()
