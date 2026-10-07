"""
Modelo de fuga de clientes (churn) - Laboratorio Sesion 2, Curso MLOps UTEC.

Uso:
    python train.py

Lee los hiperparametros de config.json, entrena un Random Forest
y muestra el AUC en el conjunto de prueba.
"""
import json
import os
import pickle

import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


def cargar_config(ruta="config.json"):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def cargar_datos(cfg):
    # Datos sinteticos de clientes: 20% de fuga (clase 1)
    X, y = make_classification(
        n_samples=6000, n_features=20, n_informative=8, n_redundant=4,
        weights=[0.8], flip_y=0.02, class_sep=0.9, random_state=7,
    )
    return train_test_split(X, y, test_size=cfg["test_size"],
                            random_state=cfg["random_state"], stratify=y)


def entrenar(cfg, X_train, y_train):
    # label_noise: % de etiquetas de entrenamiento alteradas (para pruebas de robustez)
    rng = np.random.default_rng(cfg["random_state"])
    y_train = y_train.copy()
    n_ruido = int(cfg["label_noise"] * len(y_train))
    idx = rng.choice(len(y_train), size=n_ruido, replace=False)
    y_train[idx] = 1 - y_train[idx]

    modelo = RandomForestClassifier(
        n_estimators=cfg["n_estimators"],
        max_depth=cfg["max_depth"],
        min_samples_leaf=cfg["min_samples_leaf"],
        random_state=cfg["random_state"],
        n_jobs=-1,
    )
    return modelo.fit(X_train, y_train)


def main():
    cfg = cargar_config()
    X_train, X_test, y_train, y_test = cargar_datos(cfg)
    modelo = entrenar(cfg, X_train, y_train)
    auc = roc_auc_score(y_test, modelo.predict_proba(X_test)[:, 1])

    os.makedirs("models", exist_ok=True)
    with open("models/modelo_churn.pkl", "wb") as f:
        pickle.dump(modelo, f)

    print(f"Configuracion: {cfg}")
    print(f"AUC en prueba: {auc:.3f}")


if __name__ == "__main__":
    main()
