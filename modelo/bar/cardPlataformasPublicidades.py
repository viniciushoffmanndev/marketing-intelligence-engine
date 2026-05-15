import matplotlib.pyplot as plt
import seaborn as sns

class CardPlataformasPublicidades:
    def __init__(self, dataframe):
        self.df = dataframe

    def plataformas_publicidades(self):
        fig, ax = plt.subplots(figsize=(8, 5))
        # Soma do investimento por plataforma
        investimento = self.df[['youtube', 'facebook', 'newspaper']].sum()
        sns.barplot(x=investimento.index, y=investimento.values, ax=ax, palette='viridis')
        ax.set_title('Total de Investimento por Plataforma')
        return fig