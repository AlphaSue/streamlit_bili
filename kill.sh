kill -9 $(ps aux | grep '[s]treamlit' | awk '{print $2}')

