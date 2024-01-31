# ProjetoDeTCC
Repository to mantain data from my tcc project
Reporitório para manter os dados do meu projeto de TCC

INTERFACE_IP=[54.224.27.138:8501](http://54.224.27.138:8501/)

OPENSEARCH_HOST=3.92.43.154

## Manual de uso do software

Trataremos aqui de como baixar e utilizar o código do algoritmo.

### 1 - Reproduzir localmente a interface

Caso queira reproduzir o que foi feito, é necessário clonar o repositório ou fazer o download de todos os dados. Uma vez feito isso, você deve:

1. Ter instalado o Python3 na sua máquina
2. Verificar se os pacotes presentes em `requirements.txt` estão instalados na sua
máquina
3. Editar o arquivo `.env` para alterar o valor da variável de ambiente `OPENSEARCH_HOST`
para colocar o ip da máquina ec2 do opensearch (este ip pode ser encontrado no
início desse arquivo README).
4. Executar o comando
```shell
streamlit run main.py
```

### 2 - Utilizar a interface na nuvem da AWS

Caso queira utilizar a interface já hospedada na nuvem, basta acessar o ip no início desse README.md  localizar o ip da máquina onde está hospedada a interface (`INTERFACE_IP`). Este ip pode variar, pois a cada vez que a instância EC2 reinicia, um novo endereço de ip público é atribuído a ela.

Uma vez acessada o ip da máquina na porta 8501 pelo seu navegador, já é possível utilizar a interface.
