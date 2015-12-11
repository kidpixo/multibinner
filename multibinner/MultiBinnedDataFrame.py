import numpy
import collections
import pandas

class MultiBinnedDataFrame(object):

    def __init__(self, binstocolumns=False, **kwargs):
        # essentially assign all the variables we need here

        # this is only for internal use, could be huge so not deliver to output
        internal_df               = kwargs.get('dataframe')
        self.group_variables      = kwargs.get('group_variables')
        self.aggregated_functions = kwargs.get('aggregated_functions')
        self.out_columns          = kwargs.get('out_columns')
        self.binstocolumns        = binstocolumns

        self.functionsgenerator(internal_df)

        # this is only for internal use, not deliver to output
        grouped = self.variablesgrouper(internal_df)

        # final dataproduct for end user
        self.MBDataFrame          = self.multibin(grouped,binstocolumns)

    def variablesgrouper(self,internal_df):
        """
        Purpose : to assemble the grouping variables based on input bins
        output : pandas.DataFrame.groupby
        """
        grouping_variable = []

        # 0-based digitizer
        def digitize_0_based(arg1, bin):
            return numpy.digitize(arg1, bin)-1
        # function generator: dinamyc generation of digitizer
        def generate_digitizer(worker, arg1, bin):
            return worker(arg1, bin)

        # assemble the grouping lable using dinamyc functions generator
        for k in self.group_variables.iterkeys():
            grouping_variable.append(
            generate_digitizer(digitize_0_based,internal_df[k], self.group_variables[k]['bins'])
            )

        # this uses level_0, level_1,...,level_n for indexes
        grouped = internal_df.groupby(grouping_variable)
        # delete array from memory
        # del grouping_variable

        return grouped

    def functionsgenerator(self,internal_df):
        """
        Purpose : to assemble build the columns -> functions dictionary
        output : update the self.aggregated_functions to use directly with
                pandas.DataFrame.groupby.agg() method
        """

        # check if the keys in the passed functions are all  actual columns of
        # the dataframe, in this case pass to the groupby.aggregate function
        if set(self.aggregated_functions.keys()) <= set(internal_df.columns):
            agg_functions = self.aggregated_functions
        else:
            agg_functions = collections.OrderedDict()
            for i in self.out_columns:
                agg_functions[i] = self.aggregated_functions

        self.aggregated_functions = agg_functions

    def multibin(self,grouped,binstocolumns=False):
        """
        Purpose : to generate the output MultiBinnedDataFrame
         output : pandas.DataFrame.groupby
        """
        temporary_df = grouped.agg(self.aggregated_functions)
        # compress  multi level index with original name + '_' + func name
        temporary_df.columns =   [i[0] if len(i[1]) is 0 else '_'.join(i) for i in temporary_df.columns]
        # only used if a has level_0, level_1,..
        if temporary_df.index.names == [None] * len(temporary_df.index.names):
            temporary_df.index.set_names([k+'_binned' for k in self.group_variables.iterkeys()],inplace=True)

        if binstocolumns:
            # assign the central bin value to new columns,previously used for grouping
            for k,v in self.group_variables.iteritems():
                temporary_df[k] = v['bins_center'][temporary_df.index.get_level_values(k+'_binned').values]

        return temporary_df

    def col_df_to_array(self,column):
        """
        Purpose : to assemble a numpy array with size based on the bins defined in the MultiBinnedDataFrame
          input : the desired output columns from the input MultiBinnedDataFrame
         output : numpy array with size based on the bins defined in the MultiBinnedDataFrame.
        """

        m_indexes = [self.MBDataFrame.index.get_level_values(indname).values for indname in self.MBDataFrame.index.names]
        empty = numpy.empty([ v['n_bins'] for v in self.group_variables.itervalues()])
        empty[:] = numpy.nan
        empty[m_indexes] = self.MBDataFrame[column].values

        return empty

    def all_df_to_array(self):
        """
        Purpose : to assemble a dictionary of numpy array with size based on the bins defined in the MultiBinnedDataFrame
          input : already in the class.
         output : dictionary of numpy array with size based on the bins defined in the MultiBinnedDataFrame.
        """
        out_dictionary = {}
        m_indexes = [self.MBDataFrame.index.get_level_values(indname).values for indname in self.MBDataFrame.index.names]
        for c in self.MBDataFrame.columns:
            out_dictionary[c] = numpy.empty([ v['n_bins'] for v in self.group_variables.itervalues()])
            out_dictionary[c][:] = numpy.nan
            out_dictionary[c][m_indexes ] = self.MBDataFrame[c].values

        return out_dictionary


