import pandas as pd
from joblib import dump
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Cargar los datos
data = pd.read_csv("train.csv")

# Dividir en características (X) y etiquetas (y)
X = data.drop(columns=["Source", "Target"])  # Eliminar columnas de identificación
y = (data["o3D Distance"] > 0.4).astype(int)  # Umbral para definir si deben combinarse o no

# Escalamiento de características
#scaler = StandardScaler()
#print(X)
#X_scaled = scaler.fit_transform(X)
#print("X_scaled: ", X_scaled)
## Dividir en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("============")

print(X_test)
# Seleccionar un modelo y entrenarlo
model = LogisticRegression()
model.fit(X_train, y_train)

# Guardar el modelo entrenado en un archivo "modelo_entrenado.pkl"
dump(model, "modelo_entrenado.pkl")

# Predicciones en el conjunto de prueba
y_pred = model.predict(X_test)

# Métricas de evaluación
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
