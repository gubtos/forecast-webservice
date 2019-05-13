# forecast-webservice

Flask REST webservice. Este serviço exibe a média de precipitação e a máxima temperatura da lista de cidades cadastradas.

Projeto desenvolvido para processo seletivo.

## Executar

Para funcionamento do acesso a API climatempo obtenha uma API_KEY e adicione-a no arquivo `config.py`.

Para alterar o endereço do banco de dados edite as configurações no arquivo `config.py`. Por padrão está na pasta temporária `/tmp/` .

Para rodar o código execute na pasta raíz

```python3 run.py```

## Dependências
- flask 
- flask-sqlalchemy
- requests

## Recursos
Lista de recursos fornecidos pelo webservice 

### cidade

Operações permitidas:
 - GET 
    - **/cidade/?id=< id >** Cadastro de cidade
    - **/cidade/** Acessar todas as cidades
    - **/cidade/< id >** Acessar temperaturas de cidade específica
 - POST
    - **/cidade/ id=< id >** Cadastro de cidade

### análise
 - GET
    - **/analise/?data_inicial=dd/mm/YYYY&data_final=dd/mm/YYYY** Retorna a cidade com temperatura máxima, a temperatura máxima e uma lista de cidades com a precipitação média no intervalo escolhido



## Authors

* **Gustavo Okuyama** - *Backend Development* - [gubtos](https://github.com/gubtos)

## License

This project is licensed under the MIT License - see the [LICENSE](https://raw.githubusercontent.com/gubtos/forecast-webservice/master/LICENSE) file for details
