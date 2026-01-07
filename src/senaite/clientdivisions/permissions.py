# -*- coding: utf-8 -*-

# Add Permissions
# ===============
# For "Add" permissions, keep the name of the variable as "Add<portal_type>".
# When the module gets initialized (bika.lims.__init__), the function initialize
# will look through these Add permissions attributes when registering types and
# will automatically associate them with their types.
AddDivision = "senaite.clientdivisions: Add Division"
