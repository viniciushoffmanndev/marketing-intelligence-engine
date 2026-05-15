from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

class RegressaoLinear:
    def __init__(self, dataframe):
        self.df = dataframe

    def regressao(self):
        # Definindo X (investimentos) e Y (vendas)
        X = self.df[['youtube', 'facebook', 'newspaper']]
        Y = self.df['sales']
        
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        
        modelo = LinearRegression()
        modelo.fit(X_train, Y_train)
        
        Y_pred = modelo.predict(X_test)
        return Y_test, Y_pred