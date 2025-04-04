poetry install --no-root
eval $(poetry env activate)
python3 teste_3.py
deactivate
mysql -u root TESTE_3 < teste_3.sql