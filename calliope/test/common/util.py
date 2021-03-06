import os

import calliope
from calliope import AttrDict


constraint_sets = AttrDict.from_yaml(os.path.join(os.path.dirname(__file__), 'constraint_sets.yaml'))

_defaults_files = {
    k: os.path.join(os.path.dirname(calliope.__file__), 'config', k + '.yaml')
    for k in ['model', 'defaults']
}
defaults = AttrDict.from_yaml(_defaults_files['defaults'])
defaults_model = AttrDict.from_yaml(_defaults_files['model'])


def build_test_model(override_dict=None, override_groups=None):
    this_path = os.path.dirname(__file__)
    model_location = os.path.join(this_path, 'test_model', 'model.yaml')
    override_location = os.path.join(this_path, 'test_model', 'overrides.yaml')
    if override_groups:
        override_file = override_location + ':' + override_groups
    else:
        override_file = None

    return calliope.Model(
        model_location, override_dict=override_dict,
        override_file=override_file
    )
