<h1>Extraindo dados da Web para o BigQuery</h1>

<h2>Sobre:</h2 >

<p>
O objetivo deste projeto é a extração de dados de um site de venda de jogos para o BigQuery, onde os dados poderão ser analisados.
</p>

#

<h2>Tecnologias:</h2>



  <table>
    <tr>
      <td>OS</td>
      <td>Python</td>
      <td>SQL</td>
    </tr>
      <tr>
      <td>Ubuntu </td>
      <td>3.7 até 3.10 </td>
      <td>BigQuery</td>
    </tr>
  </table>

#

<h2>Pré-requisitos:</h2 >



<h3>

- Python
  - It's necessary a version between 3.7 - 3.10, you can check the versions in this link : https://www.python.org/downloads/ or if you already has python, you can check the version passing this code

  ```
  python -V
  ```


- Projeto

  - É necessário que já exista um projeto criado
<p></p>

- Conta de Serviço

  - A conta de serviço é algo necessário para poder rodar aplicações que utilizam de qualquer serviço da Google.
<p></p>

- Chave Conta de Serviço

  - É necessário atribuir uma chave a conta de serviço criada, e logo em seguida, extrair essa chave para o projeto, como o arquivo **sample_confog.json** está representando.

<p></p>

**OBS**: Este site explica como concluir os passos acima:
 https://support.google.com/a/answer/7378726?hl=pt-BR

<p></p>

- Permissão

  - É necessário que você dê as permissões necessárias para a sua conta de serviço, pois só assim ela conseguirá executar a aplicação.

**OBS**: Este site explica como concluir o passo acima:
https://cloud.google.com/data-fusion/docs/how-to/granting-service-account-permission?hl=pt-br#grant_roles_to_service_accounts

<p></p>

- Ativação API

  - É necessário que haja a ativação da API do BigQuery. Para isto basta ir até o serviço BigQuery no console da GCP e clicar em ativar API.

</h3>

<p></p>

#

<h2>Criando o ambiente Python:</h2>
<p>
<h3>1- Crie o ambiente de desenvolvimento usando os comandos abaixo.</h3>

```
python -m venv .venv
```
<h3>2 - Ative o projeto.</h3>

```
.venv/Scripts/Activate
```
<h3>3 - Instale as dependências por meio do comando abaixo.</h3>

```
pip install -r requirements.txt
```
</p>

<h3>4 - Crie o config.json</h3>

- **sample_config**:
  - Este arquivo serve como referência para a chave de acesso que deve ser extraída. Após extrair a chave, coloque-a na pasta principal e renomeie-a para config.json.

#

<h2>Setting the main.py file</h2 >

<p>
  <h3>
  After setting all the enviroment's you can start the setting the main.py file.
  </h3>
</p>

<p>
  <h3>
  Let's open the main.py and understand how it's works
  </h3>
</p>

<p>
  <h3>
  Variables:
</h3>

- **project_name** = Bote o nome do projeto que foi criado no BigQuery para esta aplicacao

- **dataset_name** = Defina o nome de um dataset de sua escolha

- **table_name** = Defina o nome de uma tabela de sua escolha

#

<h2>Running main.py</h2 >

<p>
  <h3>
  Apos configurar todo o ambiente, basta executar o codigo.

  ```
  python3 main.py
  ```
  </h3>
</p>

#

<h2>Fluxo do processo</h2>

