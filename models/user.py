#!/usr/bin/python3
""" holds class User"""
from models.base_model import BaseModel
import models


class User(BaseModel):
    """Representation of a user """
    user_name = ""
    email = ""
    password = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
