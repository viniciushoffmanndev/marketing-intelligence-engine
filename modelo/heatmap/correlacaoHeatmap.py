import matplotlib.pyplot as plt
import seaborn as sns

class CorrelacaoHeatmap:
    def __init__(self, dataframe):
        self.df = dataframe

    def heatmap(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(self.df.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        ax.set_title('Matriz de Correlação: Investimentos vs Vendas')
        return fig