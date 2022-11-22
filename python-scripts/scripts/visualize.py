'''Data preparatie en visualisaite defenities'''

def sentimentVisDfBool(df,subject):
    '''Deze defenitie prepareert data van een sentiment analyse voor visualisatie
    NOTE! deze functie kan alleen gebruikt worden voor sentiment analyse die 
    positief en negatief weergeeft (dus geen neutraal) '''

    temp_df = df.copy()

    # grouperen naar gekozen onderwerp
    temp_df = temp_df.groupby([subject,'label_onderwerp_1']).size()

    # omzetten naar dataframe
    import pandas as pd
    temp_df = pd.DataFrame(temp_df.reset_index(name='aantal'))

    # lege waarde classifeseren als neutraal (niet classificeerbaar)
    import numpy as np

    temp_df.rename(columns={'label_onderwerp_1':'sentiment', subject: 'thema'},inplace=True)

    # maak een lijst met nieuwe kolom namen
    cols = temp_df['sentiment'].drop_duplicates().values.tolist()

    # reframe dataframe
    vis_df = temp_df[['thema']].drop_duplicates()

    for c in cols:
        temp = temp_df[temp_df['sentiment']==c][['thema','aantal']]
        temp.rename(columns={'aantal':c},inplace=True)
        vis_df = vis_df.merge(temp, 'left')

    vis_df['Totaal'] =vis_df[cols].sum(axis=1)
    vis_df.sort_values('Totaal', ascending=False, inplace=True)
    vis_df.reset_index(inplace=True,drop=True)

    return vis_df


def sentimentVisDfLikert(df,subject):
    '''Deze defenitie prepareert data van een sentiment analyse voor visualisatie
    NOTE! deze functie kan alleen gebruikt worden voor sentiment die gebruik maakt 
    van een likert scale weergeeft'''

    labels = ['Very negative', 'Negative', 'Neutral', 'Positive', 'Very positive']
    temp_df = df.copy()

    # grouperen naar gekozen onderwerp
    temp_df = temp_df[[subject]+labels].groupby(subject).mean()
    temp_df.reset_index(inplace=True)
    
    # aantallen telleven voor sortering
    aantal = df.copy()
    aantal = aantal.groupby([subject]).size()

    # series to dataframe
    temp_df = temp_df.merge(aantal.reset_index(), 'left')

    # sort naar aantal
    temp_df.sort_values(0, ascending=False, inplace=True)

    # omzetten naar dataframe
    import pandas as pd
    temp_df.reset_index(inplace=True, drop=True)
    temp_df.rename(columns={subject: 'thema', 0: 'aantal'},inplace=True)

    # Cul waardes maken    
    for i in range(1,len(labels)+1):
        temp_df['{}_cul'.format(labels[i-1])] = temp_df.loc[:,labels[0:i]].sum(axis=1)


    return temp_df


def sentimentBarPlotBool(df, title):
    import seaborn as sns
    import matplotlib.pyplot as plt
    sns.set_style('dark')
    sns.set(font_scale=1)

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(6, 15))

    # Plot totaal aantal waardes
    sns.set_color_codes('pastel')
    t =  sns.barplot(x='Totaal', y='thema', data=df,
                label='Positief', color='#93c47d')

    # Plot aantal negatieve
    sns.set_color_codes('muted')
    sns.barplot(x='Negative', y='thema', data=df,
                label='Negatief', color='#c47d93')

    # Legenda toevoegen
    ax.legend(ncol=3, loc='lower right', frameon=True)
    ax.set(xlim=(0, max(df['Totaal']+10)), ylabel='',
        xlabel='')
    sns.despine(left=True, bottom=True)

    # titel toevoegen
    t.axes.set_title(label=title,fontsize=13)



def sentimentBarPlotLikert(df, title):
    import seaborn as sns
    import matplotlib.pyplot as plt
    sns.set_style('dark')
    sns.set(font_scale=1)

    labels = ['Very negative', 'Negative', 'Neutral', 'Positive', 'Very positive']

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(6, 15))

    # Plot totaal aantal Very positive
    sns.set_color_codes('pastel')
    t =  sns.barplot(x='Very positive_cul', y='thema', data=df,
                label='Very positive', color='#49623e')

    # Plot aantal Positive
    sns.set_color_codes('muted')
    sns.barplot(x='Positive_cul', y='thema', data=df,
                label='Positive', color='#93C47D')

    # Plot aantal Neutral
    sns.set_color_codes('muted')
    sns.barplot(x='Neutral_cul', y='thema', data=df,
                label='Neutral', color='#b7c47d')

    # Plot aantal Very negative
    sns.set_color_codes('muted')
    sns.barplot(x='Negative_cul', y='thema', data=df,
                label='Negative', color='#c47d93')
    
    # Plot aantal Very negative
    sns.set_color_codes('muted')
    sns.barplot(x='Very negative_cul', y='thema', data=df,
                label='Very negative', color='#754b58')


    # Legenda toevoegen
    ax.legend(ncol=3, loc='lower right', frameon=True)
    ax.set(xlim=(0, max(df['Very positive_cul'])), ylabel='',
        xlabel='')
    sns.despine(left=True, bottom=True)

    # titel toevoegen
    t.axes.set_title(label=title,fontsize=13)

def scatterRegplot(df, title):
    import seaborn as sns
    import matplotlib.pyplot as plt
    import scipy.stats as stats
    r = stats.pearsonr(df['rating'], df['sentiment'])
    sns.set_style("dark")
    pallette = sns.color_palette("ch:s=-.2,r=.6", as_cmap=True)

    p = sns.FacetGrid(
        data=df,
        height=4.5, 
        aspect=2.5)

    # set scatter with color hue
    p.map(
        func=sns.scatterplot,
        data=df,
        x='rating', 
        y='sentiment', 
        hue='sentiment',
        palette=pallette)

    # plot line range
    p.map(
        func=sns.regplot, 
        data=df,
        x='rating', 
        y='sentiment', 
        scatter = False, 
        ci = 95, 
        fit_reg = True, 
        color = '#ADADAD') 

    # plot line
    p.map(
        func=sns.regplot, 
        data=df,
        x='rating', 
        y='sentiment',  
        scatter = False, 
        ci = 0, 
        fit_reg = True, 
        color = '#5B5B5B')


    # set labels and titles
    plt.xlabel('User ratings')
    plt.ylabel('Sentiment score')
    plt.title('\n{} (n={})\nPearsons R: {}'.format(title,len(df), round(r.statistic,2)))
    plt.show()


def divergentBarPlot(df):
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import seaborn as sns


    p = sns.FacetGrid(
        data=df,
        height=4.5, 
        aspect=2.5)

    sns.set_style("dark")
    ax = sns.barplot(x=df['sentiment'], y=df['ref_domein'])

    widths = np.array([bar.get_width() for bar in ax.containers[0]])
    divnorm = mpl.colors.TwoSlopeNorm(vmin=widths.min(), vcenter=0, vmax=widths.max())
    div_colors = plt.cm.RdYlGn(divnorm(widths))
    for bar, color in zip(ax.containers[0], div_colors):
        bar.set_facecolor(color)

    plt.xlabel('')
    plt.ylabel('')
    plt.title('\nGemiddelde sentiment score op topdeskmeldingen uitgeslpitst naar domein (n=334)\n')

    plt.tight_layout()
    plt.show()