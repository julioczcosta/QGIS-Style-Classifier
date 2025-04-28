# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 09:41:19 2025

@author: julio
"""

import unicodedata
from qgis.core import QgsFillSymbol, QgsSVGFillSymbolLayer, QgsRendererCategory, QgsCategorizedSymbolRenderer, QgsProject, QgsLinePatternFillSymbolLayer
from PyQt5.QtGui import QColor

# ===============================
# CONFIGURAÇÕES DO USUÁRIO
# ===============================

# Nome da camada a ser estilizada
layer_name = 'Uso do solo'

# Caminho do SVG padrão do QGIS para representar "Silvicultura"
svg_path = r'C:/PROGRA~1/QGIS33~1.3/apps/qgis/svg/gpsicons/tree.svg'

# Campo da camada que contém as classes temáticas
field_name = 'tema'

# ===============================
# FUNÇÕES AUXILIARES
# ===============================

def normalize_text(text):
    """Remove acentos, normaliza para minúsculas e limpa espaços extras do texto."""
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return ' '.join(text.lower().strip().split())

# ===============================
# CLASSIFICAÇÕES E CORES
# ===============================

classifications = {
    "APP": ("#99be76", ["APP", "app"]),
    "Área aberta": ("#3f9571", ["Área aberta", "area aberta", "aberta"]),
    "Área de benfeitoria": ("#ff1a01", ["Área de benfeitoria", "area de benfeitoria", "área de benfeitoria", "benfeitoria", "Area de benf"]),
    "Corpo d'água": ("#37f6e0", ["Corpo d'água", "corpo d'água", "corpo dagua", "agua", "Corpos d'água"]),
    "Lavoura": ("#cfee00", ["Lavoura", "lavoura"]),
    "Lavoura Irrigada": ("#41a391", ["Lavoura Irrigada", "lavoura irrigada", "irrigada"]),
    "Pastagem": ("#ebd762", ["Pastagem", "pastagem", "pasto"]),
    "Pasto sujo": ("#b2df8a", ["Pasto sujo", "pasto sujo"]),
    "Silvicultura": ("#ff9a01", ["Silvicultura", "silvicultura"]),
    "Vegetação Nativa": ("#088708", ["Vegetação Nativa", "vegetacao nativa", "Vegetacao", "Vegetacao nativa", "veg"]),
    "Área de várzea": ("#091d61", ["Área de várzea", "area de várzea", "várzea", "varzea", "área de várzea", "area de varzea"]),
    "Área de servição administrativa": ("#9300c0", ["Servidão Administrativa"]),
    "Estrada": ("#9300c0", ["estrada", "Estrada"]),
    "Cafeicultura": ("#ff9a01", ["cafe", "cafeicultura", "Cafeicultura"])
}

# ===============================
# EXECUÇÃO PRINCIPAL
# ===============================

# Obter a camada
tema_dict = {}
layer = QgsProject.instance().mapLayersByName(layer_name)
if not layer:
    raise ValueError(f"Camada '{layer_name}' não encontrada no projeto.")
layer = layer[0]

for feature in layer.getFeatures():
    original_value = feature[field_name]
    normalized_value = normalize_text(original_value)
    tema_dict[normalized_value] = original_value

categories = []

for category, (color, values) in classifications.items():
    for value in values:
        normalized_value = normalize_text(value)

        if normalized_value in tema_dict:
            original_value = tema_dict[normalized_value]

            symbol = QgsFillSymbol.createSimple({"color": color, "outline_color": color})

            # Se for Silvicultura, adiciona camada SVG
            if category == "Silvicultura":
                svg_layer = QgsSVGFillSymbolLayer(svg_path)
                svg_layer.setFillColor(QColor("black"))
                svg_layer.setStrokeColor(QColor("black"))
                svg_layer.setRenderingPass(1)
                svg_layer.setPatternWidth(2)
                symbol.appendSymbolLayer(svg_layer)

            # Se for Área Aberta, adiciona camada de preenchimento com linha
            if category == "Área aberta":
                line_layer = QgsLinePatternFillSymbolLayer()
                line_layer.setDistance(2.0)
                line_layer.setStrokeColor(QColor("black"))
                symbol.appendSymbolLayer(line_layer)

            categories.append(QgsRendererCategory(original_value, symbol, category))
            break  # Garante que apenas um valor seja usado por categoria

renderer = QgsCategorizedSymbolRenderer(field_name, categories)
layer.setRenderer(renderer)
layer.triggerRepaint()

print("[SUCCESS] Classificação aplicada com sucesso!")