from os.path import basename, dirname
from glob import glob
import pandas as pd
import numpy as np
import graphing as gp


class CTData():

    def __init__(self, folder, rachis):
        try:
            self.df = self.make_dataframe(folder, get_rachis=rachis)
            self.clean_data()
        except ValueError:
            return('No data found, check input directory')

    def get_data(self):
        """
        Returns the dataframe used in this class
        """
        return self.df

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
        # we aren't bothered about the raw files so lets remove them
        candidate_files = [f for f in candidate_files if 'raw' not in f]
        # now let's separate out the rachis
        rachis = [f for f in candidate_files if 'rachis' in f]
        # and just assume the rest is what we want
        candidate_files = [f for f in candidate_files if 'rachis' not in f]
        return (candidate_files, rachis)

    def make_dataframe(self, folder, get_rachis=False):
        """
        this function returns a dataframe of
        grain parameters and optionally of the rachis top and bottom
        @param grain_files is the output from gather_data
        @param rachis_files is an optional output from gather_data also
        @returns a dataframe of the information pre-joining
        """
        grain_files, rachis_files = self.gather_data(folder)
        # load the files as dfs
        dfs = {f: pd.read_csv(f) for f in grain_files}
        # load the files for rachis too
        if get_rachis:
            rachis = {f: pd.read_csv(f) for f in rachis_files}
            # add plant name to files
            # and rachis if applicable
        for k, v in dfs.items():
            # Grab the plant name and the folder name
            v['scanid'] = basename(k).split('.', 1)[0]
            v['folderid'] = dirname(k).rsplit('/', 1)[-1]
            if get_rachis:
                # reverse the rachis here so we don't have to later
                v['rbot'] = rachis['{0}-rachis.csv'.format(k[:-4])]['rtop'][0]
                v['rtop'] = rachis['{0}-rachis.csv'.format(k[:-4])]['rbot'][0]
                # Flip the scans so that the Z makes sense
        df = pd.concat(dfs.values())
        df['z'] = abs(df['z'] - df['z'].max())
        # Finally just turn the folder number into an int so that it's easier to
        # compare with the look-up table later
        df['folderid'] = df['folderid'].astype(int)
        return df

    def clean_data(self):
        """
        Following parameters outlined in the 
        CT software documentation I remove outliers 
        which are known to be errors 
        """
        self.df = self.df[self.df['volume'] > 30]
        self.df = self.df[self.df['volume'] < 60]

    def fix_colnames(self):
        """
        Because Biologists like to give data which are not normalised to any degree
        this function exists to attempt to correct the grouping columns,
        after standardisation https://github.com/SirSharpest/CT_Analysing_Library/issues/2
        this shouldn't be needed anymore, but kept for legacy issues that could arise!
        """
        self.df['Sample name'] = self.df['Sample name'].map(
            lambda x: str(x)[:-2])

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
        """

        # Grab the linking excel file
        info = pd.read_excel(excel_file,
                             index_col='Folder#')

        # These are the features to grab
        features = ['Hulled/Naked', 'Common name', 'Genome', 'Ploidy',
                    'Wild/Domesticated', 'Sample name', 'Sub type', 'Ear']

        # Lambda to look up the feature in excel spreadsheet
        def look_up(x, y): return info.loc[x['folderid']][y]

        # Lambda form a series (data row) and apply it to dataframe
        def gather_data(x): return pd.Series([look_up(x, y) for y in features])

        self.df[features] = self.df.apply(gather_data, axis=1)

    def make_plot(self, plot_type, x_var='Sample name', hue='', one_legend=False):
        """
        Returns false if plot could not be created for invalid parameters
        """
        if plot_type == 'box':
            try:
                gp.plot_boxplots(self.df, self.df.columns[:8],
                                 x_var=x_var, hue=hue, one_legend=one_legend)
            except gp.InvalidPlot:
                print('invalid plot')
                return None
        else:
            print('Sorry that current function isn\'t supported yet!')
