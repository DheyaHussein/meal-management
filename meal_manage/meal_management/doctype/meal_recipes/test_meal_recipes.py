# Copyright (c) 2025, diaa and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class UnitTestMealRecipes(UnitTestCase):
	"""
	Unit tests for MealRecipes.
	Use this class for testing individual functions and methods.
	"""

	pass


class IntegrationTestMealRecipes(IntegrationTestCase):
	"""
	Integration tests for MealRecipes.
	Use this class for testing interactions between multiple components.
	"""

	pass
