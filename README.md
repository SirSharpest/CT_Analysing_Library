#+TITLE: Machine Learning Assignment 2
#+AUTHOR: Nathan Hughes ([[mailto:nah31@aber.ac.uk][nah26@aber.ac.uk]])
#+OPTIONS: toc:nil H:4 ^:nil
#+LaTeX_CLASS: article
#+LaTeX_CLASS_OPTIONS: [a4paper]
#+LaTeX_HEADER: \usepackage[margin=0.8in]{geometry}
#+LaTeX_HEADER: \usepackage{amssymb,amsmath}
#+LaTeX_HEADER: \usepackage{fancyhdr} %For headers and footers
#+LaTeX_HEADER: \pagestyle{fancy} %For headers and footers
#+LaTeX_HEADER: \usepackage{lastpage} %For getting page x of y
#+LaTeX_HEADER: \usepackage{float} %Allows the figures to be positioned and formatted nicely
#+LaTeX_HEADER: \restylefloat{figure} %and this command
#+LaTeX_HEADER: \usepackage{hyperref}
#+LaTeX_HEADER: \hypersetup{urlcolor=blue}
#+LaTex_HEADER: \usepackage{titlesec}
#+LaTex_HEADER: \setcounter{secnumdepth}{4}
#+LaTeX_HEADER: \usepackage{minted}
#+LATEX_HEADER: \setminted{frame=single,framesep=10pt}
#+LaTeX_HEADER: \chead{}
#+LaTeX_HEADER: \rhead{\today}
#+LaTeX_HEADER: \cfoot{}
#+LaTeX_HEADER: \rfoot{\thepage\ of \pageref{LastPage}}
#+LaTeX_HEADER: \usepackage[parfill]{parskip}
#+LaTeX_HEADER:\usepackage{subfig}
#+latex_header: \hypersetup{colorlinks=true,linkcolor=black, citecolor=black}
#+LATEX_HEADER_EXTRA:  \usepackage{framed}
#+LATEX: \maketitle
#+LATEX: \clearpage
#+LATEX: \tableofcontents
#+LATEX: \clearpage

* CTData.py
** CTData
*** =__init__=
*** get_data

        Returns the dataframe used in this class
        
*** gather_data

        this function gathers together all
        the data of interest
        @param folder is a starting folder
        @returns tuple of (seed files, rachis files)
        
*** make_dataframe

        this function returns a dataframe of
        grain parameters and optionally of the rachis top and bottom
        @param grain_files is the output from gather_data
        @param rachis_files is an optional output from gather_data also
        @returns a dataframe of the information pre-joining
        
*** clean_data

        Following parameters outlined in the
        CT software documentation I remove outliers
        which are known to be errors
        
*** get_files

        Returns a tuple of grain files and rachis files
        
*** fix_colnames

        Because Biologists like to give data which are not normalised to any degree
        this function exists to attempt to correct the grouping columns,
        after standardisation https://github.com/SirSharpest/CT_Analysing_Library/issues/2
        this shouldn't be needed anymore, but kept for legacy issues that could arise!
        
*** join_spikes_by_rachis

        So important part of this function is that we accept that the data is what it is
        that is to say: rtop, rbot and Z are all orientated in the proper direction

        It's main purpose is to join split spikes by rachis nodes identified in the
        analysis process

        @param grain_df is the grain dataframe to take on-board
        
*** remove_percentile

        This function is targeted at removing a percentile of a dataframe
        it uses a column to decide which to measure against. By default this
        will remove everything above the percentile value

        @param df is the dataframe to manipulate
        @param column is the attribute column to base the removal of
        @param target_percent is the percentage to aim for
        @param bool_below is a default param which if set
        to True will remove values below rather than above percentage
        
*** get_spike_info

        This function should do something akin to adding additional
        information to the data frame

        @note there is some confusion in the NPPC about whether to use
        folder name or file name as the unique id when this is made into
        end-user software, a toggle should be added to allow this
        
*** look_up
*** gather_data
*** make_plot

        Returns false if plot could not be created for invalid parameters
        
