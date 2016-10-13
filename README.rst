***************************************************************
`.gov.br: Página de Destaque`
***************************************************************

.. contents:: Conteúdo
   :depth: 2

Introdução
-----------

Complemento para a criação de microsites dentro do Portal Padrão. A instalação deste pacote disponibiliza
um novo tipo de conteúdo chamado PÁGINA DE DESTAQUE, que poderá ser utilizado para a criação de campanhas
e hotsites dentro do Portal Padrão, com um tema específico para este uso.

Importante: Este pacote foi desenvolvido para ser utilizado dentro do Portal Padrão, e depende de diversas
ferramentas disponíveis no Portal. Por isso seu uso isolado não é aconselhado.

Estado deste pacote
-------------------

.. image:: http://img.shields.io/pypi/v/brasil.gov.paginadestaque.svg
    :target: https://pypi.python.org/pypi/brasil.gov.paginadestaque

.. image:: https://img.shields.io/travis/plonegovbr/brasil.gov.paginadestaque/master.svg
    :target: http://travis-ci.org/plonegovbr/brasil.gov.paginadestaque

.. image:: https://img.shields.io/coveralls/plonegovbr/brasil.gov.paginadestaque/master.svg
    :target: https://coveralls.io/r/plonegovbr/brasil.gov.paginadestaque
    
Rodando o buildout de uma tag antiga do pacote
----------------------------------------------

Para atender ao relato de ter vários jobs de integração contínua em pacotes brasil.gov.* (ver https://github.com/plonegovbr/portalpadrao.release/issues/11), no fim da seção extends do buildout.cfg de todos os pacotes brasil.gov.* temos a seguinte linha:

.. code-block:: cfg

    https://raw.githubusercontent.com/plonegovbr/portal.buildout/master/buildout.d/versions.cfg

Hoje, esse arquivo contém sempre as versões pinadas de um release a ser lançado. Por esse motivo, quando é feito o checkout de uma tag mais antiga provavelmente você não conseguirá rodar o buildout. Dessa forma, após fazer o checkout de uma tag antiga, recomendamos que adicione, na última linha do extends, o arquivo de versões do IDG compatível com aquela tag, presente no repositório https://github.com/plonegovbr/portalpadrao.release/.

Exemplo: você clonou o repositório do brasil.gov.portal na sua máquina, e deu checkout na tag 1.0.5. Ao editar o buildout.cfg, ficaria dessa forma, já com a última linha adicionada:

.. code-block:: cfg

    extends =
        https://raw.github.com/collective/buildout.plonetest/master/test-4.3.x.cfg
        https://raw.github.com/collective/buildout.plonetest/master/qa.cfg
        http://downloads.plone.org.br/release/1.0.4/versions.cfg
        https://raw.githubusercontent.com/plonegovbr/portal.buildout/master/buildout.d/versions.cfg
        https://raw.githubusercontent.com/plone/plone.app.robotframework/master/versions.cfg
        https://raw.githubusercontent.com/plonegovbr/portalpadrao.release/master/1.0.5/versions.cfg
        
Para saber qual arquivo de versões é compatível, no caso do brasil.gov.portal, é simples pois é a mesma versão (no máximo um bug fix, por exemplo, brasil.gov.portal é 1.1.3 e o arquivo de versão é 1.1.3.1). Para os demais pacotes, recomendamos comparar a data da tag do pacote e a data nos changelog entre uma versão e outra para adivinhar a versão compatível.
