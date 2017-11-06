# Datahound
    BMSTU, 2017
    ___________________________
    The project is the implementation of quantitative or qualitative analysis of the largest social 
    network in Russia, describing the features of the network either through numerical or 
    visual representation.
    
    
### Example of settings.py (required)

```python
TOKEN = "" # your token here
GOOGLE_TOKEN = ""   # your token here
BASE_URL = "https://api.vk.com/method/execute."
MEMBERS_FIELDS = "sex"  # bdate, city, country, online, online_mobile, education, last_seen, relation
PLATFORM = {1: "Mobile", 2: 'iPhone', 3: "iPad", 4: "Android",
            5: "Windows Phone", 6: "Windows 10", 7: "Web", 8: 'Unknown'}

SEX_COLORS = ['#FFD7E9', '#6495ED', '#B22222']
PLATFORM_COLORS = ['#66CDAA', '#EE5C42', '#B22222', '#1874CD']
SYSTEM_COLORS = ['#8B8386', '#FFE4C4']

COUNTRIES = {1: 'Россия',
             2: 'Украина',
             3: 'Беларусь',
             4: 'Казахстан',
             5: 'Азербайджан',
             6: 'Армения',
             7: 'Грузия',
             8: 'Израиль',
             9: 'США',
             10: 'Канада'}
```
:collision: To get your token please visit [Получение ключа доступа](https://vk.com/dev/access_token)

:collision: Run `pip3 install -r requirements.txt` to install all dependencies at once.

### TODO List
- Async
- Data Base
- Tests
- ???

````