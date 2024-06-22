# Copyright (c) 2024, reshmakunjuty@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from datetime import date, timedelta,datetime
from frappe.utils import today, ceil, flt, comma_and, getdate

def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
	return[
	_('Sales Person') + ':Link\Sales Person:280',
	_('Commission Rate') + ':Currency:280'
	]

def get_sales_person_hierarchy():
    hierarchy = []
    sales_person_list = frappe.db.get_list("Sales Person", filters={"enabled": 1}, fields=[
                                           "name", "sales_person_name", "parent_sales_person"], order_by="parent_sales_person")

    def add_sales_person(sales_person, indent=0):
        sales_person["indent"] = indent
        hierarchy.append(sales_person)

        children = [
            sp for sp in sales_person_list if sp["parent_sales_person"] == sales_person["name"]]
        for child in children:
            add_sales_person(child, indent=indent+1)

    root_sales_persons = [
        sp for sp in sales_person_list if not sp["parent_sales_person"]]
    for root_sales_person in root_sales_persons:
        add_sales_person(root_sales_person)

    return hierarchy



def get_data(filters=None):
	data=[]
	for sales in get_sales_person_hierarchy():
		commission_rate = frappe.db.get_value("Sales Person", sales.name, "SUM(commission_rate) as commission_rate")
		row = frappe._dict(
				{
					"sales_person": sales.name,
					"commission_rate": commission_rate,
					"indent": sales.indent
				}
			)
		data.append(row)
	return data
