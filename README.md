# Crypto-arbitrage
Срипт предназначен для сбора данных об ценах монет на различных биржах, фильтрации данных по заданным критериям и нахождения максимально прибыльной пары для арбитража. Сначала скрипт через API сайта cryptorank.com получает список содержащий названия всех доступных монет на сайте. Затем данные поочередно для каждой монеты собираются с помощью библиотеки BeautifulSoap. Делается это из-за того что API сайта имеет ограничение по колличеству запросов и используя BS для парсинга страниц сайта можно обойти данное ограничение. Дальше по указанным пользователем критериям производится фильтрация полученных данных. 
Критерии для фильтрации торговых пар можно указывать следующие: 
- Значение минимальной и максимальной прибыли для арбитража. 
- Названия монет или валют, которые пользователь хочет исключить из поиска.
- Названия бирж, которые пользователь хочет исключить из поиска.
- Названия бирж, по которым нужно произвожить поиск (остальные биржи будут исключены из поиска).
Результаты работы скрипта записываются в файл "results.csv". Также для ускорения работы скрипта была подключена библиотека MultiProcessing.
На данный момент скрипт анализирует 5300 монет.

Crypto-arbitrage
---------------------------------------
The script is designed to collect data on coin prices on various exchanges, filter data according to specified criteria and find the most profitable pair for arbitration. First, the script receives a list containing the names of all available coins on the site via the cryptorank.com website API. Then the data is collected for each coin in turn using the BeautifulSoap library. This is done due to the fact that the site's API has a limit on the number of requests, and using BS to parse the site's pages, you can bypass this restriction. Further, according to the criteria specified by the user, the received data is filtered.
The criteria for filtering trading pairs can be specified as follows:
- The value of the minimum and maximum profit for arbitration.
- Names of coins or currencies that the user wants to exclude from the search.
- The names of the exchanges that the user wants to exclude from the search.
- Names of exchanges to search for (other exchanges will be excluded from the search).

The results of the script's work are written to the "results.csv" file. Also, to speed up the script, the MultiProcessing library was connected.
At the moment, the script analyzes 5300 coins.
