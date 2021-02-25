# Global options across all copies
katex = False  # Specifies whether to replace mathjax with katex for local processing -- may not always render correctly!
edgebundleR = False  # Specifies embedding custom positional fixes for this package
ref_r_functions = True  # Replaces r functions of the form `function()` with function references
ref_r_packages = True  # Replaces r packages of the form `package:function` with package references
output_code = True  # Outputs an R notebook of code to recreate slide content.

versions = {}

versions['print'] = True
# options for print copy -- what to strip out
versions['print_search'] = True       # True = Remove search plugin
versions['print_chalkboard'] = True   # True = Remove chalkboard plugin
versions['print_exclude'] = False     # True = Remove any slides marked exclude
versions['print_presentonly'] = True  # True = Remove any slides marked presentonly
versions['print_survey'] = True       # True = Remove any survey links
versions['print_scaling'] = False      # True = fixed scaling

versions['preprint'] = True
# options for pre-presenting print copy -- what to strip out
versions['preprint_search'] = True
versions['preprint_chalkboard'] = True
versions['preprint_exclude'] = True
versions['preprint_presentonly'] = True
versions['preprint_survey'] = True
versions['preprint_scaling'] = False

versions['pre'] = True
# options for pre-present html copy -- what to strip out
versions['pre_search'] = False
versions['pre_chalkboard'] = True
versions['pre_exclude'] = True
versions['pre_presentonly'] = True
versions['pre_survey'] = True
versions['pre_scaling'] = False

versions['post'] = True
# options for post-presentation html copy -- what to strip out
versions['post_search'] = False
versions['post_chalkboard'] = True
versions['post_exclude'] = False
versions['post_presentonly'] = True
versions['post_survey'] = True
versions['post_scaling'] = False

versions['base'] = True
# options for presentation html copy -- what to strip out
versions['base_search'] = False
versions['base_chalkboard'] = False
versions['base_exclude'] = False
versions['base_presentonly'] = False
versions['base_survey'] = False
versions['base_scaling'] = False

# printing options
printing = True # Print out pdf files for any chosen 'print' specifications
compress = True  # Compress pdf files (shrinks by ~90%)
retain_full = False  # Deletes original pdf file after compression if False

# Script location
# If False, assumes printreveal.py is in PATH (windows) or search path (Linux)
# If True, assumes printreveal is in the same directory as prep.py
use_local_printreveal_instance = True

# number overrides for printing (for slides not printing properly otherwise)
overrides = []
