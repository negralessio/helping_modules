import pandas as pd
from bokeh.io import show, output_notebook
from bokeh.resources import INLINE
from bokeh.plotting import figure
import bokeh.plotting as bpl
import bokeh.models as bmo
from bokeh.palettes import Viridis256, viridis, magma, Cividis256, Turbo256, Spectral6, Category20c, Bokeh, Category20, inferno

class MyVisualization:
    """
    Class to visualize TSNE (or PCA) results as a scatter plot to allow hovering over the objects.
    """

    def __init__(self, X:pd.DataFrame):
        """
        Constructor for the MyVisualization class.
        :param X: DataFrame to plot
        """
        self.X = X
        self.N = X.shape[0]
        output_notebook()

    def plot_bokeh_scatterplot(self, 
                               plot_width=900, 
                               plot_height=500,
                               blobsize=10,
                               n_clusters=3,
                               axis_name = ["PC1", "PC2"],
                               title = "Test Title"):
        """
        Function to plot an interactive bokeh scatter plot
        :param plot_width: Width of the plot
        :param plot_height: Height of the plot
        :param axis_name:list Axis Name, i.e. ["TC1", "TC2"] or ["PC1", "PC2", ...]
        :param n_clusters: Number of clusters
        :param blobsize: Size of the blobs in the scatterplot
        :param title: Title of the plot
        :return: None
        """

        # Add color column to df
        if n_clusters <= 20:
            palette = Category20[20]
        else:
            palette = viridis(n_clusters)
        self.X["bokeh_color"] = [palette[i] for i in self.X.cluster]

        # Create bokeh DataSource from Pandas DF
        source = bpl.ColumnDataSource(self.X)

        # Color settings
        color_map = bmo.CategoricalColorMapper(factors=self.X['cluster'].astype(str).unique(),
                                               palette=palette)

        # Plot settings
        p = figure(plot_width=plot_width, plot_height=plot_height,
                   title=f"{title} | n_clusters = {n_clusters} | N = {self.X.shape[0]}",
                   toolbar_location=None,
                   tools="hover", tooltips="[Index: @index][Cluster: @cluster] {x:@PC1, y:@PC2}")
        # Scatter settings
        p.scatter(axis_name[0],
                  axis_name[1],
                  source=source,
                  fill_alpha=0.8,
                  size=blobsize,
                  line_color="black",
                  legend_group="cluster",
                  color="bokeh_color")
        p.xaxis.axis_label = axis_name[0]
        p.yaxis.axis_label = axis_name[1]
        p.legend.location = "top_right"
        show(p)