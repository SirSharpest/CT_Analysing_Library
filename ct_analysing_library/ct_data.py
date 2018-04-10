#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Nathan

"""
import sys
from os.path import basename, dirname
from glob import glob
import pandas as pd
from pandas.errors import EmptyDataError
import numpy as np


class NoDataFoundException(Exception):
    pass


class CTData():
    def __init__(self, folder, rachis):
        """
        This is the initialise function for the CTData object,
        this will only need called once.

        @param folder the folder to look for data in
        @param rachis a boolean to decide to load in rachis data or not
        """
        try:
            self.make_dataframe(folder, get_rachis=rachis)
            self.clean_data()
            self.create_dimensions_ratio()
            self.df = self.df.reset_index(drop=True)
        except (ValueError, NoDataFoundException):
            raise NoDataFoundException
        self.additional_data = None

    def get_data(self):
        """
        Grabs the dataframe inside the class
        @returns a copy of the dataframe used in this class
        """
        return self.df.copy(deep=True)

    def gather_data(self, folder):
        """
        this function gathers together all
        the data of interest
        @param folder is a starting folder
        @returns tuple of (seed files, rachis files)
        """
        # check the end of the folder has a '/'
        if folder[-1] != '/':
            folder = folder + '/'
        search_params = '{0}*/*.csv'
        candidate_files = glob(search_params.format(folder))
        # Check data was found
        if len(candidate_files) == 0:
            raise NoDataFoundException
        # we aren't bothered about the raw files so lets remove them
        candidate_files = [f for f in candidate_files if 'raw' not in f]
        # now let's separate out the rachis
        rachis = [f for f in candidate_files if 'rachis' in f]
        # and just assume the rest is what we want
        candidate_files = [f for f in candidate_files if 'rachis' not in f]
        return (candidate_files, rachis)

    def create_dimensions_ratio(self):
        """
        This is an additional phenotype which is of someuse for
        finding out the relationship between the dimension variales
        """
        self.df['length_depth_width'] = self.df.apply(
            lambda x: x['length'] * x['depth'] * x['width'], axis=1)

    def make_dataframe(self, folder, get_rachis=False):
        """
        this function returns a dataframe of
        grain parameters and optionally of the rachis top and bottom
        @param grain_files is the output from gather_data
        @param rachis_files is an optional output from gather_data also
        @returns a dataframe of the information pre-joining
        """
        self.grain_files, self.rachis_files = self.gather_data(folder)
        # load the files as dfs
        dfs = {f: pd.read_csv(f) for f in self.grain_files}
        # load the files for rachis too
        if get_rachis:
            rachis = {}
            for f in self.rachis_files:
                try:
                    rachis[f] = pd.read_csv(f)
                except EmptyDataError:
                    pass
            # add plant name to files
            # and rachis if applicable
        for k, v in dfs.items():
            # Grab the plant name and the folder name
            v['scanid'] = basename(k).split('.', 1)[0]
            v['folderid'] = dirname(k).rsplit('/', 1)[-1]
            if get_rachis:
                try:
                    # reverse the rachis here so we don't have to later
                    v['rbot'] = rachis['{0}-rachis.csv'.format(
                        k[:-4])]['rtop'][0]
                    v['rtop'] = rachis['{0}-rachis.csv'.format(
                        k[:-4])]['rbot'][0]
                # Flip the scans so that the Z makes sense
                except (IndexError, KeyError):
                    pass
                    try:
                        v['rbot'] = v['z'].max()
                        v['rtop'] = v['z'].min()
                    except KeyError:
                        continue
        df = pd.concat(dfs.values())
        df['z'] = abs(df['z'] - df['z'].max())
        # Finally just turn the folder number into an int so that it's
        # easier to compare with the look-up table later
        df['folderid'] = df['folderid'].astype(int)
        self.df = df
        return df  # returns a dataframe for use outside of object too!

    def clean_data(self, remove_small=False, remove_large=False):
        """
        Following parameters outlined in the
        CT software documentation I remove outliers
        which are known to be errors

        @param remove_small a boolean to remove small grains or not
        @param remove_large a boolean to remove larger grains or not
        """
        self.df = self.df.dropna(axis=1, how='all')
        self.df = self.df[self.df['surface_area'] < 100]
        self.df = self.df[self.df['volume'] > 3.50]  # this is given for brachy
        self.df = self.df[self.df['volume'] < 60]

        if remove_large:
            self.df = self.df[self.df['volume'] <
                              self.df['volume'].quantile(.95)]
        if remove_small:
            self.df = self.df[self.df['volume'] >
                              self.df['volume'].quantile(.05)]

    def get_files(self):
        """
        Grabs a tuple of grain files and rachis
        @returns a tuple of grain files and rachis files
        """
        return self.grain_files, self.rachis_files

    def fix_colnames(self):
        """
        Because Biologists like to give data which are not normalised to any degree
        this function exists to attempt to correct the grouping columns,
        after standardisation https://github.com/SirSharpest/CT_Analysing_Library/issues/2
        this shouldn't be needed anymore, but kept for legacy issues that could arise!
        """
        self.df['Sample Type'] = self.df['Sample name'].map(
            lambda x: ''.join([i for i in str(x) if not i.isdigit()]))

    def join_spikes_by_rachis(self):
        """
        So important part of this function is that we accept that the data is what it is
        that is to say: rtop, rbot and Z are all orientated in the proper direction

        It's main purpose is to join split spikes by rachis nodes identified in the
        analysis process

        @param grain_df is the grain dataframe to take on-board
        """
        # So we are only really interested in grains which are not labelled with
        # 'all' in partition, so let's id them to start with
        for sn in self.df[self.df['Ear'] != 'all']['Sample name'].unique():

            bot = self.df.loc[(self.df['Sample name'] == sn)
                              & (self.df['Ear'] == 'bot')]['rbot']

            self.df.loc[(self.df['Sample name'] == sn) & (self.df['Ear'] == 'top'), 'z'] = self.df.loc[(
                self.df['Sample name'] == sn) & (self.df['Ear'] == 'top'), 'z'] + bot

    def remove_percentile(self, df, column, target_percent, bool_below=False):
        """
        This function is targeted at removing a percentile of a dataframe
        it uses a column to decide which to measure against. By default this
        will remove everything above the percentile value

        @param df is the dataframe to manipulate
        @param column is the attribute column to base the removal of
        @param target_percent is the percentage to aim for
        @param bool_below is a default param which if set
        to True will remove values below rather than above percentage
        """
        P = np.percentile(df[column], target_percent)
        df = df[df[column] < P] if bool_below else df[df[column] < P]

    def get_spike_info(self, excel_file, join_column='Folder#'):
        """
        This function should do something akin to adding additional
        information to the data frame

        @note there is some confusion in the NPPC about whether to use
        folder name or file name as the unique id when this is made into
        end-user software, a toggle should be added to allow this

        @param excel_file a file to attach and read data from
        @param join_column if the column for joining data is different then it should be stated
        """
        try:
            # Grab the linking excel file
            info = pd.read_excel(excel_file,
                                 index_col='Folder#')

            info = info.replace(np.nan, 'None', regex=True)

            features = list(info.columns)
            # Lambda to look up the feature in excel spreadsheet

            def look_up(x, y): return info.loc[x['folderid']][y]

            # Lambda form a series (data row) and apply it to dataframe
            def gather_data(x): return pd.Series(
                [look_up(x, y) for y in features])

            self.df[features] = self.df.apply(gather_data, axis=1)
        except KeyError as e:
            print(e)
            raise NoDataFoundException
        except AttributeError as e:
            print(e)
            raise NoDataFoundException

    def aggregate_spike_averages(self, attributes, groupby):
        """
        This will aggregate features (specified by attributes) into their medians
        on a per-spike basis.


        Makes direct changes to the dataframe (self.df)

        @param attributes list of features to average
        @param groupby how the data should be aggregated
        """

        trans_funcs = {'median': np.median,
                       'mean': np.mean, 'std': np.std, 'sum': np.sum}

        for att in attributes:
            for col, func in trans_funcs.items():
                self.df['{0}_{1}'.format(col, att)] = self.df.groupby(groupby)[
                    att].transform(func)

        self.df['grain_count'] = self.df.groupby(
            groupby)[groupby].transform(len)

    def find_troublesome_spikes(self):
        """
        This will attempt to identify spikes
        which are not performing as expected

        The default criteria for this is simply a count check
        So it requires that aggregate_spike_averages has been run

        @returns a dataframe with candidates for manual investigation
        """
        df = self.df.filter(['Sample name', 'grain_count',
                             'folderid', 'scanid'], axis=1)
        df = df.sort_values(by=['grain_count'])
        return df
