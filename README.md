# IntuitiveCarePS
processo seletivo da IntuitiveCare

cada teste possui seu próprio pacote de dependencias gerenciado pelo poetry, caso seja desejado um ambiente preparado, para instalar basta usar 
pip install poetry
poetry install

para executar, basta ativar o env e rodar o código
eval $(poetry env activate)
python3 teste_x.py

com exceção do servidor frontend que pode ser executado com 
npm run serve

ou utilizar os a.sh encontrados dentro das pastas