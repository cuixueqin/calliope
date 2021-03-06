"""
Copyright (C) 2013-2018 Calliope contributors listed in AUTHORS.
Licensed under the Apache 2.0 License (see LICENSE file).

util.py
~~~~~~~~

Plotting util functions.

"""

import numpy as np


def get_data_layout(
        get_var_data, get_var_layout,
        relevant_vars, layout, model, dataset,
        subset, sum_dims, squeeze,
        get_var_data_kwargs={},
        get_var_layout_kwargs={}):
    # data_len is used to populate visibility of traces, for dropdown
    data_len = [0]
    data = []
    buttons = []
    # fill trace data and add number of traces per var to 'data_len' for use with
    # visibility. first var in loop has visibility == True by default
    visible = True

    for var in relevant_vars:
        data += get_var_data(
            var, model, dataset, visible, subset, sum_dims, squeeze,
            **get_var_data_kwargs)
        data_len.append(len(data))
        visible = False

    # Initialise all visibility to False for dropdown updates
    total_data_arrays = np.array([False for i in range(data_len[-1])])
    var_num = 0
    for var in relevant_vars:
        # update visibility to True for all traces linked to this variable `var`
        visible_data = total_data_arrays.copy()
        visible_data[data_len[var_num]:data_len[var_num + 1]] = True

        # Get variable-specific layout
        var_layout = get_var_layout(var, dataset, **get_var_layout_kwargs)

        if var_num == 0:
            layout['title'] = var_layout['title']
            if 'barmode' in var_layout:
                layout['barmode'] = var_layout['barmode']

        if len(relevant_vars) > 1:
            var_layout = [{'visible': list(visible_data)}, var_layout]
            buttons.append(dict(label=var, method='update', args=var_layout))

        var_num += 1

    # If there are multiple vars to plot, use dropdowns via 'updatemenus'
    if len(relevant_vars) > 1:
        updatemenus = list([dict(
            active=0, buttons=buttons, type='dropdown',
            xanchor='left', x=0, y=1.13, pad=dict(t=0.05, b=0.05, l=0.05, r=0.05)
        )])
        layout['updatemenus'] = updatemenus
    else:
        layout.update(var_layout)
    return data, layout


def hex_to_rgba(hex_color, opacity):
    _NUMERALS = '0123456789abcdefABCDEF'
    _HEXDEC = {v: int(v, 16) for v in (x + y for x in _NUMERALS for y in _NUMERALS)}
    hex_color = hex_color.lstrip('#')
    rgb = [_HEXDEC[hex_color[0:2]], _HEXDEC[hex_color[2:4]], _HEXDEC[hex_color[4:6]]]
    return 'rgba({1}, {2}, {3}, {0})'.format(opacity, *rgb)
