def bingenerator(bin_tuple):

    import numpy

    # commodity function to generate bins extra attributes
    bin_tuple['n_edges']   = bin_tuple['n_bins']+1
    bin_tuple['size_bin'] = (bin_tuple['stop']-bin_tuple['start'])/numpy.float(bin_tuple['n_bins'])
    bin_tuple['bins']     = numpy.linspace(bin_tuple['start'] , bin_tuple['stop'] , num = bin_tuple['n_edges'])
    # bins_center is it 0-indexed, numpy-digitize output is also adapted below
    bin_tuple['bins_center'] = (bin_tuple['bins']-bin_tuple['size_bin']/2.)[1:]

    return bin_tuple
