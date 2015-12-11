## What is this 

This is (my first) python module based on pandas to generate multidimensional bin of large dataset.

## Requirements

Multibinner requires pandas and numpy

## Installation

Clone this repository and set the paths yourself or

    pip install git+git://github.com/kidpixo/multibinner.git

or 

    pip install git+https://github.com/kidpixo/multibinner.git

## The problem

The problem I want to solve is:

    I have a huge pandas.DataFrame.
    I want to rebin some columns.
    I want the oupt of custom function on those bins.

The Multibinner module solve this problems. It accepts as input:

- a pandas.DataFrame
- bins definition linked to each columns via a dictionary
- the functions to calculate on the bins

The output is a multi-indexed `pandas.DataFrame` stored in `multibinner.MBDataFrame`, addressing which row goes in which bin.
There are also two useful functions:

- `multibinner.col_df_to_array(column_name)` to get an actual numpy array of a single columns
- `multibinner.all_df_to_array()` to get a dictionary of all the columns -> numpy arrays .


## Example

See the examples ipython notebook in [examples/](https://github.com/kidpixo/multibinner/tree/master/examples) or the super basic one here:

```python
    import pandas as pd
    import numpy as np
    import multibinner as mb
    import collections

    data = pd.DataFrame({'x' : np.random.random_sample(10),
                                'y' : np.random.random_sample(10) ,
                                'z' : np.random.random_sample(10) })
    data
            x         y         z
    0  0.528028  0.461097  0.962175
    1  0.490757  0.783239  0.757769
    2  0.915778  0.042979  0.504223
    3  0.240565  0.532206  0.228318
    4  0.945771  0.084394  0.473350
    5  0.453645  0.363603  0.245930
    6  0.954963  0.844241  0.726222
    7  0.912119  0.566655  0.706003
    8  0.322697  0.661911  0.885819
    9  0.025065  0.544047  0.047445

    # the columns we want to have in output:
    out_columns = ['z']

    # functions we want to apply on the data in a single multidimensional bin:
    aggregated_functions = {'elements' : len ,'average' : np.average}

    # define the bins
    group_variables = collections.OrderedDict([
                        ('y',mb.bingenerator({ 'start'   : 0 ,
                                                'stop'   : 1,
                                                'n_bins' : 5})),
                        ('x',mb.bingenerator({ 'start'   : 0 ,
                                                'stop'   : 1,
                                                'n_bins' : 5}))
                                            ])
    # I use OrderedDict to have fixed order, a normal dict is fine too but you loose your order obviously.

    group_variables

    OrderedDict([('y',
                {'bins': array([ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ]),
                'bins_center': array([ 0.1,  0.3,  0.5,  0.7,  0.9]),
                'n_bins': 5,
                'n_edges': 6,
                'size_bin': 0.2,
                'start': 0,
                'stop': 1}),
                ('x',
                {'bins': array([ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ]),
                'bins_center': array([ 0.1,  0.3,  0.5,  0.7,  0.9]),
                'n_bins': 5,
                'n_edges': 6,
                'size_bin': 0.2,
                'start': 0,
                'stop': 1})])

    # that is the object collectig all the data that define the multi binning
    mbdf =  mb.MultiBinnedDataFrame(binstocolumns = False,
                                    dataframe = irisdf,
                                    group_variables = group_variables,
                                    aggregated_functions = aggregated_functions,
                                    out_columns = out_columns)

    # that's ipython completion with tab 
    mbdf.

    mbdf.MBDataFrame           mbdf.all_df_to_array
    mbdf.col_df_to_array       mbdf.group_variables
    mbdf.out_columns           mbdf.aggregated_functions
    mbdf.binstocolumns         mbdf.functionsgenerator
    mbdf.multibin              mbdf.variablesgrouper

    mbdf.MBDataFrame

                z_average  z_elements    y    x
    y_binned x_binned
    0        4          0.488786           2  0.1  0.9
    1        2          0.245930           1  0.3  0.5
    2        0          0.047445           1  0.5  0.1
             1          0.228318           1  0.5  0.3
             2          0.962175           1  0.5  0.5
             4          0.706003           1  0.5  0.9
    3        1          0.885819           1  0.7  0.3
             2          0.757769           1  0.7  0.5
    4        4          0.726222           1  0.9  0.9

    # assemble one numpy array from the columns z_average
    mbdf.col_df_to_array('z_average')[  ]

    array([[        nan,         nan,         nan,         nan,  0.48878639],
           [        nan,         nan,  0.24592997,         nan,         nan],
           [ 0.04744482,  0.22831788,  0.96217527,         nan,  0.70600342],
           [        nan,  0.88581869,  0.75776871,         nan,         nan],
           [        nan,         nan,         nan,         nan,  0.72622249]])

    # all the columns to numpy array
    mbdf.all_df_to_array().keys()

    ['y', 'x', 'z_average', 'z_elements']
```
