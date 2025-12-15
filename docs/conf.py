# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Guía de Física'
copyright = '2025, Prof. Ing. Luciano Lamaita'
author = 'Prof. Ing. Luciano Lamaita'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.mathjax',
]


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'es'
root_doc = 'index' # Asegúrese de que esta línea esté presente

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

# docs/conf.py (Agregar si no está, o modificar)
source_encoding = 'utf-8-sig'

source_suffix = {
    '.rst': 'restructuredtext',
    '.myst': 'markdown',
}


# Configuración específica para MyST para garantizar el soporte de LaTeX/MathJax
myst_enable_extensions = [
    "amsmath",
    "dollarmath",  # Habilita la sintaxis $...$ y $$...$$
]
