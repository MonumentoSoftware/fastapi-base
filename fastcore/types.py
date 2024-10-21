
from typing import TypeVar

import pymongo
from pymongo.database import Database
from pymongo.collection import Collection
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase


CLIENTS = TypeVar('CLIENTS', pymongo.MongoClient, AsyncIOMotorClient)
DATABASES = TypeVar('DATABASES', Database, AsyncIOMotorDatabase)
COLLECTIONS = TypeVar('COLLECTIONS', Collection, AsyncIOMotorCollection)
