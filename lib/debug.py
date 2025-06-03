#!/usr/bin/env python3
# lib/debug.py

from lib.models import Session, Product, Order, OrderItem, Shipment
import ipdb

session = Session()
ipdb.set_trace()
