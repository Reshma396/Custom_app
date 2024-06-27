import frappe
from frappe.model.document import Document
from frappe import _
from datetime import date, timedelta, datetime
from frappe.utils import today, ceil, flt, comma_and, getdate

def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_columns():
    return [
        _('Sales Person') + ':Link/Sales Person:280',
        _('Commission Rate') + ':Currency:280'
    ]

def get_data(filters=None):
    query = """
    SELECT
        st.sales_person,
        st.commission_rate
    FROM
        `tabSales Person` sp,
        `tabSales Team` st
    WHERE
        sp.name = st.sales_person
        AND sp.is_group = 1
    GROUP BY
        sp.name
    """
    sales_person_details = frappe.db.sql(query, as_dict=1)
    return sales_person_details
