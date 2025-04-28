# QGIS-Style-Classifier

Descrição:
Este script automatiza a categorização e a estilização de camadas vetoriais de uso e cobertura da terra no QGIS, atribuindo cores e padrões personalizados conforme a classificação temática dos dados.

O script normaliza os valores de texto (removendo acentos e variações), aplica simbologia categorizada e adiciona padrões específicos para classes como "Silvicultura" e "Área aberta".

Funcionalidades
- Normalização de textos para evitar inconsistências de digitação.
- Estilização automática por cor de preenchimento baseada em classificação de uso do solo.
- Aplicação de padrão SVG (árvore) para silvicultura.
- Aplicação de preenchimento com linhas para áreas abertas.



Pré-requisitos:
- QGIS 3.x
- PyQt5 (já incluído no QGIS)
- Ambiente Python do QGIS

Como usar:
1. Abra o QGIS e carregue a camada vetorial desejada.

2. Certifique-se de que sua camada contém um campo chamado tema (responsável pela classificação).

3. Execute o script no console Python do QGIS ou como script externo.

4. A simbologia será aplicada automaticamente!
